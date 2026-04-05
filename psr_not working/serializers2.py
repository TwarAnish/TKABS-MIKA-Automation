# core/serializers.py
from decimal import Decimal
from datetime import timezone
from rest_framework import serializers
from psr.models import *
from django.contrib.auth import get_user_model



class PSRProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PSRProject
        fields = [
            "id",
            "co_no",
            "project_name",
        ]



class PODataImportSerializer(serializers.Serializer):
    file = serializers.FileField()
    dry_run = serializers.BooleanField(required=False, default=False)


class TimesheetImportSerializer(serializers.Serializer):
    file = serializers.FileField()
    dry_run = serializers.BooleanField(required=False, default=False)




class PSRSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = PSRSnapshot
        fields = [
            'snapshot_date',
            'frequency',
            'data',
            'total_actual_cost',
            'total_forecast_cost',
            'total_prognosis_cost',
            'total_budget_cost',
            'overall_balance',
            'overall_balance_percentage',
            'generated_at',
        ]


User = get_user_model()

class SubDepartmentBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PSRSubDepartment
        fields = ['id', 'budget_hours']

    def update(self, instance, validated_data):
        instance.budget_hours = validated_data.get('budget_hours', instance.budget_hours)
        
        # Auto-calculate budget_cost
        dept = instance.department
        project = dept.project
        # instance.budget_cost = instance.budget_hours * dept.hourly_rate * project.exchange_rate
        instance.budget_cost = instance.budget_hours * dept.hourly_rate
        
        # If forecast is not overridden, keep it auto (we'll recalc in snapshot)
        instance.save()
        return instance


class SubDepartmentForecastOverrideSerializer(serializers.ModelSerializer):
    class Meta:
        model = PSRSubDepartment
        fields = ['id', 'forecast_hours', 'forecast_override']

    def validate(self, data):
        if not data.get('forecast_override', False):
            raise serializers.ValidationError("forecast_override must be True when using this endpoint")
        if 'forecast_hours' not in data:
            raise serializers.ValidationError("forecast_hours is required when overriding")
        return data

    def update(self, instance, validated_data):
        user = self.context['request'].user
        
        instance.forecast_override = validated_data.get('forecast_override', instance.forecast_override)
        instance.forecast_hours = validated_data.get('forecast_hours', instance.forecast_hours)
        
        # Auto-calculate forecast_cost from hours
        dept = instance.department
        project = dept.project
        # instance.forecast_cost = instance.forecast_hours * dept.hourly_rate * project.exchange_rate
        instance.forecast_cost = instance.forecast_hours * dept.hourly_rate
        
        # Audit
        instance.forecast_overridden_by = user
        instance.forecast_overridden_at = timezone.now()
        
        instance.save()
        return instance



from decimal import Decimal
from rest_framework import serializers
from .models import PSRProject
from accounts.models import CustomUser   # adjust import if needed


class ProjectCreateSerializer(serializers.ModelSerializer):
    project_manager = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = PSRProject
        fields = [
            # === INPUT FIELDS (user can edit) ===
            'co_no',
            'project_name',
            'location',
            'project_manager',
            'project_manager_email',
            'sales_person',
            'sales_person_email',
            'settlement_period',
            'sales_value_foreign_curr',
            'direct_margin_percentage',      # ← NEW input
            'sgna_percentage',
            'eff_percentage',
            'ter_percentage',
            'risk',
            'currency',
            'exchange_rate',

            # === CALCULATED / DERIVED FIELDS (returned after creation) ===
            'sales_value',
            'ebit_percentage',      # now calculated
            'ebit_value',
            'sgna_value',
            'cost_with_sgna',
            'hk',
            'hk2',
            'sk_value',
            'direct_margin_value',
            'ter_value',
            'eff_value',
            'actual_budget',
            'budget',
        ]

        read_only_fields = [
            'sales_value',          # always overwritten in save()
            'ebit_percentage',
            'ebit_value',
            'sgna_value',
            'cost_with_sgna',
            'hk',
            'hk2',
            'sk_value',
            'direct_margin_value',
            'ter_value',
            'eff_value',
            'actual_budget',
            'budget',
        ]

    def validate_co_no(self, value):
        if PSRProject.objects.filter(co_no=value).exists():
            raise serializers.ValidationError(
                "A project with this CO number already exists."
            )
        return value






class ProjectBasicSerializer(serializers.ModelSerializer):
    project_manager = serializers.SerializerMethodField()

    class Meta:
        model = PSRProject
        fields = [
            'co_no',
            'project_name',
            'project_manager',  # now returns full name
            'cw_no',
            'current_phase',
            'settlement_period',
        ]

    def get_project_manager(self, obj):
        if obj.project_manager:
            return f"{obj.project_manager.first_name} {obj.project_manager.last_name}"
        return None


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PSRProject
        fields = ['cw_no', 'current_phase', 'settlement_period']

class PSRSnapshotKPISerializer(serializers.ModelSerializer):

    class Meta:
        model = PSRSnapshot
        fields = [
            'sales_value',
            'total_budget_cost',
            'ter_value',
            'eff_value',
            'risk_value',
            'total_actual_cost',
            'total_forecast_cost',
            'total_prognosis_cost',
            'sum_prognosis',
            'margin',
            'factor',
            'ebit_value',
            'ebit_percentage',
            'net_marginal_income',
            'net_marginal_income_percentage',
        ]


class ProjectLatestSnapshotSerializer(serializers.Serializer):
    project_id = serializers.IntegerField(source='id')
    co_no = serializers.CharField()
    project_name = serializers.CharField()
    sales_value = serializers.DecimalField(max_digits=15, decimal_places=2)

    total_budget_cost = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)
    ter_value = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)
    eff_value = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_actual_cost = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_forecast_cost = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_prognosis_cost = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)
    margin = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)
    factor = serializers.DecimalField(max_digits=8, decimal_places=4, default=0.0)
    ebit_value = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)
    ebit_percentage = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_marginal_income = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_marginal_income_percentage = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)

class MonthlyCumulativeKPISerializer(serializers.Serializer):
    month = serializers.CharField()
    sales_value = serializers.DecimalField(max_digits=18, decimal_places=2)
    total_budget_cost = serializers.DecimalField(max_digits=18, decimal_places=2)
    ter_value = serializers.DecimalField(max_digits=18, decimal_places=2)
    eff_value = serializers.DecimalField(max_digits=18, decimal_places=2)
    total_actual_cost = serializers.DecimalField(max_digits=18, decimal_places=2)
    total_forecast_cost = serializers.DecimalField(max_digits=18, decimal_places=2)
    total_prognosis_cost = serializers.DecimalField(max_digits=18, decimal_places=2)
    margin = serializers.DecimalField(max_digits=18, decimal_places=2)
    factor = serializers.DecimalField(max_digits=8, decimal_places=4)
    ebit_value = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)
    ebit_percentage = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_marginal_income = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_marginal_income_percentage = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)



class RKActualLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = RKActualAdjustmentLine
        fields = ['id', 'description', 'amount']

class RKActualAdjustmentSerializer(serializers.ModelSerializer):
    lines = RKActualLineSerializer(many=True)

    class Meta:
        model = RKActualAdjustment
        fields = ['id', 'note', 'adjusted_at', 'adjusted_by', 'lines']

    def create(self, validated_data):
        lines_data = validated_data.pop('lines')
        adjustment = RKActualAdjustment.objects.create(**validated_data)
        for line_data in lines_data:
            RKActualAdjustmentLine.objects.create(adjustment=adjustment, **line_data)
        return adjustment




class AssemblyActualAdjustmentLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssemblyActualAdjustmentLine
        fields = ['description', 'amount']

class AssemblyActualAdjustmentSerializer(serializers.ModelSerializer):
    lines = AssemblyActualAdjustmentLineSerializer(many=True, read_only=True)
    
    class Meta:
        model = AssemblyActualAdjustment
        fields = ['id', 'note', 'adjusted_by', 'adjusted_at', 'lines']

class FVActualAdjustmentLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = FVActualAdjustmentLine
        fields = ['description', 'amount']

class FVActualAdjustmentSerializer(serializers.ModelSerializer):
    lines = FVActualAdjustmentLineSerializer(many=True, read_only=True)
    
    class Meta:
        model = FVActualAdjustment
        fields = ['id', 'note', 'adjusted_by', 'adjusted_at', 'lines']






class SOKOActualAdjustmentLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SOKOActualAdjustmentLine
        fields = ['description', 'amount']

class SOKOActualAdjustmentSerializer(serializers.ModelSerializer):
    lines = SOKOActualAdjustmentLineSerializer(many=True, read_only=True)
    
    class Meta:
        model = FVActualAdjustment
        fields = ['id', 'note', 'adjusted_by', 'adjusted_at', 'lines']



# ------------------------------------------ BUDGET


from rest_framework import serializers
from .models import PSRBudgetChangeRequest, PSRApprovalAction
from accounts.models import CustomUser  # adjust import

class PSRApprovalActionSerializer(serializers.ModelSerializer):
    approver_username = serializers.CharField(source='approver.username', read_only=True)
    
    class Meta:
        model = PSRApprovalAction
        fields = ['id', 'approver_username', 'stage', 'action', 'comment', 'timestamp']
        read_only_fields = ['id', 'approver_username', 'timestamp']


class PSRBudgetChangeRequestSerializer(serializers.ModelSerializer):
    approval_actions = PSRApprovalActionSerializer(many=True, read_only=True)
    target_name = serializers.SerializerMethodField()
    current_value = serializers.SerializerMethodField()
    approval_progress = serializers.SerializerMethodField()

    class Meta:
        model = PSRBudgetChangeRequest
        fields = [
            'id', 'submitter', 'note', 'status', 'created_at', 'updated_at',
            'sub_department', 'project_cost_category',
            'proposed_budget_hours', 'proposed_budget_cost',
            'target_name', 'current_value', 'approval_progress',
            'approval_actions'
        ]
        read_only_fields = ['id', 'submitter', 'status', 'created_at', 'updated_at', 'approval_actions']

    def get_target_name(self, obj):
        if obj.sub_department:
            return str(obj.sub_department)
        return str(obj.project_cost_category)

    def get_current_value(self, obj):
        if obj.sub_department:
            return float(obj.sub_department.budget_hours) if obj.sub_department.budget_hours else None
        return float(obj.project_cost_category.budget_cost) if obj.project_cost_category.budget_cost else None

    def get_approval_progress(self, obj):
        if obj.status == 'PENDING_APPROVERS':
            approvals = obj.approval_actions.filter(stage='APPROVER', action='APPROVE').count()
            required = 2 if obj.submitter.role != 'approver' else 1  # rough heuristic
            return f"{approvals}/{required} Approvers approved"
        if obj.status == 'PENDING_ADMIN':
            return "Waiting for Admin approval"
        return obj.get_status_display()


class PSRBudgetChangeRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PSRBudgetChangeRequest
        fields = [
            'sub_department', 'project_cost_category',
            'proposed_budget_hours', 'proposed_budget_cost',
            'note'
        ]

    def validate(self, data):
        if bool(data.get('sub_department')) == bool(data.get('project_cost_category')):
            raise serializers.ValidationError(
                "Exactly one of 'sub_department' or 'project_cost_category' must be provided."
            )
        if data.get('sub_department') and not data.get('proposed_budget_hours'):
            raise serializers.ValidationError("'proposed_budget_hours' is required for sub-department changes.")
        if data.get('project_cost_category') and not data.get('proposed_budget_cost'):
            raise serializers.ValidationError("'proposed_budget_cost' is required for cost category changes.")
        return data





# # psr/serializers.py

# from rest_framework import serializers
# from decimal import Decimal

# from .models import (
#     PSRForecastChangeRequest,
#     PSRForecastApprovalAction,
#     ForecastRequestLine,
# )


# class ForecastRequestLineSerializer(serializers.ModelSerializer):
#     """
#     Serializer for individual forecast override lines (description + hours or amount)
#     """
#     class Meta:
#         model = ForecastRequestLine
#         fields = ['id', 'description', 'hours', 'amount']
#         read_only_fields = ['id']


# class PSRForecastApprovalActionSerializer(serializers.ModelSerializer):
#     """
#     Serializer for individual approval/rejection actions
#     """
#     approver_username = serializers.CharField(source='approver.username', read_only=True)
#     approver_full_name = serializers.SerializerMethodField()

#     class Meta:
#         model = PSRForecastApprovalAction
#         fields = [
#             'id',
#             'approver_username',
#             'approver_full_name',
#             'stage',
#             'action',
#             'comment',
#             'timestamp'
#         ]
#         read_only_fields = ['id', 'approver_username', 'approver_full_name', 'timestamp']

#     def get_approver_full_name(self, obj):
#         return f"{obj.approver.first_name} {obj.approver.last_name}".strip() or obj.approver.username


# class PSRForecastChangeRequestSerializer(serializers.ModelSerializer):
#     """
#     Main serializer for viewing forecast change requests:
#     - Used in list (my-pending, my-submitted), detail, and after actions
#     """
#     approval_actions = PSRForecastApprovalActionSerializer(many=True, read_only=True)
#     lines = ForecastRequestLineSerializer(many=True, read_only=True)
#     target_name = serializers.SerializerMethodField()
#     current_forecast_value = serializers.SerializerMethodField()
#     proposed_value = serializers.SerializerMethodField()
#     approval_progress = serializers.SerializerMethodField()

#     class Meta:
#         model = PSRForecastChangeRequest
#         fields = [
#             'id',
#             'submitter',
#             'note',
#             'status',
#             'created_at',
#             'updated_at',
#             'sub_department',
#             'project_cost_category',
#             'proposed_forecast_hours',
#             'proposed_forecast_cost',
#             'target_name',
#             'current_forecast_value',
#             'proposed_value',
#             'approval_progress',
#             'lines',
#             'approval_actions'
#         ]
#         read_only_fields = [
#             'id', 'submitter', 'status', 'created_at', 'updated_at',
#             'target_name', 'current_forecast_value', 'proposed_value',
#             'approval_progress', 'lines', 'approval_actions'
#         ]

#     def get_target_name(self, obj):
#         return str(obj.target)

#     def get_current_forecast_value(self, obj):
#         """Current forecast value before any override"""
#         if obj.sub_department:
#             return float(obj.sub_department.forecast_hours) if obj.sub_department.forecast_hours else None
#         return float(obj.project_cost_category.forecast_cost) if obj.project_cost_category.forecast_cost else None

#     def get_proposed_value(self, obj):
#         """The value being proposed (for display consistency)"""
#         if obj.proposed_forecast_hours is not None:
#             return float(obj.proposed_forecast_hours)
#         if obj.proposed_forecast_cost is not None:
#             return float(obj.proposed_forecast_cost)
#         return None

#     def get_approval_progress(self, obj):
#         if obj.status == 'PENDING_APPROVERS':
#             approvals = obj.approval_actions.filter(stage='APPROVER', action='APPROVE').count()
#             # Adjust required logic as per your business rule
#             required = 2 if obj.submitter.role != 'approver' else 1
#             return f"{approvals}/{required} Approvers approved"
#         if obj.status == 'PENDING_ADMIN':
#             return "Awaiting Admin final approval"
#         if obj.status == 'APPROVED':
#             return "Approved and applied"
#         if obj.status == 'REJECTED':
#             return "Rejected"
#         return obj.get_status_display()


# class PSRForecastChangeRequestCreateSerializer(serializers.ModelSerializer):
#     """
#     Updated: Calculates proposed_forecast_hours / proposed_forecast_cost automatically from lines.
#     No longer requires these fields in the payload.
#     """
#     lines = serializers.ListField(
#         child=serializers.DictField(),
#         min_length=1,
#         required=True,
#         write_only=True
#     )

#     class Meta:
#         model = PSRForecastChangeRequest
#         fields = [
#             'sub_department',
#             'project_cost_category',
#             'note',
#             'lines'
#             # Removed: 'proposed_forecast_hours', 'proposed_forecast_cost'
#         ]

#     def validate(self, data):
#         # 1. Exactly one target (still required)
#         has_sub_dept = bool(data.get('sub_department'))
#         has_cost_cat = bool(data.get('project_cost_category'))
#         if has_sub_dept == has_cost_cat:
#             raise serializers.ValidationError(
#                 "Exactly one of 'sub_department' or 'project_cost_category' must be provided."
#             )

#         # 2. Validate lines & calculate total
#         lines = data.get('lines', [])
#         total_calculated = Decimal('0')

#         for idx, line in enumerate(lines):
#             if not isinstance(line, dict):
#                 raise serializers.ValidationError(f"Line {idx+1} must be an object.")

#             if 'description' not in line or not line['description'].strip():
#                 raise serializers.ValidationError(f"Line {idx+1}: 'description' is required and cannot be empty.")

#             if has_sub_dept:
#                 if 'hours' not in line:
#                     raise serializers.ValidationError(f"Line {idx+1}: 'hours' is required for sub-department overrides.")
#                 try:
#                     hours = Decimal(str(line['hours']))
#                     if hours < 0:
#                         raise ValueError
#                     total_calculated += hours
#                 except:
#                     raise serializers.ValidationError(f"Line {idx+1}: 'hours' must be a valid positive number.")
#                 line['amount'] = None  # cleanup
#             else:  # cost category
#                 if 'amount' not in line:
#                     raise serializers.ValidationError(f"Line {idx+1}: 'amount' is required for cost category overrides.")
#                 try:
#                     amount = Decimal(str(line['amount']))
#                     if amount < 0:
#                         raise ValueError
#                     total_calculated += amount
#                 except:
#                     raise serializers.ValidationError(f"Line {idx+1}: 'amount' must be a valid positive number.")
#                 line['hours'] = None  # cleanup

#         # 3. Store calculated total in data (to be used in create)
#         if has_sub_dept:
#             data['proposed_forecast_hours'] = total_calculated
#             data['proposed_forecast_cost'] = None
#         else:
#             data['proposed_forecast_cost'] = total_calculated
#             data['proposed_forecast_hours'] = None

#         return data

#     def create(self, validated_data):
#         # Lines are already cleaned in validate()
#         lines_data = validated_data.pop('lines')

#         # Create the request with calculated proposed value
#         request_obj = PSRForecastChangeRequest.objects.create(**validated_data)

#         # Create line items
#         for line_data in lines_data:
#             ForecastRequestLine.objects.create(
#                 request=request_obj,
#                 description=line_data['description'],
#                 hours=line_data.get('hours'),
#                 amount=line_data.get('amount')
#             )

#         return request_obj






from rest_framework import serializers
from accounts.models import CustomUser

class UserDropdownSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'name']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()



class ProjectPaymentSerializer(serializers.ModelSerializer):
    days_invoice_to_receive = serializers.SerializerMethodField()
    days_expected_to_receive = serializers.SerializerMethodField()
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = ProjectPayment
        fields = (
            'id',
            'invoice_no',
            'invoice_date',
            'expected_receive_date',
            'actual_receive_date',
            'percentage',
            'amount_in_foreign_curr',
            'received_amount',
            'notes',
            'days_invoice_to_receive',
            'days_expected_to_receive',
            'project',
            'project_name',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'days_invoice_to_receive',
            'days_expected_to_receive',
            'created_at',
            'updated_at',
            'project',
            'project_name',
        )

    def get_days_invoice_to_receive(self, obj):
        return obj.days_invoice_to_receive

    def get_days_expected_to_receive(self, obj):
        return obj.days_expected_to_receive