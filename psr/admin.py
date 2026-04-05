from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from psr.models import *



@admin.register(GRRData)
class GRRDataAdmin(admin.ModelAdmin):
    # What to show in the list view
    list_display = (
        'grr_no', 'co_no', 'po_no', 'grr_date', 
        'supplier_name', 'received_qty', 'rate', 'imported_at'
    )
    
    # Sidebar filters
    list_filter = ('grr_date', 'imported_at')
    
    # Search functionality
    search_fields = ('grr_no', 'co_no', 'po_no', 'supplier_name', 'item_code')
    
    # Making these read-only helps maintain data integrity for "dump" tables
    readonly_fields = ('imported_at', 'updated_at')
    
    # Optional: Group fields in the detail view
    fieldsets = (
        ('Identifiers', {
            'fields': ('grr_no', 'co_no', 'po_no')
        }),
        ('Material Details', {
            'fields': ('item_code', 'description', 'supplier_name')
        }),
        ('Transaction Info', {
            'fields': ('grr_date', 'rate', 'received_qty')
        }),
        ('Metadata', {
            'fields': ('imported_at', 'updated_at')
        }),
    )

@admin.register(PCRData)
class PCRDataAdmin(admin.ModelAdmin):
    list_display = (
        'pcr_no', 'co_no', 'po_no', 'pcr_date', 
        'supplier_name', 'recp_qty', 'rate', 'imported_at'
    )
    list_filter = ('pcr_date', 'imported_at')
    search_fields = ('pcr_no', 'co_no', 'po_no', 'supplier_name', 'item_code')
    readonly_fields = ('imported_at', 'updated_at')
    
    fieldsets = (
        ('Identifiers', {
            'fields': ('pcr_no', 'co_no', 'po_no')
        }),
        ('Material Details', {
            'fields': ('item_code', 'description', 'supplier_name')
        }),
        ('Transaction Info', {
            'fields': ('pcr_date', 'rate', 'recp_qty')
        }),
        ('Metadata', {
            'fields': ('imported_at', 'updated_at')
        }),
    )
@admin.register(PSRProject)
class PSRProjectAdmin(admin.ModelAdmin):
    list_display = (
        'co_no',
        'project_name',
        'location',
        'project_manager',
        'currency',
        'exchange_rate',
        'sales_value',
        'ebit_percentage',              # now calculated
        'direct_margin_percentage',     # now input
        'sgna_percentage',
        'hk',
        'hk2',                          # new
        'sk_value',                     # new
        'actual_budget',
        'created_at',
    )

    list_filter = (
        'currency',
        'location',
        'created_at',
        'sgna_percentage',
    )

    search_fields = (
        'co_no',
        'project_name',
        'project_manager__username',    # works if project_manager is a User
        'sales_person',
    )

    readonly_fields = (
        'created_at',
        'updated_at',

        # All auto-calculated fields
        'sales_value',
        'ebit_percentage',              # now calculated
        'ebit_value',
        'sgna_value',
        'cost_with_sgna',               # legacy (never updated anymore)
        'hk',
        'hk2',
        'sk_value',
        'direct_margin_value',
        'ter_value',
        'eff_value',
        'actual_budget',
        'budget',
        # 'factor',                     # field no longer exists in model
    )

    fieldsets = (
        ('Project Identification', {
            'fields': ('co_no', 'project_name', 'location')
        }),
        ('Personnel', {
            'fields': (
                'project_manager',
                'project_manager_email',
                'sales_person',
                'sales_person_email',
            )
        }),
        ('Financial Planning Inputs', {
            'fields': (
                'sales_value_foreign_curr',
                'direct_margin_percentage',   # ← replaced ebit_percentage
                'sgna_percentage',
                'eff_percentage',
                'ter_percentage',
                'risk',                       # ← now editable
            ),
        }),
        ('Calculated Financial Values', {
            'fields': (
                'sales_value',
                'ebit_percentage',
                'ebit_value',
                'sgna_value',
                'cost_with_sgna',            # legacy
                'hk',
                'hk2',
                'sk_value',
                'direct_margin_value',
                'ter_value',
                'eff_value',
                'actual_budget',
                'budget',
            ),
            'classes': ('collapse',),
        }),
        ('Currency Settings', {
            'fields': ('currency', 'exchange_rate')
        }),
        ('Project Status', {
            'fields': ('cw_no', 'current_phase', 'settlement_period')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )



@admin.register(PSRDepartment)
class PSRDepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'project',
        'name',
        'hourly_rate',
        'budget_cost',
        'budget_hours',
        'created_at',
    )

    list_filter = (
        'name',
        'project__co_no',
        'project__currency',
    )

    search_fields = (
        'project__co_no',
        'project__project_name',
        'name',
    )

    raw_id_fields = ('project',)

    readonly_fields = (
        'created_at',
        'updated_at',
        'budget_cost',
        'budget_hours',
    )

    fieldsets = (
        ('Department Details', {
            'fields': (
                'project',
                'name',
                'hourly_rate',
            )
        }),
        ('Budget', {
            'fields': (
                'budget_cost',
                'budget_hours',
            ),
        }),
        ('Metadata', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )


@admin.register(PSRSubDepartment)
class PSRSubDepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'role_descrptn',
        'inkrement',
        'budget_cost',
        'budget_hours',
        'forecast_override',
        'forecast_cost',
        'department',
        'created_at',
    )

    list_filter = (
        'department__name',
        'department__project__co_no',
        'department__project__currency',
        'forecast_override',
    )

    search_fields = (
        'code',
        'role_descrptn',
        'inkrement',
        'department__project__co_no',
        'department__project__project_name',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'budget_hours',
        'baseline_budget_hours',
        'forecast_overridden_by',
        'forecast_overridden_at',
    )

    fieldsets = (
        ('Sub-Department Details', {
            'fields': (
                'department',
                'code',
                'role_descrptn',
                'inkrement',
            )
        }),
        ('Baseline Budget (Read-only)', {
            'fields': (
                'baseline_budget_hours',
            ),
            'classes': ('collapse',),
        }),
        ('Current Budget', {
            'fields': (
                'budget_cost',
                'budget_hours',
            ),
        }),
        ('Forecast Override', {
            'fields': (
                'forecast_override',
                'forecast_hours',
                'forecast_cost',
                'forecast_overridden_by',
                'forecast_overridden_at',
            ),
        }),
        ('Metadata', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )



@admin.register(TimesheetEntry)
class TimesheetEntryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'date',
        'co_no',
        'emp_cd',
        'emp_name',
        'role_description',
        'hours',
    )

    list_filter = (
        'date',
        'co_no',
        'role_description',
    )

    search_fields = (
        'emp_cd',
        'emp_name',
        'role_description',
        'co_no',
    )

    readonly_fields = (
        'imported_at',
        'updated_at',
    )

    date_hierarchy = 'date'
    list_per_page = 50



@admin.register(POData)
class PODataAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'co_no',
        'project_name',
        'mat_code',
        'po_value_inr',
    )

    list_filter = (
        'mat_code',
    )

    search_fields = (
        'co_no',
        'mat_code',
        'project_name',
    )

    readonly_fields = (
        'imported_at',
        'updated_at',
    )

    list_per_page = 50



@admin.register(CostCategory)
class CostCategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'code',
        'name',
        'mat_code',
    )

    search_fields = (
        'code',
        'name',
        'mat_code',
    )

    list_filter = (
        'code',
    )

    readonly_fields = (
        'name',
    )

    fieldsets = (
        ('Category Details', {
            'fields': (
                'code',
                'mat_code',
                'name',
            )
        }),
    )

    def has_add_permission(self, request):
        return CostCategory.objects.count() == 0 or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return False




class RKActualAdjustmentLineInline(admin.TabularInline):
    model = RKActualAdjustmentLine
    extra = 1
    fields = (
        'description',
        'amount',
    )

class RKActualAdjustmentInline(admin.TabularInline):
    model = RKActualAdjustment
    extra = 0
    fields = (
        'note',
        'adjusted_by',
        'adjusted_at',
    )
    readonly_fields = (
        'adjusted_by',
        'adjusted_at',
    )
    show_change_link = True


@admin.register(RKActualAdjustment)
class RKActualAdjustmentAdmin(admin.ModelAdmin):
    list_display = (
        'project_cost_category',
        'adjusted_by',
        'note',
        'adjusted_at',
    )

    list_filter = (
        'project_cost_category__project__co_no',
        'adjusted_by',
        'adjusted_at',
    )

    search_fields = (
        'project_cost_category__project__co_no',
        'note',
    )

    date_hierarchy = 'adjusted_at'

    inlines = (
        RKActualAdjustmentLineInline,
    )

    readonly_fields = (
        'adjusted_at',
        'adjusted_by',
    )

    fieldsets = (
        ('Adjustment Info', {
            'fields': (
                'project_cost_category',
                'note',
                'adjusted_by',
                'adjusted_at',
            )
        }),
    )






@admin.register(ProjectCostCategory)
class ProjectCostCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'project',
        'cost_category',
        'baseline_budget_cost',
        'budget_cost',
        'actual_override',
        'forecast_override',
        'forecast_cost',
        'forecast_overridden_by',
        'updated_at',
    )

    list_filter = (
        'project__co_no',
        'cost_category__code',
        'forecast_override',
        'actual_override',
    )

    search_fields = (
        'project__co_no',
        'project__project_name',
        'cost_category__code',
        'cost_category__name',
    )

    raw_id_fields = (
        'project',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'baseline_budget_cost',
        'forecast_overridden_by',
    )

    fieldsets = (
        ('Project & Category', {
            'fields': (
                'project',
                'cost_category',
            )
        }),
        ('Baseline Budget (Read-only)', {
            'fields': (
                'baseline_budget_cost',
            ),
            'classes': ('collapse',),
        }),
        ('Current Budget', {
            'fields': (
                'budget_cost',
            ),
        }),
        ('Actual Override', {
            'fields': (
                'actual_override',
            ),
            'classes': ('collapse',),
        }),
        ('Forecast Override', {
            'fields': (
                'forecast_override',
                'forecast_cost',
                'forecast_overridden_by',
            ),
        }),
        ('Metadata', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )


@admin.register(PSRSnapshot)
class PSRSnapshotAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'project',
        'snapshot_date',
        'frequency',
        'total_actual_cost',
        'total_forecast_cost',
        'total_prognosis_cost',
        'total_budget_cost',
        'generated_at',
    )

    list_filter = (
        'frequency',
        'snapshot_date',
        'project__co_no',
        'project__currency',
    )

    search_fields = (
        'project__co_no',
        'project__project_name',
    )

    date_hierarchy = 'snapshot_date'

    readonly_fields = (
        'generated_at',
        'generated_by',
        'data',

        'total_actual_cost',
        'total_forecast_cost',
        'total_prognosis_cost',
        'total_budget_cost',

        'sales_value',
        'eff_value',
        'risk_value',
        'ter_value',
        'sum_prognosis',
        'margin',
        'factor',
        'ebit_value',
        'ebit_percentage',
        'net_marginal_income',
        'net_marginal_income_percentage',
    )

    fieldsets = (
        ('Snapshot Info', {
            'fields': (
                'project',
                'snapshot_date',
                'frequency',
            )
        }),
        ('Summary', {
            'fields': (
                'total_actual_cost',
                'total_forecast_cost',
                'total_prognosis_cost',
                'total_budget_cost',
            )
        }),
        ('KPI Fields', {
            'fields': (
                'sales_value',
                'eff_value',
                'ter_value',
                'risk_value',
                'sum_prognosis',
                'margin',
                'factor',
                'ebit_value',
                'ebit_percentage',
                'net_marginal_income',
                'net_marginal_income_percentage',
            )
        }),
        ('Data', {
            'fields': (
                'data',
            ),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': (
                'generated_at',
                'generated_by',
            ),
            'classes': ('collapse',),
        }),
    )





@admin.register(SubDepartmentBudgetAdjustment)
class SubDepartmentBudgetAdjustmentAdmin(admin.ModelAdmin):
    list_display = (
        'sub_department',
        'adjustment_date',
        'adjusted_by',
        'previous_budget_hours',
        'new_budget_hours',
        'note',
    )

    list_filter = (
        'adjustment_date',
        'adjusted_by',
        'sub_department__department__project__co_no',
    )

    search_fields = (
        'sub_department__code',
        'sub_department__department__project__co_no',
        'note',
        'adjusted_by__username',
    )

    readonly_fields = (
        'adjustment_date',
        'adjusted_by',
        'previous_budget_hours',
        'new_budget_hours',
        'created_at',
    )

    date_hierarchy = 'adjustment_date'

    fieldsets = (
        ('Adjustment Overview', {
            'fields': (
                'sub_department',
                'adjustment_date',
                'adjusted_by',
            )
        }),
        ('Budget Hours Change', {
            'fields': (
                'previous_budget_hours',
                'new_budget_hours',
            )
        }),
        ('Reason', {
            'fields': (
                'note',
            )
        }),
        ('Metadata', {
            'fields': (
                'created_at',
            ),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser




# core/admin.py

@admin.register(ProjectCostCategoryBudgetAdjustment)
class ProjectCostCategoryBudgetAdjustmentAdmin(admin.ModelAdmin):
    list_display = (
        'project_cost_category',
        'adjustment_date',
        'adjusted_by',
        'previous_budget_cost',
        'new_budget_cost',
        'note',
    )

    list_filter = (
        'adjustment_date',
        'adjusted_by',
        'project_cost_category__project__co_no',
    )

    search_fields = (
        'project_cost_category__cost_category__code',
        'project_cost_category__project__co_no',
        'note',
        'adjusted_by__username',
    )

    readonly_fields = (
        'adjustment_date',
        'adjusted_by',
        'previous_budget_cost',
        'new_budget_cost',
        'created_at',
    )

    date_hierarchy = 'adjustment_date'

    fieldsets = (
        ('Adjustment Overview', {
            'fields': (
                'project_cost_category',
                'adjustment_date',
                'adjusted_by',
            )
        }),
        ('Budget Cost Change', {
            'fields': (
                'previous_budget_cost',
                'new_budget_cost',
            )
        }),
        ('Reason', {
            'fields': (
                'note',
            )
        }),
        ('Metadata', {
            'fields': (
                'created_at',
            ),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser






#---------------------------#
# Forecast Override Section #
#---------------------------#

@admin.register(ForecastAdjustment)
class ForecastAdjustmentAdmin(admin.ModelAdmin):
    list_display = (
        'sub_department',
        'adjustment_date',
        'adjusted_by',
        'previous_forecast_hours',
        'new_forecast_hours',
        'note',
    )

    list_filter = (
        'adjustment_date',
        'adjusted_by',
        'sub_department__department__project__co_no',
    )

    search_fields = (
        'sub_department__code',
        'sub_department__department__project__co_no',
        'note',
        'adjusted_by__username',
    )

    readonly_fields = (
        'adjustment_date',
        'adjusted_by',
        'previous_forecast_hours',
        'new_forecast_hours',
        'created_at',
    )

    date_hierarchy = 'adjustment_date'

    fieldsets = (
        ('Adjustment Overview', {
            'fields': (
                'sub_department',
                'adjustment_date',
                'adjusted_by',
            )
        }),
        ('Forecast Change', {
            'fields': (
                'previous_forecast_hours',
                'new_forecast_hours',
            )
        }),
        ('Reason', {
            'fields': (
                'note',
            )
        }),
        ('Metadata', {
            'fields': (
                'created_at',
            ),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(ForecastAdjustmentLine)
class ForecastAdjustmentLineAdmin(admin.ModelAdmin):
    list_display = (
        'adjustment',
        'description',
        'hours',
    )

    list_filter = (
        'adjustment__sub_department__department__project__co_no',
        'adjustment__adjustment_date',
    )

    search_fields = (
        'description',
        'adjustment__sub_department__code',
    )

    readonly_fields = (
        'adjustment',
        'description',
        'hours',
    )

    fieldsets = (
        ('Line Item', {
            'fields': (
                'adjustment',
                'description',
                'hours',
            )
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser








@admin.register(MaterialForecastAdjustment)
class MaterialForecastAdjustmentAdmin(admin.ModelAdmin):
    list_display = (
        'project_cost_category',
        'adjustment_date',
        'adjusted_by',
        'previous_forecast_cost',
        'new_forecast_cost',
        'note',
    )

    list_filter = (
        'adjustment_date',
        'adjusted_by',
        'project_cost_category__project__co_no',
    )

    search_fields = (
        'project_cost_category__project__co_no',
        'project_cost_category__cost_category__code',
        'note',
        'adjusted_by__username',
    )

    readonly_fields = (
        'adjustment_date',
        'adjusted_by',
        'previous_forecast_cost',
        'new_forecast_cost',
        'created_at',
    )

    date_hierarchy = 'adjustment_date'

    fieldsets = (
        ('Adjustment Overview', {
            'fields': (
                'project_cost_category',
                'adjustment_date',
                'adjusted_by',
            )
        }),
        ('Forecast Change', {
            'fields': (
                'previous_forecast_cost',
                'new_forecast_cost',
            )
        }),
        ('Reason', {
            'fields': (
                'note',
            )
        }),
        ('Metadata', {
            'fields': (
                'created_at',
            ),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(MaterialForecastAdjustmentLine)
class MaterialForecastAdjustmentLineAdmin(admin.ModelAdmin):
    list_display = (
        'adjustment',
        'description',
        'amount',
    )

    list_filter = (
        'adjustment__project_cost_category__project__co_no',
        'adjustment__adjustment_date',
    )

    search_fields = (
        'description',
        'adjustment__project_cost_category__project__co_no',
    )

    readonly_fields = (
        'adjustment',
        'description',
        'amount',
    )

    fieldsets = (
        ('Line Item', {
            'fields': (
                'adjustment',
                'description',
                'amount',
            )
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser



# -- Assembly Services --------------------------------------------------------

class AssemblyActualAdjustmentLineInline(admin.TabularInline):
    model = AssemblyActualAdjustmentLine
    extra = 1
    fields = ('description', 'amount',)
    verbose_name = "Assembly Line"
    verbose_name_plural = "Assembly Lines"


class AssemblyActualAdjustmentInline(admin.TabularInline):
    model = AssemblyActualAdjustment
    extra = 0
    fields = ('note', 'adjusted_by', 'adjusted_at',)
    readonly_fields = ('adjusted_by', 'adjusted_at',)
    show_change_link = True


@admin.register(AssemblyActualAdjustment)
class AssemblyActualAdjustmentAdmin(admin.ModelAdmin):
    list_display = (
        'project_cost_category',
        'adjusted_by',
        'note_short',
        'adjusted_at',
    )
    list_filter = (
        'project_cost_category__project__co_no',
        'adjusted_by',
        'adjusted_at',
    )
    search_fields = (
        'project_cost_category__project__co_no',
        'note',
    )
    
    date_hierarchy = 'adjusted_at'
    
    inlines = (AssemblyActualAdjustmentLineInline,)
    
    readonly_fields = ('adjusted_at', 'adjusted_by',)
    
    fieldsets = (
        ('Adjustment Info', {
            'fields': (
                'project_cost_category',
                'note',
                'adjusted_by',
                'adjusted_at',
            )
        }),
    )
    
    def note_short(self, obj):
        return obj.note[:50] + "..." if obj.note and len(obj.note) > 50 else obj.note
    note_short.short_description = "Note"


# -- F+V (Freight + Versicherung / Insurance) ---------------------------------

class FVActualAdjustmentLineInline(admin.TabularInline):
    model = FVActualAdjustmentLine
    extra = 1
    fields = ('description', 'amount',)
    verbose_name = "F+V Line"
    verbose_name_plural = "F+V Lines"


class FVActualAdjustmentInline(admin.TabularInline):
    model = FVActualAdjustment
    extra = 0
    fields = ('note', 'adjusted_by', 'adjusted_at',)
    readonly_fields = ('adjusted_by', 'adjusted_at',)
    show_change_link = True


@admin.register(FVActualAdjustment)
class FVActualAdjustmentAdmin(admin.ModelAdmin):
    list_display = (
        'project_cost_category',
        'adjusted_by',
        'note_short',
        'adjusted_at',
    )
    list_filter = (
        'project_cost_category__project__co_no',
        'adjusted_by',
        'adjusted_at',
    )
    search_fields = (
        'project_cost_category__project__co_no',
        'note',
    )
    
    date_hierarchy = 'adjusted_at'
    
    inlines = (FVActualAdjustmentLineInline,)
    
    readonly_fields = ('adjusted_at', 'adjusted_by',)
    
    fieldsets = (
        ('Adjustment Info', {
            'fields': (
                'project_cost_category',
                'note',
                'adjusted_by',
                'adjusted_at',
            )
        }),
    )
    
    def note_short(self, obj):
        return obj.note[:50] + "..." if obj.note and len(obj.note) > 50 else obj.note
    note_short.short_description = "Note"








class SOKOActualAdjustmentLineInline(admin.TabularInline):
    model = SOKOActualAdjustmentLine
    extra = 1
    fields = ('description', 'amount',)
    verbose_name = "F+V Line"
    verbose_name_plural = "F+V Lines"


class SOKOActualAdjustmentInline(admin.TabularInline):
    model = SOKOActualAdjustment
    extra = 0
    fields = ('note', 'adjusted_by', 'adjusted_at',)
    readonly_fields = ('adjusted_by', 'adjusted_at',)
    show_change_link = True


@admin.register(SOKOActualAdjustment)
class SOKOActualAdjustmentAdmin(admin.ModelAdmin):
    list_display = (
        'project_cost_category',
        'adjusted_by',
        'note_short',
        'adjusted_at',
    )
    list_filter = (
        'project_cost_category__project__co_no',
        'adjusted_by',
        'adjusted_at',
    )
    search_fields = (
        'project_cost_category__project__co_no',
        'note',
    )
    
    date_hierarchy = 'adjusted_at'
    
    inlines = (SOKOActualAdjustmentLineInline,)
    
    readonly_fields = ('adjusted_at', 'adjusted_by',)
    
    fieldsets = (
        ('Adjustment Info', {
            'fields': (
                'project_cost_category',
                'note',
                'adjusted_by',
                'adjusted_at',
            )
        }),
    )
    
    def note_short(self, obj):
        return obj.note[:50] + "..." if obj.note and len(obj.note) > 50 else obj.note
    note_short.short_description = "Note"














from django.contrib import admin
from django.utils.html import format_html

from .models import PSRBudgetChangeRequest, PSRApprovalAction


@admin.register(PSRBudgetChangeRequest)
class PSRBudgetChangeRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'submitter',
        'target_display',
        'status_colored',
        'created_at',
        'updated_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = ('submitter__username', 'note', 'sub_department__name', 'project_cost_category__name')
    readonly_fields = ('created_at', 'updated_at', 'submitter', 'status')
    fields = (
        'submitter', 'status', 'note',
        'sub_department', 'project_cost_category',
        'proposed_budget_hours', 'proposed_budget_cost',
        'created_at', 'updated_at'
    )

    def target_display(self, obj):
        return obj.target
    target_display.short_description = "Target"

    def status_colored(self, obj):
        colors = {
            'PENDING_APPROVERS': 'orange',
            'PENDING_ADMIN': 'blue',
            'APPROVED': 'green',
            'REJECTED': 'red',
        }
        color = colors.get(obj.status, 'gray')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())
    status_colored.short_description = "Status"
    status_colored.admin_order_field = 'status'

    def has_add_permission(self, request):
        return False  # Requests created via API/views only

    def has_change_permission(self, request, obj=None):
        # Optional: restrict editing in admin if needed
        return request.user.is_superuser


@admin.register(PSRApprovalAction)
class PSRApprovalActionAdmin(admin.ModelAdmin):
    list_display = (
        'request',
        'approver',
        'stage',
        'action_colored',
        'timestamp',
        'comment_truncated',
    )
    list_filter = ('stage', 'action', 'timestamp')
    search_fields = ('request__id', 'approver__username', 'comment')
    readonly_fields = ('request', 'approver', 'stage', 'action', 'timestamp', 'comment')
    fields = ('request', 'approver', 'stage', 'action', 'comment', 'timestamp')

    def action_colored(self, obj):
        if not obj.action:
            return format_html('<span style="color: gray;">Pending</span>')
        color = 'green' if obj.action == 'APPROVE' else 'red'
        return format_html('<span style="color: {};">{}</span>', color, obj.get_action_display())
    action_colored.short_description = "Action"
    action_colored.admin_order_field = 'action'

    def comment_truncated(self, obj):
        return (obj.comment[:50] + '...') if len(obj.comment) > 50 else obj.comment
    comment_truncated.short_description = "Comment"

    def has_add_permission(self, request):
        return False  # Created via workflow logic

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser








from django.contrib import admin
from django.utils.html import format_html

from .models import (
    PSRForecastChangeRequest,
    PSRForecastApprovalAction,
    ForecastRequestLine
)


@admin.register(PSRForecastChangeRequest)
class PSRForecastChangeRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'submitter',
        'target_display',
        'status_colored',
        'created_at',
        'updated_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = (
        'submitter__username', 'note',
        'sub_department__name', 'project_cost_category__name'
    )
    readonly_fields = ('created_at', 'updated_at', 'submitter', 'status')
    fields = (
        'submitter', 'status', 'note',
        'sub_department', 'project_cost_category',
        'proposed_forecast_hours', 'proposed_forecast_cost',
        'created_at', 'updated_at'
    )

    def target_display(self, obj):
        return obj.target
    target_display.short_description = "Target"

    def status_colored(self, obj):
        colors = {
            'PENDING_APPROVERS': 'orange',
            'PENDING_ADMIN': 'blue',
            'APPROVED': 'green',
            'REJECTED': 'red',
        }
        color = colors.get(obj.status, 'gray')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())
    status_colored.short_description = "Status"
    status_colored.admin_order_field = 'status'

    def has_add_permission(self, request):
        return False  # Created via API only

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(PSRForecastApprovalAction)
class PSRForecastApprovalActionAdmin(admin.ModelAdmin):
    list_display = (
        'request',
        'approver',
        'stage',
        'action_colored',
        'timestamp',
        'comment_truncated',
    )
    list_filter = ('stage', 'action', 'timestamp')
    search_fields = ('request__id', 'approver__username', 'comment')
    readonly_fields = ('request', 'approver', 'stage', 'action', 'timestamp', 'comment')

    def action_colored(self, obj):
        if not obj.action:
            return format_html('<span style="color: gray;">Pending</span>')
        color = 'green' if obj.action == 'APPROVE' else 'red'
        return format_html('<span style="color: {};">{}</span>', color, obj.get_action_display())
    action_colored.short_description = "Action"

    def comment_truncated(self, obj):
        return (obj.comment[:50] + '...') if len(obj.comment) > 50 else obj.comment
    comment_truncated.short_description = "Comment"

    def has_add_permission(self, request):
        return False


@admin.register(ForecastRequestLine)
class ForecastRequestLineAdmin(admin.ModelAdmin):
    list_display = ('request', 'description', 'hours', 'amount')
    list_filter = ('request__status',)
    search_fields = ('description', 'request__id')
    readonly_fields = ('request', 'description', 'hours', 'amount')

    def has_add_permission(self, request):
        return False





# class ProjectPaymentInline(admin.TabularInline):
#     model = ProjectPayment
#     extra = 0
#     readonly_fields = ('amount_in_foreign_curr', 'days_invoice_to_receive', 'days_expected_to_receive')
#     fields = (
#         'invoice_no', 'invoice_date', 'expected_receive_date', 'actual_receive_date',
#         'percentage', 'amount_in_foreign_curr', 'notes',
#         'days_invoice_to_receive', 'days_expected_to_receive'
#     )

@admin.register(ProjectPayment)
class ProjectPaymentAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_no', 'project', 'invoice_date', 'expected_receive_date',
        'actual_receive_date', 'percentage', 'amount_in_foreign_curr',
        'days_invoice_to_receive', 'days_expected_to_receive'
    )
    list_filter = ('project', 'actual_receive_date')
    search_fields = ('invoice_no', 'project__name')  # adjust if project has different field

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('project')
    
    

@admin.register(PSRProjectCreationRequest)
class PSRProjectCreationRequestAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'project',
        'submitter',
        'status',
        'created_at',
    )

    list_filter = ('status', 'created_at')

    search_fields = (
        'project__co_no',
        'project__project_name',
        'submitter__username',
    )

    readonly_fields = (
    'project',
    'submitter',
    'status',
    'note',
    'created_at',
    'updated_at',
    )


    def has_add_permission(self, request):
        return False


@admin.register(PSRProjectApprovalAction)
class PSRProjectApprovalActionAdmin(admin.ModelAdmin):

    list_display = (
        'request',
        'approver',
        'stage',
        'action',
        'timestamp',
    )

    readonly_fields = (
    'request',
    'approver',
    'stage',
    'action',
    'comment',
    'timestamp',
)


    def has_add_permission(self, request):
        return False
    