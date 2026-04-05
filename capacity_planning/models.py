# capacity_planning/models.py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Sum, Count
from datetime import date, timedelta
from django.core.validators import RegexValidator
from accounts.models import Department
from psr.models import PSRProject
# =============================================================================
# 1. DEPARTMENT HIERARCHY (Refactored for Multi-level Support)
# # =============================================================================

# =============================================================================
# 2. PROJECT
# =============================================================================
STATUS_CHOICES = [
    ('QUOTED', 'Quoted'),
    ('PLANNED', 'Planned'),
    ('ORDERED', 'Ordered'),
]




class Project(models.Model):
    name = models.CharField(max_length=200)
    project_code = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        unique=True,  # recommended
        help_text="e.g. PRJ-2025-001"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='QUOTED')
    total_manhours = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Overall estimated total effort (optional global value)"
    )
    allotted_weeks = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Overall planned duration in weeks (optional global value)"
    )
    start_monday = models.DateField(
        null=True, blank=True,
        help_text="Global start (Monday) – optional"
    )
    end_monday = models.DateField(
        null=True, blank=True,
        help_text="Global end (Monday) – optional"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_projects'
    )
    color_code = models.CharField(
        max_length=7,
        null=True,
        blank=True,
        unique=True,
        validators=[RegexValidator(regex=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')],
        help_text="Hex color code for UI (e.g., #1e90ff)"
    )


    def __str__(self):
        return f"{self.project_code or 'NoCode'} – {self.name}"

    class Meta:
        ordering = ['-start_monday']

class ProjectDepartmentAllocation(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='department_allocations'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='project_allocations'
    )

    # Department-specific fields
    estimated_manhours = models.PositiveIntegerField(
        help_text="Estimated manhours for this department"
    )
    allotted_weeks = models.PositiveIntegerField(
        help_text="Allotted weeks for this department"
    )
    start_monday = models.DateField(
        help_text="Start Monday for this department's scope"
    )
    end_monday = models.DateField(
        null=True, blank=True,
        help_text="End Monday for this department's scope"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='QUOTED',
        help_text="Status specific to this department's work"
    )

    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('project', 'department')  # One allocation per project-department pair
        verbose_name = "Project-Department Allocation"
        verbose_name_plural = "Project-Department Allocations"

    def __str__(self):
        return f"{self.project} → {self.department.get_full_path()} ({self.status})"

    @property
    def duration_weeks(self):
        if self.end_monday:
            return (self.end_monday - self.start_monday).days // 7 + 1
        return self.allotted_weeks


# =============================================================================
# 3. SUPPLIER
# =============================================================================
class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField(blank=True)
    budgeted_hours = models.PositiveIntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    notes = models.TextField(blank=True, help_text="Special conditions, contacts, warnings")
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_budgeted_hours(self):
        """Update budgeted_hours based on total ExternalCapacity hours"""
        from django.db.models import Sum
        total_hours = self.external_capacities.aggregate(
            total=Sum('hours')
        )['total'] or 0
        self.budgeted_hours = total_hours
        self.save(update_fields=['budgeted_hours'])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Suppliers"


# =============================================================================
# 4. RESOURCE (Internal + External engineers)
# # =============================================================================
# ROLE_CHOICES = [
#     ('TL', 'Team Lead'),
#     ('PEM', 'Project Engineer Manager'),
#     ('SIM', 'Simulation Engineer'),
#     ('DES', 'Designer'),
#     ('PLC', 'PLC Engineer'),
#     ('ROB', 'Robotics Engineer'),
#     ('OTHER', 'Other'),
# ]

# class Resource(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

#     name = models.CharField(max_length=100)
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='OTHER')

#     emp_id = models.CharField(
#         max_length=50,
#         null=True,
#         blank=True,
#         unique=True,  # ← Enforces uniqueness in database
#         help_text="Employee ID from HR system (e.g. EMP001, 12345)"
#     )
    
#     is_internal = models.BooleanField(default=True, help_text="Uncheck for freelancers/contractors")
#     supplier = models.ForeignKey(
#         Supplier,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='external_resources'
#     )
#     hourly_rate = models.DecimalField(
#         max_digits=8,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         help_text="Only for externals – overrides supplier rate"
#     )

#     availability_per_week = models.PositiveIntegerField(null=True, blank=True, help_text="Override default availability from AppSettings")
#     is_active = models.BooleanField(default=True)

#     # Updated to use multi-level Department
#     department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True)
#     joining_date = models.DateField(null=True, blank=True, help_text="Date the resource joined the company") # Or whatever semantics fit your use case
#     leaving_date = models.DateField(null=True, blank=True, help_text="Date the resource leaves the company") # Or whatever semantics fit your use case
#     def clean(self):
#         if not self.is_internal and not self.supplier:
#             raise ValidationError("External resource must have a supplier.")
#         if self.is_internal and self.supplier:
#             raise ValidationError("Internal resource cannot have a supplier.")

#     @property
#     def effective_availability_per_week(self):
#         """Return the availability per week, using AppSettings default if not overridden"""
#         if self.availability_per_week is not None:
#             return self.availability_per_week
#         else:
#             settings = AppSettings.load()
#             return settings.default_working_hours_per_week

#     def save(self, *args, **kwargs):
#         # Only set default if this is a new instance and availability_per_week is not set
#         if self.pk is None and self.availability_per_week is None:
#             settings = AppSettings.load()
#             self.availability_per_week = settings.default_working_hours_per_week
#         super().save(*args, **kwargs)

#     def __str__(self):
#         suffix = f" ({self.supplier})" if self.supplier else " (Internal)"
#         dept_info = f" - {self.department.get_full_path()}" if self.department else ""
#         return f"{self.name}{suffix}{dept_info}"

#     class Meta:
#         ordering = ['name']
#         verbose_name_plural = "Resources"


# =============================================================================
ROLE_CHOICES = [
    ('TL', 'Team Lead'),
    ('PEM', 'Project Engineer Manager'),
    ('SIM', 'Simulation Engineer'),
    ('DES', 'Designer'),
    ('PLC', 'PLC Engineer'),
    ('ROB', 'Robotics Engineer'),
    ('OTHER', 'Other'),
]

class Resource(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='OTHER')

    emp_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        unique=True,
        help_text="Employee ID from HR system (e.g. EMP001, 12345)"
    )
    
    is_internal = models.BooleanField(default=True, help_text="Uncheck for freelancers/contractors")
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='external_resources'
    )
    hourly_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Only for externals – overrides supplier rate"
    )

    availability_per_week = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Override default availability from AppSettings"
    )
    is_active = models.BooleanField(default=True)
    
    # Changed from ForeignKey to ManyToManyField
    departments = models.ManyToManyField(
        Department,
        related_name='resources',
        blank=True,
        help_text="Departments this resource can work in"
    )

    joining_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date the resource joined the company"
    )
    leaving_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date the resource leaves the company"
    )

    def clean(self):
        if not self.is_internal and not self.supplier:
            raise ValidationError("External resource must have a supplier.")
        if self.is_internal and self.supplier:
            raise ValidationError("Internal resource cannot have a supplier.")

    @property
    def effective_availability_per_week(self):
        """Return the availability per week, using AppSettings default if not overridden"""
        if self.availability_per_week is not None:
            return self.availability_per_week
        else:
            settings = AppSettings.load()
            return settings.default_working_hours_per_week

    def save(self, *args, **kwargs):
        if self.pk is None and self.availability_per_week is None:
            settings = AppSettings.load()
            self.availability_per_week = settings.default_working_hours_per_week
        super().save(*args, **kwargs)

    def __str__(self):
        suffix = f" ({self.supplier})" if self.supplier else " (Internal)"
        depts = ", ".join(d.name for d in self.departments.all())
        dept_info = f" - {depts}" if depts else ""
        return f"{self.name}{suffix}{dept_info}"

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Resources"

# =============================================================================
# 7. PLANNED WEEKLY DEMAND (what the project needs)
# =============================================================================
# class ProjectWeekAllocation(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='planned_weeks')
#     week_monday = models.DateField(db_index=True)
#     manhours = models.PositiveIntegerField(default=0, help_text="Planned manhours needed this week")
    
#     # ← ADD THIS LINE
#     notes = models.CharField(max_length=200, blank=True, help_text="e.g. Christmas week, Waiting for BOM, Design freeze")

#     class Meta:
#         unique_together = ('project', 'week_monday')
#         ordering = ['week_monday']
#         verbose_name = "Planned Weekly Demand"

#     def __str__(self):
#         return f"{self.project.project_code} | {self.week_monday:%b %d} → {self.manhours}h {self.notes}"



class ProjectWeekAllocation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='planned_weeks')
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='planned_weeks',
        null=True, blank=True  # Allow null during transition if needed
    )
    week_monday = models.DateField(db_index=True)
    manhours = models.PositiveIntegerField(default=0)
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('project', 'department', 'week_monday')  # Updated constraint
        ordering = ['week_monday']
        verbose_name = "Planned Weekly Demand"

    def __str__(self):
        dept = self.department.name if self.department else "Global"
        return f"{self.project.project_code} | {dept} | {self.week_monday:%b %d} → {self.manhours}h"

# =============================================================================
# 5. PROJECT ↔ RESOURCE ASSIGNMENT (Team membership - Week-wise)
# =============================================================================
# class ProjectAssignment(models.Model):
#     week_allocation = models.ForeignKey(
#         ProjectWeekAllocation,
#         on_delete=models.CASCADE,           # ← Automatic deletion when parent is deleted
#         related_name='assignments',
#         null=True,
#         blank=True
#     )
#     resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='project_assignments')
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='team_members')
#     is_lead = models.BooleanField(default=False)
#     notes = models.TextField(blank=True)
#     week_monday = models.DateField(db_index=True, help_text="Monday of the week when assignment starts")
#     removed_on = models.DateField(null=True, blank=True, help_text="Monday of the week when assignment ends")

#     class Meta:
#         unique_together = ('resource', 'project', 'week_monday')
#         ordering = ['-week_monday']

#     def __str__(self):
#         lead = " (Lead)" if self.is_lead else ""
#         removed = f" (Removed: {self.removed_on})" if self.removed_on else ""
#         return f"{self.resource} → {self.project} (Week: {self.week_monday:%b %d}){lead}{removed}"


# # =============================================================================
# # 6. WEEKLY ALLOCATION (Actual hours – internal + external)
# # =============================================================================
# class ResourceAllocation(models.Model):
#     week_allocation = models.ForeignKey(
#         ProjectWeekAllocation,
#         on_delete=models.CASCADE,           # ← Automatic deletion when parent is deleted
#         related_name='resource_allocations',
#         null=True,
#         blank=True
#     )
#     resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     week_monday = models.DateField(db_index=True)
#     hours = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(45)])

#     class Meta:
#         unique_together = [('resource', 'project', 'week_monday')]
#         indexes = [models.Index(fields=['week_monday'])]
#         verbose_name = "Weekly Resource Allocation"

#     def clean(self):
#         if self.project.start_monday and self.week_monday < self.project.start_monday:
#             raise ValidationError("Cannot allocate internal capacity before the project's start date.")
#         if self.project.end_monday and self.week_monday > self.project.end_monday:
#             raise ValidationError("Cannot allocate internal capacity after the project's end date.")

#         # Check total hours per resource per week do not exceed availability
#         resource_total = ResourceAllocation.objects.filter(resource=self.resource, week_monday=self.week_monday).exclude(
#             pk=self.pk if self.pk else None
#         ).aggregate(total=Sum('hours'))['total'] or 0
#         if resource_total + self.hours > self.resource.effective_availability_per_week:
#             raise ValidationError(
#                 f"Total allocated hours for {self.resource.name} in week {self.week_monday} ({resource_total + self.hours}) would exceed their weekly availability ({self.resource.effective_availability_per_week} hours)."
#             )

#         # Check total capacity does not exceed total_manhours
#         internal_sum = ResourceAllocation.objects.filter(project=self.project).exclude(
#             pk=self.pk if self.pk else None
#         ).aggregate(total=Sum('hours'))['total'] or 0
#         external_sum = ExternalCapacity.objects.filter(project=self.project).aggregate(total=Sum('hours'))['total'] or 0
#         if internal_sum + external_sum + self.hours > self.project.total_manhours:
#             raise ValidationError(
#                 f"Total allocated capacity ({internal_sum + external_sum + self.hours} hours) would exceed the project's total manhours ({self.project.total_manhours})."
#             )

#     def save(self, *args, **kwargs):
#         self.full_clean()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.resource} → {self.project.project_code} ({self.week_monday:%b %d}): {self.hours}h"


# In capacity_planning/models.py

class ProjectAssignment(models.Model):
    week_allocation = models.ForeignKey(
        ProjectWeekAllocation,
        on_delete=models.CASCADE,
        related_name='assignments',
        null=True,
        blank=True
    )
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='project_assignments')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='team_members')
    
    # NEW: Department-specific assignment
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='project_assignments',
        null=True,
        blank=True  # Required - must know which dept this assignment is for
    )
    
    is_lead = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    week_monday = models.DateField(db_index=True)
    removed_on = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('resource', 'project', 'department', 'week_monday')  # Updated constraint
        ordering = ['-week_monday']

    def __str__(self):
        lead = " (Lead)" if self.is_lead else ""
        return f"{self.resource} → {self.project} ({self.department.name}) (Week: {self.week_monday:%b %d}){lead}"


class ResourceAllocation(models.Model):
    week_allocation = models.ForeignKey(
        ProjectWeekAllocation,
        on_delete=models.CASCADE,
        related_name='resource_allocations',
        null=True,
        blank=True
    )
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    # NEW: Department-specific allocation
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='resource_allocations',
        null=True,
        blank=True  # Required
    )
    
    week_monday = models.DateField(db_index=True)
    hours = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(45)])

    class Meta:
        unique_together = [('resource', 'project', 'department', 'week_monday')]
        indexes = [models.Index(fields=['week_monday'])]
        verbose_name = "Weekly Resource Allocation"

    def clean(self):
        # ... existing clean logic ...

        # Add department-specific capacity check (optional enhancement)
        dept_alloc = ProjectDepartmentAllocation.objects.filter(
            project=self.project,
            department=self.department
        ).first()
        if dept_alloc and self.week_monday < dept_alloc.start_monday:
            raise ValidationError("Cannot allocate before department start date.")

    def __str__(self):
        return f"{self.resource} → {self.project.project_code} ({self.department.name}) ({self.week_monday:%b %d}): {self.hours}h"

# =============================================================================
# 8. APP SETTINGS (singleton)
# =============================================================================
class AppSettings(models.Model):
    default_working_hours_per_week = models.PositiveIntegerField(default=45)

    class Meta:
        verbose_name = "App Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
    
# External Capacity Supplier-Project Wise
class ExternalCapacity(models.Model):
    supplier = models.ForeignKey(
        'Supplier',
        on_delete=models.CASCADE,
        related_name='external_capacities'
    )
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='external_capacities'
    )
    dept = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='external_capacities_dept',
        null=True,
        blank=True  # Required - must know which dept this assignment is for
    )
       
    week_monday = models.DateField(db_index=True)
    hours = models.PositiveIntegerField(
        default=0,
        help_text="Weekly hours this supplier can provide for this project (external capacity)"
    )

    class Meta:
        unique_together = ('supplier', 'project','dept','week_monday')
        verbose_name_plural = "External Capacities (Supplier-Project Level)"
        ordering = ['-week_monday']

    def clean(self):
        if self.project.start_monday and self.week_monday < self.project.start_monday:
            raise ValidationError("Cannot allocate external capacity before the project's start date.")
        if self.project.end_monday and self.week_monday > self.project.end_monday:
            raise ValidationError("Cannot allocate external capacity after the project's end date.")

        # Check total capacity does not exceed total_manhours
        internal_sum = ResourceAllocation.objects.filter(project=self.project).aggregate(total=Sum('hours'))['total'] or 0
        external_sum = ExternalCapacity.objects.filter(project=self.project).exclude(
            pk=self.pk if self.pk else None
        ).aggregate(total=Sum('hours'))['total'] or 0
        if internal_sum + external_sum + self.hours > self.project.total_manhours:
            raise ValidationError(
                f"Total allocated capacity ({internal_sum + external_sum + self.hours} hours) would exceed the project's total manhours ({self.project.total_manhours})."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.supplier.name} → {self.project.project_code} – {self.week_monday} – {self.hours}h"