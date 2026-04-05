from django.contrib import admin

# Register your models here.

from .models import *

from accounts.models import CustomUser as User

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
 
    list_display = (
        "id",
     
        "project",
        "department",
        "project_manager",
        "hod",
        "total_budget",
        "actual_expense",
        "status",
        "created_at",
    )
 
    list_filter = (
      
        "status",
        "created_at",
    )
 
    search_fields = (
        "id",
        "project__project_code",
        "project__name",
        "department__name",
        "project_manager__username",
        "hod__username",
    )
 
    readonly_fields = (
        "created_at",
        "updated_at",
        "actual_expense",
        "created_by",
    )
 
    fieldsets = (
        ("Project Details", {
            "fields": ("project", "project_manager")
        }),
        ("Non-Project / CapEx Details", {
            "fields": ("total_budget","department", "hod","project_type")
        }),
       
        ("Status & Audit", {
            "fields": ("status", "created_by", "created_at", "updated_at")
        }),
    )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ("project_manager", "hod"):
            kwargs["queryset"] = User.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs) 
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "project_manager":
    #         kwargs["queryset"] = User.objects.filter(
    #             role="Project Manager",
    #             is_active=True
    #         )
    #     elif db_field.name == "hod":
    #         kwargs["queryset"] = User.objects.filter(
    #             role="Hod",
    #             is_active=True
    #         )
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)
 
@admin.register(ProjectBudget)
class ProjectBudgetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "project",
        "budget",
        "created_at",
    )
 
    list_filter = (
        "project__status",
    )
 
    search_fields = (
        "project__project__name",
        "project__project__project_code",
    )
 
    readonly_fields = ("created_at",)
 
@admin.register(CashInflow)
class CashInflowAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "project",
        "amount",
        "date",
        "status",
        "created_at",
    )
 
    list_filter = (
        "status",
        "date",
        "project__status",
    )
 
    search_fields = (
        "project__project__name",
        "project__project__project_code",
    )
 
    readonly_fields = ("created_at",)
 
    ordering = ("-date",)

@admin.register(ProjectBoard)
class ProjectBoardAdmin(admin.ModelAdmin):
    # 1. Columns to display in the list view
    list_display = (
        'document_no', 
        'project', 
        'commodity_equipment', 
        'procurement_type', 
        'commodity_budget', 
        'pb_status', 
        'buyer'
    )

    # 2. Sidebar filters for quick navigation
    list_filter = ('pb_status', 'procurement_type', 'is_amc', 'project')

    # 3. Search functionality
    search_fields = ('document_no', 'commodity_equipment', 'project__name')

    # 4. Read-only fields (since document_no is auto-generated)
    readonly_fields = ('document_no', 'amc_end_date', 'created_at', 'updated_at')

    # 5. Organizing the Edit Form into logical sections
    fieldsets = (
        ('Basic Information', {
            'fields': ('document_no', 'project', 'commodity_equipment', 'commodity_budget')
        }),
        ('Procurement Details', {
            'fields': (
                ('procurement_type', 'pb_status'),
                ('cost_center', 'rfq_sign_off_date'),
                ('buyer', 'created_by'),
            )
        }),
        ('Financials', {
            'fields': (('currency', 'exchange_rate'),)
        }),
        ('AMC / Service Details', {
            'description': 'Only applicable if Procurement Type is Service',
            'classes': ('collapse',), # Makes this section collapsible
            'fields': ('is_amc', 'amc_start_date', 'amc_duration_months', 'amc_end_date')
        }),
        ('System Metadata', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )

    # 6. Default ordering
    ordering = ('-created_at',)
admin.site.register(CommercialRequirement)
admin.site.register(Supplier)
admin.site.register(SupplierNegotiation)
admin.site.register(LineItemNegotiation)
admin.site.register(LineItem)
admin.site.register(Term)
@admin.register(TermCondition)
class TermConditionAdmin(admin.ModelAdmin):
    # Columns to display in the list view
    list_display = ('condition_name', 'term', 'created_by')
    
    # Filters on the right sidebar
    list_filter = ('term', 'created_by')
    
    # Search functionality for quick navigation
    search_fields = ('condition_name', 'term__name') # Assuming 'Term' model has a 'name' field
    
    # Automate the 'created_by' field so the developer doesn't have to pick a user manually
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If creating a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
admin.site.register(ApprovalRejection)
admin.site.register(Approver)
admin.site.register(ExcelFile)
admin.site.register(ProcurementUpload)
@admin.register(ChangeRequest)
class ChangeRequestAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('content_type', 'object_id', 'content_object', 'requested_by', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'content_type', 'created_at')
    search_fields = ('object_id', 'requested_by__username')
    readonly_fields = ('created_at',)
    
    # Custom action to approve multiple requests at once
    actions = ['approve_changes']

    def approve_changes(self, request, queryset):
        success_count = 0
        error_count = 0
        
        for cr in queryset:
            if not cr.is_approved:
                try:
                    cr.apply_changes()
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    self.message_user(request, f"Error applying CR #{cr.id}: {str(e)}", messages.ERROR)
            else:
                self.message_user(request, f"CR #{cr.id} was already approved.", messages.WARNING)
        
        if success_count:
            self.message_user(request, f"Successfully applied {success_count} change requests.", messages.SUCCESS)

    approve_changes.short_description = "Approve and Apply selected changes"

    # Optional: Format the JSON data so it looks nice in the admin detail view
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.is_approved:
            return self.readonly_fields + ('pending_data', 'content_type', 'object_id', 'requested_by')
        return self.readonly_fields
    

@admin.register(Draft)
class ChangeRequestAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('content_type','id','is_approved')
    list_filter = ('is_approved', 'content_type', 'created_at')
    search_fields = ('object_id', 'requested_by__username')
    readonly_fields = ('created_at',)
    
    # Custom action to approve multiple requests at once
    actions = ['approve_changes']

    def approve_changes(self, request, queryset):
        success_count = 0
        error_count = 0
        
        for cr in queryset:
            if not cr.is_approved:
                try:
                    cr.apply_changes()
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    self.message_user(request, f"Error applying CR #{cr.id}: {str(e)}", messages.ERROR)
            else:
                self.message_user(request, f"CR #{cr.id} was already approved.", messages.WARNING)
        
        if success_count:
            self.message_user(request, f"Successfully applied {success_count} change requests.", messages.SUCCESS)

    approve_changes.short_description = "Approve and Apply selected changes"

    # Optional: Format the JSON data so it looks nice in the admin detail view
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.is_approved:
            return self.readonly_fields + ('pending_data', 'content_type', 'object_id', 'requested_by')
        return self.readonly_fields
    
@admin.register(TermAssignment)
class TermAssignmentAdmin(admin.ModelAdmin):
    # Columns to show in the list view
    list_display = (
        'project_board', 
        'supplier',
        'term', 
        'status_type', 
        'percentage', 
        'date', 
        'created_at'
    )
    
    # Filters on the right sidebar
    list_filter = ('status_type','supplier','project_board', 'created_at')
    
    # Search box for text details and project names
    search_fields = ('text_detail', 'comments', 'project_board__name', 'term__name')
    
    # Organize fields into sections in the detail view
    fieldsets = (
        ('Relationship', {
            'fields': ('project_board', 'supplier', 'term', 'status_type')
        }),
        ('Milestone Details', {
            'fields': ('percentage', 'date', 'text_detail', 'justification')
        }),
        ('Audit', {
            'fields': ('created_by', 'comments'),
            'classes': ('collapse',), # Hides this section by default
        }),
    )

    # Automatically set 'created_by' to the logged-in admin user
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)