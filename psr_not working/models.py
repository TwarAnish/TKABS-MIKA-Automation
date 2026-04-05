# core/models.py
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
from django.utils import timezone
from django.conf import settings
from django.db import models
from decimal import Decimal

# Updated Project model in core/models.py

class PSRProject(models.Model):
    CURRENCY_CHOICES = [
        ('INR', 'Indian Rupee'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('CHF', 'Swiss Franc'),
    ]

    co_no = models.CharField(max_length=50, unique=True)
    project_name = models.CharField(max_length=255)
    
    location = models.CharField(max_length=255, blank=True, null=True)
    project_manager = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="_procurement_projects")

    project_manager_email = models.EmailField()
    sales_person = models.CharField(max_length=100)
    sales_person_email = models.EmailField()
    
    sales_value_foreign_curr = models.DecimalField(max_digits=30, decimal_places=20, validators=[MinValueValidator(0.00)], default=0.00)
    sales_value = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0.00)], editable=True)

    cw_no = models.CharField(max_length=100, blank=True, null=True)
    current_phase = models.CharField(max_length=100, blank=True, null=True)
    settlement_period = models.CharField(max_length=100, blank=True, null=True)

    direct_margin_percentage = models.DecimalField(max_digits=30, decimal_places=20, default=0.000)
    sgna_percentage = models.DecimalField(max_digits=30, decimal_places=20, default=0.000, verbose_name="SGNA (%)")
    eff_percentage = models.DecimalField(max_digits=30, decimal_places=20, default=0.000, verbose_name="EFF Value")
    ter_percentage = models.DecimalField(max_digits=30, decimal_places=20, default=0.000, verbose_name="TER Value")
    risk = models.DecimalField(max_digits=30, decimal_places=20, default=0.000, verbose_name="Risk Value")
    
    # Currency
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='INR')
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1.0000, validators=[MinValueValidator(0.0001)])

    # === CALCULATED FIELDS (Auto-filled on save) ===
    ebit_percentage = models.DecimalField(max_digits=30, decimal_places=20, default=0.000, editable=False)
    ebit_value = models.DecimalField(max_digits=30, decimal_places=20, default=0.000, editable=False)
    sgna_value = models.DecimalField(max_digits=30, decimal_places=20, default=0.000, editable=False)
    cost_with_sgna = models.DecimalField(max_digits=30, decimal_places=20, default=0.000, editable=False)
    hk = models.DecimalField(max_digits=30, decimal_places=20, default=0.000, editable=False)
    hk2 = models.DecimalField(max_digits=30, decimal_places=20, default=0.000, editable=False)
    sk_value = models.DecimalField(max_digits=30, decimal_places=20, default=0.000)
    direct_margin_value = models.DecimalField(max_digits=30, decimal_places=20, default=0.000, editable=False)
    ter_value = models.DecimalField(max_digits=30, decimal_places=20, default=0.000, editable=False)
    eff_value = models.DecimalField(max_digits=30, decimal_places=20, default=0.000, editable=False)
    actual_budget = models.DecimalField(max_digits=30, decimal_places=20, default=0.000, editable=False)
    factor = models.DecimalField(max_digits=8, decimal_places=3, default=0.0000, editable=False)

    # Legacy field   now auto-calculated (kept for compatibility)
    budget = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['co_no']
        verbose_name = "Project"
        verbose_name_plural = "Projects"


    # def save(self, *args, **kwargs):
    #     # Always calculate sales_value in INR from foreign currency (this should always update)
    #     if self.sales_value_foreign_curr and self.exchange_rate:
    #         self.sales_value = self.sales_value_foreign_curr * self.exchange_rate
    
    #     # Only proceed with calculations if sales_value is valid
    #     if self.sales_value and self.sales_value > 0:
        
    #         # TER and EFF values   always update when percentages change
    #         # self.ter_value = self.sales_value * (self.ter_percentage / Decimal('100'))
    #         # self.eff_value = self.sales_value * (self.eff_percentage / Decimal('100'))

    #         # self.ter_value = self.ter_percentage
    #         self.eff_value = self.eff_percentage * self.exchange_rate
            
    #         # These fields should ALWAYS be recalculated on every save
    #         # (they directly depend on percentages which can change)
    #         self.direct_margin_value = self.sales_value * (self.direct_margin_percentage/ Decimal('100'))
    #         self.hk2 = self.sales_value - self.direct_margin_value
    #         # self.hk = self.hk2 * (100/(100 + self.ter_percentage))

    #         hundred = Decimal('100')
    #         self.hk = self.hk2 * (hundred / (hundred + self.ter_percentage))
    #         self.ter_value = self.hk2 - self.hk
    #         self.sgna_value = self.hk2 * (self.sgna_percentage / Decimal('100'))
    #         self.sk_value = self.hk2 + self.sgna_value + self.eff_value
    #         self.ebit_value = self.sales_value - self.sk_value
    #         self.ebit_percentage = ((self.ebit_value / self.sales_value) * 100)
    
    #         # --------------------------------------------------------------
    #         # CRITICAL CHANGE: Budget-related fields are calculated ONLY ONCE
    #         # (when the project is first created   i.e., when it has no pk yet)
    #         if self.pk is None:  # ? This means it's a NEW project being created
    #             self.actual_budget = self.hk2
    #             self.budget = self.actual_budget  # legacy field
    #             self.factor = self.sales_value / self.hk if self.hk > 0 else Decimal('0')
    #         # If this is an UPDATE ? do NOT touch actual_budget, budget, or factor anymore
    #         # --------------------------------------------------------------
    
    #     super().save(*args, **kwargs)

    # def __str__(self):
    #     return f"{self.co_no}: {self.project_name}"
    def save(self, *args, **kwargs):
            # 1. Ensure we use Decimal for constants
            hundred = Decimal('100.0')
            zero = Decimal('0.0')

            # 2. Calculate sales_value
            if self.sales_value_foreign_curr is not None and self.exchange_rate is not None:
                # Force conversion to Decimal just in case a float sneaked in from the validator/form
                self.sales_value = Decimal(str(self.sales_value_foreign_curr)) * Decimal(str(self.exchange_rate))
        
            # 3. Only proceed if sales_value is valid
            if self.sales_value and self.sales_value > zero:
            
                # Force Decimal conversion for percentages
                eff_perc = Decimal(str(self.eff_percentage))
                ex_rate = Decimal(str(self.exchange_rate))
                dm_perc = Decimal(str(self.direct_margin_percentage))
                ter_perc = Decimal(str(self.ter_percentage))
                sgna_perc = Decimal(str(self.sgna_percentage))

                self.eff_value = eff_perc * ex_rate
                
                self.direct_margin_value = self.sales_value * (dm_perc / hundred)
                self.hk2 = self.sales_value - self.direct_margin_value

                # Calculate HK (using the formula: hk2 * 100 / (100 + ter))
                self.hk = self.hk2 * (hundred / (hundred + ter_perc))
                
                self.ter_value = self.hk2 - self.hk
                self.sgna_value = self.hk2 * (sgna_perc / hundred)
                
                # Use Decimal for all additions
                self.sk_value = self.hk2 + self.sgna_value + self.eff_value
                self.ebit_value = self.sales_value - self.sk_value
                self.ebit_percentage = (self.ebit_value / self.sales_value) * hundred
        
                # 4. Budget-related fields (New Projects Only)
                if self.pk is None:
                    self.actual_budget = self.hk2
                    self.budget = self.actual_budget
                    self.factor = self.sales_value / self.hk if self.hk > zero else zero

            super().save(*args, **kwargs)


class PSRProjectCreationRequest(models.Model):

    STATUS_CHOICES = [
        ("PENDING_APPROVERS", "Pending Approvers"),
        ("PENDING_ADMIN", "Pending Admin"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    project = models.OneToOneField(
        PSRProject, on_delete=models.CASCADE, related_name="creation_request"
    )

    submitter = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    data = models.JSONField(default=dict)

    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default="PENDING_APPROVERS"
    )

    note = models.TextField(blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class PSRProjectApprovalAction(models.Model):

    ACTION_CHOICES = [
        ("APPROVE", "Approve"),
        ("REJECT", "Reject"),
    ]

    request = models.ForeignKey(
        PSRProjectCreationRequest,
        on_delete=models.CASCADE,
        related_name="approval_actions",
    )

    approver = models.ForeignKey(CustomUser, on_delete=models.PROTECT)

    stage = models.CharField(
        max_length=20, choices=[("APPROVER", "Approver"), ("ADMIN", "Admin")]
    )

    action = models.CharField(
        max_length=10, choices=ACTION_CHOICES, null=True, blank=True
    )

    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = [("request", "approver", "stage")]



class PSRDepartment(models.Model):
    project = models.ForeignKey(PSRProject,on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=50)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)], help_text="Hourly rate for this department (project-specific)")

    # Planned values (can be updated manually or via import)
    budget_hours = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0.00)], help_text="Budgeted hours for this department")
    budget_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0, validators=[MinValueValidator(0.00)], help_text="Budgeted cost (hours * rate)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['project', 'name']]
        ordering = ['name']
        verbose_name = "Department"
        verbose_name_plural = "Departments"
    
    def __str__(self):
        return f"{self.project}:{self.name}"


class PSRSubDepartment(models.Model):
    department = models.ForeignKey(PSRDepartment, on_delete=models.CASCADE, related_name='sub_departments')
    code = models.CharField(max_length=50)
    role_descrptn = models.CharField(max_length=255, null=True, blank=True)
    inkrement = models.CharField(max_length=255, null=True, blank=True)

    # Baseline (original budget from project creation - never changes)
    baseline_budget_hours = models.DecimalField(max_digits=20, decimal_places=2, default=0, validators=[MinValueValidator(0.00)])
    baseline_budget_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0, validators=[MinValueValidator(0.00)])

    # Current/Actual (updated via budget APIs)
    budget_hours = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0.00)])

    budget_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0, validators=[MinValueValidator(0.00)])

    forecast_hours = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    forecast_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
    forecast_override = models.BooleanField(default=False)

    forecast_overridden_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='forecast_overrides')
    forecast_overridden_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['department', 'code']]
        ordering = ['code']
        verbose_name = "Sub-Department"
        verbose_name_plural = "Sub-Departments"
    
    def __str__(self):
        return f"{self.department}:{self.code}"


    def save(self, *args, **kwargs):
        dept = self.department
        project = dept.project
        # rate_inr = dept.hourly_rate * project.exchange_rate
        rate_inr = dept.hourly_rate

        # Sync budget_cost ? budget_hours
        if self.budget_cost and rate_inr > 0:
            self.budget_hours = self.budget_cost / rate_inr
        elif self.budget_hours is not None:
            self.budget_cost = self.budget_hours * rate_inr

        # Forecast override
        if self.forecast_override:
            self.forecast_cost = self.forecast_hours * rate_inr

        super().save(*args, **kwargs)

    def current_forecast_hours_display(self):
        if self.forecast_override:
            return f"Manual: {self.forecast_hours} hours"
        else:
            return "Auto: Budget - Actual (calculated in snapshot)"
    current_forecast_hours_display.short_description = "Current Forecast Hours"

    def current_forecast_cost_display(self):
        if self.forecast_override:
            return f"{self.forecast_cost:,.2f}"
        else:
            return "Auto-calculated in snapshot"
    current_forecast_cost_display.short_description = "Current Forecast Cost (INR)"


class CostCategory(models.Model):
    code = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=255, editable=False)

    mat_code = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.name = self.code
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Cost Category"
        verbose_name_plural = "Cost Categories"
        ordering = ['code']
    
    def __str__(self):
        return self.name


class ProjectCostCategory(models.Model):
    project = models.ForeignKey(PSRProject, on_delete=models.CASCADE, related_name='project_cost_categories')
    cost_category = models.ForeignKey(CostCategory, on_delete=models.PROTECT)
    
    # Baseline (original budget from project creation)
    baseline_budget_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0, validators=[MinValueValidator(0.00)])

    # Current/Actual (updated via budget APIs)
    budget_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0, validators=[MinValueValidator(0.00)])

    forecast_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
    forecast_override = models.BooleanField(default=False)

    # In ProjectCostCategory model   add this field
    actual_override = models.BooleanField(default=False, help_text="If true, use manual actuals for RK instead of PO")

    forecast_overridden_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='material_forecast_overrides')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['project', 'cost_category']]
        ordering = ['cost_category__code']
        verbose_name = "Project Cost Category"
        verbose_name_plural = "Project Cost Categories"
    
    def __str__(self):
        return f"{self.project} : {self.cost_category}"


class TimesheetEntry(models.Model):
    date = models.DateField(db_index=True)
    emp_cd = models.CharField(max_length=20, db_index=True)
    emp_name = models.CharField(max_length=100)
    role_description = models.CharField(max_length=255)
    co_no = models.CharField(max_length=20, db_index=True)
    hours = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])

    imported_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Timesheet Entry (Raw)"
        verbose_name_plural = "Timesheet Entries (Raw)"
        indexes = [
            models.Index(fields=['date', 'emp_cd']),
            models.Index(fields=['co_no']),
            models.Index(fields=['date', 'co_no']),
            models.Index(fields=['date', 'emp_cd', 'co_no', 'role_description']),  # For performance
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'emp_cd', 'co_no', 'role_description'],
                name='unique_timesheet_entry'
            )
        ]

    @property
    def project_code(self) -> str:
        return self.co_no[:5] if self.co_no and len(self.co_no) >= 5 else ""


class POData(models.Model):
    # Critical fields (must be imported)
    co_no = models.CharField(max_length=20, db_index=True, help_text="CONo")
    mat_code = models.CharField(max_length=100, db_index=True, help_text="MatCode")
    po_value_inr = models.DecimalField(max_digits=18, decimal_places=2, validators=[MinValueValidator(0)])

    # Highly useful additional fields from the dump
    po_no = models.CharField(max_length=50, blank=True, help_text="PoNo")
    po_date = models.DateField(null=True, blank=True, help_text="Po.Date")
    sr_no = models.PositiveIntegerField(null=True, blank=True, help_text="SrNo")
    item_code = models.CharField(max_length=100, blank=True, help_text="ItemCode")
    description = models.TextField(blank=True, help_text="Description")
    supplier_name = models.CharField(max_length=255, blank=True, help_text="SupplierName")
    project_name = models.CharField(max_length=255, blank=True, help_text="ProjName")

    imported_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "PO Data Entry (Raw)"
        verbose_name_plural = "PO Data Entries (Raw)"
        indexes = [
            models.Index(fields=['co_no']),
            models.Index(fields=['mat_code']),
            models.Index(fields=['co_no', 'mat_code']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['co_no', 'po_no', 'sr_no'],
                name='unique_po_line'
            )
        ]

    @property
    def project_code(self) -> str:
        return self.co_no[:5] if self.co_no and len(self.co_no) >= 5 else ""

    @property
    def project_code(self) -> str:
        return self.co_no[:5] if self.co_no and len(self.co_no) >= 5 else ""


class PSRSnapshot(models.Model):
    project = models.ForeignKey(PSRProject, on_delete=models.CASCADE, related_name='psr_snapshots')
    
    snapshot_date = models.DateField()
    
    frequency = models.CharField(
        max_length=20,
        choices=[
            ('MONTHLY', 'Monthly'),
            ('BIWEEKLY', 'Bi-weekly'),
            ('WEEKLY', 'Weekly'),
        ],
        default='MONTHLY'
    )
    
    data = models.JSONField(default=dict)

    # === LABOR (TIMESHEET) TOTALS ===
    labor_actual_hours = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    labor_budget_hours = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    labor_forecast_hours = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    labor_prognosis_hours = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    labor_actual_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    labor_budget_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    labor_forecast_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    labor_prognosis_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    # === MATERIAL (COST TO GO) TOTALS ===
    material_actual_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    material_budget_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    material_forecast_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    material_prognosis_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    
    sales_value = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    eff_value = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    ter_value = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    risk_value = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    sum_prognosis = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    margin = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    factor = models.DecimalField(max_digits=8, decimal_places=3, default=0.0000)
    ebit_value = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    ebit_percentage = models.DecimalField(max_digits=30, decimal_places=10, default=0)
    net_marginal_income = models.DecimalField(max_digits=30, decimal_places=10, default=0)
    net_marginal_income_percentage = models.DecimalField(max_digits=30, decimal_places=10, default=0)

    # === COMBINED TOTALS (kept for backward compatibility) ===
    total_actual_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0)      # labor + material actual
    total_budget_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0)      # labor + material budget
    total_forecast_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0)    # labor + material forecast
    total_prognosis_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0)  # labor + material prognosis
    
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = [['project', 'snapshot_date']]
        ordering = ['-snapshot_date']
        verbose_name = "PSR Snapshot"
        verbose_name_plural = "PSR Snapshots"



#----------------------#
# Hours Update Section #
#----------------------#


class SubDepartmentBudgetAdjustment(models.Model):
    sub_department = models.ForeignKey(PSRSubDepartment, on_delete=models.CASCADE, related_name='budget_adjustments')
    adjustment_date = models.DateTimeField(auto_now_add=True)
    adjusted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    note = models.TextField(help_text="Reason for budget hours adjustment")
    
    previous_budget_hours = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    new_budget_hours = models.DecimalField(max_digits=12, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-adjustment_date']
        verbose_name = "Sub-Department Budget Adjustment"
        verbose_name_plural = "Sub-Department Budget Adjustments"






class ProjectCostCategoryBudgetAdjustment(models.Model):
    project_cost_category = models.ForeignKey(ProjectCostCategory, on_delete=models.CASCADE, related_name='budget_adjustments')
    adjustment_date = models.DateTimeField(auto_now_add=True)
    adjusted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    note = models.TextField(help_text="Reason for budget cost adjustment")
    
    previous_budget_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    new_budget_cost = models.DecimalField(max_digits=15, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-adjustment_date']
        verbose_name = "Project Cost Category Budget Adjustment"
        verbose_name_plural = "Project Cost Category Budget Adjustments"




#---------------------------------#
# Hours Forecast Override Section #
#---------------------------------#

class ForecastAdjustment(models.Model):
    sub_department = models.ForeignKey(PSRSubDepartment, on_delete=models.CASCADE, related_name='forecast_adjustments')
    adjustment_date = models.DateTimeField(auto_now_add=True)
    adjusted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    note = models.TextField(help_text="Overall reason for forecast adjustment")
    
    new_forecast_hours = models.DecimalField(max_digits=12, decimal_places=2)
    previous_forecast_hours = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    # def __str__(self):
    #     return f"{self.sub_department}"


class ForecastAdjustmentLine(models.Model):
    adjustment = models.ForeignKey(ForecastAdjustment, on_delete=models.CASCADE, related_name='lines')
    description = models.CharField(max_length=255)
    hours = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])

    # def __str__(self):
    #     return self.adjustment






#--------------------------------------#
# Cost To Go Forecast Override Section #
#--------------------------------------#


class MaterialForecastAdjustment(models.Model):
    project_cost_category = models.ForeignKey(ProjectCostCategory, on_delete=models.CASCADE, related_name='forecast_adjustments')
    adjustment_date = models.DateTimeField(auto_now_add=True)
    adjusted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    note = models.TextField(help_text="Reason for material forecast adjustment")
    
    previous_forecast_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    new_forecast_cost = models.DecimalField(max_digits=15, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    # def __str__(self):
    #     return f"{self.project_cost_category}"


class MaterialForecastAdjustmentLine(models.Model):
    adjustment = models.ForeignKey(MaterialForecastAdjustment, on_delete=models.CASCADE, related_name='lines')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0.01)])
    
    # def __str__(self):
    #     return self.adjustment







#--------------------------------------#
# Procurement Actuals Adjustments      #
#--------------------------------------#

class RKActualAdjustment(models.Model):
    project_cost_category = models.ForeignKey(ProjectCostCategory, on_delete=models.CASCADE, related_name='rk_actual_adjustments', limit_choices_to={'cost_category__code': 'RK'})
    adjusted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(help_text="Reason for entering manual actuals")
    adjusted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-adjusted_at']
        verbose_name = "RK Actual Adjustment"
        verbose_name_plural = "RK Actual Adjustments"


class RKActualAdjustmentLine(models.Model):
    adjustment = models.ForeignKey(RKActualAdjustment, on_delete=models.CASCADE, related_name='lines')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    class Meta:
        verbose_name = "RK Actual Line"
        verbose_name_plural = "RK Actual Lines"


class AssemblyActualAdjustment(models.Model):
    project_cost_category = models.ForeignKey(
        'ProjectCostCategory',
        on_delete=models.CASCADE,
        related_name='assembly_actual_adjustments',
        limit_choices_to={'cost_category__code': 'ASSEMBLY'}
    )
    adjusted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    note = models.TextField(help_text="Reason for manual adjustment of Assembly Services actuals")
    adjusted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-adjusted_at']
        verbose_name = "Assembly Services Actual Adjustment"
        verbose_name_plural = "Assembly Services Actual Adjustments"

    def __str__(self):
        return f"Assembly Adjustment for {self.project_cost_category} - {self.adjusted_at.date()}"


class AssemblyActualAdjustmentLine(models.Model):
    adjustment = models.ForeignKey(
        AssemblyActualAdjustment,
        on_delete=models.CASCADE,
        related_name='lines'
    )
    description = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    class Meta:
        verbose_name = "Assembly Services Actual Line"
        verbose_name_plural = "Assembly Services Actual Lines"

    def __str__(self):
        return f"{self.description} - ?{self.amount}"


class FVActualAdjustment(models.Model):
    project_cost_category = models.ForeignKey(
        'ProjectCostCategory',
        on_delete=models.CASCADE,
        related_name='fv_actual_adjustments',
        limit_choices_to={'cost_category__code': 'F+V'}  # adjust code if different (e.g. 'FV', 'FREIGHT')
    )
    adjusted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    note = models.TextField(help_text="Reason for manual adjustment of F+V actuals")
    adjusted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-adjusted_at']
        verbose_name = "F+V Actual Adjustment"
        verbose_name_plural = "F+V Actual Adjustments"

    def __str__(self):
        return f"F+V Adjustment for {self.project_cost_category} - {self.adjusted_at.date()}"


class FVActualAdjustmentLine(models.Model):
    adjustment = models.ForeignKey(
        FVActualAdjustment,
        on_delete=models.CASCADE,
        related_name='lines'
    )
    description = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    class Meta:
        verbose_name = "F+V Actual Line"
        verbose_name_plural = "F+V Actual Lines"

    def __str__(self):
        return f"{self.description} - ?{self.amount}"






class SOKOActualAdjustment(models.Model):
    project_cost_category = models.ForeignKey(
        'ProjectCostCategory',
        on_delete=models.CASCADE,
        related_name='soko_actual_adjustments',
        limit_choices_to={'cost_category__code': 'SOKO'}
    )
    adjusted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    note = models.TextField(help_text="Reason for manual adjustment of SOKO actuals")
    adjusted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-adjusted_at']
        verbose_name = "SOKO Actual Adjustment"
        verbose_name_plural = "SOKO Actual Adjustments"

    def __str__(self):
        return f"SOKO Adjustment for {self.project_cost_category} - {self.adjusted_at.date()}"


class SOKOActualAdjustmentLine(models.Model):
    adjustment = models.ForeignKey(
        SOKOActualAdjustment,
        on_delete=models.CASCADE,
        related_name='lines'
    )
    description = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    class Meta:
        verbose_name = "SOKO Actual Line"
        verbose_name_plural = "SOKO Actual Lines"

    def __str__(self):
        return f"{self.description} - ?{self.amount}"








#----------------------------------#
#  Budget Approval Process         #
#----------------------------------#









class PSRBudgetChangeRequest(models.Model):
    """
    Central model for a proposed budget change in PSR module.
    Only one of sub_department or project_cost_category should be set.
    """
    STATUS_CHOICES = [
        ('PENDING_APPROVERS', 'Pending Approvers'),
        ('PENDING_ADMIN', 'Pending Admin'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),  # placeholder for later
    ]

    submitter = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='submitted_psr_requests',
        verbose_name="Submitted By"
    )
    note = models.TextField(verbose_name="Reason/Note for Change")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING_APPROVERS',
        db_index=True
    )
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Target: exactly one of these two should be non-null
    sub_department = models.ForeignKey(
        PSRSubDepartment,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='budget_change_requests'
    )
    project_cost_category = models.ForeignKey(
        ProjectCostCategory,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='budget_change_requests'
    )

    # Proposed values (only one will be relevant depending on target)
    proposed_budget_hours = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        verbose_name="Proposed Budget Hours"
    )
    proposed_budget_cost = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        verbose_name="Proposed Budget Cost"
    )

    class Meta:
        verbose_name = "PSR Budget Change Request"
        verbose_name_plural = "PSR Budget Change Requests"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self):
        target = self.sub_department or self.project_cost_category
        return f"Request #{self.id} by {self.submitter} for {target} ({self.status})"

    def clean(self):
        # Ensure exactly one target is set
        if (self.sub_department is None) == (self.project_cost_category is None):
            raise ValidationError("Exactly one of sub_department or project_cost_category must be set.")
        
        # Ensure proposed value matches target
        if self.sub_department and self.proposed_budget_hours is None:
            raise ValidationError("proposed_budget_hours is required for sub-department changes.")
        if self.project_cost_category and self.proposed_budget_cost is None:
            raise ValidationError("proposed_budget_cost is required for cost category changes.")
        
        super().clean()

    @property
    def target(self):
        return self.sub_department or self.project_cost_category

    @property
    def is_hours_change(self):
        return self.sub_department is not None

    @property
    def current_value(self):
        if self.is_hours_change:
            return self.sub_department.budget_hours
        return self.project_cost_category.budget_cost


class PSRApprovalAction(models.Model):
    """
    Tracks individual approval/rejection actions per request and approver.
    Enables parallel approvals and audit trail.
    """
    ACTION_CHOICES = [
        ('APPROVE', 'Approve'),
        ('REJECT', 'Reject'),
    ]

    request = models.ForeignKey(
        PSRBudgetChangeRequest,
        on_delete=models.CASCADE,
        related_name='approval_actions'
    )
    approver = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='psr_approval_actions'
    )
    stage = models.CharField(
        max_length=20,
        choices=[('APPROVER', 'Approver'), ('ADMIN', 'Admin')],
        db_index=True
    )
    action = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES,
        null=True,
        blank=True,  # null = pending
        db_index=True
    )
    comment = models.TextField(blank=True, verbose_name="Approval/Rejection Comment")
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "PSR Approval Action"
        verbose_name_plural = "PSR Approval Actions"
        unique_together = [('request', 'approver', 'stage')]
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.approver} {self.action or 'pending'} on {self.request} ({self.stage})"

    def clean(self):
        if self.action and self.stage == 'APPROVER' and self.request.status != 'PENDING_APPROVERS':
            raise ValidationError("Cannot act on Approver stage after it has moved forward.")
        if self.action and self.stage == 'ADMIN' and self.request.status != 'PENDING_ADMIN':
            raise ValidationError("Cannot act on Admin stage unless pending.")
        super().clean()





#------------------------------#
#  Forecast Approval Process   #
#------------------------------#






class PSRForecastChangeRequest(models.Model):
    """
    Approval request for forecast override (hours or cost).
    Similar structure to PSRBudgetChangeRequest but for forecast fields.
    """
    STATUS_CHOICES = [
        ('PENDING_APPROVERS', 'Pending Approvers'),
        ('PENDING_ADMIN', 'Pending Admin'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    submitter = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='submitted_psr_forecast_requests'
    )
    note = models.TextField(verbose_name="Reason/Note for Forecast Override")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING_APPROVERS',
        db_index=True
    )
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Target: exactly one of these two
    sub_department = models.ForeignKey(
        PSRSubDepartment,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='forecast_change_requests'
    )
    project_cost_category = models.ForeignKey(
        ProjectCostCategory,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='forecast_change_requests'
    )

    # Proposed values
    proposed_forecast_hours = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        verbose_name="Proposed Forecast Hours"
    )
    proposed_forecast_cost = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        verbose_name="Proposed Forecast Cost"
    )

    class Meta:
        verbose_name = "PSR Forecast Change Request"
        verbose_name_plural = "PSR Forecast Change Requests"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['status', 'created_at'])]

    def __str__(self):
        target = self.sub_department or self.project_cost_category
        return f"Forecast Request #{self.id} by {self.submitter} for {target} ({self.status})"

    def clean(self):
        if (self.sub_department is None) == (self.project_cost_category is None):
            raise ValidationError("Exactly one of sub_department or project_cost_category must be set.")
        if self.sub_department and self.proposed_forecast_hours is None:
            raise ValidationError("proposed_forecast_hours required for sub-department.")
        if self.project_cost_category and self.proposed_forecast_cost is None:
            raise ValidationError("proposed_forecast_cost required for cost category.")
        super().clean()

    @property
    def target(self):
        return self.sub_department or self.project_cost_category

    @property
    def is_hours_override(self):
        return self.sub_department is not None


class PSRForecastApprovalAction(models.Model):
    """
    Individual approval/rejection actions for forecast requests.
    """
    ACTION_CHOICES = [
        ('APPROVE', 'Approve'),
        ('REJECT', 'Reject'),
    ]

    request = models.ForeignKey(
        PSRForecastChangeRequest,
        on_delete=models.CASCADE,
        related_name='approval_actions'
    )
    approver = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='psr_forecast_approval_actions'
    )
    stage = models.CharField(
        max_length=20,
        choices=[('APPROVER', 'Approver'), ('ADMIN', 'Admin')],
        db_index=True
    )
    action = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES,
        null=True,
        blank=True
    )
    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = [('request', 'approver', 'stage')]
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.approver} {self.action or 'pending'} on Forecast Request {self.request.id} ({self.stage})"


class ForecastRequestLine(models.Model):
    """
    Stores the individual line items (description + hours/amount) for a forecast request.
    Created when the request is submitted.
    """
    request = models.ForeignKey(
        PSRForecastChangeRequest,
        on_delete=models.CASCADE,
        related_name='lines'
    )
    description = models.CharField(max_length=255)
    hours = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "Forecast Request Line"
        verbose_name_plural = "Forecast Request Lines"

    def __str__(self):
        if self.hours:
            return f"{self.description} ({self.hours} hrs)"
        return f"{self.description} ({self.amount})"


class ProjectPayment(models.Model):
    project = models.ForeignKey(
        'PSRProject',
        on_delete=models.CASCADE,
        related_name='payments'
    )
    invoice_no = models.CharField(max_length=100,null=True, blank=True)
    invoice_date = models.DateField(null=True, blank=True)
    expected_receive_date = models.DateField()
    actual_receive_date = models.DateField(null=True, blank=True)

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    amount_in_foreign_curr = models.DecimalField(
        max_digits=30,
        decimal_places=10,
        editable=True
    )

    received_amount = models.DecimalField(
        max_digits=30,
        decimal_places=10,
        editable=True,
        null=True,
        blank=True
    )

    notes = models.TextField(blank=True, help_text="Additional details")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Project Payment Milestone"
        verbose_name_plural = "Project Payment Milestones"

    def __str__(self):
        return f"{self.invoice_no} - {self.project} ({self.percentage}%)"

    @property
    def days_invoice_to_receive(self):
        if self.actual_receive_date and self.invoice_date:
            return (self.actual_receive_date - self.invoice_date).days
        return None

    @property
    def days_expected_to_receive(self):
        if self.actual_receive_date and self.expected_receive_date:
            return (self.actual_receive_date - self.expected_receive_date).days
        return None