from rest_framework import serializers
from .models import *
from django.db.models import F,Sum
from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction
from django.contrib.auth import get_user_model
from accounts.models import CustomUser as User



class ProjectProcurementItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelFile
        fields = [
            "id",
            "item",
            "total",
            "po_release_to_supplier",
            "delivery_date",
            "created_at",
        ] 

class ProjectCreateSerializer(serializers.ModelSerializer):
    # --- Write Fields (IDs) ---
    project_id = serializers.PrimaryKeyRelatedField(queryset=MainProject.objects.all(), source='project', write_only=True, required=False, allow_null=True)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), required=False, allow_null=True)
    project_manager = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    hod = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    # --- Read Fields (Object Mappings) ---
    project_details = serializers.SerializerMethodField(read_only=True)
    dept_details = serializers.SerializerMethodField(read_only=True)
    
    # --- User Name Mappings ---
    project_manager_name = serializers.SerializerMethodField(read_only=True)
    hod_name = serializers.SerializerMethodField(read_only=True)
    actual_expense = serializers.ReadOnlyField()
    remaining_budget = serializers.ReadOnlyField()
    deviation = serializers.ReadOnlyField()
    class Meta:
        model = Project

        fields = [
            "id", "project_type", "project_id", "project_details", 
            "project_manager", "project_manager_name", 
            "hod", "hod_name", 
            "department", "dept_details",
            "total_budget", "actual_expense", "status", 
            "remaining_budget", "deviation"
        ]

    def to_representation(self, instance):
        """
        Calculates Committed Costs (Actual Expense), Remaining Budget, and Deviation.
        """
        data = super().to_representation(instance)

        # 1. Calculate Committed Costs (Actual Expense)
        # Relationship: Project -> ProjectBoard -> SupplierNegotiation
        committed_costs = SupplierNegotiation.objects.filter(
            project_board__project=instance,
            is_finalized=True
        ).aggregate(total_cost=Sum('net_total'))['total_cost'] or 0

        # 2. Budget Calculations
        total_budget = float(instance.total_budget or 0)
        actual_expense = float(committed_costs)
        
        # Remaining budget and Deviation logic
        remaining = total_budget - actual_expense
        deviation = remaining # Usually Deviation = Budget - Actual
        if total_budget > 0:
            dev_percent = (actual_expense / total_budget) * 100
        else:
            dev_percent = 0.0
        # 3. Inject into JSON output
        data['actual_expense'] = actual_expense
        data['remaining_budget'] = remaining
        data['deviation'] = round(dev_percent, 2)
        
        return data

    # --- Helper Methods ---
    def _format_user_name(self, user_instance):
        if user_instance:
            full_name = user_instance.get_full_name()
            return full_name.strip() if full_name else user_instance.username
        return "Not Assigned"

    def get_project_manager_name(self, obj):
        return self._format_user_name(obj.project_manager)

    def get_hod_name(self, obj):
        return self._format_user_name(obj.hod)

    def get_project_details(self, obj):
        if not obj.project: return None
        return {"id": obj.project.id, "code": getattr(obj.project, 'co_no', 'N/A'), "name": getattr(obj.project, 'project_name', 'N/A')}

    def get_dept_details(self, obj):
        if not obj.department: return None
        return {"id": obj.department.id, "code": getattr(obj.department, 'code', 'N/A'), "name": getattr(obj.department, 'name', 'N/A')}

    # --- Logic Fixes ---
    def to_internal_value(self, data):
        # Create a mutable copy of the data
        if hasattr(data, 'dict'):
            data = data.dict()
        elif hasattr(data, 'copy'):
            data = data.copy()

        # List of fields that might come in as empty strings from a file upload form
        nullable_fields = ['department', 'project_id', 'project_manager', 'hod']
        
        for field in nullable_fields:
            val = data.get(field)
            if val in ["", "null", "undefined", None]:
                data[field] = None
                
        return super().to_internal_value(data)

    def validate(self, data):
        project = data.get('project')
        department = data.get('department')

        if project and department:
            raise serializers.ValidationError("Choose either Project or Department, not both.")
        if not project and not department:
            raise serializers.ValidationError("You must provide a Project or a Department.")
        return data

class ProjectBudgetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['total_budget']

class BudgetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectBudget
        fields = ["project", "budget"]
 
class BudgetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectBudget
        fields = ["budget", "created_at"]
 
class CashInflowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashInflow
        fields = ["project", "amount", "date"]

class CashInflowListSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.project.project_name", read_only=True)

    class Meta:
        model = CashInflow
        fields = [
            "id",
            "project",
            "project_name",
            "amount",
            "date",
            "status",
            "created_at",
        ]
 
class CashOutflowListSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.project.project_name", read_only=True)
 
    class Meta:
        model = CashInflow
        fields = [
            "id",
            "project",
            "project_name",
            "amount",
            "date",
            "status",
            "created_at",
        ]

class ExcelFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelFile
        fields = '__all__'

class ProjectBoardReadSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.get_full_name', read_only=True)
    project_code = serializers.CharField(source='project.project_code', read_only=True)
    
    # New field to show the Project's total budget
    project_total_budget = serializers.DecimalField(
        source='project.total_budget', # Adjust 'total_budget' to the actual field name in your Project model
        max_digits=14, 
        decimal_places=2, 
        read_only=True
    )
    
    remaining_budget = serializers.SerializerMethodField(read_only=True)
    attachments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProjectBoard
        fields = '__all__'

    def get_remaining_budget(self, obj):
        # 1. Fetch budget from the Project table mapped to this PB
        # Ensure 'total_budget' is the correct field name in your Project model
        project_budget = obj.project.total_budget if obj.project else 0
        
        # 2. Calculate costs specifically for this Project Board
        committed_costs = SupplierNegotiation.objects.filter(
            project_board=obj,
            is_finalized=True
        ).aggregate(total_cost=Sum('net_total'))['total_cost'] or 0
        
        return float(project_budget) - float(committed_costs)

    def get_attachments(self, obj):
        queryset = ProcurementUpload.objects.filter(pb=obj)
        return ProcurementUploadSerializer(
            queryset, 
            many=True, 
            context={'request': self.context.get('request')}
        ).data

class ProjectBoardSummarySerializer(serializers.ModelSerializer):
    buyer_name = serializers.SerializerMethodField()
    project_total_budget = serializers.DecimalField(
        source='project.total_budget', # Adjust 'total_budget' to the actual field name in your Project model
        max_digits=14, 
        decimal_places=2, 
        read_only=True
    )
    
    remaining_budget = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ProjectBoard
        fields = '__all__'
        read_only_fields = ['document_no', 'project_total_budget','remaining_budget', 'created_by', 'amc_end_date', 'buyer_name']


    def get_remaining_budget(self, obj):
        # 1. Fetch budget from the Project table mapped to this PB
        # Ensure 'total_budget' is the correct field name in your Project model
        project_budget = obj.project.total_budget if obj.project else 0
        
        # 2. Calculate costs specifically for this Project Board
        committed_costs = SupplierNegotiation.objects.filter(
            project_board=obj,
            is_finalized=True
        ).aggregate(total_cost=Sum('net_total'))['total_cost'] or 0
        
        return float(project_budget) - float(committed_costs)        
    def get_buyer_name(self, obj):
        # 1. Check if the 'approver' relationship exists on the object
        if obj.buyer:
            # 2. Use get_full_name() if available, otherwise fallback to username
            full_name = obj.buyer.get_full_name()
            return full_name.strip() if full_name else obj.buyer.username
        return "No Approver Assigned"

class ProjectBoardCreateUpdateSerializer(serializers.ModelSerializer):
    buyer_name = serializers.SerializerMethodField()

    class Meta:
        model = ProjectBoard
        fields = '__all__'
        # Added 'buyer_name' to read_only_fields as it's a MethodField
        read_only_fields = ['document_no', 'created_by', 'amc_end_date', 'buyer_name']

    def get_buyer_name(self, obj):
        # 1. Check if the 'approver' relationship exists on the object
        if obj.buyer:
            # 2. Use get_full_name() if available, otherwise fallback to username
            full_name = obj.buyer.get_full_name()
            return full_name.strip() if full_name else obj.buyer.username
        return "No Approver Assigned"

    def validate(self, data):
        # Trigger model clean for combined field validation
        instance = ProjectBoard(**data)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message)
        return data

class ProcurementUploadSerializer(serializers.ModelSerializer):
    attachment_url = serializers.SerializerMethodField()

    class Meta:
        model = ProcurementUpload
        fields = ['id', 'pb', 'attachment', 'attachment_url', 'created_at']

    def get_attachment_url(self, obj):
        if obj.attachment:
            # This returns just the path starting from /media/
            return obj.attachment.url
        return None


class CommercialRequirementSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommercialRequirement
        fields = '__all__'

class CommercialRequirementCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommercialRequirement
        fields = '__all__'

    def validate(self, data):
        # Trigger model clean for combined field validation
        instance = CommercialRequirement(**data)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message)
        return data

class SupplierCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

    def validate(self, data):
        # Trigger model clean for combined field validation
        instance = Supplier(**data)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message)
        return data



class SupplierNegotiationSerializer(serializers.ModelSerializer):
    # Include supplier details for context (read-only)
    supplier_details = SupplierCreateUpdateSerializer(source='supplier', read_only=True)
    # Human-readable name for the person who finalized
    finalized_by_name = serializers.ReadOnlyField(source='finalized_by.username')

    class Meta:
        model = SupplierNegotiation
        fields = [
            'id', 'project_board', 'supplier', 'supplier_details',
            'gross_total', 'net_total', 'discount_overall_percentage', 
            'discount_overall_net', 'is_finalized', 'finalized_by',
            'finalized_by_name', 'finalized_comment', 'finalized_at', 'created_at'
        ]
        read_only_fields = ['created_at']


class SupplierSummarySerializer(serializers.ModelSerializer):
    # This must match the related_name='project_negotiations' in your model
    project_negotiations = SupplierNegotiationSerializer(many=True, read_only=True)
    
    # Optional: If you want to show the username of the creator
    created_by_name = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Supplier
        # Using specific fields is safer, but '__all__' works too
        fields = [
            'id', 'project_board', 'supplier_name', 'project_negotiations',
            'quotation_validity_before', 'quotation_validity_after',
            'energy_efficiency_before', 'energy_efficiency_after',
            'risk_category_before', 'risk_category_after',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]



# class SupplierNegotiationSerializer(serializers.ModelSerializer):
#     # Include supplier details so the frontend knows who the negotiation is for
#     supplier_details = SupplierCreateUpdateSerializer(source='supplier', read_only=True)
    
#     # Optional: Display the name of the person who finalized it
#     finalized_by_name = serializers.ReadOnlyField(source='finalized_by.username')

#     class Meta:
#         model = SupplierNegotiation
#         fields = [
#             'id', 
#             'project_board', 
#             'supplier', 
#             'supplier_details',
#             'gross_total', 
#             'net_total', 
#             'discount_overall_percentage', 
#             'discount_overall_net', 
#             'is_finalized', 
#             'finalized_by',
#             'finalized_by_name',
#             'finalized_comment', 
#             'finalized_at', 
#             'created_at'
#         ]
#         read_only_fields = ['created_at']



class LineItemNegotiationSerializer(serializers.ModelSerializer):
    supplier_details = SupplierCreateUpdateSerializer(source='supplier', read_only=True)
    
    class Meta:
        model = LineItemNegotiation
        fields = '__all__'
        # These fields are required by the model, but we mark them read_only
        # here so they pass validation in the POST request.
        read_only_fields = [
            'project_board', 
            'line_item', 
            'created_by', 
            'finalized_by'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If finalized_comment is mandatory in the model but you want 
        # it optional during creation, you can override it here:
        self.fields['finalized_comment'].required = False

class LineItemSerializer(serializers.ModelSerializer):
    negotiations = LineItemNegotiationSerializer(many=True, required=False)

    class Meta:
        model = LineItem
        fields = '__all__'
        read_only_fields = ['created_by', 'budget_enterd_by']

class TermConditionSerializer(serializers.ModelSerializer):
    # This allows you to pass the term ID when creating/updating
    # term = serializers.PrimaryKeyRelatedField(queryset=Term.objects.all())

    class Meta:
        model = TermCondition
        fields = '__all__'
        read_only_fields = ['created_by']

class TermSerializer(serializers.ModelSerializer):
    # This matches the related_name='conditions' in your model
    conditions = TermConditionSerializer(many=True, read_only=True)

    class Meta:
        model = Term
        fields = ['id', 'name', 'conditions']

class TermSerializer1(serializers.ModelSerializer):
    # This matches the related_name='conditions' in your model

    class Meta:
        model = Term
        fields = ['id', 'name', 'conditions']        

class TermAssignmentSummarySerializer(serializers.ModelSerializer):
    """Used for GET requests - Returns all data including timestamps"""
    term = TermSerializer1(read_only=True)
    class Meta:
        model = TermAssignment
        fields = '__all__'

class TermAssignmentCreateUpdateSerializer(serializers.ModelSerializer):
    """Used for POST/PATCH - Excludes audit fields from input"""
    class Meta:
        model = TermAssignment
        # Exclude internal fields so the frontend doesn't see/send them
        exclude = ['created_by', 'created_at']

    def validate(self, data):
        # We use a temporary instance to trigger model-level clean()
        instance = TermAssignment(**data)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict if hasattr(e, 'message_dict') else e.message)
        return data



class ApproverSummarySerializer(serializers.ModelSerializer):
    approver_name = serializers.SerializerMethodField()
    submission_status = serializers.SerializerMethodField()

    class Meta:
        model = Approver
        fields = [
            'id', 'level', 'email', 'approver', 
            'approver_name', 'submission_status'
        ]

    def get_approver_name(self, obj):
        if obj.approver:
            full_name = obj.approver.get_full_name()
            return full_name.strip() if full_name else obj.approver.username
        return "No Approver Assigned"

    def get_submission_status(self, obj):
        if not obj.approver:
            return "No Approver"

        # The 5 models we are looking for
        target_models = [
            'projectboard', 'commercialrequirement', 
            'suppliernegotiation', 'lineitemnegotiation', 'termassignment'
        ]
        
        # Count how many of these models have a record for this user and PB
        completed_count = ApprovalRejection.objects.filter(
            pb_id=obj.project_board,
            created_by=obj.approver,
            content_type__model__in=target_models,
        ).values('content_type').distinct().count()

        return "Submitted" if completed_count  else f"Not Submitted"
        
class ApproverCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approver
        fields = '__all__'
        # Mark created_by as read_only so the serializer doesn't 
        # expect it from the frontend request body
        extra_kwargs = {
            'created_by': {'read_only': True}
        }

    def validate(self, data):
        # We create a temporary instance to run model-level clean()
        # We use .get() or pop() to ensure unexpected fields don't crash __init__
        try:
            instance = Approver(**data)
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        except TypeError as e:
            # This catches cases where fields in 'data' aren't in the model
            raise serializers.ValidationError(f"Invalid field provided: {str(e)}")
        return data


# class PBSummarySerializer(serializers.ModelSerializer):
#     basicDetails = serializers.SerializerMethodField()
#     commercialRequirements = serializers.SerializerMethodField()
#     suppliers = serializers.SerializerMethodField()
#     tableRows = serializers.SerializerMethodField()
#     customerSelection = serializers.SerializerMethodField()
#     terms = serializers.SerializerMethodField()
#     approvers = serializers.SerializerMethodField()

#     class Meta:
#         model = ProjectBoard
#         fields = [
#             'basicDetails', 'commercialRequirements', 'suppliers', 
#             'tableRows', 'customerSelection', 'terms', 'approvers'
#         ]

#     def get_basicDetails(self, obj):
#         return {
#             "projectName": obj.project.project.project_name if obj.project else "N/A",
#             "commodity": obj.commodity_equipment,
#             "costUnit": obj.cost_center,
#             "rfqSignOff": obj.rfq_sign_off_date.strftime('%Y-%m-%d') if obj.rfq_sign_off_date else None,
#             "documentNo": obj.document_no,
#             "buyerName": obj.buyer.get_full_name() if obj.buyer else "N/A",
#             "currency": obj.currency,
#         }

#     def get_commercialRequirements(self, obj):
#         comm = obj.commercial_requirement.first()
        
#         return {
#                 "Period Of Quotation Validity": comm.quotation_validity,
#                 "Energy Efficiency Requirements": comm.energy_efficiency,
#                 "Risk Category / Supplier Qualification": comm.risk_category,
#                 "Customer Pre-Selected": comm.customer_pre_selected,
#                 "Pre-negotiated": comm.pre_negotiated,
#                 "According Customer Preferred List": comm.customer_preferred_list,
#                 "Restrictions Functional Department": comm.functional_restrictions or "None"
#             }
#     def get_suppliers(self, obj):
#         suppliers_data = []
#         # Fetch all suppliers linked to this Project Board
#         for s in obj.suppliers.all():
#             suppliers_data.append({
#                 "id": s.id,
#                 "supplierName": s.supplier_name,
                
#                 # Before Negotiation Values
#                 "beforeRiskCategory": s.risk_category_before,
#                 "beforeQuotationValidity": s.quotation_validity_before,
#                 "beforeEnergyEfficiency": s.energy_efficiency_before,
                
#                 # After Negotiation Values
#                 "afterRiskCategory": s.risk_category_after,
#                 "afterQuotationValidity": s.quotation_validity_after,
#                 "afterEnergyEfficiency": s.energy_efficiency_after,
                
#                 # Metadata for tracking
#                 "auditDetails": {
#                     "addedBy": s.created_by.get_full_name() if s.created_by else "N/A",
#                     "addedOn": s.created_at.strftime('%d-%m-%Y')
#                 }
#             })
#         return suppliers_data

#     def get_tableRows(self, obj):
#         rows = []
#         line_items = obj.line_items.all().prefetch_related('negotiations')
        
#         for item in line_items:
#             supplier_cols = {}
#             for neg in item.negotiations.all():
#                 # Format: [Unit Before, Unit After, Total Before, Total After]
#                 supplier_cols[str(neg.supplier_id)] = {
#                     "supplierName": neg.supplier.supplier_name,
#                     "metrics": {
#                         "unitPriceBefore": float(neg.unit_price_before or 0),
#                         "unitPriceAfter": float(neg.unit_price_after or 0),
#                         "totalPriceBefore": float(neg.total_price_before or 0),
#                         "totalPriceAfter": float(neg.total_price_after or 0),
#                         "savingsNet": float(neg.discount_overall_net or 0),
#                         "savingsPercentage": float(neg.discount_overall_percantage or 0)
#                     }
#                 }
            
#             rows.append({
#                 "pos": item.position_no,
#                 "coNo": item.co_no,
#                 "itemCd": item.item_code,
#                 "desc": item.description,
#                 "unitNo": item.unit_no,
#                 "refPo": item.reference_po_no,
#                 "qty": float(item.quantity),
#                 "unit": item.unit,
#                 "budget": f"{item.budget} {obj.currency}",
#                 "target": f"{item.target_price} {obj.currency}",
#                 "suppliers": supplier_cols
#             })
#         return rows

#     def get_customerSelection(self, obj):
#         # 1. Fetch the finalized negotiation record with linked supplier data
#         finalized = obj.supplier_negotiations.filter(is_finalized=True).select_related('supplier', 'finalized_by').first()

#         # If no supplier is finalized yet, return None to hide the section
#         if not finalized:
#             return None 

#         # 2. Get the Commercial Requirement for the 'Pre-selected' status
#         comm = obj.commercial_requirement.first()
        
#         # 3. Pull the Winning Supplier's Profile
#         winning_supplier = finalized.supplier

#         return {
#             "selectedSupplier": winning_supplier.supplier_name,
            
#             # Crucial Supplier Profile (Final Status after negotiation)
#             "supplierCrucialDetails": {
#                 "riskCategory": winning_supplier.risk_category_after,
#                 "quotationValidity": winning_supplier.quotation_validity_after,
#                 "energyEfficiency": winning_supplier.energy_efficiency_after,
#             },
            
#             # Overall Negotiation Totals
#             "negotiationOverall": {
#                 "grossTotal": f"{finalized.gross_total} {obj.currency}",
#                 "netTotal": f"{finalized.net_total} {obj.currency}",
#                 "discountNet": f"{finalized.discount_overall_net} {obj.currency}",
#                 "discountPercent": f"{finalized.discount_overall_percentage}%"
#             },
            
#             # Finalization & Audit Trail
#             "finalizedDetails": {
#                 "comment": finalized.finalized_comment,
#                 "finalizedBy": finalized.finalized_by.get_full_name() if finalized.finalized_by else "N/A",
#                 "finalizedAt": finalized.finalized_at.strftime('%Y-%m-%d %H:%M') if finalized.finalized_at else "N/A"
#             }
#         }

#     def get_terms(self, obj):
#         data = []
#         # Get all distinct term names for this Project Board
#         term_names = obj.term_assignments.values_list('term__name', flat=True).distinct()

#         for t_name in term_names:
#             # Fetch all assignments for this term name to handle multi-line terms (like milestones)
#             assignments = obj.term_assignments.filter(term__name=t_name)
            
#             expected_list = assignments.filter(status_type='Expected')
#             agreed_list = assignments.filter(status_type='Agreed')

#             def format_term_detail(assignment):
#                 """Helper to format text, percentage, date, and justification."""
#                 parts = []
#                 if assignment.text_detail:
#                     parts.append(assignment.text_detail)
#                 if assignment.percentage:
#                     parts.append(f"{assignment.percentage}%")
#                 if assignment.date:
#                     parts.append(f"Date: {assignment.date.strftime('%d-%m-%Y')}")
#                 if assignment.justification:
#                     parts.append(f"(Justification: {assignment.justification})")
                
#                 return " | ".join(parts) if parts else None

#             # If there's only one entry, return as string. If multiple, join them with newlines.
#             expected_text = "\n".join([format_term_detail(a) for a in expected_list if format_term_detail(a)])
#             agreed_text = "\n".join([format_term_detail(a) for a in agreed_list if format_term_detail(a)])

#             data.append({
#                 "term": t_name,
#                 "expected": expected_text if expected_text else None,
#                 "agreed": agreed_text if agreed_text else None,
#                 # Optional: Add raw fields if your frontend needs to process them separately
#                 "has_milestones": assignments.filter(percentage__isnull=False).exists()
#             })
            
#         return data

#     def get_approvers(self, obj):
#         return [{
#             "level": app.level,
#             "project_name": obj.project.project.project_name if obj.project else "N/A",
#             "role": app.approver.role if app.approver.role else "N/A",

#             "approver_name": app.approver.get_full_name() if app.approver else "N/A",
#             "status": "PENDING", # You can add logic here to check actual approval status
#             "comments": ""
#         } for app in obj.approvers.all().order_by('level')]

from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import ProjectBoard, ChangeRequest  # Ensure ChangeRequest is imported


class ApprovalRejectionSerializer(serializers.ModelSerializer):
    # This shows "commercialrequirement" instead of an ID like 42
    model_name = serializers.ReadOnlyField(source='content_type.model')
    created_by = serializers.ReadOnlyField(source='created_by.get_full_name')
    class Meta:
        model = ApprovalRejection
        fields = [
            'id', 'pb_id', 'model_name', 'status', 
            'comments', 'created_by', 'created_at'
        ]
        read_only_fields = ['created_by', 'created_at']



class ChangeRequestApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeRequest
        fields = ['is_approved']

    def update(self, instance, validated_data):
        is_approved = validated_data.get('is_approved')
        
        if is_approved and not instance.is_approved:
            try:
                instance.apply_changes()
            except Exception as e:
                raise serializers.ValidationError(f"Error applying changes: {str(e)}")
        
        return super().update(instance, validated_data)


class HydrateProjectBoardSerializer(serializers.Serializer):
    def to_representation(self, instance):
        # instance is the raw dictionary from pending_data
        data = super().to_representation(instance)
        
        # Keep all original fields from your JSON
        result = instance.copy() 

        # Add/Replace values for readable names
        try:
            result['project_name'] = Project.objects.get(id=instance.get('project')).project.project_name
        except: result['project_name'] = None
            
        try:
            result['buyer_name'] = User.objects.get(id=instance.get('buyer')).get_full_name()
        except: result['buyer_name'] = None

        return result

class HydrateCommercialSerializer(serializers.Serializer):
    def to_representation(self, instance):
        # instance is the raw dictionary: {"project_board": 7, "risk_category": "Low Risk", ...}
        
        # 1. Create a copy to keep all original fields (quotation_validity, energy_efficiency, etc.)
        result = instance.copy()

        # 2. Resolve Project Board Document Number
        pb_id = instance.get('project_board')
        if pb_id:
            try:
                # We fetch the document_no from the ProjectBoard model
                pb = ProjectBoard.objects.get(id=pb_id)
                result['project_board_document'] = pb.document_no
            except ProjectBoard.DoesNotExist:
                result['project_board_document'] = "Unknown PB"
        else:
            result['project_board_document'] = None

        return result


class HydrateLineItemSerializer(serializers.Serializer):
    def to_representation(self, instance):
        # instance is the raw dictionary from pending_data
        
        # 1. Create a copy to keep all original fields (co_no, item_code, etc.)
        result = instance.copy()

        # 2. Resolve Project Board Document No (Optional context)
        pb_id = instance.get('project_board')
        if pb_id:
            try:
                pb = ProjectBoard.objects.get(id=int(pb_id))
                result['project_board_document'] = pb.document_no
            except (ProjectBoard.DoesNotExist, ValueError):
                pass

        # 3. Hydrate Nested Negotiations List
        negotiations_list = instance.get('negotiations', [])
        if negotiations_list:
            hydrated_negs = []
            for neg in negotiations_list:
                neg_copy = neg.copy()
                supplier_id = neg.get('supplier')
                
                try:
                    # Convert supplier ID to actual name
                    s = Supplier.objects.get(id=supplier_id)
                    neg_copy['supplier_name'] = s.supplier_name
                except (Supplier.DoesNotExist, ValueError):
                    neg_copy['supplier_name'] = "Unknown"
                
                hydrated_negs.append(neg_copy)
            
            # Update the copy with the new hydrated list
            result['negotiations'] = hydrated_negs

        return result

class HydrateTermAssignmentSerializer(serializers.Serializer):
    # --- Base Data Fields (Must be explicitly defined) ---
    id = serializers.IntegerField(read_only=True)
    status_type = serializers.CharField(allow_null=True, required=False)
    text_detail = serializers.CharField(allow_null=True, required=False)
    date = serializers.DateField(allow_null=True, required=False)
    percentage = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True, required=False)
    justification = serializers.CharField(allow_null=True, required=False)
    project_board = serializers.IntegerField(required=False)
    
    # --- ID Fields (Stored in JSON) ---
    term = serializers.IntegerField(write_only=True)
    supplier = serializers.IntegerField(write_only=True)

    # --- Lookup Fields (Calculated) ---
    term_name = serializers.SerializerMethodField()
    supplier_name = serializers.SerializerMethodField()

    def get_term_name(self, obj):
        try: 
            term_id = obj.get('term')
            if not term_id: return None
            # Using .get() here is okay for small sets, 
            # but see the 'Optimization' note below for production
            return Term.objects.get(id=term_id).name
        except Exception:
            return f"Unknown Term ({obj.get('term')})"

    def get_supplier_name(self, obj):
        try: 
            sup_id = obj.get('supplier')
            if not sup_id: return None
            return Supplier.objects.get(id=sup_id).supplier_name
        except Exception:
            return f"Unknown Supplier ({obj.get('supplier')})"

class HydrateSupplierSerializer(serializers.Serializer):
    def to_representation(self, instance):
        result = instance.copy()
        
        # Resolve Project Board
        pb_id = instance.get('project_board')
        if pb_id:
            try:
                pb = ProjectBoard.objects.get(id=int(pb_id))
                result['project_board_document'] = pb.document_no
            except: pass

        # Resolve the actual Supplier Name if it's an ID change
        # Note: If 'supplier' is an ID in your JSON, we convert it
        supplier_id = instance.get('supplier')
        if supplier_id:
            try:
                result['supplier_name'] = Supplier.objects.get(id=supplier_id).supplier_name
            except: pass
            
        return result



HYDRATION_MAP = {
    'projectboard': HydrateProjectBoardSerializer,
    'commercialrequirement': HydrateCommercialSerializer,
    'supplier': HydrateSupplierSerializer, # Use previous logic for supplier
    'lineitem': HydrateLineItemSerializer,
    'termassignment': HydrateTermAssignmentSerializer,
}

from django.contrib.contenttypes.models import ContentType

# from django.db.models.query import QuerySet
# class PBSummarySerializer(serializers.ModelSerializer):
#     basicDetails = serializers.SerializerMethodField()
#     commercialRequirements = serializers.SerializerMethodField()
#     suppliers = serializers.SerializerMethodField()
#     tableRows = serializers.SerializerMethodField()
#     customerSelection = serializers.SerializerMethodField()
#     terms = serializers.SerializerMethodField()
#     approvers = serializers.SerializerMethodField()

#     class Meta:
#         model = ProjectBoard
#         fields = [
#             'basicDetails', 'commercialRequirements', 'suppliers', 
#             'tableRows', 'customerSelection', 'terms', 'approvers'
#         ]


#     # def get_pending_data(self, instance, filter_key=None, filter_value=None):
#     #     if not instance:
#     #         return None
            
#     #     ct = ContentType.objects.get_for_model(instance)
        
#     #     # IMPORTANT: If all term assignments are stored under ONE ChangeRequest, 
#     #     # we might need to find the CR by the common link (like project_board_id) 
#     #     # or ensure the object_id matches what you saved.
#     #     change = ChangeRequest.objects.filter(
#     #         content_type=ct, 
#     #         object_id=instance.id, 
#     #         is_approved=False
#     #     ).first()
#     #     # Fallback: If not found by instance ID, you might need to find it via the 
#     #     # ProjectBoard ID if that's how you're grouping "Bulk" terms.
        
#     #     if not change or not change.pending_data:
#     #         return None

#     #     raw_json = change.pending_data
        
#     #     # Flatten if it's a list of lists: [[{item1}, {item2}]] -> [{item1}, {item2}]
#     #     if isinstance(raw_json, list) and len(raw_json) > 0 and isinstance(raw_json[0], list):
#     #         raw_json = raw_json[0]

#     #     if filter_key and filter_value and isinstance(raw_json, list):
#     #         # Filter the list to only include items for THIS specific term (e.g., 'Warranty')
#     #         filtered_items = [item for item in raw_json if item.get(filter_key) == filter_value]
#     #         return filtered_items if filtered_items else None

#     #     return raw_json


#     def get_pending_data(self, instance, filter_key=None, filter_value=None):
#         """
#         Fetch pending ChangeRequest data for a given instance.

#         Handles:
#         - Dict type (basic details)
#         - List type (terms, bulk updates)

#         Returns:
#         - None if no pending data
#         - Dict with pending data + metadata
#         """

#         if not instance:
#             return None

#         try:
#             ct = ContentType.objects.get_for_model(instance)

#             change = (
#                 ChangeRequest.objects
#                 .filter(
#                     content_type=ct,
#                     is_approved=False,
#                     object_id=instance.id
#                 )
#                 .order_by("-created_at")  # safer than .first()
#                 .first()
#             )

#             if not change or not change.pending_data:
#                 return None

#             raw_json = change.pending_data
#             cr_id = change.id
#             username = (
#                 change.requested_by.username
#                 if change.requested_by else "Unknown"
#             )

#             # ============================================================
#             # --- HANDLE LIST TYPE (TERMS / BULK DATA) ---
#             # ============================================================
#             if isinstance(raw_json, list):

#                 # Debug (optional - remove in prod)
#                 print(f"\n--- DEBUG: PENDING LIST FOR {instance} ---")
#                 print(f"CR ID: {cr_id} | Requested By: {username}")
#                 print(json.dumps(raw_json, indent=2))
#                 print("------------------------------------------\n")

#                 # Optional filtering (returns single item wrapped with metadata)
#                 if filter_key and filter_value:
#                     filtered_item = next(
#                         (
#                             item for item in raw_json
#                             if isinstance(item, dict)
#                             and str(item.get(filter_key)) == str(filter_value)
#                         ),
#                         None
#                     )

#                     if not filtered_item:
#                         return None

#                     return {
#                         "pending": filtered_item,
#                         "cr_id": cr_id,
#                         "requested_by": username
#                     }

#                 # Default: return full list with single CR metadata
#                 return {
#                     "pending": raw_json,
#                     "cr_id": cr_id,
#                     "requested_by": username
#                 }

#             # ============================================================
#             # --- HANDLE DICT TYPE (BASIC DETAILS) ---
#             # ============================================================
#             elif isinstance(raw_json, dict):

#                 # Avoid mutating original JSON (important!)
#                 data = raw_json.copy()

#                 data.update({
#                     "cr_id": cr_id,
#                     "requested_by": username
#                 })

#                 return data

#             # ============================================================
#             # --- UNKNOWN TYPE ---
#             # ============================================================
#             return None

#         except Exception as e:
#             print(f"[ERROR] get_pending_data failed: {str(e)}")
#             return None

#     def get_basicDetails(self, obj):
#         # 'obj' here is the ProjectBoard
#         # 'project_record' is the Project model instance you shared
#         project_record = obj.project 
#         pending = self.get_pending_data(obj)
#         currency_map = {
#             'INR': '₹',  # ₹
#             'USD': '$',    # $
#             'EUR': '€',  # €
#             'GBP': '£',   # £
#             'JPY': '¥',   # ¥
#         }
#         # Initialize variables with default "N/A"
#         display_name = "N/A"
#         responsible_person = "N/A"

#         if project_record:
#             # Check if it is a linked MainProject
#             if project_record.project:
#                 display_name = project_record.project.project_name
#                 responsible_person = project_record.project_manager.get_full_name() if project_record.project_manager else "N/A"
            
#             # Fallback to Department/HOD if project is not linked
#             elif project_record.department:
#                 display_name = project_record.department.name
#                 responsible_person = project_record.hod.get_full_name() if project_record.hod else "N/A"

#         return {
#             "currency_symbol": currency_map.get(obj.currency, obj.currency),  # Default to code if symbol not found
#             "projectName": display_name,
#             "projectManager": responsible_person,
#             "commodity": obj.commodity_equipment,
#             "costUnit": obj.cost_center,
#             "rfqSignOff": obj.rfq_sign_off_date.strftime('%Y-%m-%d') if obj.rfq_sign_off_date else None,
#             "documentNo": obj.document_no,
#             "buyerName": obj.buyer.get_full_name() if obj.buyer else "N/A",
#             "currency": obj.currency,
#             "projectType": project_record.get_project_type_display() if project_record else "N/A",
#             "pendingChanges": pending
#         }
 
 
#     def get_commercialRequirements(self, obj):
#         comm = obj.commercial_requirement.first()
#         if not comm:
#             return None
        
#         pending = self.get_pending_data(comm)
        
#         return {
#             "Period Of Quotation Validity": comm.quotation_validity,
#             "Energy Efficiency Requirements": comm.energy_efficiency,
#             "Risk Category / Supplier Qualification": comm.risk_category,
#             "Customer Pre-Selected": comm.customer_pre_selected,
#             "Pre-negotiated": comm.pre_negotiated,
#             "According Customer Preferred List": comm.customer_preferred_list,
#             "Restrictions Functional Department": comm.functional_restrictions or "None",
#             "pendingChanges": pending
#         }

#     def get_suppliers(self, obj):
#         suppliers_data = []
#         for s in obj.suppliers.all():
#             # Check if specific supplier details are being changed
#             pending = self.get_pending_data(s)
            
#             suppliers_data.append({
#                 "id": s.id,
#                 "supplierName": s.supplier_name,
#                 "beforeRiskCategory": s.risk_category_before,
#                 "afterRiskCategory": s.risk_category_after,
#                 "auditDetails": {
#                     "addedBy": s.created_by.get_full_name() if s.created_by else "N/A",
#                     "addedOn": s.created_at.strftime('%d-%m-%Y')
#                 },
#                 "pendingChanges": pending
#             })
#         return suppliers_data

#     def get_tableRows(self, obj):
#         rows = []
#         line_items = obj.line_items.all().prefetch_related('negotiations')
        
#         for item in line_items:
#             # Check if LineItem attributes (desc, qty, etc) are being changed
#             pending = self.get_pending_data(item)
            
#             supplier_cols = {}
#             for neg in item.negotiations.all():
#                 supplier_cols[str(neg.supplier_id)] = {
#                     "supplierName": neg.supplier.supplier_name,
#                     "metrics": {
#                         "unitPriceBefore": float(neg.unit_price_before or 0),
#                         "totalPriceBefore": float(neg.total_price_before or 0),                        
#                         "unitPriceAfter": float(neg.unit_price_after or 0),
#                         "totalPriceAfter": float(neg.total_price_after or 0),
#                     }
#                 }
            
#             rows.append({
#                 "pos": item.position_no,
#                 "co_no": item.co_no,
#                 "itemCd": item.item_code,
#                 "unit_no": item.unit_no,
#                 "unit": item.unit,
#                 "reference_po_no": item.reference_po_no,
#                 "desc": item.description,
#                 "qty": float(item.quantity),
#                 "budget":item.budget,
#                 "target": item.target_price,
#                 "suppliers": supplier_cols,
#                 "pendingChanges": pending
#             })
#         return rows

#     def get_customerSelection(self, obj):
#         finalized = obj.supplier_negotiations.filter(is_finalized=True).select_related('supplier', 'finalized_by').first()
#         if not finalized:
#             return None 

#         # Selection/Negotiation change requests (e.g. changing the winning supplier)
#         pending = self.get_pending_data(finalized)

#         return {
#             "selectedSupplier": finalized.supplier.supplier_name,
#             "grosstotal": finalized.gross_total,
#             "riskCategory":finalized.supplier.risk_category_after,
#             "negotiationOverall": {
#                 "netTotal": finalized.net_total,
#                 "discountPercent": f"{finalized.discount_overall_percentage}%"
#             },
#             "finalizedDetails": {
#                 "finalizedBy": finalized.finalized_by.get_full_name() if finalized.finalized_by else "N/A",
#             },
#             "pendingChanges": pending
#         }

#     def get_terms(self, obj):
#         existing_data = []
#         formatted_pending = []

#         finalized = obj.supplier_negotiations.filter(is_finalized=True).first()

#         if not finalized:
#             return {
#                 "existing": [],
#                 "pending": [],
#                 "cr_id": None,
#                 "requested_by": None,
#                 "message": "No supplier finalized yet"
#             }

#         # =========================
#         # EXISTING TERMS
#         # =========================
#         assignments = obj.term_assignments.filter(
#             supplier=finalized.supplier
#         ).select_related('term').order_by('term__name')

#         term_map = {t.term_id: t.term.name for t in assignments}

#         def get_row_details(rows):
#             result = []
#             for r in rows:
#                 result.append({
#                     "text_detail": r.text_detail or "",
#                     "percentage": float(r.percentage) if r.percentage else None,
#                     "date": r.date.strftime('%Y-%m-%d') if r.date else None,
#                     "comments": r.comments or "",
#                     "justification": r.justification or ""
#                 })
#             return result

#         term_ids = sorted(set(assignments.values_list('term__id', flat=True)))

#         for t_id in term_ids:
#             expected_rows = assignments.filter(term__id=t_id, status_type='Expected')
#             agreed_rows = assignments.filter(term__id=t_id, status_type='Agreed')

#             existing_data.append({
#                 "term": term_map.get(t_id, f"Term {t_id}"),
#                 "expected": get_row_details(expected_rows),
#                 "agreed": get_row_details(agreed_rows)
#             })

#         # =========================
#         # PENDING TERMS (FIXED)
#         # =========================
#         # IMPORTANT: fetch CR using ONE assignment (since all share same CR)
#         first_assignment = assignments.first()

#         pending_data = self.get_pending_data(first_assignment) if first_assignment else None

#         cr_id = None
#         requested_by = None

#         if pending_data:
#             cr_id = pending_data.get("cr_id")
#             requested_by = pending_data.get("requested_by")

#             raw_pending = pending_data.get("pending", [])

#             # Normalize (handle nested list)
#             if isinstance(raw_pending, list) and len(raw_pending) > 0 and isinstance(raw_pending[0], list):
#                 raw_pending = raw_pending[0]

#             pending_term_ids = sorted(set(
#                 item.get("term") for item in raw_pending if item.get("term")
#             ))

#             for t_id in pending_term_ids:
#                 p_exps = [
#                     i for i in raw_pending
#                     if i.get("term") == t_id and i.get("status_type") == "Expected"
#                 ]
#                 p_agrs = [
#                     i for i in raw_pending
#                     if i.get("term") == t_id and i.get("status_type") == "Agreed"
#                 ]

#                 def format_pending(rows):
#                     result = []
#                     for r in rows:
#                         result.append({
#                             "text_detail": r.get("text_detail") or "",
#                             "percentage": r.get("percentage"),
#                             "date": r.get("date"),
#                             "comments": r.get("comments") or "",
#                             "justification": r.get("justification") or ""
#                         })
#                     return result

#                 formatted_pending.append({
#                     "term": term_map.get(t_id, f"Term {t_id}"),
#                     "expected": format_pending(p_exps),
#                     "agreed": format_pending(p_agrs)
#                 })

#         return {
#             "existing": existing_data,
#             "pending": formatted_pending,
#             "cr_id": cr_id,
#             "requested_by": requested_by
#         }
    


#     def get_approvers(self, obj):
#         from django.contrib.contenttypes.models import ContentType
        
#         approver_data = []
#         # Fetch all actions for this PB
#         approval_actions = ApprovalRejection.objects.filter(pb_id=obj).select_related('created_by')

#         for app in obj.approvers.all().order_by('level'):
#             # 1. Look at ALL actions by this specific user for this PB
#             user_actions = approval_actions.filter(created_by=app.approver)

#             if user_actions.exists():
#                 # 2. Priority Logic: If they REJECTED any section, the status is REJECTED
#                 if user_actions.filter(status=ApprovalStatus.REJECTED).exists():
#                     action_record = user_actions.filter(status=ApprovalStatus.REJECTED).first()
#                     current_status = "REJECTED"
#                 # 3. If they APPROVED everything they touched, it's APPROVED
#                 elif not user_actions.filter(status=ApprovalStatus.PENDING).exists():
#                     action_record = user_actions.first()
#                     current_status = "APPROVED"
#                 else:
#                     action_record = user_actions.filter(status=ApprovalStatus.PENDING).first()
#                     current_status = "PENDING"
                
#                 user_comment = action_record.comments or ""
#                 action_date = action_record.created_at.strftime("%Y-%m-%d")
#             else:
#                 # No record found for this user
#                 has_any_pending = approval_actions.filter(status=ApprovalStatus.PENDING).exists()
#                 current_status = "ON HOLD" if has_any_pending else "PENDING"
#                 user_comment = ""
#                 action_date = None

#             approver_data.append({
#                 "level": app.level,
#                 "approver_name": app.approver.get_full_name() if app.approver else "N/A",
#                 "status": current_status,
#                 "comments": user_comment,
#                 "action_date": action_date
#             })
        
#         return approver_data



from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
import json


class PBSummarySerializer(serializers.ModelSerializer):
    basicDetails = serializers.SerializerMethodField()
    commercialRequirements = serializers.SerializerMethodField()
    suppliers = serializers.SerializerMethodField()
    tableRows = serializers.SerializerMethodField()
    customerSelection = serializers.SerializerMethodField()
    terms = serializers.SerializerMethodField()
    approvers = serializers.SerializerMethodField()

    class Meta:
        model = ProjectBoard
        fields = [
            'basicDetails', 'commercialRequirements', 'suppliers',
            'tableRows', 'customerSelection', 'terms', 'approvers'
        ]

    # ============================================================
    # COMMON PENDING FETCH (FOR SINGLE OBJECT CR)
    # ============================================================
    def get_pending_data(self, instance, filter_key=None, filter_value=None):
        if not instance:
            return None

        try:
            ct = ContentType.objects.get_for_model(instance)

            change = (
                ChangeRequest.objects
                .filter(
                    content_type=ct,
                    is_approved=False,
                    object_id=instance.id
                )
                .select_related('requested_by')
                .order_by("-created_at")
                .first()
            )

            if not change or not change.pending_data:
                return None

            raw_json = change.pending_data
            if 'buyer' in raw_json:
                b_id = raw_json.get('buyer')
                buyer_user = User.objects.filter(id=b_id).first() if b_id else None
                raw_json['buyer'] = buyer_user.get_full_name() if buyer_user else "N/A"

            # Project Resolution
            if 'project' in raw_json:
                p_id = raw_json.get('project')
                proj = Project.objects.filter(id=p_id).first() if p_id else None
                raw_json['project'] = proj.project.project_name if proj else "N/A"            
            # Use dictionary unpacking to flatten the JSON fields
            # This moves "buyer", "cost_center", etc. up one level
            return {
                **raw_json, 
                "cr_id": change.id,
                "requested_by": change.requested_by.username if change.requested_by else "Unknown"
            }

        except Exception as e:
            print(f"[ERROR] get_pending_data: {str(e)}")
            return None

    # ============================================================
    # BASIC DETAILS
    # ============================================================
    def get_basicDetails(self, obj):
        project_record = obj.project
        pending = self.get_pending_data(obj)

        currency_map = {
            'INR': '₹', 'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥'
        }

        display_name = "N/A"
        responsible_person = "N/A"

        if project_record:
            if project_record.project:
                display_name = project_record.project.project_name
                responsible_person = (
                    project_record.project_manager.get_full_name()
                    if project_record.project_manager else "N/A"
                )
            elif project_record.department:
                display_name = project_record.department.name
                responsible_person = (
                    project_record.hod.get_full_name()
                    if project_record.hod else "N/A"
                )

        return {
            "currency_symbol": currency_map.get(obj.currency, obj.currency),
            "projectName": display_name,
            "projectManager": responsible_person,
            "commodity": obj.commodity_equipment,
            "costUnit": obj.cost_center,
            "rfqSignOff": obj.rfq_sign_off_date.strftime('%Y-%m-%d') if obj.rfq_sign_off_date else None,
            "documentNo": obj.document_no,
            "buyerName": obj.buyer.get_full_name() if obj.buyer else "N/A",
            "currency": obj.currency,
            "projectType": project_record.get_project_type_display() if project_record else "N/A",
            "pendingChanges": pending
        }

    # ============================================================
    # COMMERCIAL REQUIREMENTS
    # ============================================================
    def get_commercialRequirements(self, obj):
        # 1. Get the commercial requirement record
        comm = obj.commercial_requirement.first()
        if not comm:
            return None

        # 2. Get pending changes safely
        pending = self.get_pending_data(comm)
        
        # Use an empty dict if pending is None to avoid the TypeError
        safe_pending = pending if pending is not None else {}

        if 'project_board' in safe_pending:
            b_id = safe_pending.get('project_board')
            pb = ProjectBoard.objects.filter(id=b_id).first() if b_id else None
            safe_pending['project_board'] = pb.document_no if pb else "N/A"

        # 3. Fetch multiple approval/rejection comments for this specific sub-model
        content_type = ContentType.objects.get_for_model(comm)


        return {
            "Period Of Quotation Validity": comm.quotation_validity,
            "Energy Efficiency Requirements": comm.energy_efficiency,
            "Risk Category / Supplier Qualification": comm.risk_category,
            "Customer Pre-Selected": comm.customer_pre_selected,
            "Pre-negotiated": comm.pre_negotiated,
            "According Customer Preferred List": comm.customer_preferred_list,
            "Restrictions Functional Department": comm.functional_restrictions or "None",
            "pendingChanges": pending, # Returns original None or the dict
        }

    # ============================================================
    # SUPPLIERS
    # ============================================================
    def get_suppliers(self, obj):
        data = []
        for s in obj.suppliers.all():
            pending = self.get_pending_data(s)

            data.append({
                "id": s.id,
                "supplierName": s.supplier_name,
                "beforeRiskCategory": s.risk_category_before,
                "afterRiskCategory": s.risk_category_after,
                "auditDetails": {
                    "addedBy": s.created_by.get_full_name() if s.created_by else "N/A",
                    "addedOn": s.created_at.strftime('%d-%m-%Y')
                },
                "pendingChanges": pending
            })
        return data

    # ============================================================
    # TABLE ROWS
    # ============================================================
    def get_tableRows(self, obj):
        rows = []
        items = obj.line_items.all().prefetch_related('negotiations')

        for item in items:
            pending = self.get_pending_data(item)

            supplier_cols = {}
            for neg in item.negotiations.all():
                supplier_cols[str(neg.supplier_id)] = {
                    "supplierName": neg.supplier.supplier_name,
                    "metrics": {
                        "unitPriceBefore": float(neg.unit_price_before or 0),
                        "totalPriceBefore": float(neg.total_price_before or 0),
                        "unitPriceAfter": float(neg.unit_price_after or 0),
                        "totalPriceAfter": float(neg.total_price_after or 0),
                    }
                }

            rows.append({
                "pos": item.position_no,
                "co_no": item.co_no,
                "itemCd": item.item_code,
                "unit_no": item.unit_no,
                "unit": item.unit,
                "reference_po_no": item.reference_po_no,
                "desc": item.description,
                "qty": float(item.quantity),
                "budget": item.budget,
                "target": item.target_price,
                "suppliers": supplier_cols,
                "pendingChanges": pending
            })

        return rows

    # ============================================================
    # CUSTOMER SELECTION
    # ============================================================
    def get_customerSelection(self, obj):
        finalized = obj.supplier_negotiations.filter(is_finalized=True).select_related('supplier', 'finalized_by').first()
        if not finalized:
            return None

        pending = self.get_pending_data(finalized)

        return {
            "selectedSupplier": finalized.supplier.supplier_name,
            "grosstotal": finalized.gross_total,
            "riskCategory": finalized.supplier.risk_category_after,
            "negotiationOverall": {
                "netTotal": finalized.net_total,
                "discountPercent": f"{finalized.discount_overall_percentage}%"
            },
            "finalizedDetails": {
                "finalizedBy": finalized.finalized_by.get_full_name() if finalized.finalized_by else "N/A"
            },
            "pendingChanges": pending
        }

    # ============================================================
    # TERMS (🔥 FIXED BULK CR HANDLING)
    # ============================================================
    
    def get_terms(self, obj):
        existing_data = []
        formatted_pending = []
        
        finalized = obj.supplier_negotiations.filter(is_finalized=True).first()
        if not finalized:
            return {"existing": [], "pending": [], "cr_map": {}, "requested_by_map": {}}

        assignments = obj.term_assignments.filter(
            supplier=finalized.supplier
        ).select_related('term').order_by('term__name')

        term_map = {t.term_id: t.term.name for t in assignments}

        # 1. FORMAT EXISTING DB DATA
        def format_db(rows):
            return [{
                "text_detail": r.text_detail or "",
                "percentage": float(r.percentage) if r.percentage else None,
                "date": r.date.strftime('%Y-%m-%d') if r.date else None,
                "comments": r.comments or "",
                "justification": r.justification or ""
            } for r in rows]

        db_term_ids = sorted(set(assignments.values_list('term__id', flat=True)))
        for t_id in db_term_ids:
            existing_data.append({
                "term": term_map.get(t_id),
                "expected": format_db(assignments.filter(term__id=t_id, status_type='Expected')),
                "agreed": format_db(assignments.filter(term__id=t_id, status_type='Agreed'))
            })

        # 2. FETCH PENDING CHANGE REQUESTS (BROAD SEARCH)
        assignment_ids = list(assignments.values_list("id", flat=True))
        ct = ContentType.objects.get_for_model(TermAssignment)

        # We fetch ALL pending CRs for TermAssignments. 
        # Since 'object_id' can be 0 or a specific ID, we'll filter them in Python 
        # to ensure they belong to THIS project board (ID 33 in your case).
        pending_changes = ChangeRequest.objects.filter(
            content_type=ct,
            is_approved=False
        ).select_related('requested_by').order_by("-created_at")

        cr_map = {"Expected": None, "Agreed": None}
        requested_by_map = {"Expected": None, "Agreed": None}
        all_pending_raw = []

        # 3. FILTER AND MERGE
        for change in pending_changes:
            raw = change.pending_data
            data_to_process = []
            
            # Normalize structure (handles [[...]] or [...])
            if isinstance(raw, list):
                data_to_process = raw[0] if len(raw) > 0 and isinstance(raw[0], list) else raw
            elif isinstance(raw, dict):
                data_to_process = [raw]

            # SECURITY: Only include data belonging to THIS Project Board
            # This is crucial if object_id is 0 or a different term's ID
            valid_for_this_pb = [
                item for item in data_to_process 
                if item.get('project_board') == obj.id
            ]

            if valid_for_this_pb:
                for item in valid_for_this_pb:
                    status = item.get("status_type")
                    if status in cr_map and cr_map[status] is None:
                        cr_map[status] = change.id
                        requested_by_map[status] = change.requested_by.username if change.requested_by else "Unknown"
                
                all_pending_raw.extend(valid_for_this_pb)

        # 4. FORMAT PENDING DATA
        if all_pending_raw:
            # Fix: set() operations require both sides to be sets
            pending_term_ids_set = set(i.get("term") for i in all_pending_raw if i.get("term"))
            missing_ids = pending_term_ids_set - set(term_map.keys())

            if missing_ids:
                from purchase.models import Term
                missing_names = Term.objects.filter(id__in=missing_ids).values('id', 'name')
                for m in missing_names:
                    term_map[m['id']] = m['name']

            sorted_ids = sorted(list(pending_term_ids_set))
            for t_id in sorted_ids:
                formatted_pending.append({
                    "term": term_map.get(t_id, f"Term {t_id}"),
                    "expected": [
                        {
                            "text_detail": i.get("text_detail") or "",
                            "percentage": i.get("percentage"),
                            "date": i.get("date"),
                            "comments": i.get("comments") or "",
                            "justification": i.get("justification") or ""
                        } for i in all_pending_raw if i.get("term") == t_id and i.get("status_type") == "Expected"
                    ],
                    "agreed": [
                        {
                            "text_detail": i.get("text_detail") or "",
                            "percentage": i.get("percentage"),
                            "date": i.get("date"),
                            "comments": i.get("comments") or "",
                            "justification": i.get("justification") or ""
                        } for i in all_pending_raw if i.get("term") == t_id and i.get("status_type") == "Agreed"
                    ]
                })

        return {
            "existing": existing_data,
            "pending": formatted_pending,
            "cr_map": cr_map,
            "requested_by_map": requested_by_map
        }
    # ============================================================
    # APPROVERS (UNCHANGED)
    # ============================================================
    def get_approvers(self, obj):
        approver_data = []
        approval_actions = ApprovalRejection.objects.filter(pb_id=obj).select_related('created_by')

        for app in obj.approvers.all().order_by('level'):
            user_actions = approval_actions.filter(created_by=app.approver)

            if user_actions.exists():
                if user_actions.filter(status=ApprovalStatus.REJECTED).exists():
                    action_record = user_actions.filter(status=ApprovalStatus.REJECTED).first()
                    status = "REJECTED"
                elif not user_actions.filter(status=ApprovalStatus.PENDING).exists():
                    action_record = user_actions.first()
                    status = "APPROVED"
                else:
                    action_record = user_actions.filter(status=ApprovalStatus.PENDING).first()
                    status = "PENDING"

                comment = action_record.comments or ""
                action_date = action_record.created_at.strftime("%Y-%m-%d")
            else:
                status = "PENDING"
                comment = ""
                action_date = None

            approver_data.append({
                "level": app.level,
                "approver_name": app.approver.get_full_name() if app.approver else "N/A",
                "status": status,
                "comments": comment,
                "action_date": action_date
            })

        return approver_data

