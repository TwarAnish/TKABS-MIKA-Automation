from django.db import models
from django.conf import settings
from capacity_planning.models import Project as CoreProject
from accounts.models import Department
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from datetime import date
from psr.models import PSRProject as MainProject
from decimal import Decimal
from django.apps import apps
from django.db.models import UniqueConstraint

class QuotationValidity(models.TextChoices):
    DAYS_30 = "30 Days", "30 Days"
    DAYS_45 = "45 Days", "45 Days"
    DAYS_60 = "60 Days", "60 Days"
    MONTHS_6 = "6 Months", "6 Months"
    YEAR_1 = "1 Year", "1 Year"
    NA = "NA", "NA"

class EnergyEfficiency(models.TextChoices):
    RELEVANT = "Relevant", "Relevant"
    NOT_RELEVANT = "Not Relevant", "Not Relevant"
    NA = "NA", "NA"

class RiskCategory(models.TextChoices):
    LOW = "Low Risk", "Low Risk"
    MEDIUM = "Medium Risk", "Medium Risk"
    HIGH = "High Risk", "High Risk"
    NA = "NA", "NA"


class ProjectType(models.TextChoices):
    PROJECT = "PROJECT", "Project"
    NON_PROJECT = "NON_PROJECT", "Non-Project"
    CAPEX = "CAPEX", "CapEx"

class Status(models.TextChoices):
    COMPLETED = "COMPLETED", "Completed"
    ACTIVE = "ACTIVE", "Active"

class PBStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    NEGOTIATION = "NEGOTIATION", "Negotiation In Progress"
    SUPPLIER_FINALIZED = "SUPPLIER_FINALIZED", "Supplier Finalized"
    APPROVAL = "APPROVAL", "Approval In Progress"
    REJECTED = "REJECTED", "Rejected"
    APPROVED = "APPROVED", "Approved"

class Currency(models.TextChoices):
    INR = "INR", "INR"
    USD = "USD", "USD"
    EUR = "EUR", "EUR"
    CNY = "CNY", "CNY"
    JPY = "JPY", "JPY"

class ProcurementType(models.TextChoices):
    MATERIAL = "MATERIAL", "Material"
    SERVICE = "SERVICE", "Service"

from django.db.models import UniqueConstraint, Q

class Project(models.Model):
    project_type = models.CharField(max_length=20,choices=ProjectType.choices,db_index=True)
 
    total_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    actual_expense = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.ACTIVE)
    project = models.ForeignKey(MainProject,on_delete=models.SET_NULL,null=True,blank=True,related_name="capacity_planning_projects")
    project_manager = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="managed_procurement_projects")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True, related_name="created_procurement_projects")
    #Non-Project/CapEx
    hod = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="hod_procurement_projects")
    department = models.ForeignKey('accounts.Department', on_delete=models.SET_NULL, null=True, blank=True,related_name="procurement_projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=["status"]),
        ]
        constraints = [
            # RULE 1: Project must be unique (One entry per Main Project)
            models.UniqueConstraint(
                fields=['project'], 
                condition=Q(project__isnull=False),
                name='unique_project_entry'
            ),
            # RULE 2: Department + Project Type combo must be unique
            models.UniqueConstraint(
                fields=['department', 'project_type'], 
                name='unique_dept_type_combo'
            )
        ]

    def __str__(self):
        project_label = getattr(self.project, 'co_no', 'Standalone')
        return f"{project_label} - {self.get_project_type_display()}"
class ProjectBudget(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="budget_history"
    )
 
    budget = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )
 
    is_active = models.BooleanField(default=True)
 
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
 
    class Meta:
        ordering = ["-created_at"]
 
    def __str__(self):
            return f"{self.project_id} - {self.budget}"
 
 
class CashInflow(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="cash_inflows"
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField(db_index=True)
    status = models.CharField(
        max_length=20,
        choices=[("PENDING", "Pending"), ("APPROVED", "Approved"), ("REJECTED", "Rejected")],
        default="PENDING"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.SET_NULL,
    #     null=True
    # )
 
    def __str__(self):
        return f"Inflow {self.amount} - {self.project_id}"
 



class ProjectBoard(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name="project_boards")
    commodity_equipment = models.CharField(max_length=255)
    commodity_budget = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    cost_center = models.CharField(max_length=100, null=True, blank=True)
    procurement_type = models.CharField(max_length=20, choices=ProcurementType.choices, default=ProcurementType.MATERIAL)
    rfq_sign_off_date = models.DateField(null=True, blank=True)
    document_no = models.CharField(max_length=100, unique=True, editable=False, null=True, blank=True)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="buyer_rfqs")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_rfqs")
    currency = models.CharField(max_length=10, choices=Currency.choices, default=Currency.INR)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    pb_status = models.CharField(max_length=20, choices=PBStatus.choices, default=PBStatus.DRAFT)
    is_amc = models.BooleanField(default=False)
    amc_start_date = models.DateField(null=True, blank=True)
    amc_duration_months = models.PositiveIntegerField(null=True, blank=True)
    amc_end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def clean(self):
    #     super().clean()
    #     if self.procurement_type == ProcurementType.SERVICE:
    #         if not self.is_amc: raise ValidationError("AMC is mandatory for Service procurement.")
    #         if not self.amc_start_date or not self.amc_duration_months: raise ValidationError("AMC start date and duration are required.")

    @staticmethod
    def get_financial_year():
        today = date.today()
        return f"{today.year}-{str(today.year + 1)[-2:]}" if today.month >= 4 else f"{today.year - 1}-{str(today.year)[-2:]}"

    def save(self, *args, **kwargs):
        if self.is_amc and self.amc_start_date and self.amc_duration_months:
            self.amc_end_date = self.amc_start_date + relativedelta(months=self.amc_duration_months)
        super().save(*args, **kwargs)
        if not self.document_no:
            self.document_no = f"PSM/{self.get_financial_year()}/{str(self.id).zfill(3)}"
            super().save(update_fields=["document_no"])

    def __str__(self): return self.document_no or f"PB-{self.id}"


class ProcurementUpload(models.Model):
    # project = models.ForeignKey(Project, on_delete=models.CASCADE)
    pb = models.ForeignKey(ProjectBoard, on_delete=models.CASCADE,null=True,blank=True)
    attachment = models.FileField(upload_to='procurement_excel/')
    uploaded_by = models.ForeignKey(
            settings.AUTH_USER_MODEL, 
            on_delete=models.SET_NULL, 
            null=True, 
            blank=True,
            related_name="approved_uploads"
        )
    created_at = models.DateTimeField(auto_now_add=True)



class ExcelFile(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE, related_name="procurement_items")
    item = models.CharField(max_length=1000)
    item_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=15,decimal_places=2)
    po_release_to_supplier = models.CharField(max_length=255,null=True,blank=True)
    # upload_session = models.ForeignKey(ProcurementUpload,on_delete=models.CASCADE,related_name="items",null=True,blank=True)    
    delivery_date = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False) # Only True if the session is approved    
    def __str__(self):
        return f"{self.item} - {self.total}"



class CommercialRequirement(models.Model):
    project_board = models.ForeignKey(ProjectBoard, on_delete=models.CASCADE, related_name='commercial_requirement')
    quotation_validity = models.CharField(max_length=20, choices=QuotationValidity.choices, default=QuotationValidity.NA)
    energy_efficiency = models.CharField(max_length=100, choices=EnergyEfficiency.choices, default=EnergyEfficiency.NA)
    risk_category = models.CharField(max_length=50, choices=RiskCategory.choices, default=RiskCategory.NA)
    customer_pre_selected = models.CharField(max_length=50, choices=[('Customer Preferred', 'Customer Preferred'), ('Customer Pre-Selected', 'Customer Pre-Selected'), ('None', 'None'), ('NA','NA')])
    pre_negotiated = models.CharField(max_length=50, choices=[('Non-negotiated', 'Non-negotiated'), ('Customer Pre-negotiated', 'Customer Pre-negotiated'), ('Previous PO Value', 'Previous PO Value'), ('CE-Stage negotiated','CE-Stage negotiated'), ('NA','NA')])
    customer_preferred_list = models.CharField(max_length=50, choices=[('Yes', 'Yes'), ('No', 'No'), ('NA','NA')])
    functional_restrictions = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='commercial_created_by')
    created_at, updated_at = models.DateTimeField(auto_now_add=True), models.DateTimeField(auto_now=True)
    def __str__(self): return f"Commercial Requirement - {self.project_board.document_no}"



class Supplier(models.Model):
    project_board = models.ForeignKey(ProjectBoard, on_delete=models.CASCADE, related_name='suppliers')
    supplier_name = models.CharField(max_length=255)
    quotation_validity_before = models.CharField(max_length=100, choices=QuotationValidity.choices, default=QuotationValidity.NA)
    quotation_validity_after = models.CharField(max_length=100, choices=QuotationValidity.choices, default=QuotationValidity.NA)
    energy_efficiency_before = models.CharField(max_length=100, choices=EnergyEfficiency.choices, default=EnergyEfficiency.NA)
    energy_efficiency_after = models.CharField(max_length=100, choices=EnergyEfficiency.choices, default=EnergyEfficiency.NA)
    risk_category_before = models.CharField(max_length=50, choices=RiskCategory.choices, default=RiskCategory.NA)
    risk_category_after = models.CharField(max_length=50, choices=RiskCategory.choices, default=RiskCategory.NA)
               
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='supplier_created_by')
    created_at, updated_at = models.DateTimeField(auto_now_add=True), models.DateTimeField(auto_now=True)
    def __str__(self): return self.supplier_name



class SupplierNegotiation(models.Model):
    project_board = models.ForeignKey(ProjectBoard, on_delete=models.CASCADE, related_name='supplier_negotiations')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='project_negotiations')
    gross_total, net_total = models.DecimalField(max_digits=15, decimal_places=2, default=0), models.DecimalField(max_digits=15, decimal_places=2, default=0)
    discount_overall_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_overall_net = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    is_finalized, finalized_by = models.BooleanField(default=False), models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    finalized_comment, finalized_at, created_at = models.TextField(), models.DateTimeField(null=True, blank=True), models.DateTimeField(auto_now_add=True)



class LineItem(models.Model):
    project_board = models.ForeignKey(ProjectBoard, on_delete=models.CASCADE, related_name='line_items')
    position_no, co_no, item_code = models.IntegerField(), models.CharField(max_length=50, blank=True, null=True), models.CharField(max_length=100, blank=True, null=True)
    description, unit_no, reference_po_no = models.TextField(), models.CharField(max_length=50, blank=True, null=True), models.CharField(max_length=100, blank=True, null=True)
    quantity, unit = models.DecimalField(max_digits=10, decimal_places=2), models.CharField(max_length=50, choices=[('Pcs','Pcs'),('Meter','Meter'),('Set','Set'),('Liter','Liter'),('Days','Days'),('Hrs','Hrs'),('Nos','Nos')])
    budget, target_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True), models.DecimalField(max_digits=15, decimal_places=2)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='line_item_created_by')
    budget_enterd_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='budget_enterd_by')
    po_value, created_at, updated_at = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True), models.DateTimeField(auto_now_add=True), models.DateTimeField(auto_now=True)
    def __str__(self): return f"Item {self.position_no} - {self.project_board.document_no}"

class LineItemNegotiation(models.Model):
    project_board = models.ForeignKey(ProjectBoard, on_delete=models.CASCADE, related_name='negotiations')
    supplier, line_item = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='negotiations'), models.ForeignKey(LineItem, on_delete=models.CASCADE, related_name='negotiations')
    unit_price_before, total_price_before = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True), models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    unit_price_after, total_price_after = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True), models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    discount_overall_percantage, discount_overall_net = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True), models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    is_finalized, finalized_comment = models.BooleanField(default=False), models.TextField(null=True,blank=True)
    finalized_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='finalized_by')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='supplier_negotiation_created_by')
    created_at, updated_at = models.DateTimeField(auto_now_add=True), models.DateTimeField(auto_now=True)
    def __str__(self): return f"{self.supplier} - {self.line_item}"

    def calculate_totals(self):
        """
        Logic to calculate totals based on Unit Price and Quantity.
        Can be called manually or during save().
        """
        # Get quantity from the parent LineItem
        qty = Decimal(str(self.line_item.quantity or 0))
        
        # Get unit prices
        up_before = Decimal(str(self.unit_price_before or 0))
        up_after = Decimal(str(self.unit_price_after or 0))

        # Perform Math
        self.total_price_before = (qty * up_before).quantize(Decimal('0.01'))
        self.total_price_after = (qty * up_after).quantize(Decimal('0.01'))
        
        # Calculate Savings/Discount
        self.discount_overall_net = self.total_price_before - self.total_price_after
        
        if self.total_price_before > 0:
            perc = (self.discount_overall_net / self.total_price_before) * 100
            self.discount_overall_percantage = perc.quantize(Decimal('0.01'))
        else:
            self.discount_overall_percantage = Decimal('0.00')

    def save(self, *args, **kwargs):
        self.calculate_totals()
        super().save(*args, **kwargs)


class Term(models.Model):
    name, created_by = models.CharField(max_length=255, unique=True), models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='term_created_by')
    created_at, updated_at = models.DateTimeField(auto_now_add=True), models.DateTimeField(auto_now=True)
    def __str__(self): return self.name

class TermCondition(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='conditions')
    condition_name = models.CharField(max_length=255)
    # Changed related_name to be unique for TermCondition
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='conditions_created'
    )
    class Meta:
            # This ensures 'Available' can exist, but only ONCE per Term.
            unique_together = ('term', 'condition_name')    


class TermAssignment(models.Model):
    STATUS_CHOICES = [('Expected', 'Expected'), ('Agreed', 'Agreed')]
    
    project_board = models.ForeignKey(ProjectBoard, on_delete=models.CASCADE, related_name='term_assignments')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='supplier_term_assignments')

    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='assignments',null=True,blank=True)
    
    # Identifies if this specific row is the 'Expected' version or the 'Agreed' version
    status_type = models.CharField(max_length=10, choices=STATUS_CHOICES)

    # Common Fields
    text_detail = models.TextField(blank=True, null=True) # Used for general text or descriptions
    comments = models.TextField(blank=True, null=True)
    
    # Milestone Fields (Used for Payment/Delivery rows)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    justification = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)



class Approver(models.Model):
    project_board = models.ForeignKey('ProjectBoard', on_delete=models.CASCADE, related_name='approvers')
    approver, level = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='approver'), models.PositiveIntegerField(help_text="Approval level: 1, 2, 3 etc.")
    email = models.EmailField()
    approval_type = models.CharField(max_length=20, choices=[("RECOMMENDED", "Recommended"), ("MANDATORY", "Mandatory")], blank=True, null=True)
    def __str__(self): return f"{self.approver} - Level {self.level} - {self.project_board.document_no}"




from django.db import models, transaction
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class ChangeRequest(models.Model):
    # Link to any table (ProjectBoard, LineItem, etc.)
    LIMIT_MODELS = models.Q(model__in=[
        'projectboard', 'commercialrequirement', 'supplier', 
        'suppliernegotiation', 'lineitem', 'lineitemnegotiation',
        'termassignment'
    ])
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=LIMIT_MODELS)  
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # The data to be applied
    pending_data = models.JSONField(help_text="Stores the updated fields as JSON")
    
    is_approved = models.BooleanField(default=False)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def apply_changes(self):
        """Applies JSON data to the target object, handling relations and lists."""
        with transaction.atomic():
            model_name = self.content_type.model
            data = self.pending_data

            # 1. SPECIAL HANDLING FOR TERM ASSIGNMENT
            # Bypass content_object to avoid MultipleObjectsReturned/GFK crashes
            if model_name == 'termassignment' and isinstance(data, list):
                self._handle_list_payload(data)
            
            else:
                instance = self.content_object
                if not instance:
                    raise ValidationError("Target object no longer exists.")
                
                if isinstance(data, list):
                    # For other models using lists (if any)
                    self._handle_list_payload(data, instance=instance)
                else:
                    self._handle_dict_payload(instance, data)

            # 2. MARK AS APPROVED
            # Use update() here instead of self.save() to avoid re-triggering signals
            ChangeRequest.objects.filter(id=self.id).update(is_approved=True)

    def _handle_dict_payload(self, instance, data):
        for field, value in data.items():
            # 1. Handle nested negotiations inside LineItem
            if field == 'negotiations' and isinstance(value, list):
                self._handle_negotiations(instance, value)
                continue

            # 2. Resolve Foreign Keys (Convert ID to Object)
            try:
                field_obj = instance._meta.get_field(field)
                if field_obj.is_relation and value is not None:
                    related_model = field_obj.related_model
                    value = related_model.objects.get(pk=value)
            except Exception:
                pass # Not a relation or field doesn't exist on instance

            setattr(instance, field, value)
        instance.save()

    def _handle_negotiations(self, line_item_instance, neg_list):
        LineItemNegotiation = apps.get_model('purchase', 'LineItemNegotiation')
        for neg_data in neg_list:
            # Match by supplier and line_item
            LineItemNegotiation.objects.update_or_create(
                line_item=line_item_instance,
                supplier_id=neg_data.get('supplier'),
                defaults={
                    'unit_price_before': neg_data.get('unit_price_before'),
                    'unit_price_after': neg_data.get('unit_price_after'),
                }
            )

    def _handle_list_payload(self, data_list, instance=None):
            """Sync by Snapshot: Create, Update, and Delete within a specific Scope."""
            TermAssignment = apps.get_model('purchase', 'TermAssignment')
            if not data_list:
                return

            active_ids = []
            
            # Identify the Scope from the first item
            # We use .get() with exact keys to ensure deletion safety
            scope_pb = data_list[0].get('project_board')
            scope_supplier = data_list[0].get('supplier')
            scope_status = data_list[0].get('status_type')

            for item in data_list:
                item_id = item.get('id')

                # --- CREATE OR UPDATE ---
                if item_id:
                    assignment_obj = TermAssignment.objects.filter(id=item_id).first()
                    if not assignment_obj:
                        continue
                else:
                    # Use the user who requested the change as the creator
                    assignment_obj = TermAssignment(created_by=self.requested_by)

                # --- MAP FIELDS DYNAMICALLY ---
                for field, value in item.items():
                    if field == 'id': continue
                    
                    # Protect parent relations on existing records
                    if item_id and field in ['project_board', 'supplier']:
                        continue

                    try:
                        field_obj = TermAssignment._meta.get_field(field)
                        
                        # Fix: Handle ForeignKey mapping (e.g., term -> term_id)
                        if field_obj.is_relation and not field_obj.many_to_many:
                            target_attr = f"{field}_id"
                        else:
                            target_attr = field
                        
                        if hasattr(assignment_obj, target_attr):
                            setattr(assignment_obj, target_attr, value)
                    except FieldDoesNotExist:
                        continue
                
                assignment_obj.save()
                active_ids.append(assignment_obj.id)

            # --- SCOPED SNAPSHOT DELETION ---
            # This is the "Safety Valve" that prevents Agreed from deleting Expected
            if scope_pb and scope_supplier and scope_status:
                TermAssignment.objects.filter(
                    project_board_id=scope_pb,
                    supplier_id=scope_supplier,
                    status_type=scope_status
                ).exclude(id__in=active_ids).delete()
    # def apply_changes(self):
    #     """Applies the JSON data to the actual record columns."""
    #     with transaction.atomic():
    #         instance = self.content_object
    #         for field, value in self.pending_data.items():
    #             setattr(instance, field, value)
    #         instance.save()
    #         self.is_approved = True
    #         self.save()


class ApprovalStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'

class ApprovalRejection(models.Model):
    LIMIT_MODELS = models.Q(model__in=[
        'projectboard', 'commercialrequirement', 
        'suppliernegotiation', 'lineitemnegotiation', 'termassignment'
    ])
    
    # Link to the main Project Board
    pb_id = models.ForeignKey(ProjectBoard, on_delete=models.CASCADE, related_name='approval_pb')

    # Just store the MODEL TYPE, no specific record ID
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=LIMIT_MODELS)

    status = models.CharField(
        max_length=20, 
        choices=ApprovalStatus.choices, 
        default=ApprovalStatus.PENDING,
        db_index=True
    )
    
    comments = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.status} - {self.content_type.model} for PB {self.pb_id.document_no}"



class Draft(models.Model):
    # Link to any table (ProjectBoard, LineItem, etc.)
    LIMIT_MODELS = models.Q(model__in=[
        'projectboard', 'commercialrequirement', 'supplier', 
        'suppliernegotiation', 'lineitem', 'lineitemnegotiation',
        'term', 'termassignment','termcondition','approver'
    ])
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=LIMIT_MODELS)  
    object_id = models.PositiveIntegerField(null=True,blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # The data to be applied
    pending_data = models.JSONField(help_text="Stores the updated fields as JSON")
    
    is_approved = models.BooleanField(default=False)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def apply_changes(self):
        """Applies the JSON data to the actual record columns."""
        with transaction.atomic():
            instance = self.content_object
            for field, value in self.pending_data.items():
                setattr(instance, field, value)
            instance.save()
            self.is_approved = True
            self.save()
            