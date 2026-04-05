"""
Management command script to populate the capacity planning database with realistic historical data.
Enforces strict capacity planning rules:
- Each employee works exactly 45h/week on ONE project only
- Supplier budgeted_hours = sum of actual external capacity
- Total capacity (internal+external) <= project.total_manhours
- No allocations beyond project.end_monday

Run with: python populate_database.py
"""

import os
import sys
import django
import random
from datetime import date, timedelta, datetime
from decimal import Decimal
from collections import defaultdict
from django.db import models

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SRC.settings')
django.setup()

from django.core.management import call_command
from django.db import transaction
from django.contrib.auth import get_user_model
from capacity_planning.models import (
    Department, Project, Resource, Supplier,
    ProjectAssignment, ResourceAllocation, ProjectWeekAllocation,
    ExternalCapacity, AppSettings
)

User = get_user_model()

# --- Constants & Data ---

START_DATE_RANGE = (date(2023, 1, 1), date(2025, 3, 31))

DEPARTMENTS_STRUCT = {
    "Design Engineering": [
        "Project Engineering",
        "GESH",
        "Controls Design"
    ],
    "Assembly Engineering": [],
    "Robotics Engineering": [],
    "PLC Commissioning": [],
    "Project Management": [],
    "Quality": [],
    "Purchase": []
}

SUPPLIERS_LIST = [
    ("TechFreelance Ltd", "contact@techfreelance.com", 85.00),
    ("AutoEng Contractors", "info@autoeng.com", 75.00),
    ("Global Engineering Sol", "support@globaleng.com", 80.00),
    ("Precision Systems", "sales@precision.com", 90.00),
]

FIRST_NAMES = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen",
    "Hans", "Klaus", "Juergen", "Stefan", "Markus", "Michael", "Thomas", "Andreas", "Peter", "Frank",
    "Anna", "Maria", "Ursula", "Monika", "Petra", "Elisabeth", "Sabine", "Renate", "Helga", "Birgit"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Mueller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann"
]

ROLES = ['PEM', 'SIM', 'DES', 'PLC', 'ROB', 'TL']

PROJECT_NAMES_PREFIX = [
    "Assembly Line", "Conveyor System", "Welding Cell", "Paint Shop", "Body Shop", "Chassis Line",
    "Battery Pack", "Motor Assembly", "Final Trim", "Quality Station", "Logistics Hub", "AGV System"
]

PROJECT_NAMES_SUFFIX = [
    "Redesign", "Optimization", "Expansion", "Upgrade", "Greenfield", "Automation", "Retrofit", "Integration"
]

# --- Helper Functions ---

def get_random_date(start, end):
    delta = end - start
    random_days = random.randrange(delta.days)
    return start + timedelta(days=random_days)

def get_next_monday(d):
    days_ahead = 0 - d.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return d + timedelta(days=days_ahead)

def generate_project_name():
    return f"{random.choice(PROJECT_NAMES_PREFIX)} {random.choice(PROJECT_NAMES_SUFFIX)}"

def is_holiday_period(d):
    # Summer: July/August
    if d.month in [7, 8]:
        return "Summer Vacation"
    # Christmas: Dec 20 - Jan 6
    if d.month == 12 and d.day >= 20:
        return "Christmas Break"
    if d.month == 1 and d.day <= 6:
        return "Christmas Break"
    return None

def create_bell_curve_demand(total_hours, weeks):
    """
    Distribute hours over weeks using a rough bell curve approximation.
    Returns list of weekly hour targets (will be adjusted later)
    """
    if weeks <= 0: return []
    
    # Simple triangular/trapezoidal distribution
    ramp_up_len = max(1, int(weeks * 0.15))
    ramp_down_len = max(1, int(weeks * 0.15))
    plateau_len = weeks - ramp_up_len - ramp_down_len
    
    # Weights
    weights = []
    # Ramp up (1 to 10)
    for i in range(ramp_up_len):
        weights.append(1 + (9 * (i / ramp_up_len)))
    # Plateau (10)
    for i in range(plateau_len):
        weights.append(10)
    # Ramp down (10 to 1)
    for i in range(ramp_down_len):
        weights.append(10 - (9 * (i / ramp_down_len)))
        
    total_weight = sum(weights)
    if total_weight == 0: return [0] * weeks
    
    weekly_hours = [int((w / total_weight) * total_hours) for w in weights]
    
    # Adjust rounding errors
    diff = total_hours - sum(weekly_hours)
    if plateau_len > 0:
        mid = ramp_up_len + (plateau_len // 2)
        weekly_hours[mid] += diff
    else:
        weekly_hours[weeks // 2] += diff
        
    return weekly_hours

# --- Main Script ---

@transaction.atomic
def run():
    print("="*80)
    print("POPULATING DATABASE WITH STRICT CAPACITY CONSTRAINTS")
    print("="*80)
    print("Rules:")
    print("1. Each employee: 45h/week on ONE project only")
    print("2. Supplier budgeted_hours = sum of external capacity")
    print("3. Total capacity (int+ext) <= project.total_manhours")
    print("4. No allocations beyond project.end_monday")
    print("="*80)

    # 0. Cleanup
    print("\nCleaning up existing data...")
    call_command('flush', interactive=False)
    
    # Re-create AppSettings
    AppSettings.objects.create(default_working_hours_per_week=45)
    print("OK AppSettings created.")

    # 1. Departments
    print("\nCreating Departments...")
    all_depts = []
    order_counter = 1
    for dept_name, sub_list in DEPARTMENTS_STRUCT.items():
        main_dept = Department.objects.create(name=dept_name, order=order_counter)
        order_counter += 1
        all_depts.append(main_dept)
        print(f"  ✓ {dept_name}")
        for idx, sub_name in enumerate(sub_list):
            sub_dept = Department.objects.create(name=sub_name, parent=main_dept, order=idx+1)
            all_depts.append(sub_dept)
            print(f"    - {sub_name}")

    # 2. Suppliers (start with 0 budget)
    print("\nCreating Suppliers...")
    suppliers = []
    for name, email, rate in SUPPLIERS_LIST:
        s = Supplier.objects.create(
            name=name,
            contact_email=email,
            hourly_rate=Decimal(rate),
            budgeted_hours=0  # Will be calculated later
        )
        suppliers.append(s)
        print(f"  ✓ {name}")

    # 3. Internal Resources (all 45h/week)
    print("\nCreating Internal Resources...")
    resources = []
    used_names = set()
    
    target_count = 40
    dept_names = [d.name for d in all_depts]
    depts_dict = {d.name: d for d in all_depts}

    for i in range(target_count):
        # Generate unique name
        while True:
            fname = random.choice(FIRST_NAMES)
            lname = random.choice(LAST_NAMES)
            full_name = f"{fname} {lname}"
            if full_name not in used_names:
                used_names.add(full_name)
                break

        dept_name = dept_names[i % len(dept_names)]
        dept = depts_dict[dept_name]
        role = random.choice(ROLES)
        
        r = Resource.objects.create(
            name=full_name,
            role=role,
            is_internal=True,
            department=dept,
            availability_per_week=45,
            is_active=True
        )
        resources.append(r)
    
    print(f"  ✓ Created {len(resources)} internal resources")

    # 4. Projects and Allocations
    print("\nCreating Projects with Constrained Allocations...")
    projects = []
    project_counter = 1
    
    # Tracking structures
    employee_week_assignments = defaultdict(set)  # {res_id: {week_monday, ...}}
    supplier_hours_accumulated = defaultdict(int)  # {sup_id: total_hours}
    
    # Pre-assign employees to prevent conflicts
    weekly_resource_pool = defaultdict(list)  # {week_monday: [resource_ids]}
    
    for dept in all_depts:
        num_projects = random.randint(15, 20)  # Reduced to fit constraints
        print(f"\n  Department: {dept.name} ({num_projects} projects)")
        
        # Get department resources
        dept_resources = [r for r in resources if r.department == dept or r.department.parent == dept]
        
        for _ in range(num_projects):
            # Create project
            p_code = f"PRJ-2025-{project_counter:03d}"
            project_counter += 1
            p_name = generate_project_name()
            
            rand_date = get_random_date(*START_DATE_RANGE)
            start_monday = get_next_monday(rand_date)
            duration_weeks = random.randint(26, 78)
            total_manhours = random.randint(1350, 4500)  # Multiple of 45
            
            # Ensure total_manhours is divisible by 45
            total_manhours = (total_manhours // 45) * 45
            
            project = Project(
                name=p_name,
                project_code=p_code,
                status=random.choice(['QUOTED', 'PLANNED', 'ORDERED']),
                department=dept,
                total_manhours=total_manhours,
                allotted_weeks=duration_weeks,
                start_monday=start_monday
            )
            project.save()
            projects.append(project)
            
            # Calculate weeks for this project
            project_weeks = []
            current_week = start_monday
            while current_week <= project.end_monday:
                project_weeks.append(current_week)
                current_week += timedelta(weeks=1)
            
            # --- Phase 1: Internal Allocations (45h blocks) ---
            target_internal = int(total_manhours * random.uniform(0.5, 0.7))
            target_internal = (target_internal // 45) * 45
            
            internal_hours = 0
            assignments = []
            allocations = []
            
            # Shuffle weeks for random distribution
            random_weeks = project_weeks.copy()
            random.shuffle(random_weeks)
            
            for week in random_weeks:
                if internal_hours >= target_internal:
                    break
                    
                # Find available employee
                available = [r for r in dept_resources if week not in employee_week_assignments[r.id]]
                if not available:
                    continue
                
                employee = available[0]
                
                # Create assignment and allocation
                assignments.append(ProjectAssignment(
                    resource=employee,
                    project=project,
                    is_lead=False,
                    week_monday=week
                ))
                
                allocations.append(ResourceAllocation(
                    resource=employee,
                    project=project,
                    week_monday=week,
                    hours=45
                ))
                
                # Track
                employee_week_assignments[employee.id].add(week)
                internal_hours += 45
            
            # Bulk create
            ProjectAssignment.objects.bulk_create(assignments)
            ResourceAllocation.objects.bulk_create(allocations)
            
            # --- Phase 2: External Allocations (remaining) ---
            remaining = total_manhours - internal_hours
            
            if remaining > 0:
                proj_suppliers = random.sample(suppliers, random.randint(1, 2))
                external_caps = []
                
                # Fill remaining weeks
                for week in project_weeks:
                    if remaining <= 0:
                        break
                        
                    # Skip weeks with internal allocation
                    if ResourceAllocation.objects.filter(project=project, week_monday=week).exists():
                        continue
                    
                    # Holiday check
                    if is_holiday_period(week):
                        continue
                    
                    # Allocate external capacity
                    hours = min(45, remaining)
                    supplier = random.choice(proj_suppliers)
                    
                    external_caps.append(ExternalCapacity(
                        supplier=supplier,
                        project=project,
                        week_monday=week,
                        hours=hours
                    ))
                    
                    supplier_hours_accumulated[supplier.id] += hours
                    remaining -= hours
                
                ExternalCapacity.objects.bulk_create(external_caps)
            
            # Create planned weekly demand (bell curve)
            weekly_targets = create_bell_curve_demand(total_manhours, len(project_weeks))
            
            planned_allocs = []
            for i, week in enumerate(project_weeks):
                if i < len(weekly_targets):
                    target_hours = weekly_targets[i]
                    # Adjust for holidays
                    holiday = is_holiday_period(week)
                    if holiday:
                        target_hours = max(20, int(target_hours * 0.2))
                        note = holiday
                    else:
                        note = ""
                        if random.random() < 0.05:
                            note = random.choice(["Waiting for BOM", "Design freeze"])
                    
                    planned_allocs.append(ProjectWeekAllocation(
                        project=project,
                        week_monday=week,
                        manhours=target_hours,
                        notes=note
                    ))
            
            ProjectWeekAllocation.objects.bulk_create(planned_allocs)
            
            # Progress indicator
            if project_counter % 50 == 0:
                print(f"    ✓ {project_counter-1} projects created...")

    # 5. Update Supplier Budgeted Hours
    print("\nUpdating Supplier Budgeted Hours...")
    for supplier in suppliers:
        total_hours = supplier_hours_accumulated[supplier.id]
        Supplier.objects.filter(id=supplier.id).update(budgeted_hours=total_hours)
        print(f"  ✓ {supplier.name}: {total_hours} hours")

    # Final Statistics
    print("\n" + "="*80)
    print("POPULATION COMPLETE")
    print("="*80)
    print(f"Total Departments: {Department.objects.count()}")
    print(f"Total Projects: {Project.objects.count()}")
    print(f"Total Internal Resources: {Resource.objects.filter(is_internal=True).count()}")
    print(f"Total Suppliers: {Supplier.objects.count()}")
    print(f"Total Assignments: {ProjectAssignment.objects.count()}")
    print(f"Total Allocations: {ResourceAllocation.objects.count()}")
    print(f"Total External Capacity Entries: {ExternalCapacity.objects.count()}")
    print(f"Total Planned Weekly Demands: {ProjectWeekAllocation.objects.count()}")

    # Validation Checks
    print("\nVALIDATION REPORT:")
    print("-" * 40)
    
    # Check 1: No employee has multiple allocations in same week
    duplicates = ResourceAllocation.objects.values(
        'resource', 'week_monday'
    ).annotate(count=models.Count('id')).filter(count__gt=1)
    print(f"✓ Employee-week duplicates: {duplicates.count()} (should be 0)")
    
    # Check 2: All internal allocations are exactly 45h
    non_45 = ResourceAllocation.objects.filter(
        resource__is_internal=True
    ).exclude(hours=45).count()
    print(f"✓ Non-45h allocations: {non_45} (should be 0)")
    
    # Check 3: Supplier budgets match actual capacity
    budget_mismatch = 0
    for sup in Supplier.objects.all():
        actual = ExternalCapacity.objects.filter(supplier=sup).aggregate(
            t=models.Sum('hours')
        )['t'] or 0
        if sup.budgeted_hours != actual:
            budget_mismatch += 1
    print(f"✓ Supplier budget mismatches: {budget_mismatch} (should be 0)")
    
    # Check 4: No allocations beyond project end
    invalid_alloc = ResourceAllocation.objects.filter(
        week_monday__gt=models.F('project__end_monday')
    ).count()
    invalid_ext = ExternalCapacity.objects.filter(
        week_monday__gt=models.F('project__end_monday')
    ).count()
    print(f"✓ Invalid internal allocations: {invalid_alloc}")
    print(f"✓ Invalid external allocations: {invalid_ext}")
    print("="*80)

if __name__ == "__main__":
    run()