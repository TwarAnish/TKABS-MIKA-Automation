# capacity_planning/serializers.py
from rest_framework import serializers
from django.db.models import Sum
from .models import *
from collections import defaultdict

import random
import string
from django.db import transaction
from accounts.models import CustomUser,Department
from psr.models import PSRProject
class DepartmentSerializer(serializers.ModelSerializer):
    full_path = serializers.SerializerMethodField()
    children_count = serializers.SerializerMethodField()
    level = serializers.IntegerField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Department
        fields = ['id', 'name', 'icon_text', 'parent', 'order', 'level', 'full_path', 'children_count']

    def get_full_path(self, obj):
        return obj.get_full_path()

    def get_children_count(self, obj):
        return obj.children.count()


class DepartmentTreeSerializer(DepartmentSerializer):
    children = serializers.SerializerMethodField()

    class Meta(DepartmentSerializer.Meta):
        fields = DepartmentSerializer.Meta.fields + ['children']

    def get_children(self, obj):
        children = obj.children.all().order_by('order', 'name')
        return DepartmentTreeSerializer(children, many=True, context=self.context).data


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_email', 'budgeted_hours', 'hourly_rate', 'notes', 'is_active']
        read_only_fields = ['created_at', 'updated_at']


class ResourceDetailSerializer(serializers.ModelSerializer):
    department_full_path = serializers.CharField(
        source='department.get_full_path', read_only=True, allow_null=True
    )
    supplier_name = serializers.CharField(
        source='supplier.name', read_only=True, allow_null=True
    )
    role_name = serializers.CharField(source='get_role_display', read_only=True)
    # Add department_name field
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    # CORRECTED: Mark effective_availability_per_week as read_only in ResourceDetailSerializer too
    effective_availability_per_week = serializers.IntegerField(
        read_only=True # Changed from allowing write to read_only
    )

    class Meta:
        model = Resource
        fields = [
            'id', 'name', 'role', 'role_name',
            'is_internal', 'supplier', 'supplier_name',
            'hourly_rate', 'availability_per_week',
            'effective_availability_per_week', # Include the read-only calculated field
            'is_active', 'department_name', 'department_full_path', # Include department_name, exclude department ID
            'joining_date' # Add joining_date field (must exist in model)
        ]
        read_only_fields = [
            'id', 'role_name', 'department_full_path', 'supplier_name', 'department_name',
            'effective_availability_per_week' # Add this line to explicitly mark it as read-only
        ]



class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    Safe version - no duration_weeks on Project, uses first allocation instead
    """
    # Safe department info from allocation
    department_name = serializers.SerializerMethodField(read_only=True)
    department_full_path = serializers.SerializerMethodField(read_only=True)

    status_display = serializers.CharField(source='get_status_display', read_only=True)
    total_allocated_hours = serializers.SerializerMethodField()
    total_planned_hours = serializers.SerializerMethodField()
    total_external_hours = serializers.SerializerMethodField()

    # Removed: duration_weeks (because Project no longer has it)
    # If needed → add department-specific duration below

    class Meta:
        model = Project
        fields = [
            'id', 'project_code', 'name', 'status', 'status_display',
            'total_manhours', 'allotted_weeks', 'start_monday', 'end_monday',
            'department_name', 'department_full_path',
            'total_allocated_hours', 'total_planned_hours', 'total_external_hours',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'created_at', 'updated_at', 'status_display',
            'total_allocated_hours', 'total_planned_hours', 'total_external_hours',
            'department_name', 'department_full_path'
        ]

    def get_department_name(self, obj):
        first = obj.department_allocations.first()
        return first.department.name if first else None

    def get_department_full_path(self, obj):
        first = obj.department_allocations.first()
        return first.department.get_full_path() if first else None

    def get_total_allocated_hours(self, obj):
        return obj.resourceallocation_set.aggregate(total=Sum('hours'))['total'] or 0

    def get_total_planned_hours(self, obj):
        return obj.planned_weeks.aggregate(total=Sum('manhours'))['total'] or 0

    def get_total_external_hours(self, obj):
        return obj.external_capacities.aggregate(total=Sum('hours'))['total'] or 0


class ProjectWeekAllocationSerializer(serializers.ModelSerializer):
    """
    Main serializer for ProjectWeekAllocation
    Uses ProjectDetailSerializer (now safe)
    """
    project = ProjectDetailSerializer(read_only=True)
    project_code = serializers.CharField(source='project.project_code', read_only=True)

    # Optional: department-specific duration (recommended)
    duration_weeks = serializers.SerializerMethodField(read_only=True, allow_null=True)
    internal_consumed = serializers.SerializerMethodField(read_only=True)
    external_consumed = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ProjectWeekAllocation
        fields = [
            'id', 'project', 'project_code', 'department',
            'week_monday', 'manhours', 'notes',
            'duration_weeks', 'internal_consumed',  'external_consumed'# safe, optional
        ]
        read_only_fields = ['id', 'project', 'project_code', 'duration_weeks','internal_consumed', 'external_consumed']

    def get_duration_weeks(self, obj):
        """Get duration from the matching department allocation"""
        if not obj.department:
            return None

        alloc = ProjectDepartmentAllocation.objects.filter(
            project=obj.project,
            department=obj.department
        ).first()

        if alloc:
            if alloc.end_monday:
                days = (alloc.end_monday - alloc.start_monday).days
                return (days // 7) + 1
            return alloc.allotted_weeks

        return None
    
    def get_internal_consumed(self, obj):
        return ResourceAllocation.objects.filter(
            project=obj.project,
            department=obj.department,
            week_monday=obj.week_monday
        ).aggregate(total=Sum('hours'))['total'] or 0

    def get_external_consumed(self, obj):
        return ExternalCapacity.objects.filter(
            project=obj.project,
            dept=obj.department, # Fixed keyword here
            week_monday=obj.week_monday
        ).aggregate(total=Sum('hours'))['total'] or 0
    
    def validate(self, data):
        project = data.get('project')
        week_monday = data.get('week_monday')
        manhours = data.get('manhours', 0)
        department = data.get('department')

        if not project:
            raise serializers.ValidationError({"project": "Required"})

        # Strongly recommend requiring department now
        if not department:
            raise serializers.ValidationError({"department": "Required for planned allocation"})

        # Duplicate check (department-aware)
        if self.instance is None:
            if ProjectWeekAllocation.objects.filter(
                project=project, department=department, week_monday=week_monday
            ).exists():
                raise serializers.ValidationError(
                    f"Allocation already exists for {project.project_code} "
                    f"in {department.name} on {week_monday}"
                )

        # Capacity check - department-specific preferred
        if manhours > 0:
            try:
                alloc = ProjectDepartmentAllocation.objects.get(
                    project=project, department=department
                )
                current = ProjectWeekAllocation.objects.filter(
                    project=project, department=department
                ).exclude(pk=self.instance.pk if self.instance else None
                ).aggregate(total=Sum('manhours'))['total'] or 0

                if current + manhours > alloc.estimated_manhours:
                    raise serializers.ValidationError(
                        f"Planned {current + manhours} manhours exceed "
                        f"department estimate {alloc.estimated_manhours}"
                    )
            except ProjectDepartmentAllocation.DoesNotExist:
                raise serializers.ValidationError(
                    f"No allocation found for project {project.project_code} "
                    f"in department {department.name}"
                )

        return data



    
import random
import string
from django.db import transaction
from rest_framework import serializers

class ResourceSerializer(serializers.ModelSerializer):
    # -------------------------------
    # READ-ONLY DERIVED FIELDS
    # -------------------------------
    department_full_path = serializers.CharField(
        source='departments.first.get_full_path',
        read_only=True,
        allow_null=True
    )

    department_name = serializers.CharField(
        source='departments.first.name',
        read_only=True,
        allow_null=True
    )

    supplier_name = serializers.CharField(
        source='supplier.name',
        read_only=True,
        allow_null=True
    )

    role_name = serializers.CharField(
        source='get_role_display',
        read_only=True
    )

    idle_weeks_count = serializers.SerializerMethodField()
    effective_availability_per_week = serializers.IntegerField(read_only=True)
    projects = serializers.SerializerMethodField()
    allocated_weeks_count = serializers.SerializerMethodField()

    # -------------------------------
    # WRITE-ONLY INPUT FIELD
    # -------------------------------
    department_name_input = serializers.CharField(
        write_only=True,
        required=False,
        help_text="Exact department name to assign (replaces existing department)"
    )

    empId = serializers.CharField(
        source='emp_id',
        max_length=50,
        allow_null=True,
        required=False
    )

    class Meta:
        model = Resource
        fields = [
            'id', 'name', 'empId', 'emp_id', 'role', 'role_name',
            'is_internal', 'supplier', 'supplier_name', 'hourly_rate',
            'availability_per_week', 'effective_availability_per_week',
            'is_active', 'department_name', 'department_full_path',
            'joining_date', 'projects', 'allocated_weeks_count',
            'idle_weeks_count', 'department_name_input',
        ]
        read_only_fields = [
            'id', 'role_name', 'supplier_name', 'department_name',
            'department_full_path', 'effective_availability_per_week',
            'projects', 'allocated_weeks_count', 'idle_weeks_count', 'emp_id'
        ]

    # -------------------------------
    # HELPERS
    # -------------------------------
    def _get_date_range(self):
        """
        Dramatically improved: Checks context for URL params first, 
        then falls back to default window.
        """
        start_param = self.context.get('start_date')
        end_param = self.context.get('end_date')

        try:
            if start_param and end_param:
                # If strings are passed (e.g., '2007-01-01'), convert to date objects
                if isinstance(start_param, str):
                    return date.fromisoformat(start_param), date.fromisoformat(end_param)
                return start_param, end_param
        except (ValueError, TypeError):
            pass

        # Default fallback: +/- 6 months from today
        today = date.today()
        return today - timedelta(days=180), today + timedelta(days=180)

    def get_allocated_weeks_count(self, obj):
        start_date, end_date = self._get_date_range()
        
        return (
            ProjectAssignment.objects
            .filter(
                resource=obj,
                week_monday__range=(start_date, end_date)
            )
            .values('week_monday')
            .distinct()
            .count()
        )

    def get_idle_weeks_count(self, obj):
        start_date, end_date = self._get_date_range()
        
        # 1. Adjust start based on joining date
        # If they joined AFTER the window started, we only count from their join date
        effective_start = max(start_date, obj.joining_date) if obj.joining_date else start_date
        
        if effective_start > end_date:
            return 0

        # 2. Generate list of all Mondays in the range [effective_start, end_date]
        days_to_monday = (7 - effective_start.weekday()) % 7
        current_monday = effective_start + timedelta(days=days_to_monday)
        
        total_possible_weeks = 0
        while current_monday <= end_date:
            total_possible_weeks += 1
            current_monday += timedelta(days=7)
        
        # 3. Subtract only the weeks allocated WITHIN THIS SPECIFIC RANGE
        allocated = self.get_allocated_weeks_count(obj)
        return max(0, total_possible_weeks - allocated)

    def get_projects(self, obj):
        # Using .all() assumes you prefetch this in the view for speed
        assignments = ProjectAssignment.objects.filter(resource=obj).select_related('project')
        unique_projects = {a.project for a in assignments}
        
        return [
            {
                'id': p.id,
                'project_code': p.project_code,
                'name': p.name,
                'status': p.get_status_display(),
                'department': (
                    p.department_allocations.first().department.get_full_path()
                    if p.department_allocations.exists() else None
                )
            } for p in unique_projects
        ]

    # -------------------------------
    # CREATE / UPDATE
    # -------------------------------
    def create(self, validated_data):
        dept_name = validated_data.pop('department_name_input', None)
        with transaction.atomic():
            resource = super().create(validated_data)
            if dept_name:
                self._set_department(resource, dept_name)
        return resource

    def update(self, instance, validated_data):
        dept_name = validated_data.pop('department_name_input', None)
        instance = super().update(instance, validated_data)
        if dept_name:
            self._set_department(instance, dept_name)
        return instance

    def _set_department(self, instance, dept_name):
        department = Department.objects.filter(name__iexact=dept_name.strip()).first()
        if not department:
            raise serializers.ValidationError({"department_name_input": f"Department '{dept_name}' not found"})
        instance.departments.set([department])


class ProjectDepartmentAllocationSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_full_path = serializers.CharField(source='department.get_full_path', read_only=True)
    project_code = serializers.CharField(source='project.project_code', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    # FIXED: Remove redundant source= argument
    duration_weeks = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProjectDepartmentAllocation
        fields = [
            'id', 'project', 'project_code', 'project_name',
            'department', 'department_name', 'department_full_path',
            'estimated_manhours', 'allotted_weeks', 'start_monday', 'end_monday',
            'duration_weeks', 'status', 'notes'
        ]
        read_only_fields = [
            'id', 'duration_weeks', 'project_code', 'project_name',
            'department_name', 'department_full_path'
        ]

class ProjectSerializer(serializers.ModelSerializer):
    department_allocations = ProjectDepartmentAllocationSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    total_allocated_hours = serializers.SerializerMethodField()
    total_planned_hours = serializers.SerializerMethodField()
    total_external_hours = serializers.SerializerMethodField()
    color = serializers.CharField(source='color_code', required=False, allow_blank=True)
    total_hours_allocated_to_depts = serializers.SerializerMethodField()    
    # NEW: Remaining hours after department allocations
    remaining_hours_to_allocate = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = [
            'id', 'project_code', 'name', 'status', 'status_display',
            'total_manhours', 'allotted_weeks', 'start_monday', 'end_monday',
            'department_allocations',
            'total_allocated_hours', 'total_planned_hours', 'total_external_hours',
            'total_hours_allocated_to_depts',  # ← Added field
            'remaining_hours_to_allocate',  # ← NEW field (added here)
            'created_at', 'updated_at', 'color'
        ]
        read_only_fields = [
            'created_at', 'updated_at', 'status_display',
            'total_allocated_hours', 'total_planned_hours', 'total_external_hours',
            'department_allocations', 'remaining_hours_to_allocate'
        ]


    def get_total_allocated_hours(self, obj):
        return obj.resourceallocation_set.aggregate(total=Sum('hours'))['total'] or 0

    def get_total_planned_hours(self, obj):
        return obj.planned_weeks.aggregate(total=Sum('manhours'))['total'] or 0

    def get_total_external_hours(self, obj):
        return obj.external_capacities.aggregate(total=Sum('hours'))['total'] or 0

    def get_total_hours_allocated_to_depts(self, obj):
        return obj.department_allocations.aggregate(
            total=Sum('estimated_manhours')
        )['total'] or 0

    # 2. Updated the remaining hours method to use the first method
    def get_remaining_hours_to_allocate(self, obj):
        if obj.total_manhours is None:
            return 0 

        # Reuse the logic from above
        allocated = self.get_total_hours_allocated_to_depts(obj)
        
        remaining = obj.total_manhours - allocated
        return max(0, remaining)

    def create(self, validated_data):
        color_code = validated_data.pop('color', None)
        if color_code:
            validated_data['color_code'] = color_code
        return super().create(validated_data)

    def update(self, instance, validated_data):
        color_code = validated_data.pop('color', None)
        if color_code:
            validated_data['color_code'] = color_code
        return super().update(instance, validated_data)

class ProjectSerializer1(serializers.ModelSerializer):
    department_allocations = ProjectDepartmentAllocationSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    total_allocated_hours = serializers.SerializerMethodField()
    total_planned_hours = serializers.SerializerMethodField()
    total_external_hours = serializers.SerializerMethodField()
    color = serializers.CharField(source='color_code', required=False, allow_blank=True)
    total_hours_allocated_to_depts = serializers.SerializerMethodField()    
    # NEW: Remaining hours after department allocations
    remaining_hours_to_allocate = serializers.SerializerMethodField()
    department_usage_summary = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = [
            'id', 'project_code', 'name', 'status', 'status_display',
            'total_manhours', 'allotted_weeks', 'start_monday', 'end_monday',
            'department_allocations',
            'total_allocated_hours', 'total_planned_hours', 'total_external_hours',
            'total_hours_allocated_to_depts',  # ← Added field
            'remaining_hours_to_allocate',  # ← NEW field (added here)
            'created_at', 'updated_at', 'color','department_usage_summary'
        ]
        read_only_fields = [
            'created_at', 'updated_at', 'status_display',
            'total_allocated_hours', 'total_planned_hours', 'total_external_hours',
            'department_allocations', 'remaining_hours_to_allocate','department_usage_summary'
        ]




    def get_department_usage_summary(self, obj):
        # 1. Get all departments
        all_departments = Department.objects.all()
        
        # 2. Map the "Allocated" (Planned) hours from ProjectDepartmentAllocation
        # We use a dict for fast lookup: {dept_id: hours}
        planned_map = {
            alloc.department_id: alloc.estimated_manhours 
            for alloc in obj.department_allocations.all()
        }

        summary = []
        for dept in all_departments:
            # Get planned hours (default to 0 if not assigned to this project)
            allocated_hrs = planned_map.get(dept.id, 0)
            
            # 3. FIX: Filter using the ManyToMany field 'departments'
            # We look for all ResourceAllocations in this project where 
            # the Resource is associated with the current department.
            used_hrs = obj.resourceallocation_set.filter(
                resource__departments=dept
            ).aggregate(total=Sum('hours'))['total'] or 0

            summary.append({
                "department_name": dept.name,
                "allocated": float(allocated_hrs),
                "used": float(used_hrs),
                "free": float(max(0, allocated_hrs - used_hrs))
            })

        return summary
    
    def get_total_allocated_hours(self, obj):
        return obj.resourceallocation_set.aggregate(total=Sum('hours'))['total'] or 0

    def get_total_planned_hours(self, obj):
        return obj.planned_weeks.aggregate(total=Sum('manhours'))['total'] or 0

    def get_total_external_hours(self, obj):
        return obj.external_capacities.aggregate(total=Sum('hours'))['total'] or 0

    def get_total_hours_allocated_to_depts(self, obj):
        return obj.department_allocations.aggregate(
            total=Sum('estimated_manhours')
        )['total'] or 0

    # 2. Updated the remaining hours method to use the first method
    def get_remaining_hours_to_allocate(self, obj):
        if obj.total_manhours is None:
            return 0 

        # Reuse the logic from above
        allocated = self.get_total_hours_allocated_to_depts(obj)
        
        remaining = obj.total_manhours - allocated
        return max(0, remaining)

    def create(self, validated_data):
        color_code = validated_data.pop('color', None)
        if color_code:
            validated_data['color_code'] = color_code
        return super().create(validated_data)

    def update(self, instance, validated_data):
        color_code = validated_data.pop('color', None)
        if color_code:
            validated_data['color_code'] = color_code
        return super().update(instance, validated_data)


class ProjectAssignmentListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        # =================================================================
        # 1. Resolve input fields (project_code_input, resource_id, etc.)
        # =================================================================
        resolved_data = []
        for idx, item in enumerate(validated_data):
            item_copy = item.copy()

            # ---- Resolve project ----
            project_code = item_copy.pop('project_code_input', None)
            if project_code:
                try:
                    project = Project.objects.get(project_code=project_code.strip())
                    item_copy['project'] = project
                except Project.DoesNotExist:
                    raise serializers.ValidationError({
                        "index": idx,
                        "error": f"Project with code '{project_code}' not found"
                    })
            elif 'project' not in item_copy:
                raise serializers.ValidationError({
                    "index": idx,
                    "error": "Project is required. Use 'project_code_input' or provide 'project' directly."
                })

            # ---- Resolve resource ----
            resource_id = item_copy.pop('resource_id', None)
            resource_name = item_copy.pop('resource_name_input', None)

            if resource_id:
                try:
                    resource = Resource.objects.get(id=resource_id)
                    item_copy['resource'] = resource
                except Resource.DoesNotExist:
                    raise serializers.ValidationError({
                        "index": idx,
                        "error": f"Resource with ID {resource_id} not found"
                    })
            elif resource_name:
                try:
                    resource = Resource.objects.get(name__iexact=resource_name.strip())
                    item_copy['resource'] = resource
                except Resource.DoesNotExist:
                    raise serializers.ValidationError({
                        "index": idx,
                        "error": f"Resource '{resource_name}' not found"
                    })
                except Resource.MultipleObjectsReturned:
                    raise serializers.ValidationError({
                        "index": idx,
                        "error": f"Multiple resources found with name '{resource_name}'. Use resource_id instead."
                    })
            elif 'resource' not in item_copy:
                raise serializers.ValidationError({
                    "index": idx,
                    "error": "Resource is required. Use 'resource_id' or 'resource_name_input'."
                })

            resolved_data.append(item_copy)

        # =================================================================
        # 2. Check for duplicates in database
        # =================================================================
        duplicates = []
        for idx, item in enumerate(resolved_data):
            if ProjectAssignment.objects.filter(
                resource=item['resource'],
                project=item['project'],
                week_monday=item['week_monday']
            ).exists():
                duplicates.append({
                    "index": idx,
                    "resource_name": item['resource'].name,
                    "project_code": item['project'].project_code,
                    "week_monday": str(item['week_monday'])
                })

        if duplicates:
            raise serializers.ValidationError({
                "error": "Some assignments already exist in database",
                "duplicates": duplicates
            })

        # =================================================================
        # 3. Check for duplicates within the current request
        # =================================================================
        seen_triplets = set()
        for index, item in enumerate(resolved_data):
            key = (item['resource'].id, item['project'].id, item['week_monday'])
            if key in seen_triplets:
                raise serializers.ValidationError(
                    f"Duplicate entry at index {index}: "
                    f"{item['resource'].name} → {item['project'].project_code} on {item['week_monday']}"
                )
            seen_triplets.add(key)

        # =================================================================
        # 4. Validate project date ranges and accumulate for capacity checks
        # =================================================================
        resource_week_totals = defaultdict(int)  # (resource_id, week_monday) → hours
        project_totals = defaultdict(int)        # project_id → hours

        for item in resolved_data:
            project = item['project']
            week_monday = item['week_monday']
            hours = item.get('hours', 0)

            # Project date range check
            if project.start_monday and week_monday < project.start_monday:
                raise serializers.ValidationError(
                    f"Cannot allocate before project start ({project.start_monday}). "
                    f"Project: {project.project_code}, Week: {week_monday}"
                )
            if project.end_monday and week_monday > project.end_monday:
                raise serializers.ValidationError(
                    f"Cannot allocate after project end ({project.end_monday}). "
                    f"Project: {project.project_code}, Week: {week_monday}"
                )

            if hours > 0:
                resource_key = (item['resource'].id, week_monday)
                resource_week_totals[resource_key] += hours
                project_totals[project.id] += hours

        # =================================================================
        # 5. Validate resource weekly availability
        # =================================================================
        for (resource_id, week_monday), total_hours in resource_week_totals.items():
            resource = Resource.objects.get(id=resource_id)
            availability = resource.effective_availability_per_week

            existing_hours = ResourceAllocation.objects.filter(
                resource=resource,
                week_monday=week_monday
            ).aggregate(total=Sum('hours'))['total'] or 0

            if existing_hours + total_hours > availability:
                raise serializers.ValidationError(
                    f"Total hours for {resource.name} in week {week_monday} "
                    f"({existing_hours + total_hours}) exceeds availability ({availability} hours)."
                )

        # =================================================================
        # 6. Validate project total manhours not exceeded
        # =================================================================
        for project_id, added_hours in project_totals.items():
            project = Project.objects.get(id=project_id)

            existing_internal = ResourceAllocation.objects.filter(project=project).aggregate(total=Sum('hours'))['total'] or 0
            existing_external = ExternalCapacity.objects.filter(project=project).aggregate(total=Sum('hours'))['total'] or 0

            if existing_internal + existing_external + added_hours > project.total_manhours:
                raise serializers.ValidationError(
                    f"Adding {added_hours} hours to {project.project_code} would exceed "
                    f"total manhours ({project.total_manhours}). Current: {existing_internal + existing_external}"
                )

        # =================================================================
        # 7. Prepare ResourceAllocation records (if hours provided)
        # =================================================================
        allocations_to_create = []
        for item in resolved_data:
            hours = item.pop('hours', 0)  # Remove hours from assignment data
            if hours > 0:
                allocations_to_create.append(ResourceAllocation(
                    resource=item['resource'],
                    project=item['project'],
                    week_monday=item['week_monday'],
                    hours=hours
                ))

        # =================================================================
        # 8. Bulk create ProjectAssignments
        # =================================================================
        assignments = ProjectAssignment.objects.bulk_create([
            ProjectAssignment(**item) for item in resolved_data
        ])

        # =================================================================
        # 9. Bulk create ResourceAllocations (if any)
        # =================================================================
        if allocations_to_create:
            ResourceAllocation.objects.bulk_create(allocations_to_create)

        return assignments

    # =================================================================
    # Existing validate() method (kept for within-request duplicate check, etc.)
    # =================================================================
    def validate(self, data):
        # This runs before create() and catches duplicates within the request
        seen_triplets = set()
        for index, item in enumerate(data):
            # Note: at this stage we may still have input fields; we only check raw keys if available
            resource = item.get('resource') or item.get('resource_id')
            project = item.get('project') or item.get('project_code_input')
            week = item.get('week_monday')

            if resource and project and week:
                # Build a rough key – best effort
                res_id = resource.id if hasattr(resource, 'id') else resource
                proj_id = project.id if hasattr(project, 'id') else str(project)
                key = (res_id, proj_id, str(week))
                if key in seen_triplets:
                    raise serializers.ValidationError(
                        f"Duplicate entry at index {index}: same resource/project/week"
                    )
                seen_triplets.add(key)
        return data


# ================================================
# Enhanced ProjectAssignmentSerializer
# ================================================
class ProjectAssignmentSerializer(serializers.ModelSerializer):
    # Display fields (read-only for GET)
    resource = ResourceDetailSerializer(read_only=True)
    resource_name = serializers.CharField(source='resource.name', read_only=True)
    project = ProjectDetailSerializer(read_only=True)
    project_code = serializers.CharField(source='project.project_code', read_only=True)
    
    # Write-only input fields for POST/PUT/PATCH
    project_code_input = serializers.CharField(
        write_only=True, 
        required=False, 
        help_text="Set project by project_code instead of ID"
    )
    resource_id = serializers.PrimaryKeyRelatedField(
        queryset=Resource.objects.all(),
        source='resource',
        write_only=True,
        required=False,
        help_text="Set resource by ID (required if not using resource_name_input)"
    )
    # Optional: Keep name input for single-item requests only
    resource_name_input = serializers.CharField(
        write_only=True,
        required=False,
        help_text="Set resource by exact name (fails if multiple exist)"
    )
    # Optional hours field for bulk assignment with allocation creation
    hours = serializers.IntegerField(
        write_only=True,
        required=False,
        min_value=0,
        help_text="Hours to allocate (creates ResourceAllocation if provided)"
    )

    class Meta:
        model = ProjectAssignment
        fields = [
            'id', 'resource', 'resource_name', 'project', 'project_code',
            'is_lead', 'notes', 'week_monday', 'removed_on',
            'project_code_input', 'resource_id', 'resource_name_input', 'hours'
        ]
        read_only_fields = [
            'id', 'resource', 'resource_name', 'project', 'project_code'
        ]
        extra_kwargs = {
            'resource': {'required': False},
            'project': {'required': False}
        }
        list_serializer_class = ProjectAssignmentListSerializer

    def validate(self, data):
        # 1. Resolve project_code_input
        project_code = data.pop('project_code_input', None)
        if project_code:
            try:
                project = Project.objects.get(project_code=project_code.strip())
                data['project'] = project
            except Project.DoesNotExist:
                raise serializers.ValidationError({
                    "project_code_input": f"Project with code '{project_code}' not found"
                })
        elif not data.get('project'):
            raise serializers.ValidationError("Project is required. Use 'project_code_input'.")

        # 2. Resolve resource (prefer ID, fall back to name with validation)
        resource_id = data.pop('resource_id', None)
        resource_name = data.pop('resource_name_input', None)
        
        if resource_id:
            data['resource'] = resource_id
        elif resource_name:
            # Strict name matching - fails if duplicates
            try:
                resource = Resource.objects.get(name=resource_name.strip())
                data['resource'] = resource
            except Resource.DoesNotExist:
                raise serializers.ValidationError({
                    "resource_name_input": f"Resource '{resource_name}' not found"
                })
            except Resource.MultipleObjectsReturned:
                raise serializers.ValidationError({
                    "resource_name_input": f"Multiple resources found with name '{resource_name}'. Use resource_id instead."
                })
        elif not data.get('resource'):
            raise serializers.ValidationError("Resource is required. Use 'resource_id' or 'resource_name_input'.")

        # 3. Check for existing assignment (CREATE only)
        resource = data.get('resource')
        project = data.get('project')
        week_monday = data.get('week_monday')
        if resource and project and week_monday and self.instance is None:
            if ProjectAssignment.objects.filter(
                resource=resource, 
                project=project, 
                week_monday=week_monday
            ).exists():
                raise serializers.ValidationError(
                    f"Assignment already exists for {resource.name} on {project.project_code} in week {week_monday}"
                )
        
        return data

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ResourceAllocationSerializer(serializers.ModelSerializer):
    # Uses ResourceDetailSerializer which now has the correct read_only definition
    resource = ResourceDetailSerializer(read_only=True)
    project = ProjectDetailSerializer(read_only=True)

    class Meta:
        model = ResourceAllocation
        fields = ['id', 'resource', 'project', 'week_monday', 'hours']

    def validate(self, data):
        resource = data.get('resource')
        project = data.get('project')
        week_monday = data.get('week_monday')
        hours = data.get('hours', 0)

        # 1. Check total capacity does not exceed total_manhours
        if project:
            internal_sum = ResourceAllocation.objects.filter(project=project).exclude(
                pk=self.instance.pk if self.instance else None
            ).aggregate(total=Sum('hours'))['total'] or 0
            external_sum = ExternalCapacity.objects.filter(project=project).aggregate(total=Sum('hours'))['total'] or 0
            if internal_sum + external_sum + hours > project.total_manhours:
                raise serializers.ValidationError(
                    f"Total allocated capacity ({internal_sum + external_sum + hours} hours) would exceed the project's total manhours ({project.total_manhours})."
                )

        # 2. Check against project date range
        if project and week_monday:
            if project.start_monday and week_monday < project.start_monday:
                raise serializers.ValidationError(
                    f"Cannot allocate capacity before the project's start date ({project.start_monday})."
                )
            if project.end_monday and week_monday > project.end_monday:
                raise serializers.ValidationError(
                    f"Cannot allocate capacity after the project's end date ({project.end_monday})."
                )

        return data


# ================================================
# Bulk List Serializer for Strict Mode
# ================================================
class ProjectWeekAllocationListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        # Check against database before bulk_create
        duplicates = []
        allocated_weeks = []
        capacity_exceeded = []

        # Group by project to check total capacity
        project_totals = {}
        for idx, item in enumerate(validated_data):
            project = item['project']
            week_monday = item['week_monday']
            manhours = item['manhours']

            # Check for existing ProjectWeekAllocation
            if ProjectWeekAllocation.objects.filter(
                project=project,
                week_monday=week_monday
            ).exists():
                duplicates.append({
                    "index": idx,
                    "project_code": project.project_code,
                    "week_monday": str(week_monday),
                    "reason": "ProjectWeekAllocation already exists"
                })

            # Check for existing actual allocations (ResourceAllocation or ExternalCapacity)
            has_resource_allocation = ResourceAllocation.objects.filter(
                project=project,
                week_monday=week_monday
            ).exists()
            has_external_capacity = ExternalCapacity.objects.filter(
                project=project,
                week_monday=week_monday
            ).exists()

            if has_resource_allocation or has_external_capacity:
                allocated_weeks.append({
                    "index": idx,
                    "project_code": project.project_code,
                    "week_monday": str(week_monday),
                    "has_resource_allocation": has_resource_allocation,
                    "has_external_capacity": has_external_capacity
                })

            # Accumulate planned demand per project
            if project.id not in project_totals:
                project_totals[project.id] = {
                    'project': project,
                    'total_manhours': 0,
                    'items': []
                }
            project_totals[project.id]['total_manhours'] += manhours
            project_totals[project.id]['items'].append((idx, manhours))

        # Check capacity limits per project
        for project_id, data in project_totals.items():
            project = data['project']
            total_planned = data['total_manhours']

            # Get existing planned demand for this project
            existing_planned = ProjectWeekAllocation.objects.filter(project=project).aggregate(
                total=Sum('manhours'))['total'] or 0

            if existing_planned + total_planned > project.total_manhours:
                for idx, manhours in data['items']:
                    capacity_exceeded.append({
                        "index": idx,
                        "project_code": project.project_code,
                        "requested_manhours": manhours,
                        "existing_planned": existing_planned,
                        "total_would_be": existing_planned + total_planned,
                        "project_limit": project.total_manhours
                    })

        # Combine errors
        errors = {}
        if duplicates:
            errors["existing_allocations"] = duplicates
        if allocated_weeks:
            errors["already_allocated_weeks"] = allocated_weeks
        if capacity_exceeded:
            errors["capacity_exceeded"] = capacity_exceeded

        if errors:
            error_message = "Cannot create planned allocations"
            if capacity_exceeded:
                error_message += " - planned demand would exceed project total_manhours"
            elif allocated_weeks:
                error_message += " for weeks that are already allocated or have existing planned allocations"
            else:
                error_message += " due to duplicates"

            raise serializers.ValidationError({
                "error": error_message,
                **errors
            })

        # Optimized bulk create
        return ProjectWeekAllocation.objects.bulk_create([
            ProjectWeekAllocation(**item) for item in validated_data
        ])

    def validate(self, data):
        # Check for duplicates within the bulk request
        seen_pairs = set()
        for index, item in enumerate(data):
            key = (item['project'].id, item['week_monday'])
            if key in seen_pairs:
                raise serializers.ValidationError(
                    f"Duplicate entry at index {index}: "
                    f"Project {item['project'].project_code} on {item['week_monday']}"
                )
            seen_pairs.add(key)
        return data


class ExternalCapacityListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        # Check against database before bulk_create
        duplicates = []
        for idx, item in enumerate(validated_data):
            if ExternalCapacity.objects.filter(
                supplier=item['supplier'],
                project=item['project'],
                week_monday=item['week_monday']
            ).exists():
                duplicates.append({
                    "index": idx,
                    "supplier_name": item['supplier'].name,
                    "project_code": item['project'].project_code,
                    "week_monday": str(item['week_monday'])
                })

        if duplicates:
            raise serializers.ValidationError({
                "error": "Some external capacities already exist in database",
                "duplicates": duplicates
            })

        # Optimized bulk create
        return ExternalCapacity.objects.bulk_create([
            ExternalCapacity(**item) for item in validated_data
        ])

    def validate(self, data):
        # Check for duplicates within the bulk request
        seen_triplets = set()
        for index, item in enumerate(data):
            key = (item['supplier'].id, item['project'].id, item['week_monday'])
            if key in seen_triplets:
                raise serializers.ValidationError(
                    f"Duplicate entry at index {index}: "
                    f"{item['supplier'].name} → {item['project'].project_code} on {item['week_monday']}"
                )
            seen_triplets.add(key)
        return data


# class ExternalCapacitySerializer(serializers.ModelSerializer):
#     supplier_name = serializers.CharField(source='supplier.name', read_only=True)
#     project_code = serializers.CharField(source='project.project_code', read_only=True)
#     supplier = SupplierSerializer(read_only=True)
#     project = ProjectDetailSerializer(read_only=True)
#     # Write-only fields for input
#     supplier_id = serializers.PrimaryKeyRelatedField(
#         queryset=Supplier.objects.all(),
#         source='supplier',
#         write_only=True,
#         required=False
#     )
#     project_code_input = serializers.CharField(
#         write_only=True,
#         required=False,
#         help_text="Set project by project_code instead of ID"
#     )

#     dept = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
#     class Meta:
#         model = ExternalCapacity
#         fields = [
#             'id', 'supplier', 'supplier_name', 'project', 'dept', 
#             'project_code', 'week_monday', 'hours', 'supplier_id', 
#             'project_code_input', 'notes'
#         ]
#         read_only_fields = ['id', 'supplier', 'supplier_name']
#         extra_kwargs = {'supplier': {'required': False}, 'project': {'required': False}}
#         list_serializer_class = ExternalCapacityListSerializer

#     def validate(self, data):
#         # Resolve project_code_input
#         project_code = data.pop('project_code_input', None)
        
#         if project_code:
#             try:
#                 project = Project.objects.get(project_code=project_code.strip())
#                 data['project'] = project
#             except Project.DoesNotExist:
#                 raise serializers.ValidationError({
#                     "project_code_input": f"Project with code '{project_code}' not found"
#                 })
#         elif not data.get('project'):
#             raise serializers.ValidationError("Project is required. Use 'project_code_input' or 'project' field.")

#         # Check for existing external capacity (CREATE only)
#         supplier = data.get('supplier')
#         project = data.get('project')
#         week_monday = data.get('week_monday')
#         dept = data.get('dept')
#         if supplier and project and week_monday and dept and self.instance is None:
#             if ExternalCapacity.objects.filter(
#                 supplier=supplier,
#                 dept=dept,
#                 project=project,
#                 week_monday=week_monday
#             ).exists():
#                 raise serializers.ValidationError(
#                     f"External capacity already exists for {supplier.name} on {project.project_code} in week {week_monday}"
#                 )

#         # 2. Check total capacity does not exceed total_manhours
#         hours = data.get('hours', 0)
#         if project:
#             internal_sum = ResourceAllocation.objects.filter(project=project).aggregate(total=Sum('hours'))['total'] or 0
#             external_sum = ExternalCapacity.objects.filter(project=project).exclude(
#                 pk=self.instance.pk if self.instance else None
#             ).aggregate(total=Sum('hours'))['total'] or 0
#             if internal_sum + external_sum + hours > project.total_manhours:
#                 raise serializers.ValidationError(
#                     f"Total allocated capacity ({internal_sum + external_sum + hours} hours) would exceed the project's total manhours ({project.total_manhours})."
#                 )

#         # 3. Check against project date range
#         if project and week_monday:
#             if project.start_monday and week_monday < project.start_monday:
#                 raise serializers.ValidationError(
#                     f"Cannot allocate external capacity before the project's start date ({project.start_monday})."
#                 )
#             if project.end_monday and week_monday > project.end_monday:
#                 raise serializers.ValidationError(
#                     f"Cannot allocate external capacity after the project's end date ({project.end_monday})."
#                 )

#         return data

class ExternalCapacitySerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    project_code = serializers.CharField(source='project.project_code', read_only=True)
    
    # FIX: Make these PrimaryKeyRelatedFields so they accept the IDs passed from your View
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), required=False)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=False)
    dept = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())

    # Keeping your helper fields
    # supplier_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Supplier.objects.all(),
    #     source='supplier',
    #     write_only=True,
    #     required=False
    # )
    project_code_input = serializers.CharField(
        write_only=True,
        required=False
    )

    class Meta:
        model = ExternalCapacity
        fields = [
            'id', 'supplier', 'supplier_name', 'project', 'dept', 
            'project_code', 'week_monday', 'hours', 
            'project_code_input'
        ]
        # ONLY id and the "name/code" strings should be read_only
        read_only_fields = ['id', 'supplier_name', 'project_code']
        list_serializer_class = ExternalCapacityListSerializer

    def validate(self, data):
        # 1. Resolve project_code_input if provided (e.g. from direct API call)
        project_code_str = data.pop('project_code_input', None)
        if project_code_str:
            try:
                data['project'] = Project.objects.get(project_code=project_code_str.strip())
            except Project.DoesNotExist:
                raise serializers.ValidationError({"project_code_input": f"Project '{project_code_str}' not found"})
        
        # 2. Check if project exists (This will now work because 'project' is writeable)
        project = data.get('project')
        if not project:
            raise serializers.ValidationError("Project is required. Use 'project_code_input' or 'project' field.")

        # 3. Existing record check
        supplier = data.get('supplier')
        week_monday = data.get('week_monday')
        dept = data.get('dept')
        if supplier and project and week_monday and dept and self.instance is None:
            if ExternalCapacity.objects.filter(
                supplier=supplier,
                dept=dept,
                project=project,
                week_monday=week_monday
            ).exists():
                raise serializers.ValidationError(f"External capacity already exists for {supplier.name} on {project.project_code} in week {week_monday}")

        # 4. Capacity constraints
        hours = data.get('hours', 0)
        internal_sum = ResourceAllocation.objects.filter(project=project).aggregate(total=Sum('hours'))['total'] or 0
        external_sum = ExternalCapacity.objects.filter(project=project).exclude(
            pk=self.instance.pk if self.instance else None
        ).aggregate(total=Sum('hours'))['total'] or 0
        
        if internal_sum + external_sum + hours > project.total_manhours:
            raise serializers.ValidationError(f"Total capacity ({internal_sum + external_sum + hours}) exceeds limit ({project.total_manhours}).")

        return data

class AppSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppSettings
        fields = ['id', 'default_working_hours_per_week']


