

# capacity_planning/admin.py
from django.contrib import admin
from django.db.models import Sum, Count
from django.utils.html import format_html
from .models import *

from accounts.models import Department

# =============================================================================
# 1. DEPARTMENT ADMIN (unchanged, still supports hierarchy)
# =============================================================================
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'level', 'order', 'children_count']
    list_filter = ['level', 'parent']
    search_fields = ['name']
    ordering = ['order', 'name']
    list_editable = ['order']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'parent', 'order')
        }),
        ('Hierarchy Info (Auto-calculated)', {
            'fields': ('level',),
            'classes': ('collapse',),
            'description': 'This field is automatically calculated based on parent hierarchy.'
        }),
    )
    
    readonly_fields = ['level']
    
    def children_count(self, obj):
        return obj.children.count()
    children_count.short_description = 'Sub-departments'


# =============================================================================
# 2. PROJECT DEPARTMENT ALLOCATION ADMIN (NEW - for department-specific project details)
# =============================================================================
@admin.register(ProjectDepartmentAllocation)
class ProjectDepartmentAllocationAdmin(admin.ModelAdmin):
    list_display = [
        'project_code', 'department_path', 'estimated_manhours', 
        'allotted_weeks', 'start_monday', 'duration_weeks', 'status'
    ]
    list_filter = ['status', 'department', 'start_monday']
    search_fields = ['project__name', 'project__project_code', 'department__name']
    date_hierarchy = 'start_monday'
    autocomplete_fields = ['project', 'department']
    
    fieldsets = (
        ('Project & Department', {
            'fields': ('project', 'department')
        }),
        ('Department-Specific Timeline', {
            'fields': ('start_monday', 'end_monday', 'allotted_weeks')
        }),
        ('Effort & Status', {
            'fields': ('estimated_manhours', 'status')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )
    
    readonly_fields = ['duration_weeks']
    
    def project_code(self, obj):
        return obj.project.project_code
    project_code.short_description = 'Project Code'
    
    def department_path(self, obj):
        return obj.department.get_full_path()
    department_path.short_description = 'Department'
    
    @admin.display(description='Duration Weeks')
    def duration_weeks(self, obj):
        return obj.duration_weeks


# =============================================================================
# 3. PROJECT ADMIN (updated – no direct department, uses inline allocations)
# =============================================================================
class ProjectDepartmentAllocationInline(admin.TabularInline):
    model = ProjectDepartmentAllocation
    extra = 1
    autocomplete_fields = ['department']
    fields = ['department', 'estimated_manhours', 'allotted_weeks', 'start_monday', 'end_monday', 'status']
    verbose_name = "Department Allocation"
    verbose_name_plural = "Department Allocations"


class ProjectAssignmentInline(admin.TabularInline):
    model = ProjectAssignment
    extra = 1
    autocomplete_fields = ['resource']


class ProjectWeekAllocationInline(admin.TabularInline):
    model = ProjectWeekAllocation
    extra = 3
    fields = ['week_monday', 'manhours', 'notes']


class ExternalCapacityInline(admin.TabularInline):
    model = ExternalCapacity
    extra = 1
    autocomplete_fields = ['supplier']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'project_code', 'name', 'status', 'global_duration', 
        'total_manhours', 'department_count', 'team_size'
    ]
    list_filter = ['status', 'start_monday']
    search_fields = ['name', 'project_code']
    list_editable = ['status']
    date_hierarchy = 'start_monday'
    
    fieldsets = (
        ('Project Information', {
            'fields': ('name', 'project_code', 'status', 'color_code')
        }),
        ('Global Timeline (Optional)', {
            'fields': ('start_monday', 'end_monday', 'allotted_weeks')
        }),
        ('Global Effort (Optional)', {
            'fields': ('total_manhours',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    inlines = [
        ProjectDepartmentAllocationInline,  # ← NEW: assign multiple departments here
        ProjectAssignmentInline,
        ProjectWeekAllocationInline,
        ExternalCapacityInline
    ]
    
    def global_duration(self, obj):
        if obj.end_monday:
            return f"{obj.start_monday} → {obj.end_monday}"
        return f"{obj.allotted_weeks} weeks"
    global_duration.short_description = 'Global Duration'
    
    def department_count(self, obj):
        count = obj.department_allocations.count()
        return format_html('<b>{}</b>', count) if count > 0 else '-'
    department_count.short_description = 'Departments'
    
    def team_size(self, obj):
        count = obj.team_members.values('resource').distinct().count()
        return format_html('<b>{}</b>', count)
    team_size.short_description = 'Team Size'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by on new projects
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# =============================================================================
# 4. SUPPLIER ADMIN (unchanged)
# =============================================================================
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_email', 'budgeted_hours', 'hourly_rate', 'is_active', 'resource_count']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'contact_email']
    list_editable = ['is_active', 'hourly_rate']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'contact_email', 'is_active')
        }),
        ('Financial', {
            'fields': ('budgeted_hours', 'hourly_rate')
        }),
        ('Additional Info', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def resource_count(self, obj):
        return obj.external_resources.count()
    resource_count.short_description = 'Resources'


# =============================================================================
# 5. RESOURCE ADMIN (updated for M2M departments)
# =============================================================================
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'role', 'get_departments', 'is_internal', 
        'supplier', 'availability_per_week', 'is_active'
    ]
    list_filter = ['is_internal', 'is_active', 'role', 'supplier']
    search_fields = ['name', 'user__username', 'user__email', 'departments__name']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'role', 'departments')  # ← M2M field
        }),
        ('Employment Type', {
            'fields': ('is_internal', 'supplier', 'hourly_rate')
        }),
        ('Availability', {
            'fields': ('availability_per_week', 'is_active')
        }),
        ('Dates', {
            'fields': ('joining_date', 'leaving_date')
        }),
    )
    
    @admin.display(description='Departments')
    def get_departments(self, obj):
        return ", ".join([d.name for d in obj.departments.all()]) or "—"


# =============================================================================
# 6. PROJECT ASSIGNMENT ADMIN (unchanged)
# =============================================================================
@admin.register(ProjectAssignment)
class ProjectAssignmentAdmin(admin.ModelAdmin):
    list_display = ['resource', 'project', 'week_monday', 'removed_on', 'is_lead']
    list_filter = ['is_lead', 'week_monday', 'project__status']
    search_fields = ['resource__name', 'project__name', 'project__project_code']
    date_hierarchy = 'week_monday'
    autocomplete_fields = ['resource', 'project']
    
    fieldsets = (
        ('Assignment', {
            'fields': ('resource', 'project', 'is_lead')
        }),
        ('Timeline', {
            'fields': ('week_monday', 'removed_on')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )


# =============================================================================
# 7. RESOURCE ALLOCATION ADMIN (unchanged)
# =============================================================================
@admin.register(ResourceAllocation)
class ResourceAllocationAdmin(admin.ModelAdmin):
    list_display = ['resource', 'project', 'week_monday', 'hours', 'utilization_indicator']
    list_filter = ['week_monday', 'project__status']
    search_fields = ['resource__name', 'project__name', 'project__project_code']
    date_hierarchy = 'week_monday'
    autocomplete_fields = ['resource', 'project']
    
    fieldsets = (
        ('Allocation', {
            'fields': ('resource', 'project', 'week_monday', 'hours')
        }),
    )
    
    def utilization_indicator(self, obj):
        if obj.hours >= 40:
            color = 'green'
        elif obj.hours >= 20:
            color = 'orange'
        else:
            color = 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} hrs</span>',
            color, obj.hours
        )
    utilization_indicator.short_description = 'Utilization'


# =============================================================================
# 8. PROJECT WEEK ALLOCATION ADMIN (unchanged)
# =============================================================================
@admin.register(ProjectWeekAllocation)
class ProjectWeekAllocationAdmin(admin.ModelAdmin):
    list_display = ['project', 'week_monday', 'manhours', 'notes']
    list_filter = ['week_monday', 'project__status']
    search_fields = ['project__name', 'project__project_code', 'notes']
    date_hierarchy = 'week_monday'
    autocomplete_fields = ['project']
    
    fieldsets = (
        ('Allocation', {
            'fields': ('project', 'week_monday', 'manhours')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )


# =============================================================================
# 9. EXTERNAL CAPACITY ADMIN (unchanged)
# =============================================================================
@admin.register(ExternalCapacity)
class ExternalCapacityAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'project','dept', 'week_monday', 'hours']
    list_filter = ['supplier', 'week_monday', 'project__status']
    search_fields = ['supplier__name', 'project__name', 'project__project_code']
    date_hierarchy = 'week_monday'
    autocomplete_fields = ['supplier', 'project']
    
    fieldsets = (
        ('Capacity Allocation', {
            'fields': ('supplier', 'project','dept', 'week_monday', 'hours')
        }),
    )


# =============================================================================
# 10. APP SETTINGS ADMIN (Singleton - unchanged)
# =============================================================================
@admin.register(AppSettings)
class AppSettingsAdmin(admin.ModelAdmin):
    list_display = ['default_working_hours_per_week']
    
    fieldsets = (
        ('Default Settings', {
            'fields': ('default_working_hours_per_week',),
            'description': 'These settings apply globally to all resources unless overridden.'
        }),
    )
    
    def has_add_permission(self, request):
        return not AppSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False