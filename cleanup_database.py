#!/usr/bin/env python
"""
Database cleanup script for Capacity Planning application.
Clears all dynamic data while preserving static Department structure.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SRC.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from capacity_planning.models import *

def show_current_counts():
    """Display current database counts"""
    print("=== CURRENT DATABASE COUNTS ===")
    print(f"Departments: {Department.objects.count()}")
    print(f"Projects: {Project.objects.count()}")
    print(f"Suppliers: {Supplier.objects.count()}")
    print(f"Resources: {Resource.objects.count()}")
    print(f"ProjectAssignments: {ProjectAssignment.objects.count()}")
    print(f"ResourceAllocations: {ResourceAllocation.objects.count()}")
    print(f"ProjectWeekAllocations: {ProjectWeekAllocation.objects.count()}")
    print(f"ExternalCapacities: {ExternalCapacity.objects.count()}")
    print(f"AppSettings: {AppSettings.objects.count()}")
    print()

def cleanup_database():
    """Clear all dynamic data while preserving Departments"""

    print("=== STARTING DATABASE CLEANUP ===")

    # Delete in reverse dependency order to avoid constraint issues
    deleted_counts = {}

    # 1. ExternalCapacity (depends on Supplier, Project)
    count = ExternalCapacity.objects.count()
    ExternalCapacity.objects.all().delete()
    deleted_counts['ExternalCapacity'] = count

    # 2. ResourceAllocation (depends on Resource, Project)
    count = ResourceAllocation.objects.count()
    ResourceAllocation.objects.all().delete()
    deleted_counts['ResourceAllocation'] = count

    # 3. ProjectWeekAllocation (depends on Project)
    count = ProjectWeekAllocation.objects.count()
    ProjectWeekAllocation.objects.all().delete()
    deleted_counts['ProjectWeekAllocation'] = count

    # 4. ProjectAssignment (depends on Resource, Project)
    count = ProjectAssignment.objects.count()
    ProjectAssignment.objects.all().delete()
    deleted_counts['ProjectAssignment'] = count

    # 5. Project (has FK to Department but nullable)
    count = Project.objects.count()
    Project.objects.all().delete()
    deleted_counts['Project'] = count

    # 6. Resource (has FK to Department and Supplier, both nullable)
    count = Resource.objects.count()
    Resource.objects.all().delete()
    deleted_counts['Resource'] = count

    # 7. Supplier (no dependencies)
    count = Supplier.objects.count()
    Supplier.objects.all().delete()
    deleted_counts['Supplier'] = count

    # Reset AppSettings to defaults (optional - comment out if you want to keep current settings)
    try:
        settings_obj = AppSettings.load()
        settings_obj.default_working_hours_per_week = 45
        settings_obj.save()
        print("[OK] AppSettings reset to defaults")
    except Exception as e:
        print(f"[WARNING] Could not reset AppSettings: {e}")

    print("\n=== CLEANUP COMPLETED ===")
    for model_name, count in deleted_counts.items():
        print(f"[DELETED] {count} {model_name} records")

    print(f"[PRESERVED] {Department.objects.count()} Department records")
    print()

def show_final_counts():
    """Display final database counts"""
    print("=== FINAL DATABASE COUNTS ===")
    print(f"Departments: {Department.objects.count()} ✓ PRESERVED")
    print(f"Projects: {Project.objects.count()}")
    print(f"Suppliers: {Supplier.objects.count()}")
    print(f"Resources: {Resource.objects.count()}")
    print(f"ProjectAssignments: {ProjectAssignment.objects.count()}")
    print(f"ResourceAllocations: {ResourceAllocation.objects.count()}")
    print(f"ProjectWeekAllocations: {ProjectWeekAllocation.objects.count()}")
    print(f"ExternalCapacities: {ExternalCapacity.objects.count()}")
    print(f"AppSettings: {AppSettings.objects.count()}")
    print()

if __name__ == "__main__":
    show_current_counts()
    cleanup_database()
    show_final_counts()
    print("SUCCESS: Database cleanup completed successfully!")
    print("Your client now has a clean Capacity Planning instance with preserved Department structure.")