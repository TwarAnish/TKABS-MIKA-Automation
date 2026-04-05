# capacity_planning/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from accounts.permissions import ModuleViewPermission, ModulePreparePermission
from .models import ResourceAllocation
from .serializers import ResourceAllocationSerializer


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import ResourceAllocation, ProjectAssignment
from .serializers import ResourceAllocationSerializer



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from accounts.permissions import ModuleViewPermission, ModulePreparePermission
from .models import ResourceAllocation, ProjectAssignment
from .serializers import ResourceAllocationSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from accounts.permissions import ModuleViewPermission, ModulePreparePermission
from .models import ExternalCapacity
from .serializers import ExternalCapacitySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import ModuleViewPermission, ModulePreparePermission
from .models import ExternalCapacity
from .serializers import ExternalCapacitySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import Sum
from datetime import datetime
from collections import defaultdict
from django.db.models import Max

from collections import defaultdict
from datetime import datetime

from django.db import transaction
from django.db.models import F, Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import transaction
from django.db.models import Sum
from collections import defaultdict
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from accounts.permissions import ModuleViewPermission, ModulePreparePermission
from .models import ProjectDepartmentAllocation, Project
from .serializers import ProjectDepartmentAllocationSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ProjectDepartmentAllocation, ProjectWeekAllocation, Department
from .serializers import ProjectDepartmentAllocationSerializer
# assume you have get_monday_of_week(date) helper if needed
# capacity_planning/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from psr.models import PSRProject
from .models import Project

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import date, timedelta
from typing import Optional
from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ResourceAllocation, ProjectAssignment  # adjust import
from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from .models import ProjectWeekAllocation, ProjectDepartmentAllocation
from .serializers import ProjectWeekAllocationSerializer  # assuming you have this

from django.db.models import Sum, Q, F, Case, When, IntegerField, Value
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from collections import defaultdict
from django.db import transaction
from accounts.permissions import *
from collections import defaultdict
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from capacity_planning.models import Resource
from collections import defaultdict
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import ModuleViewPermission

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from capacity_planning.models import Resource
from capacity_planning.serializers import ResourceSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db.models import Q
from capacity_planning.models import Resource
from .serializers import ResourceSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from capacity_planning.models import Resource
from capacity_planning.serializers import ResourceSerializer

from .models import *
from .serializers import *
from collections import defaultdict
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.db.models import Q, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from collections import defaultdict
from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Department
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime, timedelta
from collections import defaultdict
from django.db.models import Sum, Count
from django.conf import settings
import logging
from collections import defaultdict
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum, Q
from rest_framework.views import APIView
from rest_framework.response import Response

from collections import defaultdict
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from collections import defaultdict
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from collections import defaultdict
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q, Sum
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.db.models import Sum
from collections import defaultdict
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import ModuleViewPermission, ModulePreparePermission
from .models import ProjectAssignment
from .serializers import ProjectAssignmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import ModuleViewPermission, ModulePreparePermission
from .models import Supplier
from .serializers import SupplierSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_date
from accounts.permissions import ModuleViewPermission, ModulePreparePermission
from .models import ProjectAssignment
from .serializers import ProjectAssignmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum
# Set up logging to track errors in your server console
logger = logging.getLogger(__name__)
# =============================================================================
# BASE VIEWSET – No default ordering that breaks things
# =============================================================================
class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # ← Removed any global ordering here → let each ViewSet define its own


# =============================================================================
# 1. DEPARTMENT
# =============================================================================
class DepartmentViewSet(BaseViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    search_fields = ['name']
    ordering_fields = ['order', 'name']
    # Explicit safe ordering
    def get_queryset(self):
        return Department.objects.all().order_by('order', 'name')

    @action(detail=False, methods=['get'], url_path='tree')
    def tree(self, request):
        try:
            roots = Department.objects.filter(parent=None).order_by('order', 'name')
            serializer = DepartmentTreeSerializer(
                roots,
                many=True,
                context={'request': request}   
            )
            return Response(serializer.data)

        except Exception as e:
            # 'e' is the error object. str(e) gives you the specific error message.
            return Response(
                {
                    "error": "Failed to retrieve department tree.",
                    "message": str(e)  # This shows exactly what went wrong
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# =============================================================================
# 2. PROJECT
# =============================================================================
class ProjectViewSet(BaseViewSet):
    queryset = Project.objects.select_related('department', 'created_by').prefetch_related('planned_weeks', 'external_capacities')
    serializer_class = ProjectSerializer
    filterset_fields = ['status', 'department']
    search_fields = ['name', 'project_code']
    ordering_fields = ['start_monday', 'project_code', '-start_monday']
    ordering = ['-start_monday']  # ← safe explicit ordering

    def get_queryset(self):
        qs = super().get_queryset()
        dept_id = self.request.query_params.get('department')
        
        if dept_id:
            try:
                # 1. Try to fetch the department
                dept = Department.objects.get(id=dept_id)
                descendants = dept.get_descendants()
                qs = qs.filter(department__in=[dept] + list(descendants))
                
            except (Department.DoesNotExist, ValueError, TypeError) as e:
                # 2. Raise the error using DRF's ValidationError
                # This automatically returns a 400 Bad Request with the message below
                error_msg = f"Invalid department ID '{dept_id}': {str(e)}"
                raise ValidationError({"department": error_msg})
                
            except Exception as e:
                # 3. Catch unexpected system/database errors
                raise ValidationError({"server_error": f"An unexpected error occurred: {str(e)}"})

        return qs

    from rest_framework.views import APIView

class GlobalDepartmentWeeklyDetailView(APIView):
    permission_classes = [ModuleViewPermission]

    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]




class GlobalDepartmentWeeklyDetailView(APIView):
    permission_classes = [ModuleViewPermission]

    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            # --- 1. Date Range Logic ---
            today = timezone.now().date()
            current_monday = today - timedelta(days=today.weekday())

            start_str = request.query_params.get("start")
            end_str = request.query_params.get("end")

            if start_str and end_str:
                try:
                    start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
                    end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
                except ValueError as e:
                    return Response({
                        "error": "Invalid date format. Use YYYY-MM-DD",
                        "message": str(e)
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                start_date = current_monday - timedelta(weeks=24)
                end_date = current_monday + timedelta(weeks=24)

            start_monday = start_date - timedelta(days=start_date.weekday())
            end_monday = end_date - timedelta(days=end_date.weekday())

            mondays = []
            curr = start_monday
            while curr <= end_monday:
                mondays.append(curr)
                curr += timedelta(days=7)

            # --- 2. Map Departments & Resources ---
            resources = Resource.objects.filter(is_internal=True).prefetch_related('departments')
            
            dept_resource_map = defaultdict(list)
            active_dept_ids = set()

            for res in resources:
                for d in res.departments.all():
                    dept_resource_map[d.id].append(res)
                    active_dept_ids.add(d.id)

            all_depts = {d.id: d for d in Department.objects.filter(id__in=active_dept_ids)}
            all_projs = {p.id: p for p in Project.objects.all()}

            # --- 3. Fetch Data ---
            internal_data = ResourceAllocation.objects.filter(
                week_monday__range=(start_monday, end_monday),
                department_id__in=active_dept_ids
            ).values('project_id', 'department_id', 'week_monday').annotate(
                hours=Sum('hours', default=0),
                emp_count=Count('resource', distinct=True)
            )

            planned_data = ProjectWeekAllocation.objects.filter(
                week_monday__range=(start_monday, end_monday),
                department_id__in=active_dept_ids
            ).values('project_id', 'department_id', 'week_monday').annotate(
                hours=Sum('manhours', default=0)
            )

            external_data = ExternalCapacity.objects.filter(
                week_monday__range=(start_monday, end_monday)
            ).values('project_id', 'week_monday').annotate(
                ext_hours=Sum('hours', default=0),
                ext_emp_count=Count('id', distinct=True) 
            )

            # --- 4. Process Lookups ---
            usage_map = defaultdict(lambda: {"internal": 0.0, "planned": 0.0, "internal_emp_count": 0})
            external_lookup = {
                (item['week_monday'], item['project_id']): {
                    "hours": float(item['ext_hours']),
                    "count": item['ext_emp_count']
                } for item in external_data
            }
            
            dept_weekly_internal_used = defaultdict(lambda: defaultdict(float))
            dept_projects_per_week = defaultdict(lambda: defaultdict(set))
            dept_weekly_planned = defaultdict(lambda: defaultdict(float))

            for item in internal_data:
                w, d, p = item['week_monday'], item['department_id'], item['project_id']
                usage_map[(w, d, p)]["internal"] = float(item['hours'])
                usage_map[(w, d, p)]["internal_emp_count"] = item['emp_count']
                dept_weekly_internal_used[d][w] += float(item['hours'])
                dept_projects_per_week[d][w].add(p)

            for item in planned_data:
                w, d, p = item['week_monday'], item['department_id'], item['project_id']
                usage_map[(w, d, p)]["planned"] = float(item['hours'])
                dept_weekly_planned[d][w] += float(item['hours'])
                dept_projects_per_week[d][w].add(p)

            # --- 5. Build Result ---
            result = []

            for d_id in active_dept_ids:
                dept = all_depts.get(d_id)
                # SAFETY: If department object doesn't exist in map, skip it
                if not dept:
                    continue

                dept_resources = dept_resource_map[d_id]

                for week in mondays:
                    active_res_count = sum(
                        1 for res in dept_resources 
                        if res.joining_date and res.joining_date <= week 
                        and (not res.leaving_date or res.leaving_date > week)
                    )
                    
                    avail_cap = active_res_count * 45.0
                    total_dept_internal = dept_weekly_internal_used[d_id][week]
                    total_dept_planned = dept_weekly_planned[d_id][week]
                    projs_in_week = dept_projects_per_week[d_id][week]

                    if not projs_in_week:
                        row = self.make_row(dept.name, week, None, avail_cap, avail_cap, 0, 0, 0, 0, 0)
                        row["dept_weekly_total_planned"] = 0.0
                        result.append(row)
                    else:
                        for p_id in projs_in_week:
                            proj = all_projs.get(p_id)
                            # SAFETY: Fallback if project is missing from the all_projs map
                            if not proj:
                                continue

                            vals = usage_map[(week, d_id, p_id)]
                            
                            ext_info = external_lookup.get((week, p_id), {"hours": 0.0, "count": 0})
                            sharing_depts = [
                                id for id in active_dept_ids 
                                if p_id in dept_projects_per_week[id][week]
                            ]
                            
                            ext_share_hours = ext_info["hours"] / len(sharing_depts) if sharing_depts else 0.0
                            ext_share_count = ext_info["count"] / len(sharing_depts) if sharing_depts else 0.0

                            free_cap = max(0.0, avail_cap - total_dept_internal - ext_share_hours)

                            row = self.make_row(
                                dept.name, week, proj, avail_cap, free_cap, 
                                vals["internal"], vals["planned"], ext_share_hours,
                                vals["internal_emp_count"], ext_share_count
                            )
                            row["dept_weekly_total_planned"] = round(total_dept_planned, 1)
                            result.append(row)

            result.sort(key=lambda x: (x["week_monday"], x["department"]))

            return Response({
                "period": {
                    "start_monday": start_monday.isoformat(),
                    "end_monday": end_monday.isoformat(),
                    "weeks_count": len(mondays)
                },
                "data": result
            })

        except Exception as e:
            # Logs the detailed error on the server
            logger.exception("Capacity Report Generation Failed")
            # Sends the specific error message back to the frontend
            return Response(
                {
                    "error": "Failed to generate weekly detail report.",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def make_row(self, dept_name, week, proj, avail, free, internal, planned, external, int_emp, ext_emp):
        return {
            "department": dept_name,
            "week_monday": week.isoformat(),
            "calendar_week": f"CW{week.isocalendar()[1]:02d}",
            "project_code": proj.project_code if proj else "N/A",
            "project_name": proj.name if proj else "No Active Projects",
            "project_color": proj.color_code if proj else "#eeeeee",
            "manhours": round(planned, 1),
            "data": {
                "internal": round(internal, 1),
                "external": round(external, 1),
                "internal_emp_count": round(int_emp, 1),
                "external_emp_count": round(ext_emp, 1),
                "total_emp_count": round(int_emp + ext_emp, 1),
                "total_used": round(internal + external, 1),
                "available_capacity": round(avail, 1),
                "free_capacity": round(free, 1)
            }
        }
# =============================================================================
# 3. RESOURCE
# =============================================================================


class ResourceViewSet(BaseViewSet):
    queryset = Resource.objects.select_related('department', 'supplier', 'user')
    serializer_class = ResourceSerializer
    filterset_fields = ['is_internal', 'department', 'role', 'is_active']
    search_fields = ['name']
    ordering_fields = ['name', 'department__name']
    ordering = ['name']

    @action(detail=True, methods=['get'], url_path='weekly-load')
    def weekly_load(self, request, pk=None):
        try:
            # 1. Fetch the Resource (Handles 404 automatically)
            resource = self.get_object()
            
            start_str = request.query_params.get('start')
            weeks_str = request.query_params.get('weeks', '26')

            # 2. Validate weeks parameter
            try:
                weeks = int(weeks_str)
                if weeks <= 0 or weeks > 104:
                    return Response({
                        "error": "Validation Error",
                        "message": "weeks must be a positive integer between 1 and 104"
                    }, status=status.HTTP_400_BAD_REQUEST)
            except ValueError as e:
                return Response({
                    "error": "Validation Error", 
                    "message": f"weeks must be a valid integer: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

            # 3. Validate start date
            if start_str:
                try:
                    # Note: using datetime.strptime directly for standard date parsing
                    from datetime import datetime
                    start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
                except (ValueError, TypeError) as e:
                    return Response({
                        "error": "Validation Error",
                        "message": f"Invalid start date format. Use YYYY-MM-DD. Error: {str(e)}"
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Default to current week's Monday
                today = timezone.now().date()
                start_date = today - timedelta(days=today.weekday())

            # 4. Logic & Database Query
            mondays = [start_date + timedelta(weeks=i) for i in range(weeks)]

            allocations = ResourceAllocation.objects.filter(
                resource=resource, 
                week_monday__in=mondays
            ).values('week_monday').annotate(total_hours=Sum('hours'))

            alloc_dict = {str(a['week_monday']): a['total_hours'] for a in allocations}

            # 5. Build Result
            result = []
            for monday in mondays:
                result.append({
                    'week_monday': str(monday),
                    'hours': float(alloc_dict.get(str(monday), 0) or 0)
                })

            return Response({
                'resource': resource.name,
                'availability_per_week': getattr(resource, 'effective_availability_per_week', 0),
                'data': result
            })

        except Exception as e:
            # Catch-all for unexpected crashes (Database down, AttributeErrors, etc.)
            logger.exception(f"Weekly Load calculation failed for resource {pk}")
            return Response({
                "error": "Failed to retrieve weekly load data.",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# =============================================================================
# 4. OTHER VIEWSETS (safe ordering)
# =============================================================================
class ProjectAssignmentViewSet(BaseViewSet):
    queryset = ProjectAssignment.objects.select_related('resource__department', 'project').all()
    serializer_class = ProjectAssignmentSerializer
    filterset_fields = ['project', 'resource', 'is_lead']
    ordering = ['-week_monday']

    def get_queryset(self):
        """
        Custom get_queryset with error handling for filtering or database issues.
        """
        try:
            return super().get_queryset()
        except Exception as e:
            logger.exception("Error in ProjectAssignment get_queryset")
            # We raise a DRF ValidationError so it returns a 400/500 cleanly
            raise DRFValidationError({
                "error": "Queryset retrieval failed",
                "message": str(e)
            })

    def list(self, request, *args, **kwargs):
        """
        Wraps the standard list action in a try-except to catch 
        filtering errors or serialization crashes.
        """
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.exception("Error in ProjectAssignment list view")
            return Response(
                {
                    "error": "Failed to retrieve project assignments.",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        """
        Wraps the detail view (GET /id/) in a try-except.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            logger.exception(f"Error retrieving ProjectAssignment {kwargs.get('pk')}")
            return Response(
                {
                    "error": "Failed to retrieve assignment details.",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ResourceAllocationViewSet(BaseViewSet):
    queryset = ResourceAllocation.objects.select_related('resource', 'project').all()
    serializer_class = ResourceAllocationSerializer
    filterset_fields = ['project', 'resource', 'week_monday']
    ordering = ['week_monday', 'resource__name']

    def list(self, request, *args, **kwargs):
        """
        Wraps the list view to catch database timeouts or filtering errors.
        """
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.exception("ResourceAllocation list fetch failed")
            return Response(
                {
                    "error": "Failed to retrieve resource allocations.",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        """
        Wraps creation to provide specific error messages if the data is malformed.
        """
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.exception("ResourceAllocation creation failed")
            return Response(
                {
                    "error": "Failed to create resource allocation.",
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        """
        Wraps update to handle cases where the ID doesn't exist or data is invalid.
        """
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            logger.exception("ResourceAllocation update failed")
            return Response(
                {
                    "error": "Failed to update resource allocation.",
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        """
        Wraps deletion to handle database constraints or missing IDs.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.exception("ResourceAllocation deletion failed")
            return Response(
                {
                    "error": "Failed to delete resource allocation.",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




class ProjectWeekAllocationViewSet(BaseViewSet):
    queryset = ProjectWeekAllocation.objects.select_related('project').all()
    serializer_class = ProjectWeekAllocationSerializer
    filterset_fields = ['project', 'week_monday']
    ordering = ['week_monday']

    def list(self, request, *args, **kwargs):
        """
        Catches issues during data retrieval or invalid filter parameters.
        """
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.exception("ProjectWeekAllocation list retrieval failed")
            return Response(
                {
                    "error": "Failed to retrieve planned allocations.",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        """
        Catches errors during creation (e.g., integrity errors or bad data).
        """
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.exception("ProjectWeekAllocation creation failed")
            return Response(
                {
                    "error": "Failed to save the planned allocation.",
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        """
        Handles errors during manhour updates or project re-assignments.
        """
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            logger.exception("ProjectWeekAllocation update failed")
            return Response(
                {
                    "error": "Failed to update the planned allocation.",
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        """
        Ensures a clean response if a record cannot be deleted.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.exception("ProjectWeekAllocation deletion failed")
            return Response(
                {
                    "error": "Failed to remove the planned allocation.",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExternalCapacityViewSet(BaseViewSet):
    queryset = ExternalCapacity.objects.select_related('supplier', 'project').all()
    serializer_class = ExternalCapacitySerializer
    filterset_fields = ['supplier', 'project', 'week_monday']
    ordering = ['-week_monday']

    def list(self, request, *args, **kwargs):
        """
        Catches database connection issues or invalid supplier/project filters.
        """
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.exception("ExternalCapacity list retrieval failed")
            return Response(
                {
                    "error": "Failed to retrieve external capacity records.",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        """
        Catches errors when adding new external manhours (e.g., missing supplier ID).
        """
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.exception("ExternalCapacity creation failed")
            return Response(
                {
                    "error": "Failed to record external capacity.",
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        """
        Handles errors during updates to external manhours or supplier changes.
        """
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            logger.exception("ExternalCapacity update failed")
            return Response(
                {
                    "error": "Failed to update external capacity record.",
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        """
        Provides a clean error if a record cannot be deleted due to dependencies.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.exception("ExternalCapacity deletion failed")
            return Response(
                {
                    "error": "Failed to delete external capacity record.",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class SupplierViewSet(BaseViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    search_fields = ['name']
    ordering = ['name']


class AppSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AppSettingsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return AppSettings.objects.all()

    def get_object(self):
        return AppSettings.load()  # singleton


# =============================================================================
# DASHBOARD ENDPOINTS
# =============================================================================


class CapacitySummaryView(APIView):
    permission_classes = [ModuleViewPermission]

    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            # --- 1. Parameter Extraction ---
            start_str = request.query_params.get('start')
            weeks_str = request.query_params.get('weeks', '26')
            dept_id = request.query_params.get('department')

            # --- 2. Validation with specific error messages ---
            try:
                weeks = int(weeks_str)
                if weeks <= 0 or weeks > 104:
                    return Response({
                        "error": "Validation Error",
                        "message": "weeks must be a positive integer between 1 and 104"
                    }, status=status.HTTP_400_BAD_REQUEST)
            except ValueError as e:
                return Response({
                    "error": "Validation Error",
                    "message": f"weeks must be a valid integer: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

            if start_str:
                try:
                    start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
                except (ValueError, TypeError) as e:
                    return Response({
                        "error": "Validation Error",
                        "message": f"Invalid start date format. Use YYYY-MM-DD: {str(e)}"
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                today = timezone.now().date()
                start_date = today - timedelta(days=today.weekday())

            # Validate department and get descendants early to avoid repeated queries
            descendants = None
            if dept_id:
                try:
                    dept = Department.objects.get(id=dept_id)
                    descendants = dept.get_descendants(include_self=True)
                except Department.DoesNotExist:
                    return Response({
                        "error": "Not Found",
                        "message": f"Department with id {dept_id} not found"
                    }, status=status.HTTP_404_NOT_FOUND)
                except ValueError as e:
                    return Response({
                        "error": "Validation Error",
                        "message": f"Department ID must be an integer: {str(e)}"
                    }, status=status.HTTP_400_BAD_REQUEST)

            # --- 3. Main Logic ---
            start_monday = start_date - timedelta(days=start_date.weekday())
            mondays = [start_monday + timedelta(weeks=i) for i in range(weeks)]
            result = []

            for monday in mondays:
                # Planned demand
                planned_qs = ProjectWeekAllocation.objects.filter(week_monday=monday)
                if descendants:
                    planned_qs = planned_qs.filter(project__department__in=descendants)
                planned_h = planned_qs.aggregate(t=Sum('manhours'))['t'] or 0.0

                # Internal supply
                internal_qs = ResourceAllocation.objects.filter(
                    week_monday=monday,
                    resource__is_internal=True
                )
                if descendants:
                    internal_qs = internal_qs.filter(resource__department__in=descendants)
                internal_h = internal_qs.aggregate(t=Sum('hours'))['t'] or 0.0

                # External supply
                external_qs = ExternalCapacity.objects.filter(week_monday=monday)
                if descendants:
                    external_qs = external_qs.filter(project__department__in=descendants)
                external_h = external_qs.aggregate(t=Sum('hours'))['t'] or 0.0

                total_supply = internal_h + external_h
                gap = planned_h - total_supply

                result.append({
                    'week_monday': str(monday),
                    'planned_demand': round(float(planned_h), 1),
                    'internal_allocated': round(float(internal_h), 1),
                    'external_capacity': round(float(external_h), 1),
                    'total_supply': round(float(total_supply), 1),
                    'gap': round(float(gap), 1),
                    'is_overallocated': gap < 0,
                    'is_underallocated': gap > 0,
                })

            return Response({'weeks': result})

        except Exception as e:
            # Catch any unexpected logic or DB errors
            logger.exception("Capacity Summary generation failed")
            return Response({
                "error": "An unexpected error occurred while calculating the summary.",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CapacityGapsView(APIView):
    permission_classes = [ModuleViewPermission]

    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            # --- 1. Parameter Extraction & Validation ---
            threshold_str = request.query_params.get('threshold', '20')
            dept_id = request.query_params.get('department')

            try:
                threshold = int(threshold_str)
                if threshold < 0:
                    return Response({
                        "error": "Validation Error",
                        "message": "threshold must be a non-negative integer"
                    }, status=status.HTTP_400_BAD_REQUEST)
                threshold_hours = threshold * 8  # convert man-days to hours
            except ValueError as e:
                return Response({
                    "error": "Validation Error",
                    "message": f"threshold must be a valid integer: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

            # --- 2. Department Filtering Logic ---
            department_filter = Q()
            descendants = None
            if dept_id:
                try:
                    dept = Department.objects.get(id=dept_id)
                    descendants = dept.get_descendants(include_self=True)
                    department_filter = Q(project__department__in=descendants)
                except Department.DoesNotExist:
                    return Response({
                        "error": "Not Found",
                        "message": f"Department with id {dept_id} not found"
                    }, status=status.HTTP_404_NOT_FOUND)
                except ValueError as e:
                    return Response({
                        "error": "Validation Error",
                        "message": f"department must be a valid integer ID: {str(e)}"
                    }, status=status.HTTP_400_BAD_REQUEST)

            # --- 3. Data Processing ---
            # Using try-except here specifically for DB query issues
            weeks = ProjectWeekAllocation.objects.values_list('week_monday', flat=True).distinct().order_by('week_monday')

            gaps = []
            for monday in weeks:
                planned = ProjectWeekAllocation.objects.filter(week_monday=monday)
                internal = ResourceAllocation.objects.filter(week_monday=monday, resource__is_internal=True)
                external = ExternalCapacity.objects.filter(week_monday=monday)

                if dept_id and descendants:
                    planned = planned.filter(department_filter)
                    internal = internal.filter(resource__department__in=descendants)
                    external = external.filter(project__department__in=descendants)

                # Aggregations
                planned_h = planned.aggregate(t=Sum('manhours'))['t'] or 0.0
                int_sum = internal.aggregate(t=Sum('hours'))['t'] or 0.0
                ext_sum = external.aggregate(t=Sum('hours'))['t'] or 0.0
                
                supply_h = int_sum + ext_sum
                gap = planned_h - supply_h

                if gap > threshold_hours:
                    gaps.append({
                        'week_monday': str(monday),
                        'gap_manhours': round(float(gap), 1),
                        'gap_man_days': round(float(gap / 8), 1)
                    })

            return Response({'gaps': gaps})

        except Exception as e:
            # Catch-all for unexpected logic errors or database crashes
            logger.exception("Capacity Gaps generation failed")
            return Response({
                "error": "An unexpected error occurred while calculating capacity gaps.",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =============================================================================
# Weekly Project Breakdown
# =============================================================================
# ——————————————————— WEEKLY PROJECT BREAKDOWN (Internal vs External) ———————————————————

class WeeklyProjectBreakdownView(APIView):
    permission_classes = [ModuleViewPermission]

    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            # ------------------------------------------------------------------
            # 1. Query parameters & Validation
            # ------------------------------------------------------------------
            start_str = request.query_params.get("start")
            end_str = request.query_params.get("end")
            project_code = request.query_params.get("project_code")

            # Validate project_code if provided
            if project_code:
                if not Project.objects.filter(project_code=project_code).exists():
                    return Response({
                        "error": "Not Found",
                        "message": f"Project with code '{project_code}' not found"
                    }, status=status.HTTP_404_NOT_FOUND)

            # Default range logic
            today = timezone.now().date()
            default_start = today - timedelta(days=today.weekday())

            try:
                start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else default_start
                end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else default_start + timedelta(weeks=52)
            except ValueError as e:
                return Response({
                    "error": "Validation Error",
                    "message": f"Invalid date format. Use YYYY-MM-DD: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

            if start_date > end_date:
                start_date, end_date = end_date, start_date

            # ------------------------------------------------------------------
            # 2. Planned demand
            # ------------------------------------------------------------------
            planned_qs = ProjectWeekAllocation.objects.filter(
                week_monday__gte=start_date,
                week_monday__lte=end_date
            ).select_related("project")

            if project_code:
                planned_qs = planned_qs.filter(project__project_code=project_code)

            # Build dict safely
            planned_dict = {
                (item.project.project_code, item.week_monday): item.manhours
                for item in planned_qs if item.project
            }

            # ------------------------------------------------------------------
            # 3. Actual allocated hours
            # ------------------------------------------------------------------
            allocation_qs = ResourceAllocation.objects.filter(
                week_monday__gte=start_date,
                week_monday__lte=end_date
            ).select_related("project", "resource")

            if project_code:
                allocation_qs = allocation_qs.filter(project__project_code=project_code)

            actual_data = allocation_qs.values(
                "project__project_code",
                "project__name",
                "week_monday"
            ).annotate(
                internal_hours=Sum(
                    Case(
                        When(resource__is_internal=True, then=F("hours")),
                        default=0,
                        output_field=IntegerField(),
                    )
                ),
                external_hours=Sum(
                    Case(
                        When(resource__is_internal=False, then=F("hours")),
                        default=0,
                        output_field=IntegerField(),
                    )
                ),
            ).order_by("week_monday")

            # ------------------------------------------------------------------
            # 4. Build final response
            # ------------------------------------------------------------------
            result = []
            for item in actual_data:
                proj_code = item["project__project_code"]
                week = item["week_monday"]

                key = (proj_code, week)
                planned_manhours = planned_dict.get(key, 0)

                # Skip empty weeks
                if (planned_manhours or 0) == 0 and \
                   (item["internal_hours"] or 0) == 0 and \
                   (item["external_hours"] or 0) == 0:
                    continue

                result.append({
                    "project_name": item["project__name"] or "Unknown Project",
                    "project_code": proj_code,
                    "manhours": round(float(planned_manhours or 0), 1),
                    "data": {
                        "internal": round(float(item["internal_hours"] or 0), 1),
                        "external": round(float(item["external_hours"] or 0), 1),
                    },
                    "week_monday": str(week),
                    "calendar_week": f"CW{week.isocalendar()[1]:02d}",
                })

            result.sort(key=lambda x: (x["week_monday"], x["project_code"]))

            return Response({
                "date_range": {
                    "start": str(start_date),
                    "end": str(end_date)
                },
                "data": result
            })

        except Exception as e:
            logger.exception("Weekly Project Breakdown generation failed")
            return Response({
                "error": "An unexpected error occurred while calculating project breakdown.",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# =============================================================================
# Department Weekly Project Breakdown
# =============================================================================
# ———————————————————Department WEEKLY PROJECT BREAKDOWN (Internal vs External) ———————————————————



class DepartmentWeeklyBreakdownView(APIView):
    permission_classes = [ModuleViewPermission]

    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            # --- 1. Parameter Extraction ---
            start_str = request.query_params.get("start")
            end_str = request.query_params.get("end")
            dept_filter = request.query_params.get("department")

            # --- 2. Date Range Logic & Validation ---
            today = timezone.now().date()
            default_start = today - timedelta(days=today.weekday()) - timedelta(weeks=26)
            default_end = default_start + timedelta(weeks=52)

            try:
                start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else default_start
                end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else default_end
            except (ValueError, TypeError) as e:
                return Response({
                    "error": "Validation Error",
                    "message": f"Invalid date format. Use YYYY-MM-DD: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

            if start_date > end_date:
                start_date, end_date = end_date, start_date

            # Aligning dates to Mondays
            start_monday = start_date + timedelta(days=(7 - start_date.weekday()) % 7)
            if start_monday < start_date:
                start_monday += timedelta(days=7)
            end_monday = end_date - timedelta(days=end_date.weekday())

            mondays = []
            current = start_monday
            while current <= end_monday:
                mondays.append(current)
                current += timedelta(days=7)

            # --- 3. Build Department Filter ---
            dept_q = Q()
            descendants = []
            if dept_filter:
                dept_filter = dept_filter.strip()
                try:
                    dept_id = int(dept_filter)
                    dept = Department.objects.get(id=dept_id)
                    descendants = list(dept.get_descendants()) + [dept]
                    dept_q = Q(resource__department__in=descendants)
                except (ValueError, Department.DoesNotExist):
                    # Fallback to name search if not an ID
                    dept_q = Q(resource__department__name__icontains=dept_filter)

            # --- 4. Fetch Actual Allocation Data ---
            actual_qs = ResourceAllocation.objects.filter(
                week_monday__gte=start_monday,
                week_monday__lte=end_monday
            )
            if dept_filter:
                actual_qs = actual_qs.filter(dept_q)

            actual_data = actual_qs.values(
                "resource__department__name",
                "week_monday"
            ).annotate(
                internal=Sum(Case(When(resource__is_internal=True, then=F("hours")), default=0, output_field=IntegerField())),
                external=Sum(Case(When(resource__is_internal=False, then=F("hours")), default=0, output_field=IntegerField())),
            )

            actual_dict = {}
            dept_names = set()

            for item in actual_data:
                dept_name = item["resource__department__name"] or "No Department"
                week = item["week_monday"]
                key = (dept_name, week)
                int_val = item["internal"] or 0
                ext_val = item["external"] or 0
                actual_dict[key] = {
                    "internal": int_val,
                    "external": ext_val,
                    "total": int_val + ext_val,
                }
                dept_names.add(dept_name)

            # --- 5. Fetch Planned Demand ---
            planned_dict = {}
            planned_qs = ProjectWeekAllocation.objects.filter(
                week_monday__gte=start_monday,
                week_monday__lte=end_monday,
                project__department__isnull=False
            )
            if dept_filter and descendants:
                planned_qs = planned_qs.filter(project__department__in=descendants)

            for item in planned_qs.values("project__department__name", "week_monday").annotate(planned=Sum("manhours")):
                dept = item["project__department__name"] or "No Department"
                planned_dict[(dept, item["week_monday"])] = item["planned"] or 0

            # Include empty departments
            if not dept_filter:
                dept_names.update(Department.objects.filter(resource__isnull=False).values_list("name", flat=True))

            # --- 6. Build Result ---
            result = []
            for dept_name in sorted(dept_names):
                for monday in mondays:
                    key = (dept_name, monday)
                    actual = actual_dict.get(key, {"internal": 0, "external": 0, "total": 0})
                    planned = planned_dict.get(key, 0)
                    
                    # Ensure numeric types for calculation
                    planned_val = float(planned or 0)
                    actual_total = float(actual["total"] or 0)

                    result.append({
                        "department": dept_name,
                        "week_monday": str(monday),
                        "calendar_week": f"CW{monday.isocalendar()[1]:02d}",
                        "week_display": monday.strftime("%b %d"),
                        "planned_manhours": round(planned_val, 1),
                        "data": {
                            "internal": round(float(actual["internal"] or 0), 1),
                            "external": round(float(actual["external"] or 0), 1),
                            "total": round(actual_total, 1),
                        },
                        "gap": round(planned_val - actual_total, 1),
                    })

            result.sort(key=lambda x: (x["week_monday"], x["department"]))

            return Response({
                "date_range": {"start": str(start_monday), "end": str(end_monday)},
                "department_filter": dept_filter or "All",
                "total_weeks": len(mondays),
                "data": result
            })

        except Exception as e:
            # Catch all unexpected crashes
            logger.exception("Department Weekly Breakdown failed")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# =============================================================================
# Project Role Utilization
# =============================================================================
# ———————————————————Project Role Utilization BREAKDOWN (Internal vs External) ———————————————————

class ProjectRoleUtilizationView(APIView):
    permission_classes = [ModuleViewPermission]

    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            # --- 1. Parameter Extraction ---
            project_code = request.query_params.get("project_code")
            role_filter = request.query_params.get("role")
            start_str = request.query_params.get("start")
            end_str = request.query_params.get("end")

            if not project_code:
                return Response({
                    "error": "Validation Error",
                    "message": "project_code parameter is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            # --- 2. Project Retrieval ---
            try:
                project = Project.objects.get(project_code=project_code)
            except Project.DoesNotExist:
                return Response({
                    "error": "Not Found",
                    "message": f"Project '{project_code}' not found"
                }, status=status.HTTP_404_NOT_FOUND)

            # --- 3. Role Resolution Logic ---
            # Assuming ROLE_CHOICES is imported/available globally
            valid_role_codes = [code for code, _ in ROLE_CHOICES]
            role_code = None
            role_display = dict(ROLE_CHOICES)

            if role_filter:
                role_upper = role_filter.strip().upper()
                if role_upper in valid_role_codes:
                    role_code = role_upper
                else:
                    for code, name in ROLE_CHOICES:
                        if role_upper in name.upper() or role_upper in code:
                            role_code = code
                            break
                    else:
                        return Response({
                            "error": "Validation Error",
                            "message": f"Invalid role: '{role_filter}'. Valid options: {', '.join(valid_role_codes)}"
                        }, status=status.HTTP_400_BAD_REQUEST)

            # --- 4. Date Range Logic & Validation ---
            try:
                # Fallback to project dates or today if not provided
                start_date = (datetime.strptime(start_str, "%Y-%m-%d").date() 
                              if start_str else (project.start_monday or timezone.now().date()))
                
                end_date = (datetime.strptime(end_str, "%Y-%m-%d").date() 
                            if end_str else (project.end_monday or (start_date + timedelta(weeks=52))))
            except (ValueError, TypeError) as e:
                return Response({
                    "error": "Validation Error",
                    "message": f"Invalid date format. Use YYYY-MM-DD: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Align to Mondays
            start_monday = start_date - timedelta(days=start_date.weekday())
            end_monday = end_date - timedelta(days=end_date.weekday())

            mondays = []
            current = start_monday
            while current <= end_monday:
                mondays.append(current)
                current += timedelta(days=7)

            # --- 5. Query & Aggregation ---
            qs = ResourceAllocation.objects.filter(
                project=project,
                week_monday__in=mondays
            )

            if role_code:
                qs = qs.filter(resource__role=role_code)

            data = qs.values("resource__role", "week_monday").annotate(
                internal=Sum(
                    Case(When(resource__is_internal=True, then=F("hours")), default=0, output_field=IntegerField())
                ),
                external=Sum(
                    Case(When(resource__is_internal=False, then=F("hours")), default=0, output_field=IntegerField())
                ),
            ).order_by("week_monday")

            # --- 6. Build Result ---
            result = []
            for item in data:
                role = item["resource__role"]
                week = item["week_monday"]
                int_h = float(item["internal"] or 0)
                ext_h = float(item["external"] or 0)
                
                result.append({
                    "role": role,
                    "role_name": role_display.get(role, "Unknown"),
                    "week_monday": str(week),
                    "calendar_week": f"CW{week.isocalendar()[1]:02d}",
                    "week_display": week.strftime("%b %d"),
                    "actual_hours": {
                        "internal": round(int_h, 1),
                        "external": round(ext_h, 1),
                        "total": round(int_h + ext_h, 1),
                    },
                })

            # Fill missing weeks with zeros if a specific role was requested
            if not result and role_code:
                for monday in mondays:
                    result.append({
                        "role": role_code,
                        "role_name": role_display.get(role_code, "Unknown"),
                        "week_monday": str(monday),
                        "calendar_week": f"CW{monday.isocalendar()[1]:02d}",
                        "week_display": monday.strftime("%b %d"),
                        "actual_hours": {"internal": 0.0, "external": 0.0, "total": 0.0},
                    })

            result.sort(key=lambda x: (x["week_monday"], x["role"]))

            return Response({
                "project": {
                    "code": project.project_code,
                    "name": project.name,
                    "department": project.department.get_full_path() if (project.department and hasattr(project.department, 'get_full_path')) else str(project.department),
                },
                "filtered_role": role_code,
                "date_range": {"start": str(start_monday), "end": str(end_monday)},
                "data": result
            })

        except Exception as e:
            logger.exception("Project Role Utilization calculation failed")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# =============================================================================
# Internal Resource Utilization
# =============================================================================
# ———————————————————Internal Resource Utilization BREAKDOWN  ———————————————————


class InternalResourceUtilizationView(APIView):
    """
    Weekly utilization of internal resources + projects they worked on
    """
    permission_classes = [ModuleViewPermission]

    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            # --- 1. Query Parameters ---
            department_filter = request.query_params.get("department")
            resource_filter = request.query_params.get("resource")
            start_str = request.query_params.get("start")
            end_str = request.query_params.get("end")

            # --- 2. Date Range Logic & Validation ---
            today = timezone.now().date()
            default_start = today - timedelta(days=today.weekday()) - timedelta(weeks=26)
            default_end = default_start + timedelta(weeks=52)

            try:
                start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else default_start
                end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else default_end
            except (ValueError, TypeError) as e:
                return Response({
                    "error": "Validation Error",
                    "message": f"Invalid date format. Use YYYY-MM-DD: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

            start_monday = start_date - timedelta(days=start_date.weekday())
            end_monday = end_date - timedelta(days=end_date.weekday())

            mondays = []
            current = start_monday
            while current <= end_monday:
                mondays.append(current)
                current += timedelta(days=7)

            # --- 3. Base Query (Resources) ---
            resource_qs = Resource.objects.filter(is_internal=True, is_active=True).select_related('department')

            if department_filter:
                try:
                    dept_id = int(department_filter)
                    dept = Department.objects.get(id=dept_id)
                    descendants = dept.get_descendants(include_self=True)
                    resource_qs = resource_qs.filter(department__in=descendants)
                except (ValueError, Department.DoesNotExist):
                    resource_qs = resource_qs.filter(department__name__icontains=department_filter)

            if resource_filter:
                resource_qs = resource_qs.filter(name__icontains=resource_filter)

            # Convert to list and build a map for quick lookup (prevents N+1 queries)
            resources = list(resource_qs)
            resource_map = {r.id: r for r in resources}

            # --- 4. Allocations Query ---
            allocations = ResourceAllocation.objects.filter(
                resource__in=resources,
                week_monday__in=mondays
            ).select_related(
                'project', 'resource', 'resource__department'
            ).values(
                'resource__id',
                'resource__name',
                'resource__role',
                'resource__department__name',
                'week_monday',
                'project__project_code',
                'project__name',
                'hours'
            ).order_by('week_monday', 'resource__name')

            # --- 5. Data Processing ---
            weekly_data = {}
            # Assuming ROLE_CHOICES is available
            role_display = dict(ROLE_CHOICES) if 'ROLE_CHOICES' in globals() else {}

            for alloc in allocations:
                res_id = alloc['resource__id']
                week = alloc['week_monday']
                key = (res_id, week)

                if key not in weekly_data:
                    # SAFETY: Get department path from pre-loaded resource_map
                    res_obj = resource_map.get(res_id)
                    dept_path = "Unassigned"
                    if res_obj and res_obj.department:
                        # Handle both MPTT and standard models
                        dept_path = getattr(res_obj.department, 'get_full_path', lambda: res_obj.department.name)()

                    weekly_data[key] = {
                        "resource_id": res_id,
                        "resource_name": alloc['resource__name'],
                        "role": alloc['resource__role'],
                        "role_name": role_display.get(alloc['resource__role'], "Unknown"),
                        "department": dept_path,
                        "week_monday": str(week),
                        "calendar_week": f"CW{week.isocalendar()[1]:02d}",
                        "week_display": week.strftime("%b %d"),
                        "available_hours": 0.0,
                        "allocated_hours": 0.0,
                        "projects": [],
                    }

                item = weekly_data[key]
                alloc_h = float(alloc['hours'] or 0)
                item["allocated_hours"] += alloc_h

                # Add project details
                proj_code = alloc['project__project_code'] or "N/A"
                existing_proj = next((p for p in item["projects"] if p["project_code"] == proj_code), None)
                
                if not existing_proj:
                    item["projects"].append({
                        "project_code": proj_code,
                        "project_name": alloc['project__name'] or "Unknown Project",
                        "hours": round(alloc_h, 1)
                    })
                else:
                    existing_proj["hours"] = round(existing_proj["hours"] + alloc_h, 1)

            # --- 6. Fill Availability & Build Result ---
            result = []
            for resource in resources:
                avail = float(getattr(resource, 'effective_availability_per_week', 0) or 0)

                for monday in mondays:
                    key = (resource.id, monday)
                    if key in weekly_data:
                        item = weekly_data[key]
                        item["available_hours"] = round(avail, 1)
                        allocated = float(item["allocated_hours"] or 0)
                        item["allocated_hours"] = round(allocated, 1)
                        
                        item["utilization_pct"] = round((allocated / avail) * 100, 1) if avail > 0 else 0.0
                        item["over_allocated"] = allocated > avail
                        item["under_allocated"] = allocated < (avail * 0.8)
                        item["gap_hours"] = round(allocated - avail, 1)
                        result.append(item)
                    else:
                        # No allocation this week: build empty entry
                        dept_obj = resource.department
                        dept_path = getattr(dept_obj, 'get_full_path', lambda: dept_obj.name)() if dept_obj else "Unassigned"
                        
                        result.append({
                            "resource_id": resource.id,
                            "resource_name": resource.name,
                            "role": resource.role,
                            "role_name": role_display.get(resource.role, "Unknown"),
                            "department": dept_path,
                            "week_monday": str(monday),
                            "calendar_week": f"CW{monday.isocalendar()[1]:02d}",
                            "week_display": monday.strftime("%b %d"),
                            "available_hours": round(avail, 1),
                            "allocated_hours": 0.0,
                            "utilization_pct": 0.0,
                            "over_allocated": False,
                            "under_allocated": True,
                            "gap_hours": round(-avail, 1),
                            "projects": []
                        })

            # Sort by week, then department, then name
            result.sort(key=lambda x: (x["week_monday"], x["department"], x["resource_name"]))

            return Response({
                "date_range": {"start": str(start_monday), "end": str(end_monday)},
                "filters": {
                    "department": department_filter,
                    "resource": resource_filter
                },
                "total_resources_shown": len(resources),
                "data": result
            })

        except Exception as e:
            logger.exception("Internal Resource Utilization report failed")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepartmentWeeklyDetailView(APIView):
    """
    Department weekly capacity & utilization breakdown (project-level detail)
    """
    permission_classes = [ModuleViewPermission]

    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            dept_filter = request.query_params.get("department")
            start_str = request.query_params.get("start")
            end_str = request.query_params.get("end")

            # === 1. Date Range Logic & Validation ===
            today = timezone.now().date()
            current_monday = today - timedelta(days=today.weekday())

            if start_str and end_str:
                try:
                    start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
                    end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
                except ValueError as e:
                    return Response({
                        "error": "Validation Error",
                        "message": f"Invalid date format. Use YYYY-MM-DD: {str(e)}"
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                if start_date > end_date:
                    start_date, end_date = end_date, start_date
            else:
                start_date = current_monday - timedelta(weeks=26)
                end_date = current_monday + timedelta(weeks=26)

            # Align to Mondays
            start_monday = start_date + timedelta(days=(7 - start_date.weekday()) % 7)
            if start_monday < start_date:
                start_monday += timedelta(days=7)
            end_monday = end_date - timedelta(days=end_date.weekday())

            mondays = []
            current = start_monday
            while current <= end_monday:
                mondays.append(current)
                current += timedelta(days=7)

            # === 2. Department Filter Validation ===
            descendants = []
            dept_q = Q()

            if dept_filter:
                dept_filter = dept_filter.strip()
                dept = None
                try:
                    # Try ID first
                    if dept_filter.isdigit():
                        dept = Department.objects.get(id=int(dept_filter))
                except Department.DoesNotExist:
                    pass

                if not dept:
                    try:
                        # Try Name match
                        dept = Department.objects.get(name__iexact=dept_filter)
                    except (Department.DoesNotExist, Department.MultipleObjectsReturned):
                        return Response({
                            "error": "Not Found",
                            "message": f"Department '{dept_filter}' not found or matches multiple records."
                        }, status=status.HTTP_404_NOT_FOUND)

                descendants = [dept] + list(dept.get_descendants())
                dept_q = Q(project__department__in=descendants)

            # === 3. Load & Process Data ===
            internal_qs = ResourceAllocation.objects.filter(week_monday__range=(start_monday, end_monday))
            if dept_filter: internal_qs = internal_qs.filter(dept_q)
            internal_data = internal_qs.values(
                'project__project_code', 'project__name', 'project__department__name', 'week_monday'
            ).annotate(internal_hours=Sum('hours', default=0))

            external_qs = ExternalCapacity.objects.filter(week_monday__range=(start_monday, end_monday))
            if dept_filter: external_qs = external_qs.filter(dept_q)
            external_data = external_qs.values(
                'project__project_code', 'project__name', 'project__department__name', 'week_monday'
            ).annotate(external_hours=Sum('hours', default=0))

            planned_qs = ProjectWeekAllocation.objects.filter(week_monday__range=(start_monday, end_monday))
            if dept_filter: planned_qs = planned_qs.filter(dept_q)

            # Build planned map
            planned_dict = {}
            project_codes = set()
            for alloc in planned_qs:
                if not alloc.project: continue
                code = alloc.project.project_code
                week = alloc.week_monday
                planned_dict[(code, week)] = float(alloc.manhours or 0)
                if code: project_codes.add(code)

            # Build project cache
            project_cache = {}
            if project_codes:
                qs = Project.objects.filter(project_code__in=project_codes).select_related('department')
                for p in qs:
                    project_cache[p.project_code] = p

            # === 4. Capacity Logic ===
            available_dict = defaultdict(lambda: defaultdict(float))
            resource_filter_q = Q(is_internal=True, is_active=True)
            if descendants:
                resource_filter_q &= Q(departments__in=descendants)

            resources = Resource.objects.filter(resource_filter_q).prefetch_related('departments').distinct()

            for res in resources:
                if not res.joining_date: continue
                
                # Use first department as primary grouping for capacity
                first_dept = res.departments.first()
                dept_name = first_dept.name if first_dept else "Unknown"
                capacity = float(res.effective_availability_per_week or 45)

                for monday in mondays:
                    if res.joining_date <= monday:
                        available_dict[dept_name][monday] += capacity

            # === 5. Aggregation & Formatting ===
            dept_weekly_used = defaultdict(lambda: defaultdict(float))
            dept_weekly_planned = defaultdict(lambda: defaultdict(float))
            combined = defaultdict(lambda: {"internal": 0.0, "external": 0.0, "planned": 0.0})

            # Process Internal
            for item in internal_data:
                d_name = item['project__department__name'] or "Unknown"
                w = item['week_monday']
                code = item['project__project_code']
                hrs = float(item['internal_hours'] or 0)
                
                dept_weekly_used[d_name][w] += hrs
                combined[(d_name, w, code)]["internal"] += hrs

            # Process External
            for item in external_data:
                d_name = item['project__department__name'] or "Unknown"
                w = item['week_monday']
                code = item['project__project_code']
                hrs = float(item['external_hours'] or 0)

                dept_weekly_used[d_name][w] += hrs
                combined[(d_name, w, code)]["external"] += hrs

            # Process Planned
            for (code, week), manhours in planned_dict.items():
                proj = project_cache.get(code)
                d_name = proj.department.name if proj and proj.department else "Unknown"
                val = float(manhours or 0)
                dept_weekly_planned[d_name][week] += val
                combined[(d_name, week, code)]["planned"] = val

            # === 6. Final Result Build ===
            result = []
            for (dept_name, week, code), vals in combined.items():
                total_dept_used = dept_weekly_used[dept_name][week]
                total_planned = dept_weekly_planned[dept_name][week]
                available = available_dict[dept_name][week]
                
                # Logic check: Free capacity is at Department level
                free_cap = max(0.0, available - total_dept_used)
                proj_obj = project_cache.get(code)

                result.append({
                    "department": dept_name,
                    "week_monday": week.isoformat(),
                    "calendar_week": f"CW{week.isocalendar()[1]:02d}",
                    "project_code": code,
                    "project_name": proj_obj.name if proj_obj else "Unknown Project",
                    "manhours": round(total_planned, 1),
                    "data": {
                        "internal": round(vals["internal"], 1),
                        "external": round(vals["external"], 1),
                        "total_used": round(vals["internal"] + vals["external"], 1),
                        "available_capacity": round(available, 1),
                        "free_capacity": round(free_cap, 1)
                    }
                })

            result.sort(key=lambda x: (x["week_monday"], x["department"], x["project_code"]))

            return Response({
                "period": {
                    "start_monday": start_monday.isoformat(),
                    "end_monday": end_monday.isoformat(),
                    "weeks_count": len(mondays)
                },
                "data": result
            })

        except Exception as e:
            logger.exception("Weekly Detail Report Generation Failed")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class DepartmentWeeklyDetailView_byDeptId(APIView):
    """
    Returns weekly capacity & utilization detail per project.
    
    - For parent departments: aggregates (sums) values across all descendants
      → one row per project per week
      → department name = parent name
    - For leaf departments: detailed view per department
    """
    permission_classes = [ModuleViewPermission]   # ← change this line

    def get_permissions(self):
        # We need to tell it which module → we do it here
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request, department_id=None):
        # department_id is now from URL path (required for this endpoint)
        if department_id is None:
            return Response({"error": "Department ID is required in URL path"}, status=400)

        # === 1. Date Range ===
        today = timezone.now().date()
        days_to_monday = today.weekday()
        current_monday = today - timedelta(days=days_to_monday)

        start_str = request.query_params.get("start")
        end_str = request.query_params.get("end")

        if start_str and end_str:
            try:
                start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
            if start_date > end_date:
                start_date, end_date = end_date, start_date
        else:
            start_date = current_monday - timedelta(weeks=26)
            end_date = current_monday + timedelta(weeks=26)

        start_monday = start_date + timedelta(days=(7 - start_date.weekday()) % 7)
        if start_monday < start_date:
            start_monday += timedelta(days=7)

        end_monday = end_date - timedelta(days=end_date.weekday())

        mondays = []
        current = start_monday
        while current <= end_monday:
            mondays.append(current)
            current += timedelta(days=7)

        # === 2. Department Filter – Now uses department_id from URL ===
        descendants = []
        dept_q = Q()

        try:
            dept = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return Response({"error": f"Department with ID {department_id} not found."}, status=404)

        descendants = [dept] + dept.get_descendants()
        dept_ids = [d.id for d in descendants]
        is_parent_view = len(descendants) > 1
        # === 3. Load department-specific allocations (NEW source of truth) ===
        dept_allocs = ProjectDepartmentAllocation.objects.filter(
            department__id__in=dept_ids
        ).select_related('project', 'department')

        # Map: (project_id, dept_id) → allocation for fast lookup
        alloc_map = {(a.project_id, a.department_id): a for a in dept_allocs}

        project_ids = list(set(a.project_id for a in dept_allocs))

        # === 4. Load Data (updated to use department context) ===
        internal_qs = ResourceAllocation.objects.filter(week_monday__range=(start_monday, end_monday))
        internal_qs = internal_qs.filter(department__id__in=dept_ids)
        internal_data = internal_qs.values(
            'project_id', 'department_id', 'week_monday'
        ).annotate(internal_hours=Sum('hours', default=0))

        external_qs = ExternalCapacity.objects.filter(week_monday__range=(start_monday, end_monday))
        external_qs = external_qs.filter(project_id__in=project_ids)
        external_data = external_qs.values(
            'project_id', 'week_monday'
        ).annotate(external_hours=Sum('hours', default=0))

        planned_qs = ProjectWeekAllocation.objects.filter(week_monday__range=(start_monday, end_monday))
        planned_qs = planned_qs.filter(department__id__in=dept_ids)
        planned_data = planned_qs.values(
            'project_id', 'department_id', 'week_monday', 'manhours'
        )

        # === 5. Time-Aware Capacity – unchanged ===
        available_dict = defaultdict(lambda: defaultdict(float))

        resources = Resource.objects.filter(
            is_internal=True,
            # is_active=True,
            departments__id__in=dept_ids
        ).distinct()

        for res in resources:
            if not res.joining_date:
                continue

            dept_name = res.departments.first().name if res.departments.exists() else "Unknown"
            capacity = float(res.effective_availability_per_week or 45)

            joining_monday = None
            if res.joining_date:
                joining_monday = res.joining_date - timedelta(days=res.joining_date.weekday())

            leaving_monday = None
            if res.leaving_date:
                leaving_monday = res.leaving_date - timedelta(days=res.leaving_date.weekday())
            # for monday in mondays:
            #     if res.joining_date <= monday:
            #         available_dict[dept_name][monday] += capacity

            for monday in mondays:
                week_end = monday + timedelta(days=6)

                has_joined = joining_monday <= monday
                is_still_active = True

                if res.leaving_date:
                    # Employee contributes capacity until the end of the week they leave
                    is_still_active = leaving_monday > monday 
                if has_joined and is_still_active:
                    available_dict[dept_name][monday] += capacity

        # === 6. Department-level totals – updated source ===
        dept_weekly_used = defaultdict(lambda: defaultdict(float))
        dept_weekly_planned = defaultdict(lambda: defaultdict(float))

        # Internal & external
        for item in internal_data:
            dept = Department.objects.get(id=item['department_id'])
            dept_name = dept.name
            week = item['week_monday']
            dept_weekly_used[dept_name][week] += float(item['internal_hours'])

        for item in external_data:
            # External is project-level → add to every dept that has this project
            proj_id = item['project_id']
            week = item['week_monday']
            depts_with_proj = [
                d.name for d in descendants
                if (proj_id, d.id) in alloc_map
            ]
            if depts_with_proj:
                share = float(item['external_hours']) / len(depts_with_proj)
                for dname in depts_with_proj:
                    # dept_weekly_used[dname][week] += share
                    pass

        # Planned (from ProjectWeekAllocation)
        for item in planned_data:
            dept = Department.objects.get(id=item['department_id'])
            dept_name = dept.name
            week = item['week_monday']
            dept_weekly_planned[dept_name][week] += float(item['manhours'])

        # === 7. Combine per-project data – updated source ===
        combined = defaultdict(lambda: {"internal": 0.0, "external": 0.0, "planned": 0.0})
        for item in internal_data:
            dept = Department.objects.get(id=item['department_id'])
            dept_name = dept.name
            proj_id = item['project_id']
            week = item['week_monday']
            key = (dept_name, week, proj_id)
            combined[key]["internal"] += float(item['internal_hours'])

        for item in external_data:
            proj_id = item['project_id']
            week = item['week_monday']
            depts_with_proj = [
                d.name for d in descendants
                if (proj_id, d.id) in alloc_map
            ]
            if depts_with_proj:
                share = float(item['external_hours']) / len(depts_with_proj)
                for dname in depts_with_proj:
                    key = (dname, week, proj_id)
                    combined[key]["external"] += share

        for item in planned_data:
            dept = Department.objects.get(id=item['department_id'])
            dept_name = dept.name
            proj_id = item['project_id']
            week = item['week_monday']
            key = (dept_name, week, proj_id)
            combined[key]["planned"] += float(item['manhours'])
        # 8. Build response
        result = []

        if is_parent_view:
            # PARENT VIEW: one row per unique project per week
            # manhours = total planned in the week (across all projects & sub-depts)
            # available/free = week-level hierarchy totals
            # internal/external/total_used = summed per project across sub-depts

            # 1. Week-level totals (same for all rows in the week)
            week_totals = {}
            for week in mondays:
                # Total planned manhours in this week (all projects, all sub-departments)
                total_planned_this_week = sum(
                    vals["planned"]
                    for (_, w, _) , vals in combined.items()
                    if w == week
                )

                # Total available capacity in this week (sum across all sub-departments)
                total_available = sum(
                    available_dict[dname][week]
                    for dname in available_dict
                )

                # Total used in this week (all projects, all sub-departments)
                total_used_this_week = sum(
                    dept_weekly_used[dname][week]
                    for dname in dept_weekly_used
                )

                week_totals[week] = {
                    "manhours": total_planned_this_week,
                    "available_capacity": total_available,
                    "free_capacity": max(0.0, total_available - total_used_this_week)
                }

            # 2. Per-project per-week sums (for internal/external/total_used)
            project_week_sums = defaultdict(lambda: {
                "internal": 0.0,
                "external": 0.0
            })

            for (_, week, proj_id), vals in combined.items():
                key = (week, proj_id)
                project_week_sums[key]["internal"] += vals["internal"]
                project_week_sums[key]["external"] += vals["external"]

            # 3. Build rows: one per unique (week, project)
            for (week, proj_id), sums in project_week_sums.items():
                try:
                    proj = Project.objects.get(id=proj_id)
                except Project.DoesNotExist:
                    continue

                wt = week_totals[week]

                result.append({
                    "department": dept.name,  # parent name, e.g. "Design Engineering"
                    "week_monday": week.isoformat(),
                    "calendar_week": f"CW{week.isocalendar()[1]:02d}",
                    "project_code": proj.project_code,
                    "project_name": proj.name or "Unknown Project",
                    "project_color": proj.color_code or "#cccccc",
                    "manhours": round(wt["manhours"], 1),  # total planned in the whole week
                    "data": {
                        "internal": round(sums["internal"], 1),          # summed for this project
                        "external": round(sums["external"], 1),          # summed for this project
                        "total_used": round(sums["internal"] + sums["external"], 1),
                        "available_capacity": round(wt["available_capacity"], 1),
                        "free_capacity": round(wt["free_capacity"], 1)
                    }
                })

        else:
            for (dept_name, week, proj_id), vals in combined.items():
                this_project_used = vals["internal"] + vals["external"]
                total_dept_used = dept_weekly_used[dept_name][week]
                total_planned = dept_weekly_planned[dept_name][week]

                available = available_dict[dept_name][week]
                free_capacity = max(0.0, available - dept_weekly_used[dept_name][week])

                proj = Project.objects.get(id=proj_id)

                # Get estimated_manhours from allocation
                alloc = alloc_map.get((proj_id, dept.id))
                estimated_manhours = alloc.estimated_manhours if alloc else 0

                result.append({
                    "department": dept_name,
                    "week_monday": week.isoformat(),
                    "calendar_week": f"CW{week.isocalendar()[1]:02d}",
                    "project_code": proj.project_code,
                    "project_name": proj.name if proj else "Unknown Project",
                    "project_color":proj.color_code,
                    "manhours": round(total_planned, 1),
                    "data": {
                        "internal": round(vals["internal"], 1),
                        "external": round(vals["external"], 1),
                        "total_used": round(this_project_used, 1),
                        "available_capacity": round(available, 1),
                        "free_capacity": round(free_capacity, 1)
                    }
                })

        result.sort(key=lambda x: (x["week_monday"], x["department"], x["project_code"]))

        return Response({
            "period": {
                "start_monday": start_monday.isoformat(),
                "end_monday": end_monday.isoformat(),
                "weeks_count": len(mondays)
            },
            "data": result
        })


class EmployeeSummaryView(APIView):
    permission_classes = [ModuleViewPermission]

    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            # --- 1. Query Parameters ---
            dept_filter = request.query_params.get("department")
            resource_filter = request.query_params.get("resource")
            start_str = request.query_params.get("start")
            end_str = request.query_params.get("end")
            active_only = request.query_params.get("active_only", "true").lower() == "true"
            graph = request.query_params.get("graph", "false").lower() == "true"

            # --- 2. Load Settings Safely ---
            try:
                settings_obj = AppSettings.load()
                default_weekly_hours = getattr(settings_obj, 'default_working_hours_per_week', 45)
            except Exception:
                default_weekly_hours = 45  # Hard fallback

            # --- 3. Date Range Validation ---
            today = timezone.now().date()
            try:
                start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else today - timedelta(weeks=26)
                end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else today + timedelta(weeks=26)
            except (ValueError, TypeError) as e:
                return Response({
                    "error": "Validation Error",
                    "message": f"Invalid date format. Use YYYY-MM-DD: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

            if start_date > end_date:
                start_date, end_date = end_date, start_date

            start_monday = start_date - timedelta(days=start_date.weekday())
            end_monday = end_date - timedelta(days=end_date.weekday())

            mondays = []
            current = start_monday
            while current <= end_monday:
                mondays.append(current)
                current += timedelta(days=7)

            # --- 4. Resource Filtering ---
            resources_qs = Resource.objects.filter(is_internal=True)
            if active_only:
                resources_qs = resources_qs.filter(is_active=True)

            if dept_filter:
                dept_filter = dept_filter.strip()
                try:
                    dept_id = int(dept_filter)
                    dept = Department.objects.get(id=dept_id)
                    descendants = list(dept.get_descendants()) + [dept]
                    resources_qs = resources_qs.filter(department__in=descendants)
                except (ValueError, Department.DoesNotExist):
                    resources_qs = resources_qs.filter(department__name__iexact=dept_filter)

            if resource_filter:
                resource_filter = resource_filter.strip()
                try:
                    resource_id = int(resource_filter)
                    resources_qs = resources_qs.filter(id=resource_id)
                except ValueError:
                    resources_qs = resources_qs.filter(name__icontains=resource_filter)

            resources = resources_qs.select_related('department')
            
            # --- 5. Data Fetching & Aggregation ---
            allocations = ResourceAllocation.objects.filter(
                week_monday__in=mondays,
                resource__in=resources
            ).select_related('resource', 'project')

            resource_dates = {}
            employee_data = defaultdict(lambda: defaultdict(lambda: {"allocated": 0.0, "projects": {}}))

            for alloc in allocations:
                res_id = alloc.resource.id
                week = alloc.week_monday
                hours = float(alloc.hours or 0)
                proj = alloc.project

                # Track specific active dates for this resource
                if res_id not in resource_dates:
                    resource_dates[res_id] = {'start_date': week, 'end_date': week}
                else:
                    resource_dates[res_id]['start_date'] = min(resource_dates[res_id]['start_date'], week)
                    resource_dates[res_id]['end_date'] = max(resource_dates[res_id]['end_date'], week)

                # Aggregate hours
                week_data = employee_data[res_id][week]
                week_data["allocated"] += hours

                if proj:
                    proj_code = proj.project_code or "N/A"
                    if proj_code not in week_data["projects"]:
                        week_data["projects"][proj_code] = {
                            "code": proj_code,
                            "name": proj.name or "Unknown",
                            "status": proj.get_status_display() if hasattr(proj, 'get_status_display') else "N/A",
                            "hours": 0.0
                        }
                    week_data["projects"][proj_code]["hours"] += hours

            # --- 6. Build Final Result ---
            result = []
            # Assuming ROLE_CHOICES is defined globally
            role_display = dict(ROLE_CHOICES) if 'ROLE_CHOICES' in globals() else {}

            for res in resources:
                weekly_capacity = float(res.effective_availability_per_week or default_weekly_hours)
                weeks_list = []
                total_allocated = 0.0

                for monday in mondays:
                    data = employee_data[res.id][monday]
                    allocated = float(data["allocated"])

                    if not graph and allocated == 0 and not data["projects"]:
                        continue

                    total_allocated += allocated
                    projects = [
                        {
                            "project_code": p["code"],
                            "project_name": p["name"],
                            "status": p["status"],
                            "allocation_hours": round(p["hours"], 1)
                        }
                        for p in data["projects"].values()
                    ]

                    weeks_list.append({
                        "week_monday": str(monday),
                        "calendar_week": f"CW{monday.isocalendar()[1]:02d}",
                        "allocated_hours": round(allocated, 1),
                        "capacity_hours": round(weekly_capacity, 1),
                        "utilization_pct": round((allocated / weekly_capacity) * 100, 1) if weekly_capacity > 0 else 0.0,
                        "free_capacity": round(max(0.0, weekly_capacity - allocated), 1),
                        "is_overallocated": allocated > weekly_capacity,
                        "projects": projects
                    })

                # Calculate Averages
                total_capacity = len(mondays) * weekly_capacity
                avg_util = round((total_allocated / total_capacity) * 100, 1) if total_capacity > 0 else 0.0

                result.append({
                    "employee_id": res.id,
                    "employee": res.name,
                    "role": res.role,
                    "role_name": role_display.get(res.role, "Unknown"),
                    "department": res.department.name if res.department else "Unassigned",
                    "department_full_path": res.department.get_full_path() if (res.department and hasattr(res.department, 'get_full_path')) else "Unassigned",
                    "joining_date": str(res.joining_date) if res.joining_date else None,
                    "start_date": str(resource_dates.get(res.id, {}).get('start_date', start_monday)),
                    "end_date": str(resource_dates.get(res.id, {}).get('end_date', end_monday)),
                    "weekly_capacity": round(weekly_capacity, 1),
                    "weeks": weeks_list,
                    "total_allocated_in_period": round(total_allocated, 1),
                    "average_utilization_pct": avg_util,
                    "overall_free_capacity": round(total_capacity - total_allocated, 1)
                })

            result.sort(key=lambda x: (x["department"], x["employee"]))

            return Response({
                "generated_at": timezone.now().isoformat(),
                "date_range": {
                    "start": str(start_monday),
                    "end": str(end_monday),
                    "weeks": len(mondays)
                },
                "total_employees": len(result),
                "data": result
            })

        except Exception as e:
            logger.exception("Employee Summary report generation failed")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectSummaryView(APIView):
    """
    Project Summary — Department-wise and Project-wise
    """
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # --- 1. Parameter Extraction ---
            dept_filter = request.query_params.get("department")
            project_filter = request.query_params.get("project")
            start_str = request.query_params.get("start")
            end_str = request.query_params.get("end")
            graph = request.query_params.get("graph", "false").lower() == "true"

            # --- 2. Load Settings Safely ---
            try:
                settings_obj = AppSettings.load()
                max_weekly_hours = getattr(settings_obj, 'default_working_hours_per_week', 45)
            except Exception:
                max_weekly_hours = 45

            # --- 3. Date Range Logic & Validation ---
            today = timezone.now().date()
            try:
                start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else today - timedelta(weeks=26)
                end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else today + timedelta(weeks=26)
            except (ValueError, TypeError) as e:
                return Response({
                    "error": "Validation Error",
                    "message": f"Invalid date format. Use YYYY-MM-DD: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

            if start_date > end_date:
                start_date, end_date = end_date, start_date

            # Align to Mondays
            start_monday = start_date + timedelta(days=(7 - start_date.weekday()) % 7)
            if start_monday < start_date:
                start_monday += timedelta(days=7)
            end_monday = end_date - timedelta(days=end_date.weekday())

            mondays = []
            current = start_monday
            while current <= end_monday:
                mondays.append(current)
                current += timedelta(days=7)

            # --- 4. Department & Project Filtering ---
            descendants = []
            if dept_filter:
                dept_filter = dept_filter.strip()
                dept = None
                try:
                    if dept_filter.isdigit():
                        dept = Department.objects.get(id=int(dept_filter))
                except (ValueError, Department.DoesNotExist):
                    pass
                
                if not dept:
                    try:
                        dept = Department.objects.get(name__iexact=dept_filter)
                    except (Department.DoesNotExist, Department.MultipleObjectsReturned):
                        return Response({
                            "error": "Not Found",
                            "message": f"Department '{dept_filter}' not found."
                        }, status=status.HTTP_404_NOT_FOUND)

                descendants = [dept] + list(dept.get_descendants())

            # Project Filter Logic
            project_ids = []
            if project_filter:
                project_filter = project_filter.strip()
                project_obj = None
                try:
                    if project_filter.isdigit():
                        project_obj = Project.objects.get(id=int(project_filter))
                except (ValueError, Project.DoesNotExist):
                    pass
                
                if not project_obj:
                    try:
                        project_obj = Project.objects.get(project_code__iexact=project_filter)
                    except (Project.DoesNotExist, Project.MultipleObjectsReturned):
                        return Response({
                            "error": "Not Found",
                            "message": f"Project '{project_filter}' not found."
                        }, status=status.HTTP_404_NOT_FOUND)
                
                if project_obj:
                    project_ids = [project_obj.id]

            # --- 5. Project & Allocation Queries ---
            projects_qs = Project.objects.all()
            if descendants:
                projects_qs = projects_qs.filter(department__in=descendants)
            if project_ids:
                projects_qs = projects_qs.filter(id__in=project_ids)

            projects = list(projects_qs.select_related('department'))

            # Map Data in memory to prevent N+1
            planned_dict = {}
            for p in ProjectWeekAllocation.objects.filter(project__in=projects, week_monday__in=mondays):
                planned_dict[(p.project_id, p.week_monday)] = float(p.manhours or 0)

            internal_dict = defaultdict(float)
            for a in ResourceAllocation.objects.filter(project__in=projects, week_monday__in=mondays, resource__is_internal=True):
                internal_dict[(a.project_id, a.week_monday)] += float(a.hours or 0)

            external_dict = defaultdict(float)
            for e in ExternalCapacity.objects.filter(project__in=projects, week_monday__in=mondays):
                external_dict[(e.project_id, e.week_monday)] += float(e.hours or 0)

            # --- 6. Available Capacity Logic ---
            available_dict = defaultdict(float)
            res_qs = Resource.objects.filter(is_internal=True, is_active=True)
            if descendants:
                res_qs = res_qs.filter(departments__in=descendants).distinct()

            for res in res_qs.prefetch_related('departments'):
                dept = res.departments.first()
                # Use the full path as key to match project department path
                dept_path = dept.get_full_path() if (dept and hasattr(dept, 'get_full_path')) else "Unknown"
                capacity = float(res.effective_availability_per_week or max_weekly_hours)

                for monday in mondays:
                    if res.joining_date and res.joining_date <= monday:
                        available_dict[(dept_path, monday)] += capacity

            # --- 7. Build Result ---
            result = []
            for proj in projects:
                dept_path = proj.department.get_full_path() if (proj.department and hasattr(proj.department, 'get_full_path')) else "Unknown"
                dept_name = proj.department.name if proj.department else "Unknown"

                weeks_data = []
                t_planned = t_internal = t_external = t_available = 0.0

                for monday in mondays:
                    key = (proj.id, monday)
                    planned = float(planned_dict.get(key, 0.0))
                    internal = float(internal_dict.get(key, 0.0))
                    external = float(external_dict.get(key, 0.0))
                    total_used = internal + external
                    available = float(available_dict.get((dept_path, monday), 0.0))
                    
                    util_pct = round((total_used / available) * 100, 1) if available > 0 else 0.0

                    if graph or planned > 0 or total_used > 0:
                        weeks_data.append({
                            "week_monday": str(monday),
                            "calendar_week": f"CW{monday.isocalendar()[1]:02d}",
                            "planned_manhours": round(planned, 1),
                            "internal_hours": round(internal, 1),
                            "external_hours": round(external, 1),
                            "total_allocated": round(total_used, 1),
                            "available_capacity": round(available, 1),
                            "free_capacity": round(max(0.0, available - total_used), 1),
                            "utilization_pct": util_pct,
                            "is_overallocated": total_used > available,
                            "gap": round(planned - total_used, 1)
                        })

                    t_planned += planned
                    t_internal += internal
                    t_external += external
                    t_available += available

                t_allocated = t_internal + t_external
                overall_util = round((t_allocated / t_available) * 100, 1) if t_available > 0 else 0.0

                result.append({
                    "id": proj.id,
                    "project_code": proj.project_code,
                    "project_name": proj.name,
                    "status": (proj.get_status_display() or "N/A").upper(),
                    "department": dept_name,
                    "department_full_path": dept_path,
                    "total_manhours": round(float(proj.total_manhours or 0), 1),
                    "total_planned_manhours": round(t_planned, 1),
                    "total_internal_hours": round(t_internal, 1),
                    "total_external_hours": round(t_external, 1),
                    "total_allocated": round(t_allocated, 1),
                    "remaining_hours": round(max(0.0, (proj.total_manhours or 0) - t_planned), 1),
                    "total_available_capacity": round(t_available, 1),
                    "overall_utilization_pct": overall_util,
                    "weeks": weeks_data
                })

            result.sort(key=lambda x: (x["department_full_path"], x["project_code"]))

            return Response({
                "start_date": str(start_monday),
                "end_date": str(end_monday),
                "data": result
            })

        except Exception as e:
            logger.exception("Project Summary report failed")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProjectSummaryView_DeptId(APIView):
    permission_classes = [ModuleViewPermission]

    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request, department_id):
        try:
            # --- 1. Department Retrieval & Tree Resolution ---
            try:
                dept = Department.objects.get(id=department_id)
            except Department.DoesNotExist:
                return Response({
                    "error": "Not Found",
                    "message": f"Department {department_id} not found."
                }, status=status.HTTP_404_NOT_FOUND)

            descendants = [dept] + list(dept.get_descendants())
            dept_ids = [d.id for d in descendants]
            is_parent = len(descendants) > 1

            # --- 2. Query Parameters & Date Range Logic ---
            project_filter = request.query_params.get("project")
            start_str = request.query_params.get("start")
            end_str = request.query_params.get("end")

            try:
                settings_obj = AppSettings.load()
                max_weekly_hours = float(getattr(settings_obj, 'default_working_hours_per_week', 45))
            except Exception:
                max_weekly_hours = 45.0

            use_requested_range = bool(start_str and end_str)
            range_mondays = []
            range_start_monday = range_end_monday = None

            if use_requested_range:
                try:
                    start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
                    end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
                    if start_date > end_date:
                        start_date, end_date = end_date, start_date
                except (ValueError, TypeError) as e:
                    return Response({
                        "error": "Validation Error",
                        "message": f"Invalid date format: {str(e)}"
                    }, status=status.HTTP_400_BAD_REQUEST)

                range_start_monday = start_date + timedelta(days=(7 - start_date.weekday()) % 7)
                if range_start_monday < start_date:
                    range_start_monday += timedelta(days=7)
                range_end_monday = end_date - timedelta(days=end_date.weekday())

                current = range_start_monday
                while current <= range_end_monday:
                    range_mondays.append(current)
                    current += timedelta(days=7)

            # --- 3. Allocations & Data Fetching ---
            allocations_qs = ProjectDepartmentAllocation.objects.filter(
                department__in=descendants
            ).select_related('project', 'department')

            if project_filter:
                try:
                    project_obj = Project.objects.get(project_code__iexact=project_filter.strip())
                    allocations_qs = allocations_qs.filter(project=project_obj)
                except Project.DoesNotExist:
                    return Response({
                        "error": "Not Found",
                        "message": f"Project '{project_filter}' not found."
                    }, status=status.HTTP_404_NOT_FOUND)

            allocations = list(allocations_qs)
            if not allocations:
                return Response({"data": []})

            project_ids = list(set(alloc.project_id for alloc in allocations))

            planned_qs = ProjectWeekAllocation.objects.filter(
                project_id__in=project_ids,
                department_id__in=dept_ids
            )
            planned_dict = {(p.project_id, p.department_id, p.week_monday): float(p.manhours or 0) for p in planned_qs}

            internal_qs = ResourceAllocation.objects.filter(
                project_id__in=project_ids,
                department_id__in=dept_ids
            )
            internal_dict = defaultdict(float)
            for a in internal_qs:
                internal_dict[(a.project_id, a.department_id, a.week_monday)] += float(a.hours or 0)

            external_qs = ExternalCapacity.objects.filter(project_id__in=project_ids)
            external_dict = defaultdict(float)
            for e in external_qs:
                external_dict[(e.project_id, e.week_monday)] += float(e.hours or 0)

            # --- 4. Available Capacity Mapping ---
            available_dict = defaultdict(lambda: defaultdict(float))
            resources = Resource.objects.filter(
                is_internal=True, is_active=True, departments__id__in=dept_ids
            ).distinct().prefetch_related('departments')

            for res in resources:
                dept_obj = res.departments.first()
                dept_path = "Unknown"
                if dept_obj:
                    dept_path = getattr(dept_obj, 'get_full_path', lambda: dept_obj.name)()
                
                capacity = float(res.effective_availability_per_week or max_weekly_hours)

                for alloc in allocations:
                    alloc_start = alloc.start_monday
                    alloc_end = alloc.end_monday or (alloc.start_monday + timedelta(weeks=max(0, alloc.allotted_weeks - 1)))
                    
                    current_w = alloc_start - timedelta(days=alloc_start.weekday())
                    while current_w <= alloc_end:
                        if not res.joining_date or res.joining_date <= current_w:
                            available_dict[dept_path][current_w] += capacity
                        current_w += timedelta(days=7)

            # --- 5. Result Construction ---
            result = []
            project_groups = defaultdict(list)
            for alloc in allocations:
                project_groups[alloc.project_id].append(alloc)

            for project_id, allocs in project_groups.items():
                project = allocs[0].project
                num_depts = len(allocs)
                
                if num_depts == 1 or not is_parent:
                    alloc = allocs[0]
                    dept_name = alloc.department.name
                    dept_path = getattr(alloc.department, 'get_full_path', lambda: alloc.department.name)()
                else:
                    dept_name = "Multiple Departments"
                    dept_path = f"{dept.name} (Consolidated)"

                # Determine Monday range and Project boundaries
                p_min_start = min(a.start_monday for a in allocs)
                p_max_end = max(a.end_monday or (a.start_monday + timedelta(weeks=max(0, a.allotted_weeks - 1))) for a in allocs)
                
                if use_requested_range:
                    mondays = range_mondays
                else:
                    mondays = []
                    curr_m = p_min_start - timedelta(days=p_min_start.weekday())
                    while curr_m <= p_max_end:
                        mondays.append(curr_m)
                        curr_m += timedelta(days=7)

                weeks_data = []
                t_planned = t_internal = t_external = t_available = 0.0
                t_estimated = sum(float(a.estimated_manhours or 0) for a in allocs)

                for monday in mondays:
                    p_val = sum(planned_dict.get((project_id, a.department_id, monday), 0.0) for a in allocs)
                    i_val = sum(internal_dict.get((project_id, a.department_id, monday), 0.0) for a in allocs)
                    e_val = external_dict.get((project_id, monday), 0.0)
                    total_used = i_val + e_val
                    
                    avail_val = 0.0
                    seen_paths = set()
                    for a in allocs:
                        path = getattr(a.department, 'get_full_path', lambda: a.department.name)()
                        if path not in seen_paths:
                            avail_val += available_dict[path].get(monday, 0.0)
                            seen_paths.add(path)

                    util_pct = round((total_used / avail_val) * 100, 1) if avail_val > 0 else 0.0

                    weeks_data.append({
                        "week_monday": str(monday),
                        "calendar_week": f"CW{monday.isocalendar()[1]:02d}",
                        "planned_manhours": round(p_val, 1),
                        "internal_hours": round(i_val, 1),
                        "external_hours": round(e_val, 1),
                        "total_allocated": round(total_used, 1),
                        "available_capacity": round(avail_val, 1),
                        "free_capacity": round(max(0.0, avail_val - total_used), 1),
                        "utilization_pct": util_pct,
                        "is_overallocated": total_used > avail_val,
                        "gap": round(p_val - total_used, 1)
                    })

                    t_planned += p_val
                    t_internal += i_val
                    t_external += e_val
                    t_available += avail_val

                total_allocated = t_internal + t_external
                overall_util = round((total_allocated / t_planned) * 100, 1) if t_planned > 0 else 0.0
                
                # Calculate allotted weeks for this project
                p_allotted_weeks = ((p_max_end - p_min_start).days // 7) + 1

                result.append({
                    "id": project_id,
                    "project_code": project.project_code if project else "N/A",
                    "project_name": project.name if project else "Unknown",
                    "status": allocs[0].status.upper(),
                    "department": dept_name,
                    "department_full_path": dept_path,
                    "start_monday": str(p_min_start),
                    "end_monday": str(p_max_end),
                    "estimated_manhours": round(t_estimated, 1),
                    "allotted_weeks": p_allotted_weeks,
                    "total_planned_manhours": round(t_planned, 1),
                    "total_internal_hours": round(t_internal, 1),
                    "total_external_hours": round(t_external, 1),
                    "total_allocated": round(total_allocated, 1),
                    "remaining_hours": round(max(0.0, t_estimated - t_planned), 1),
                    "total_available_capacity": round(t_available, 1),
                    "overall_utilization_pct": overall_util,
                    "date_range": {
                        "start": str(p_min_start),
                        "end": str(p_max_end)
                    },
                    "weeks": weeks_data
                })

            result.sort(key=lambda x: (x.get("department_full_path", ""), x["project_code"]))

            return Response({
                "period": {
                    "start_monday": str(range_start_monday) if use_requested_range else "Dynamic",
                    "end_monday": str(range_end_monday) if use_requested_range else "Dynamic",
                    "weeks_count": len(range_mondays) if use_requested_range else 0
                },
                "data": result
            })

        except Exception as e:
            logger.exception(f"Project Summary (DeptID) failed for ID {department_id}")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class EmployeeTableView(APIView):
    """
    Employee Table API with basic info and current allocations
    Optimized for performance and secured with error handling.
    """
    permission_classes = [ModuleViewPermission]

    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            # --- 1. Fetch Resources (Base Query) ---
            resources = Resource.objects.filter(is_internal=True).select_related('department')
            
            # --- 2. Optimized Data Fetching (Prevent N+1) ---
            # Fetch ALL assignments for internal resources in one go
            all_assignments = ProjectAssignment.objects.filter(
                resource__is_internal=True
            ).select_related('project', 'resource')

            # Map assignments to resources in memory
            # Format: { resource_id: { "weeks": set(), "projects": {} } }
            resource_data_map = defaultdict(lambda: {"weeks": set(), "projects": {}})
            
            for assignment in all_assignments:
                res_id = assignment.resource_id
                proj = assignment.project
                
                if not proj:
                    continue
                
                # Track unique weeks
                resource_data_map[res_id]["weeks"].add(assignment.week_monday)
                
                # Track unique projects
                if proj.id not in resource_data_map[res_id]["projects"]:
                    resource_data_map[res_id]["projects"][proj.id] = {
                        'id': proj.id,
                        'code': proj.project_code or "N/A",
                        'name': proj.name or "Unknown"
                    }

            # --- 3. Build Result ---
            result = []
            for res in resources:
                data = resource_data_map.get(res.id, {"weeks": set(), "projects": {}})
                
                result.append({
                    'employee_id': res.id,
                    'employee_name': res.name or "Unnamed Employee",
                    'role': res.role or "N/A",
                    'current_allocation_weeks': len(data["weeks"]),
                    'assigned_projects': list(data["projects"].values())
                })

            # Sort by name
            result.sort(key=lambda x: x['employee_name'])
            
            return Response(result)

        except Exception as e:
            # Capture any database or logic crashes
            logger.exception("Employee Table View failed")
            return Response(
                {
                    "error": "Internal Server Error",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class EmployeeCapacityGraphView(APIView):
    """
    Graph data for Employee Capacity over date range.
    Secured with global error handling and data validation.
    """
    permission_classes = [ModuleViewPermission]

    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            # --- 1. Parameter Extraction ---
            start_str = request.query_params.get('start_date')
            end_str = request.query_params.get('end_date')
            resource_id = request.query_params.get('resource_id')

            # --- 2. Date Range Validation ---
            today = timezone.now().date()
            try:
                start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else today - timedelta(weeks=26)
                end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else today + timedelta(weeks=26)
            except (ValueError, TypeError) as e:
                return Response({
                    "error": "Validation Error",
                    "message": f"Invalid date format. Use YYYY-MM-DD: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

            if start_date > end_date:
                start_date, end_date = end_date, start_date

            start_monday = start_date - timedelta(days=start_date.weekday())
            end_monday = end_date - timedelta(days=end_date.weekday())

            mondays = []
            current = start_monday
            while current <= end_monday:
                mondays.append(current)
                current += timedelta(days=7)

            # --- 3. Capacity and Allocation Retrieval ---
            if resource_id:
                # Individual Employee Mode
                try:
                    resource = Resource.objects.get(id=int(resource_id), is_internal=True, is_active=True)
                    total_capacity = float(resource.effective_availability_per_week or 45)
                    
                    allocations = ResourceAllocation.objects.filter(
                        week_monday__in=mondays,
                        resource=resource
                    ).select_related('project').values(
                        'week_monday', 'project__project_code', 'project__name', 'hours', 'project__color_code'
                    )

                    alloc_dict = defaultdict(lambda: {'total': 0.0, 'projects': []})
                    for a in allocations:
                        week = a['week_monday']
                        hours = float(a['hours'] or 0)
                        alloc_dict[week]['total'] += hours
                        alloc_dict[week]['projects'].append({
                            'project_code': a['project__project_code'] or "N/A",
                            'project_name': a['project__name'] or "Unknown Project",
                            'hours': round(hours, 1),
                            'color': a['project__color_code'] or "#eeeeee"
                        })
                except (ValueError, Resource.DoesNotExist):
                    return Response({
                        "error": "Not Found",
                        "message": f"Active internal resource with ID {resource_id} not found."
                    }, status=status.HTTP_404_NOT_FOUND)
            else:
                # Aggregate Mode (All Employees)
                resources = Resource.objects.filter(is_internal=True, is_active=True)
                total_capacity = sum(float(r.effective_availability_per_week or 45) for r in resources)
                
                allocations = ResourceAllocation.objects.filter(
                    week_monday__in=mondays,
                    resource__is_internal=True,
                    resource__is_active=True
                ).values('week_monday').annotate(total_allocated=Sum('hours'))
                
                alloc_dict = {a['week_monday']: float(a['total_allocated'] or 0) for a in allocations}

            # --- 4. Result Building ---
            result = []
            for monday in mondays:
                if resource_id:
                    data = alloc_dict.get(monday, {'total': 0.0, 'projects': []})
                    allocated = data['total']
                    projects = data['projects']
                else:
                    allocated = alloc_dict.get(monday, 0.0)
                    projects = None

                week_data = {
                    'week_monday': str(monday),
                    'calendar_week': f"CW-{monday.isocalendar()[1]:02d}-{monday.isocalendar()[0]}",
                    'total_capacity': round(total_capacity, 1),
                    'total_allocated': round(allocated, 1),
                    'free_capacity': round(max(0.0, total_capacity - allocated), 1),
                    'utilization_pct': round((allocated / total_capacity * 100), 1) if total_capacity > 0 else 0.0
                }

                if resource_id:
                    week_data['projects'] = projects

                result.append(week_data)

            # --- 5. Summary and Metadata ---
            total_allocated_sum = sum(r['total_allocated'] for r in result)
            total_period_capacity = total_capacity * len(mondays)
            
            response_data = {
                'start_date': str(start_monday),
                'end_date': str(end_monday),
                'data': result
            }

            if resource_id:
                # Assuming ROLE_CHOICES is accessible
                role_display = dict(ROLE_CHOICES) if 'ROLE_CHOICES' in globals() else {}
                response_data.update({
                    'employee_id': resource.id,
                    'employee_name': resource.name,
                    'role': resource.role,
                    'role_name': role_display.get(resource.role, "Unknown"),
                    'total_free_capacity': round(max(0.0, total_period_capacity - total_allocated_sum), 1)
                })
            else:
                response_data['total_employees'] = resources.count()

            return Response(response_data)

        except Exception as e:
            logger.exception("Employee Capacity Graph generation failed")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class EmployeeIdleCapacityView(APIView):
    """
    Employee Master + Idle Capacity Week-wise
    Includes project breakdown per week and secured error handling.
    """
    permission_classes = [ModuleViewPermission]

    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            # --- 1. Query Parameters & Date Range Logic ---
            dept_filter = request.query_params.get("department")
            start_str = request.query_params.get("start")
            end_str = request.query_params.get("end")
            active_only = request.query_params.get("active_only", "true").lower() == "true"
            
            today = timezone.now().date()
            try:
                start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else today
                end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else start_date + timedelta(weeks=52)
            except (ValueError, TypeError) as e:
                return Response({
                    "error": "Validation Error",
                    "message": f"Invalid date format. Use YYYY-MM-DD: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

            if start_date > end_date:
                start_date, end_date = end_date, start_date

            # Standardize on Monday dates
            start_monday = start_date - timedelta(days=start_date.weekday())
            end_monday = end_date - timedelta(days=end_date.weekday())

            mondays = []
            current = start_monday
            while current <= end_monday:
                mondays.append(current)
                current += timedelta(days=7)

            # --- 2. Filter Employees (Prefetching ManyToMany) ---
            employees_qs = Resource.objects.filter(is_internal=True)
            if active_only:
                employees_qs = employees_qs.filter(is_active=True)

            if dept_filter:
                dept_filter = dept_filter.strip()
                try:
                    dept_id = int(dept_filter)
                    dept = Department.objects.get(id=dept_id)
                    descendants = list(dept.get_descendants()) + [dept]
                    employees_qs = employees_qs.filter(departments__in=descendants).distinct()
                except (ValueError, Department.DoesNotExist):
                    employees_qs = employees_qs.filter(departments__name__icontains=dept_filter).distinct()

            # Prefetch departments to avoid N+1 queries when building dept_name strings
            employees = employees_qs.prefetch_related('departments')

            # --- 3. Fetch Data & Aggregation ---
            allocations = ResourceAllocation.objects.filter(
                week_monday__in=mondays,
                resource__in=employees
            ).select_related('project', 'resource')

            # format: { emp_id: { week: { allocated: 0.0, projects: {} } } }
            employee_week_data = defaultdict(lambda: defaultdict(lambda: {
                "allocated": 0.0,
                "projects": {}
            }))

            for alloc in allocations:
                emp_id = alloc.resource.id
                week = alloc.week_monday
                hours = float(alloc.hours or 0.0)
                proj = alloc.project

                week_data = employee_week_data[emp_id][week]
                week_data["allocated"] += hours

                if proj:
                    proj_code = proj.project_code or "N/A"
                    if proj_code not in week_data["projects"]:
                        week_data["projects"][proj_code] = {
                            "project_code": proj_code,
                            "project_name": proj.name or "Unknown",
                            "status": proj.get_status_display() if hasattr(proj, 'get_status_display') else "N/A",
                            "hours": 0.0
                        }
                    week_data["projects"][proj_code]["hours"] += hours

            # --- 4. Build Result ---
            result = []
            role_display = dict(ROLE_CHOICES) if 'ROLE_CHOICES' in globals() else {}

            for emp in employees:
                capacity = float(emp.effective_availability_per_week or 45.0)
                weeks_list = []

                for monday in mondays:
                    data = employee_week_data[emp.id][monday]
                    allocated = float(data["allocated"])
                    idle_hours = float(max(0.0, capacity - allocated))

                    project_list = [
                        {
                            "project_code": p["project_code"],
                            "project_name": p["project_name"],
                            "status": p["status"],
                            "hours": round(p["hours"], 1)
                        }
                        for p in data["projects"].values()
                    ]

                    weeks_list.append({
                        "week_monday": str(monday),
                        "calendar_week": f"CW{monday.isocalendar()[1]:02d}",
                        "allocated_hours": round(allocated, 1),
                        "idle_capacity_hours": round(idle_hours, 1),
                        "utilization_pct": round((allocated / capacity) * 100, 1) if capacity > 0 else 0.0,
                        "is_overallocated": allocated > capacity,
                        "projects": project_list
                    })

                total_idle = sum(w["idle_capacity_hours"] for w in weeks_list)
                idle_weeks_count = sum(1 for w in weeks_list if w["allocated_hours"] == 0)
                weeks_with_partial_idle = sum(1 for w in weeks_list if w["idle_capacity_hours"] > 0)

                # Department naming safety
                depts = emp.departments.all()
                dept_name = depts[0].name if depts else "Unassigned"
                dept_full_path = depts[0].get_full_path() if (depts and hasattr(depts[0], 'get_full_path')) else dept_name

                result.append({
                    "employee_id": emp.id,
                    "emp_id": getattr(emp, 'emp_id', emp.id),
                    "employee_name": emp.name,
                    "role": emp.role,
                    "role_name": role_display.get(emp.role, "Unknown"),
                    "department": dept_name,
                    "department_full_path": dept_full_path,
                    "weekly_capacity": round(capacity, 1),
                    "is_active": emp.is_active,
                    "idle_capacity_summary": {
                        "total_idle_hours": round(total_idle, 1),
                        "average_idle_per_week": round(total_idle / len(weeks_list), 1) if weeks_list else 0.0,
                        "idle_weeks_count": idle_weeks_count,
                        "weeks_with_partial_idle": weeks_with_partial_idle
                    },
                    "weeks": weeks_list,
                    "joining_date": str(emp.joining_date) if emp.joining_date else None,
                })

            result.sort(key=lambda x: (x["department"], x["employee_name"]))

            return Response({
                "generated_at": timezone.now().isoformat(),
                "date_range": {
                    "start": str(start_monday),
                    "end": str(end_monday),
                    "total_weeks": len(mondays)
                },
                "total_employees": len(result),
                "data": result
            })

        except Exception as e:
            logger.exception("Employee Idle Capacity View generation failed")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class DepartmentCapacitySummaryView(APIView):
    """
    Consolidated summary of department capacity, rolling up leaf data to parents.
    """
    permission_classes = [ModuleViewPermission]

    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            # --- 1. Parameter Extraction ---
            dept_filter = request.query_params.get("department")
            start_str = request.query_params.get("start")
            end_str = request.query_params.get("end")

            # --- 2. Date Range Logic & Validation ---
            today = timezone.now().date()
            try:
                start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else today
                end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else start_date + timedelta(weeks=52)
            except (ValueError, TypeError) as e:
                return Response({
                    "error": "Validation Error",
                    "message": f"Invalid date format. Use YYYY-MM-DD: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

            if start_date > end_date:
                start_date, end_date = end_date, start_date

            start_monday = start_date + timedelta(days=(7 - start_date.weekday()) % 7)
            if start_monday < start_date:
                start_monday += timedelta(days=7)
            end_monday = end_date - timedelta(days=end_date.weekday())

            mondays = []
            current = start_monday
            while current <= end_monday:
                mondays.append(current)
                current += timedelta(days=7)

            total_weeks = len(mondays)

            # --- 3. Department Filter Logic ---
            descendants = []
            if dept_filter:
                dept_filter = dept_filter.strip()
                dept = None
                try:
                    # Try by ID
                    if dept_filter.isdigit():
                        dept = Department.objects.get(id=int(dept_filter))
                except (ValueError, Department.DoesNotExist):
                    pass

                if not dept:
                    try:
                        # Try by Name
                        dept = Department.objects.get(name__iexact=dept_filter)
                    except (Department.DoesNotExist, Department.MultipleObjectsReturned):
                        return Response({
                            "error": "Not Found",
                            "message": f"Department '{dept_filter}' not found."
                        }, status=status.HTTP_404_NOT_FOUND)

                descendants = [dept] + list(dept.get_descendants())

            # --- 4. Capacity and Utilization Aggregation ---
            # Initializing maps
            available_per_path = defaultdict(float)
            emp_count_per_path = defaultdict(int)
            internal_per_path = defaultdict(float)
            external_per_path = defaultdict(float)

            # Available Capacity
            resources = Resource.objects.filter(is_internal=True, is_active=True)
            if descendants:
                resources = resources.filter(departments__in=descendants).distinct()
            
            for res in resources.prefetch_related('departments'):
                dept_obj = res.departments.first()
                # Get path using MPTT helper or fallback
                path = getattr(dept_obj, 'get_full_path', lambda: dept_obj.name)() if dept_obj else "Unassigned"
                capacity = float(res.effective_availability_per_week or 45.0)
                available_per_path[path] += (capacity * total_weeks)
                emp_count_per_path[path] += 1

            # Internal Hours
            internal_qs = ResourceAllocation.objects.filter(week_monday__in=mondays, resource__is_internal=True)
            if descendants:
                internal_qs = internal_qs.filter(resource__departments__in=descendants)
            
            for a in internal_qs.prefetch_related('resource__departments'):
                d_obj = a.resource.departments.first()
                path = getattr(d_obj, 'get_full_path', lambda: d_obj.name)() if d_obj else "Unassigned"
                internal_per_path[path] += float(a.hours or 0.0)

            # External Hours
            external_qs = ExternalCapacity.objects.filter(week_monday__in=mondays)
            if descendants:
                external_qs = external_qs.filter(project__department__in=descendants)
            
            for e in external_qs.select_related('project__department'):
                d_obj = e.project.department
                path = getattr(d_obj, 'get_full_path', lambda: d_obj.name)() if d_obj else "Unassigned"
                external_per_path[path] += float(e.hours or 0.0)

            # --- 5. Roll Up Logic (Tree Construction) ---
            all_paths = set(available_per_path.keys()) | set(internal_per_path.keys()) | set(external_per_path.keys())
            summary = {}

            for path in all_paths:
                parts = path.split(" → ")
                current_path = ""
                for i, part in enumerate(parts):
                    current_path = part if i == 0 else f"{current_path} → {part}"
                    if current_path not in summary:
                        summary[current_path] = {"internal": 0.0, "external": 0.0, "available": 0.0, "employees": 0}

                # Update leaf node
                leaf = summary[path]
                leaf["internal"] += internal_per_path.get(path, 0.0)
                leaf["external"] += external_per_path.get(path, 0.0)
                leaf["available"] += available_per_path.get(path, 0.0)
                leaf["employees"] += emp_count_per_path.get(path, 0)

                # Roll up to parents (climbing the path string)
                for i in range(len(parts) - 1, 0, -1):
                    parent_path = " → ".join(parts[:i])
                    parent = summary[parent_path]
                    parent["internal"] += internal_per_path.get(path, 0.0)
                    parent["external"] += external_per_path.get(path, 0.0)
                    parent["available"] += available_per_path.get(path, 0.0)
                    parent["employees"] += emp_count_per_path.get(path, 0)

            # --- 6. Final Result Formatting ---
            result = []
            for path, stats in summary.items():
                utilized = stats["internal"] + stats["external"]
                available = stats["available"]
                idle = max(0.0, available - utilized)
                util_pct = round((utilized / available * 100), 1) if available > 0 else 0.0
                dept_name = path.split(" → ")[-1]

                result.append({
                    "department": dept_name,
                    "department_full_path": path,
                    "total_internal_hours": round(stats["internal"], 1),
                    "total_external_hours": round(stats["external"], 1),
                    "total_hours_utilized": round(utilized, 1),
                    "total_idle_hours": round(idle, 1),
                    "total_available_capacity": round(available, 1),
                    "average_utilization_pct": util_pct,
                    "total_employees": stats["employees"]
                })

            result.sort(key=lambda x: x["department_full_path"])

            return Response({
                "generated_at": timezone.now().isoformat(),
                "requested_department": dept_filter or "All",
                "date_range": {
                    "start_monday": str(start_monday),
                    "end_monday": str(end_monday),
                    "total_weeks": total_weeks
                },
                "summary": result
            })

        except Exception as e:
            logger.exception("Department Capacity Summary failed")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepartmentCapacitySummary_DeptId(APIView):
    """
    Department capacity summary with hierarchy roll-up.
    Secured with global error handling and path validation.
    """
    permission_classes = [ModuleViewPermission]

    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request, department_id):
        try:
            # --- 1. Department Retrieval & Hierarchy ---
            try:
                dept = Department.objects.get(id=department_id)
            except (Department.DoesNotExist, ValueError):
                return Response({
                    "error": "Not Found",
                    "message": f"Department with ID {department_id} not found."
                }, status=status.HTTP_404_NOT_FOUND)

            # Get the requested department and all its children
            descendants = [dept] + list(dept.get_descendants())

            # --- 2. Query Parameters & Date Range Logic ---
            start_str = request.query_params.get("start")
            end_str = request.query_params.get("end")
            active_only = request.query_params.get("active_only", "true").lower() == "true"

            today = timezone.now().date()
            try:
                start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else today
                end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else start_date + timedelta(weeks=52)
            except (ValueError, TypeError) as e:
                return Response({
                    "error": "Validation Error",
                    "message": f"Invalid date format. Use YYYY-MM-DD: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

            if start_date > end_date:
                start_date, end_date = end_date, start_date

            # Align to Mondays
            start_monday = start_date + timedelta(days=(7 - start_date.weekday()) % 7)
            if start_monday < start_date:
                start_monday += timedelta(days=7)
            end_monday = end_date - timedelta(days=end_date.weekday())

            mondays = []
            curr = start_monday
            while curr <= end_monday:
                mondays.append(curr)
                curr += timedelta(days=7)

            total_weeks = len(mondays)

            # --- 3. Data Collection (Leaf Level) ---
            available_per_path = defaultdict(float)
            emp_count_per_path = defaultdict(int)
            internal_per_path = defaultdict(float)
            external_per_path = defaultdict(float)

            # A. Available Capacity (Time-aware)
            resources = Resource.objects.filter(
                is_internal=True,
                is_active=active_only,
                departments__in=descendants
            ).distinct().prefetch_related('departments')

            for res in resources:
                dept_obj = res.departments.first()
                path = getattr(dept_obj, 'get_full_path', lambda: dept_obj.name)() if dept_obj else "Unassigned"
                
                capacity_per_week = float(res.effective_availability_per_week or 45.0)
                available_weeks = sum(
                    1 for monday in mondays 
                    if not res.joining_date or res.joining_date <= monday
                )
                
                available_per_path[path] += capacity_per_week * available_weeks
                emp_count_per_path[path] += 1

            # B. Internal Hours
            internal_qs = ResourceAllocation.objects.filter(
                week_monday__in=mondays,
                resource__is_internal=True,
                resource__departments__in=descendants
            ).select_related('resource')

            for a in internal_qs.prefetch_related('resource__departments'):
                d_obj = a.resource.departments.first()
                path = getattr(d_obj, 'get_full_path', lambda: d_obj.name)() if d_obj else "Unassigned"
                internal_per_path[path] += float(a.hours or 0.0)

            # C. External Hours
            external_qs = ExternalCapacity.objects.filter(
                week_monday__in=mondays,
                project__department_allocations__department__in=descendants
            ).select_related('project')

            for e in external_qs.prefetch_related('project__department_allocations__department'):
                alloc = e.project.department_allocations.filter(department__in=descendants).first()
                path = getattr(alloc.department, 'get_full_path', lambda: alloc.department.name)() if (alloc and alloc.department) else "Unassigned"
                external_per_path[path] += float(e.hours or 0.0)

            # --- 4. Roll Up Logic ---
            all_paths = set(available_per_path.keys()) | set(internal_per_path.keys()) | set(external_per_path.keys())
            summary = {}

            for path in all_paths:
                parts = path.split(" → ")
                current_path = ""
                for i, part in enumerate(parts):
                    current_path = part if i == 0 else f"{current_path} → {part}"
                    if current_path not in summary:
                        summary[current_path] = {"internal": 0.0, "external": 0.0, "available": 0.0, "employees": 0}

                # Update leaf
                node = summary[path]
                int_val = internal_per_path.get(path, 0.0)
                ext_val = external_per_path.get(path, 0.0)
                avail_val = available_per_path.get(path, 0.0)
                emp_val = emp_count_per_path.get(path, 0)

                node["internal"] += int_val
                node["external"] += ext_val
                node["available"] += avail_val
                node["employees"] += emp_val

                # Update ancestors
                for i in range(len(parts) - 1, 0, -1):
                    parent_path = " → ".join(parts[:i])
                    if parent_path not in summary:
                        summary[parent_path] = {"internal": 0.0, "external": 0.0, "available": 0.0, "employees": 0}
                    parent = summary[parent_path]
                    parent["internal"] += int_val
                    parent["external"] += ext_val
                    parent["available"] += avail_val
                    parent["employees"] += emp_val

            # --- 5. Final Result Build ---
            result = []
            for path, stats in summary.items():
                utilized = stats["internal"] + stats["external"]
                available = stats["available"]
                idle = max(0.0, available - utilized)
                util_pct = round((utilized / available * 100), 1) if available > 0 else 0.0
                dept_name = path.split(" → ")[-1]

                result.append({
                    "department": dept_name,
                    "department_full_path": path,
                    "total_internal_hours": round(stats["internal"], 1),
                    "total_external_hours": round(stats["external"], 1),
                    "total_hours_utilized": round(utilized, 1),
                    "total_idle_hours": round(idle, 1),
                    "total_available_capacity": round(available, 1),
                    "average_utilization_pct": util_pct,
                    "total_employees": stats["employees"],
                })

            result.sort(key=lambda x: x["department_full_path"])

            return Response({
                "generated_at": timezone.now().isoformat(),
                "requested_department_id": department_id,
                "date_range": {
                    "start_monday": str(start_monday),
                    "end_monday": str(end_monday),
                    "total_weeks": total_weeks
                },
                "summary": result
            })

        except Exception as e:
            logger.exception(f"Department Capacity Summary ID View failed for ID {department_id}")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class FreeCapacityEmployeeView(APIView):
    """
    List employees with zero allocated hours across the entire specified time range.
    """
    permission_classes = [ModuleViewPermission]

    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request, deptId=None):
        try:
            # 1. Validate Department ID
            if not deptId:
                return Response(
                    {"error": "Validation Error", "message": "Department ID is required in the URL"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                department_id = int(deptId)
            except ValueError:
                return Response(
                    {"error": "Validation Error", "message": "Invalid department ID format."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 2. Parse Date Parameters
            start_str = request.query_params.get('start')
            end_str = request.query_params.get('end')

            today = timezone.now().date()
            default_start = today.replace(month=1, day=1)
            default_end = today.replace(month=12, day=31)

            try:
                start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else default_start
                end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else default_end
            except (ValueError, TypeError) as e:
                return Response(
                    {"error": "Validation Error", "message": f"Invalid date format. Use YYYY-MM-DD: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if start_date > end_date:
                start_date, end_date = end_date, start_date

            # 3. Generate Mondays in Range
            start_monday = start_date - timedelta(days=start_date.weekday())
            end_monday = end_date - timedelta(days=end_date.weekday())

            mondays = []
            current = start_monday
            while current <= end_monday:
                mondays.append(current)
                current += timedelta(days=7)

            if not mondays:
                return Response({"employees": [], "message": "No full weeks found in the specified range."})

            # 4. Fetch Candidate Resources
            # Optimization: distinct() prevents duplicate results from ManyToMany joins
            resources = Resource.objects.filter(
                is_internal=True,
                is_active=True,
                departments__id=department_id,
                joining_date__lte=start_date 
            ).filter(
                Q(leaving_date__isnull=True) | Q(leaving_date__gte=end_date)
            ).prefetch_related('departments').select_related('supplier').distinct()

            # 5. Calculate Allocation Usage
            # Query A: Project Assignments
            project_usage = ProjectAssignment.objects.filter(
                resource__in=resources,
                week_monday__in=mondays,
                department_id=department_id
            ).values('resource_id', 'week_monday').annotate(
                total=Sum('week_allocation__manhours') 
            )

            # Query B: General Resource Allocations
            alloc_usage = ResourceAllocation.objects.filter(
                resource__in=resources,
                week_monday__in=mondays,
                department_id=department_id
            ).values('resource_id', 'week_monday').annotate(
                total=Sum('hours')
            )

            # 6. Consolidate Usage into Memory Map
            usage_map = defaultdict(lambda: defaultdict(float))
            # for entry in project_usage:
            #     usage_map[entry['resource_id']][entry['week_monday']] += float(entry['total'] or 0.0)
            for entry in alloc_usage:
                usage_map[entry['resource_id']][entry['week_monday']] += float(entry['total'] or 0.0)

            # 7. Strict Filtering: Must be 0 hours for EVERY week in the range
            free_capacity_resources = []
            MAX_CAPACITY=45.0
            for resource in resources:
                res_id = resource.id
                has_available_slot = False 
                
                for monday in mondays:
                    total_used = usage_map[res_id].get(monday, 0.0)
                    
                    if total_used < MAX_CAPACITY:
                        # This employee has free hours (e.g., 45 - 30 = 15 free)
                        has_available_slot = True
                        # Attach remaining hours for the first available week for UI reference (optional)
                        resource.remaining_hours = MAX_CAPACITY - total_used
                        break 
                
                if has_available_slot:
                    free_capacity_resources.append(resource)

            # 8. Serialize and Response
            serializer = ResourceSerializer(free_capacity_resources, many=True, context={'request': request})

            return Response({
                "date_range_checked": {
                    "start_week": str(start_monday),
                    "end_week": str(end_monday),
                    "total_weeks": len(mondays)
                },
                "department_id": department_id,
                "total_fully_free_resources": len(free_capacity_resources),
                "employees": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Catch unexpected database or logic failures
            logger.exception(f"FreeCapacityEmployeeView error for dept {deptId}")
            return Response(
                {
                    "error": "Internal Server Error",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SupplierMasterView(APIView):
    permission_classes = [ModuleViewPermission]

    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            # --- 1. Query Parameters & Validation ---
            supplier_filter = request.query_params.get("supplier")
            project_filter = request.query_params.get("project")
            start_str = request.query_params.get("start")
            end_str = request.query_params.get("end")

            if project_filter:
                if not Project.objects.filter(project_code=project_filter).exists():
                    return Response({
                        "error": "Not Found",
                        "message": f"Project with code '{project_filter}' not found"
                    }, status=status.HTTP_404_NOT_FOUND)

            # --- 2. Date Range Logic ---
            today = timezone.now().date()
            try:
                start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else today
                end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else start_date + timedelta(weeks=52)
            except (ValueError, TypeError) as e:
                return Response({
                    "error": "Validation Error",
                    "message": f"Invalid date format. Use YYYY-MM-DD: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

            if start_date > end_date:
                start_date, end_date = end_date, start_date

            start_monday = start_date + timedelta(days=(7 - start_date.weekday()) % 7)
            if start_monday < start_date:
                start_monday += timedelta(days=7)
            end_monday = end_date - timedelta(days=end_date.weekday())

            mondays = []
            current = start_monday
            while current <= end_monday:
                mondays.append(current)
                current += timedelta(days=7)

            # --- 3. Filter Suppliers & Capacities ---
            suppliers_qs = Supplier.objects.all()
            if supplier_filter:
                suppliers_qs = suppliers_qs.filter(name__icontains=supplier_filter.strip())
            
            # Convert to list for result mapping
            suppliers = list(suppliers_qs)

            capacities = ExternalCapacity.objects.filter(
                week_monday__in=mondays,
                supplier__in=suppliers
            ).select_related('supplier', 'project')

            if project_filter:
                capacities = capacities.filter(project__project_code=project_filter)

            # --- 4. Process Aggregations ---
            supplier_data = defaultdict(lambda: {
                "total_hours": 0.0,
                "weeks": defaultdict(lambda: {"hours": 0.0, "projects": {}}),
                "current_projects": set()
            })

            for cap in capacities:
                sup_id = cap.supplier.id
                week = cap.week_monday
                hours = float(cap.hours or 0.0)
                proj = cap.project
                if not proj: continue

                # Aggregate Data
                sup_entry = supplier_data[sup_id]
                sup_entry["total_hours"] += hours
                
                week_data = sup_entry["weeks"][week]
                week_data["hours"] += hours

                proj_code = proj.project_code or "N/A"
                if proj_code not in week_data["projects"]:
                    week_data["projects"][proj_code] = {
                        "code": proj_code,
                        "name": proj.name or "Unknown",
                        "status": proj.get_status_display() if hasattr(proj, 'get_status_display') else "N/A",
                        "department": "N/A",
                        "hours": 0.0
                    }
                week_data["projects"][proj_code]["hours"] += hours

                # Track unique projects
                sup_entry["current_projects"].add((
                    proj_code,
                    proj.name or "Unknown",
                    proj.get_status_display() if hasattr(proj, 'get_status_display') else "N/A",
                    "N/A"
                ))

            # --- 5. Build Final Response ---
            result = []
            for sup in suppliers:
                data = supplier_data.get(sup.id, {"total_hours": 0.0, "weeks": {}, "current_projects": set()})
                total_utilized = float(data["total_hours"])
                budgeted = float(sup.budgeted_hours or 0.0)

                remaining = max(0.0, budgeted - total_utilized)
                utilization_pct = round((total_utilized / budgeted) * 100, 1) if budgeted > 0 else 0.0

                current_projects = [
                    {
                        "project_code": cp[0],
                        "project_name": cp[1],
                        "status": cp[2],
                        "department": cp[3]
                    }
                    for cp in data["current_projects"]
                ]

                weeks_list = []
                for monday in mondays:
                    week_data = data["weeks"].get(monday, {"hours": 0.0, "projects": {}})
                    project_list = [
                        {
                            "project_code": p["code"],
                            "project_name": p["name"],
                            "status": p["status"],
                            "department": p["department"],
                            "allocation_hours": round(p["hours"], 1)
                        }
                        for p in week_data["projects"].values()
                    ]
                    weeks_list.append({
                        "week_monday": str(monday),
                        "calendar_week": f"CW{monday.isocalendar()[1]:02d}",
                        "allocation_hours": round(week_data["hours"], 1),
                        "projects": project_list
                    })

                result.append({
                    "supplier_id": sup.id,
                    "supplier_name": sup.name,
                    "contact_email": sup.contact_email or "",
                    "budgeted_hours": round(budgeted, 1),
                    "total_utilized_hours": round(total_utilized, 1),
                    "remaining_hours": round(remaining, 1),
                    "utilization_pct": utilization_pct,
                    "is_active": sup.is_active,
                    "hourly_rate": str(sup.hourly_rate) if sup.hourly_rate else None,
                    "notes": sup.notes or "",
                    "current_projects": current_projects,
                    "date_range": {
                        "start_monday": str(start_monday),
                        "end_monday": str(end_monday),
                        "total_weeks": len(mondays)
                    },
                    "weeks": weeks_list
                })

            result.sort(key=lambda x: x["supplier_name"])

            return Response({
                "generated_at": timezone.now().isoformat(),
                "total_suppliers": len(result),
                "data": result
            })

        except Exception as e:
            logger.exception("Supplier Master View failed")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class ProjectDetail(APIView):
    """
    Retrieve, update or delete a Project instance.
    URL: /api/projects/<int:pk>/
    """

    def get_permissions(self):
        """
        Apply different permissions based on HTTP method
        """
        if self.request.method == 'GET':
            permission = ModuleViewPermission()
        else:
            # PUT, PATCH, DELETE all use prepare permission
            permission = ModulePreparePermission()

        permission.module = "CAPACITY"
        return [permission]

    def get_object(self, pk):
        """
        Fetch the project or raise 404
        """
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return None
        except Exception as e:
            # Catching potential DB connection issues during lookup
            logger.error(f"Database error in get_object: {str(e)}")
            raise e

    def get(self, request, pk):
        try:
            project = self.get_object(pk)
            if project is None:
                return Response(
                    {"error": "Not Found", "message": f"Project with ID {pk} not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ProjectSerializer(project, context={'request': request})
            return Response(serializer.data)

        except Exception as e:
            logger.exception(f"ProjectDetail GET failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            project = self.get_object(pk)
            if project is None:
                return Response(
                    {"error": "Not Found", "message": f"Project with ID {pk} not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ProjectSerializer(
                project,
                data=request.data,
                partial=False,
                context={'request': request}
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(
                {"error": "Validation Error", "message": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            logger.exception(f"ProjectDetail PUT failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        try:
            project = self.get_object(pk)
            if project is None:
                return Response(
                    {"error": "Not Found", "message": f"Project with ID {pk} not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ProjectSerializer(
                project,
                data=request.data,
                partial=True,
                context={'request': request}
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(
                {"error": "Validation Error", "message": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            logger.exception(f"ProjectDetail PATCH failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        try:
            project = self.get_object(pk)
            if project is None:
                return Response(
                    {"error": "Not Found", "message": f"Project with ID {pk} not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            project.delete()
            return Response(
                {"message": "Project deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )

        except Exception as e:
            logger.exception(f"ProjectDetail DELETE failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



# =============================================================================
# EMPLOYEE VIEWS - Function Based 
# =============================================================================
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Change to IsAuthenticated in production
def employee_list_create(request):
    """
    GET    /api/employees/ → List all employees
    POST   /api/employees/ → Create new employee
    """
    try:
        if request.method == 'GET':
            # Optimization: prefetch ManyToMany departments to avoid N+1 queries
            employees = Resource.objects.all().prefetch_related('departments')

            # --- Department Filtering Logic ---
            dept_filter = request.query_params.get("department")
            if dept_filter:
                dept_filter = dept_filter.strip()
                try:
                    # Try Filtering by ID
                    if dept_filter.isdigit():
                        dept = Department.objects.get(id=int(dept_filter))
                        descendants = [dept] + list(dept.get_descendants())
                        employees = employees.filter(departments__in=descendants).distinct()
                    else:
                        # Fallback to Name match
                        employees = employees.filter(departments__name__iexact=dept_filter).distinct()
                except Department.DoesNotExist:
                    return Response({
                        "error": "Not Found",
                        "message": f"Department '{dept_filter}' not found."
                    }, status=status.HTTP_404_NOT_FOUND)

            serializer = ResourceSerializer(employees, many=True, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = ResourceSerializer(data=request.data, context={'request': request})
            
            if serializer.is_valid():
                try:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Exception as save_error:
                    logger.error(f"Database save error: {str(save_error)}")
                    return Response({
                        "error": "Database Error",
                        "message": "An integrity error occurred while saving the employee."
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Standardization: Wrap serializer errors in our common format
            return Response({
                "error": "Validation Error",
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Catch-all for unexpected logic or server crashes
        logger.exception("employee_list_create view failed")
        return Response({
            "error": "Internal Server Error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)\




class EmployeeListCreateAPIView(APIView):
    """
    List employees with department/date filtering and support for new employee creation.
    """

    def get(self, request, department_id=None):
        try:
            # 1. Capture query params
            start_date = request.query_params.get('start')
            end_date = request.query_params.get('end')

            # 2. Base Queryset (Optimized with select_related and prefetch_related)
            employees = Resource.objects.all().select_related('supplier').prefetch_related('departments')

            # 3. Filter by Department
            if department_id is not None:
                try:
                    dept = Department.objects.get(id=int(department_id))
                    descendants = [dept] + list(dept.get_descendants())
                    # Filter resources that belong to ANY of the descendant departments
                    employees = employees.filter(departments__in=descendants).distinct()
                except (Department.DoesNotExist, ValueError) as e:
                    return Response({
                        "error": "Not Found",
                        "message": f"Department with ID {department_id} not found or invalid."
                    }, status=status.HTTP_404_NOT_FOUND)

            # 4. Filter by Date Range
            if end_date:
                try:
                    employees = employees.filter(joining_date__lte=end_date)
                except Exception as e:
                    return Response({
                        "error": "Validation Error",
                        "message": f"Invalid date format provided for filtering: {str(e)}"
                    }, status=status.HTTP_400_BAD_REQUEST)

            # 5. Serialization
            serializer = ResourceSerializer(
                employees, 
                many=True, 
                context={
                    'request': request,
                    'start_date': start_date,
                    'end_date': end_date
                }
            )
            return Response(serializer.data)

        except Exception as e:
            logger.exception("EmployeeListCreateAPIView GET failed")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request, *args, **kwargs):
        try:
            serializer = ResourceSerializer(data=request.data, context={'request': request})
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            # Standardization: Wrap serializer errors in our common format
            return Response({
                "error": "Validation Error",
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("EmployeeListCreateAPIView POST failed")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class EmployeeDetailAPIView(APIView):
    """
    GET    /api/employees/<pk>/ → View employee (only if active)
    PUT    /api/employees/<pk>/ → Full update
    PATCH  /api/employees/<pk>/ → Partial update
    DELETE /api/employees/<pk>/ → Soft delete (is_active=False)
    """
    
    def get_permissions(self):
        if self.request.method == 'GET':
            permission = ModuleViewPermission()
        else:
            permission = ModulePreparePermission()

        permission.module = "CAPACITY"
        return [permission]
    
    def get_object(self, pk):
        try:
            return Resource.objects.get(pk=pk)
        except Resource.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Database error in get_object: {str(e)}")
            raise e

    def get(self, request, pk):
        try:
            employee = self.get_object(pk)
            if not employee or not employee.is_active:
                return Response(
                    {"error": "Not Found", "message": "Employee not found or has been deactivated"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ResourceSerializer(employee, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(f"EmployeeDetail GET failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        return self._update(request, pk, partial=False)

    def patch(self, request, pk):
        return self._update(request, pk, partial=True)

    def _update(self, request, pk, partial):
        try:
            employee = self.get_object(pk)
            if not employee:
                return Response(
                    {"error": "Not Found", "message": "Employee not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ResourceSerializer(
                employee,
                data=request.data,
                partial=partial,
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(
                {"error": "Validation Error", "message": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(f"EmployeeDetail update failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        try:
            employee = self.get_object(pk)
            if not employee:
                return Response(
                    {"error": "Not Found", "message": "Employee not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            if not employee.is_active:
                return Response(
                    {"error": "Bad Request", "message": "Employee is already deactivated"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # --- Leaving Date Logic ---
            leaving_date_str = request.data.get('leaving_date')
            if leaving_date_str:
                try:
                    leaving_date = datetime.strptime(leaving_date_str, "%Y-%m-%d").date()
                except (ValueError, TypeError):
                    return Response(
                        {"error": "Validation Error", "message": "Invalid leaving_date format. Use YYYY-MM-DD"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                leaving_date = timezone.now().date()

            # Calculate Monday of the leaving week
            leaving_monday = leaving_date - timedelta(days=leaving_date.weekday())

            # --- Transactional Deactivation ---
            with transaction.atomic():
                # 1. Soft Delete
                employee.is_active = False
                employee.leaving_date = leaving_date
                employee.save(update_fields=['is_active', 'leaving_date'])

                # 2. Cleanup Future Allocations
                alloc_count = ResourceAllocation.objects.filter(
                    resource=employee,
                    week_monday__gte=leaving_monday
                ).delete()[0]

                # 3. Cleanup Future Assignments
                assign_count = ProjectAssignment.objects.filter(
                    resource=employee,
                    week_monday__gte=leaving_monday
                ).delete()[0]

            return Response(
                {
                    "message": "Employee deactivated successfully",
                    "leaving_date": str(leaving_date),
                    "allocations_removed": alloc_count,
                    "assignments_removed": assign_count,
                    "historical_data_preserved": True
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.exception(f"EmployeeDetail deactivation failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SupplierListCreate(APIView):
    """
    List all suppliers (GET) or create a new supplier (POST)
    URL: /api/suppliers/
    """

    def get_permissions(self):
        """
        Different permissions for GET vs POST
        """
        if self.request.method == 'GET':
            permission = ModuleViewPermission()
        else:
            permission = ModulePreparePermission()

        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            suppliers = Supplier.objects.all()

            # --- Optional filtering: is_active ---
            is_active = request.query_params.get('is_active')
            if is_active is not None:
                if is_active.lower() not in ['true', 'false']:
                    return Response(
                        {
                            "error": "Validation Error",
                            "message": "is_active must be 'true' or 'false'"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                suppliers = suppliers.filter(is_active=is_active.lower() == 'true')

            # --- Optional search by name ---
            search = request.query_params.get('search')
            if search:
                suppliers = suppliers.filter(name__icontains=search.strip())

            serializer = SupplierSerializer(
                suppliers,
                many=True,
                context={'request': request}
            )
            return Response(serializer.data)

        except Exception as e:
            logger.exception("SupplierListCreate GET failed")
            return Response(
                {
                    "error": "Internal Server Error",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            serializer = SupplierSerializer(
                data=request.data,
                context={'request': request}
            )

            if serializer.is_valid():
                supplier = serializer.save()
                # Return the created object with full context
                return Response(
                    SupplierSerializer(
                        supplier,
                        context={'request': request}
                    ).data,
                    status=status.HTTP_201_CREATED
                )

            # Standardized validation error response
            return Response(
                {
                    "error": "Validation Error",
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            logger.exception("SupplierListCreate POST failed")
            return Response(
                {
                    "error": "Internal Server Error",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




class SupplierDetail(APIView):
    """
    Retrieve, update or delete a Supplier instance.
    URL: /api/suppliers/<int:pk>/
    """

    def get_permissions(self):
        if self.request.method == 'GET':
            permission = ModuleViewPermission()
        else:
            permission = ModulePreparePermission()

        permission.module = "CAPACITY"
        return [permission]

    def get_object(self, pk):
        try:
            return Supplier.objects.get(pk=pk)
        except Supplier.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Database error in Supplier get_object: {str(e)}")
            raise e

    def get(self, request, pk):
        try:
            supplier = self.get_object(pk)
            if supplier is None:
                return Response(
                    {"error": "Not Found", "message": f"Supplier with ID {pk} not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = SupplierSerializer(supplier, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            logger.exception(f"SupplierDetail GET failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            supplier = self.get_object(pk)
            if supplier is None:
                return Response(
                    {"error": "Not Found", "message": f"Supplier with ID {pk} not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = SupplierSerializer(
                supplier,
                data=request.data,
                partial=False,
                context={'request': request}
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(
                {"error": "Validation Error", "message": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(f"SupplierDetail PUT failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        try:
            supplier = self.get_object(pk)
            if supplier is None:
                return Response(
                    {"error": "Not Found", "message": f"Supplier with ID {pk} not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = SupplierSerializer(
                supplier,
                data=request.data,
                partial=True,
                context={'request': request}
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(
                {"error": "Validation Error", "message": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(f"SupplierDetail PATCH failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        try:
            supplier = self.get_object(pk)
            if supplier is None:
                return Response(
                    {"error": "Not Found", "message": f"Supplier with ID {pk} not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            try:
                supplier.delete()
                return Response(
                    {"message": "Supplier deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT
                )
            except ProtectedError:
                return Response(
                    {
                        "error": "Conflict", 
                        "message": "Cannot delete supplier because it is linked to active resources or capacity records. Consider deactivating it instead."
                    },
                    status=status.HTTP_409_CONFLICT
                )

        except Exception as e:
            logger.exception(f"SupplierDetail DELETE failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class ProjectAssignmentListCreate(APIView):
    """
    List all project assignments (GET) or create a new one (POST)
    URL: /api/project-assignments/
    """

    def get_permissions(self):
        """
        Different permissions for GET vs POST
        """
        if self.request.method == 'GET':
            permission = ModuleViewPermission()
        else:
            permission = ModulePreparePermission()

        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            # Optimization: select_related for foreign keys to prevent N+1 queries
            assignments = ProjectAssignment.objects.all().select_related('project', 'resource')

            # --- 1. ID Filtering ---
            project_id = request.query_params.get('project')
            if project_id:
                try:
                    assignments = assignments.filter(project_id=int(project_id))
                except ValueError:
                    return Response(
                        {"error": "Validation Error", "message": "project must be a valid integer ID"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            resource_id = request.query_params.get('resource')
            if resource_id:
                try:
                    assignments = assignments.filter(resource_id=int(resource_id))
                except ValueError:
                    return Response(
                        {"error": "Validation Error", "message": "resource must be a valid integer ID"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # --- 2. Week Filtering (Strict Monday) ---
            week_monday = request.query_params.get('week_monday')
            if week_monday:
                week_date = parse_date(week_monday)
                if not week_date or week_date.weekday() != 0:
                    return Response(
                        {"error": "Validation Error", "message": "week_monday must be a valid Monday (YYYY-MM-DD)"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                assignments = assignments.filter(week_monday=week_date)

            # --- 3. Status Filtering ---
            active_only = request.query_params.get('active_only')
            if active_only and active_only.lower() == 'true':
                assignments = assignments.filter(removed_on__isnull=True)

            # --- 4. Range Filtering ---
            start_date_str = request.query_params.get('start_date')
            end_date_str = request.query_params.get('end_date')
            
            s_date = None
            e_date = None

            if start_date_str:
                s_date = parse_date(start_date_str)
                if not s_date:
                    return Response(
                        {"error": "Validation Error", "message": "start_date must be YYYY-MM-DD"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                assignments = assignments.filter(week_monday__gte=s_date)

            if end_date_str:
                e_date = parse_date(end_date_str)
                if not e_date:
                    return Response(
                        {"error": "Validation Error", "message": "end_date must be YYYY-MM-DD"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                assignments = assignments.filter(week_monday__lte=e_date)

            if s_date and e_date and s_date > e_date:
                return Response(
                    {"error": "Validation Error", "message": "start_date cannot be after end_date"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = ProjectAssignmentSerializer(assignments, many=True, context={'request': request})
            return Response(serializer.data)

        except Exception as e:
            logger.exception("ProjectAssignmentListCreate GET failed")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            serializer = ProjectAssignmentSerializer(data=request.data, context={'request': request})

            if serializer.is_valid():
                assignment = serializer.save()
                # Return freshly saved object with full context
                return Response(
                    ProjectAssignmentSerializer(assignment, context={'request': request}).data,
                    status=status.HTTP_201_CREATED
                )

            return Response(
                {"error": "Validation Error", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            logger.exception("ProjectAssignmentListCreate POST failed")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProjectAssignmentDetail(APIView):
    """
    Retrieve, update or delete a ProjectAssignment instance.
    URL: /api/project-assignments/<int:pk>/
    """

    def get_permissions(self):
        """
        Apply different permissions based on HTTP method:
        - GET → view permission
        - PUT/PATCH/DELETE → prepare permission
        """
        if self.request.method == 'GET':
            permission = ModuleViewPermission()
        else:
            permission = ModulePreparePermission()

        permission.module = "CAPACITY"
        return [permission]

    def get_object(self, pk):
        """
        Helper method to fetch the assignment or raise 404.
        Optimized with select_related for linked data.
        """
        try:
            return ProjectAssignment.objects.select_related('project', 'resource').get(pk=pk)
        except ProjectAssignment.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Database error in ProjectAssignment get_object: {str(e)}")
            raise e

    def get(self, request, pk):
        try:
            assignment = self.get_object(pk)
            if assignment is None:
                return Response(
                    {"error": "Not Found", "message": f"Project assignment with ID {pk} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ProjectAssignmentSerializer(assignment, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            logger.exception(f"ProjectAssignmentDetail GET failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            assignment = self.get_object(pk)
            if assignment is None:
                return Response(
                    {"error": "Not Found", "message": f"Project assignment with ID {pk} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ProjectAssignmentSerializer(
                assignment,
                data=request.data,
                partial=False,
                context={'request': request}
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(
                {"error": "Validation Error", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(f"ProjectAssignmentDetail PUT failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        try:
            assignment = self.get_object(pk)
            if assignment is None:
                return Response(
                    {"error": "Not Found", "message": f"Project assignment with ID {pk} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ProjectAssignmentSerializer(
                assignment,
                data=request.data,
                partial=True,
                context={'request': request}
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(
                {"error": "Validation Error", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(f"ProjectAssignmentDetail PATCH failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        try:
            assignment = self.get_object(pk)
            if assignment is None:
                return Response(
                    {"error": "Not Found", "message": f"Project assignment with ID {pk} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            assignment.delete()
            return Response(
                {"message": "Project assignment deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            logger.exception(f"ProjectAssignmentDetail DELETE failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ResourceAllocationListCreate(APIView):
    """
    List resource allocations (GET), create one (POST), or bulk delete (DELETE).
    URL: /api/resource-allocations/
    """

    def get_permissions(self):
        if self.request.method == 'GET':
            permission = ModuleViewPermission()
        else:
            permission = ModulePreparePermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            # Optimization: select_related for resource and project to prevent N+1 queries
            allocations = ResourceAllocation.objects.all().select_related('resource', 'project')

            # --- 1. Parameter Extraction & Validation ---
            project_id = request.query_params.get('project')
            if project_id:
                try:
                    allocations = allocations.filter(project_id=int(project_id))
                except ValueError:
                    return Response({"error": "Validation Error", "message": "project must be an integer"}, status=400)

            resource_id = request.query_params.get('resource')
            if resource_id:
                try:
                    allocations = allocations.filter(resource_id=int(resource_id))
                except ValueError:
                    return Response({"error": "Validation Error", "message": "resource must be an integer"}, status=400)

            # --- 2. Date Filtering ---
            week_monday = request.query_params.get('week_monday')
            if week_monday:
                try:
                    week_date = datetime.strptime(week_monday, '%Y-%m-%d').date()
                    if week_date.weekday() != 0:
                        return Response({"error": "Validation Error", "message": "week_monday must be a Monday"}, status=400)
                    allocations = allocations.filter(week_monday=week_date)
                except ValueError:
                    return Response({"error": "Validation Error", "message": "Invalid date format for week_monday"}, status=400)

            start_date = request.query_params.get('start_date')
            if start_date:
                try:
                    allocations = allocations.filter(week_monday__gte=datetime.strptime(start_date, '%Y-%m-%d').date())
                except ValueError:
                    return Response({"error": "Validation Error", "message": "Invalid format for start_date"}, status=400)

            end_date = request.query_params.get('end_date')
            if end_date:
                try:
                    allocations = allocations.filter(week_monday__lte=datetime.strptime(end_date, '%Y-%m-%d').date())
                except ValueError:
                    return Response({"error": "Validation Error", "message": "Invalid format for end_date"}, status=400)

            # --- 3. Internal/External Filtering ---
            is_internal = request.query_params.get('is_internal')
            if is_internal is not None:
                if is_internal.lower() not in ['true', 'false']:
                    return Response({"error": "Validation Error", "message": "is_internal must be true/false"}, status=400)
                allocations = allocations.filter(resource__is_internal=(is_internal.lower() == 'true'))

            # Final processing
            allocations = allocations.order_by('-week_monday', 'resource__name')
            serializer = ResourceAllocationSerializer(allocations, many=True, context={'request': request})
            return Response(serializer.data)

        except Exception as e:
            logger.exception("ResourceAllocation GET failed")
            return Response({"error": "Internal Server Error", "message": str(e)}, status=500)

    def post(self, request):
        try:
            serializer = ResourceAllocationSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                allocation = serializer.save()
                return Response(ResourceAllocationSerializer(allocation, context={'request': request}).data, status=201)
            return Response({"error": "Validation Error", "message": serializer.errors}, status=400)
        except Exception as e:
            logger.exception("ResourceAllocation POST failed")
            return Response({"error": "Internal Server Error", "message": str(e)}, status=500)

    def delete(self, request):
        try:
            ids_list = request.data.get('ids')
            if not ids_list or not isinstance(ids_list, list):
                return Response({"error": "Validation Error", "message": "'ids' list is required in request body"}, status=400)

            # Optional safety filters from query params
            project_id_str = request.query_params.get('project')
            dept_id_str = request.query_params.get('depId')
            extra_filters = Q()

            try:
                if project_id_str: extra_filters &= Q(project_id=int(project_id_str))
                if dept_id_str: extra_filters &= Q(department_id=int(dept_id_str))
            except ValueError:
                return Response({"error": "Validation Error", "message": "project/depId must be integers"}, status=400)

            with transaction.atomic():
                # 1. Fetch Assignments to be deleted
                assignments = ProjectAssignment.objects.filter(id__in=ids_list).filter(extra_filters)
                if not assignments.exists():
                    return Response({"message": "No matching ProjectAssignment records found"}, status=200)

                # 2. Build cross-table deletion conditions
                delete_conditions = Q()
                for assignment in assignments:
                    delete_conditions |= Q(
                        resource_id=assignment.resource_id,
                        week_monday=assignment.week_monday,
                        project_id=assignment.project_id,
                        department_id=assignment.department_id,
                    )

                # 3. Perform synchronized deletion
                ra_deleted_count, _ = ResourceAllocation.objects.filter(delete_conditions).delete()
                pa_deleted_count, _ = assignments.delete()

                return Response({
                    "message": f"Deleted {pa_deleted_count} assignment(s) and {ra_deleted_count} allocation(s)"
                }, status=200)

        except Exception as e:
            logger.exception("ResourceAllocation bulk DELETE failed")
            return Response({"error": "Delete failed", "message": str(e)}, status=500)


class ResourceAllocationDetail(APIView):
    """
    Retrieve, update or delete a ResourceAllocation instance.
    URL: /api/resource-allocations/<int:pk>/
    """

    def get_permissions(self):
        if self.request.method == 'GET':
            permission = ModuleViewPermission()
        else:
            permission = ModulePreparePermission()

        permission.module = "CAPACITY"
        return [permission]

    def get_object(self, pk):
        """
        Fetch the ResourceAllocation with related objects or return None.
        """
        try:
            return ResourceAllocation.objects.select_related(
                'resource', 'project', 'department'
            ).get(pk=pk)
        except ResourceAllocation.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Database error in ResourceAllocation get_object: {str(e)}")
            raise e

    def get(self, request, pk):
        try:
            allocation = self.get_object(pk)
            if allocation is None:
                return Response(
                    {"error": "Not Found", "message": f"Resource allocation with ID {pk} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ResourceAllocationSerializer(allocation, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            logger.exception(f"ResourceAllocationDetail GET failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            allocation = self.get_object(pk)
            if allocation is None:
                return Response(
                    {"error": "Not Found", "message": f"Resource allocation with ID {pk} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ResourceAllocationSerializer(
                allocation,
                data=request.data,
                partial=False,
                context={'request': request}
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(
                {"error": "Validation Error", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(f"ResourceAllocationDetail PUT failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        try:
            allocation = self.get_object(pk)
            if allocation is None:
                return Response(
                    {"error": "Not Found", "message": f"Resource allocation with ID {pk} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ResourceAllocationSerializer(
                allocation,
                data=request.data,
                partial=True,
                context={'request': request}
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(
                {"error": "Validation Error", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(f"ResourceAllocationDetail PATCH failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        try:
            allocation = self.get_object(pk)
            if allocation is None:
                return Response(
                    {"error": "Not Found", "message": f"Resource allocation with ID {pk} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            with transaction.atomic():
                # Step 1: Delete matching ProjectAssignment(s)
                # We use specific filters to ensure we only remove the work actually linked to this allocation
                deleted_assignments = ProjectAssignment.objects.filter(
                    resource=allocation.resource,
                    project=allocation.project,
                    department=allocation.department,
                    week_monday=allocation.week_monday
                ).delete()

                # Step 2: Delete the ResourceAllocation itself
                allocation.delete()

                assign_count = deleted_assignments[0] if deleted_assignments else 0
                return Response(
                    {
                        "message": "Resource allocation deleted successfully",
                        "assignments_removed": assign_count
                    }, 
                    status=status.HTTP_200_OK # Changed to 200 to allow returning the JSON message
                )

        except Exception as e:
            logger.exception(f"ResourceAllocationDetail DELETE failed for ID {pk}")
            return Response(
                {
                    "error": "Delete Failed", 
                    "message": f"Could not remove allocation: {str(e)}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class ProjectWeekAllocationListCreate(APIView):
    """
    List project week allocations (GET), create one (POST), or bulk delete (DELETE).
    URL: /api/project-week-allocations/
    """

    def get_permissions(self):
        if self.request.method == 'GET':
            permission = ModuleViewPermission()
        else:
            permission = ModulePreparePermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            allocations = ProjectWeekAllocation.objects.all().select_related('project', 'department')

            # --- 1. Mandatory Department Filter ---
            dept_id = request.query_params.get('depId')
            if not dept_id:
                return Response({
                    "error": "Validation Error", 
                    "message": "depId query parameter is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                dept = Department.objects.get(id=int(dept_id))
                descendants = [dept] + list(dept.get_descendants())
                allocations = allocations.filter(department__in=descendants)
            except (ValueError, Department.DoesNotExist):
                return Response({
                    "error": "Not Found", 
                    "message": f"Department with ID {dept_id} not found or invalid."
                }, status=status.HTTP_404_NOT_FOUND)

            # --- 2. Optional Project Filter ---
            project_id = request.query_params.get('project')
            if project_id:
                try:
                    allocations = allocations.filter(project_id=int(project_id))
                except ValueError:
                    return Response({
                        "error": "Validation Error", 
                        "message": "project parameter must be an integer"
                    }, status=status.HTTP_400_BAD_REQUEST)

            # --- 3. Week/Date Filtering ---
            week_monday = request.query_params.get('week_monday')
            if week_monday:
                try:
                    week_date = datetime.strptime(week_monday, '%Y-%m-%d').date()
                    if week_date.weekday() != 0:
                        return Response({
                            "error": "Validation Error", 
                            "message": "week_monday must be a Monday"
                        }, status=status.HTTP_400_BAD_REQUEST)
                    allocations = allocations.filter(week_monday=week_date)
                except ValueError:
                    return Response({
                        "error": "Validation Error", 
                        "message": "Invalid week_monday format. Use YYYY-MM-DD"
                    }, status=status.HTTP_400_BAD_REQUEST)

            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            try:
                if start_date:
                    allocations = allocations.filter(week_monday__gte=datetime.strptime(start_date, '%Y-%m-%d').date())
                if end_date:
                    allocations = allocations.filter(week_monday__lte=datetime.strptime(end_date, '%Y-%m-%d').date())
                
                if start_date and end_date:
                    if datetime.strptime(start_date, '%Y-%m-%d').date() > datetime.strptime(end_date, '%Y-%m-%d').date():
                        return Response({
                            "error": "Validation Error", 
                            "message": "start_date cannot be after end_date"
                        }, status=status.HTTP_400_BAD_REQUEST)
            except ValueError as e:
                return Response({
                    "error": "Validation Error", 
                    "message": f"Date parsing error: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

            # --- 4. Search & Ordering ---
            notes_search = request.query_params.get('notes_search')
            if notes_search:
                allocations = allocations.filter(notes__icontains=notes_search.strip())

            allocations = allocations.order_by('-week_monday', 'project__project_code')

            serializer = ProjectWeekAllocationSerializer(allocations, many=True, context={'request': request})
            return Response(serializer.data)

        except Exception as e:
            logger.exception("ProjectWeekAllocation GET failed")
            return Response({
                "error": "Internal Server Error", 
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = ProjectWeekAllocationSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                allocation = serializer.save()
                return Response(
                    ProjectWeekAllocationSerializer(allocation, context={'request': request}).data,
                    status=status.HTTP_201_CREATED
                )
            return Response({
                "error": "Validation Error", 
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("ProjectWeekAllocation POST failed")
            return Response({
                "error": "Internal Server Error", 
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            ids_list = request.data.get('ids')
            if not ids_list or not isinstance(ids_list, list):
                return Response({
                    "error": "Validation Error", 
                    "message": "Missing 'ids' list in request body"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Extra safety checks
            dept_id_str = request.query_params.get('depId')
            project_id_str = request.query_params.get('project')
            filters = {'id__in': ids_list}

            try:
                if dept_id_str: filters['department_id'] = int(dept_id_str)
                if project_id_str: filters['project_id'] = int(project_id_str)
            except ValueError:
                return Response({"error": "Validation Error", "message": "depId/project must be integers"}, status=400)

            with transaction.atomic():
                week_allocations = ProjectWeekAllocation.objects.filter(**filters)
                if not week_allocations.exists():
                    return Response({"message": "No matching week allocations found"}, status=200)

                week_allocation_ids = list(week_allocations.values_list('id', flat=True))

                # Step-down deletion (ResourceAllocation -> ProjectAssignment -> ProjectWeekAllocation)
                ResourceAllocation.objects.filter(week_allocation_id__in=week_allocation_ids).delete()
                ProjectAssignment.objects.filter(week_allocation_id__in=week_allocation_ids).delete()
                deleted_count, _ = week_allocations.delete()

                return Response({
                    "message": f"Successfully deleted {deleted_count} allocation(s) and all linked assignments."
                }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception("ProjectWeekAllocation bulk DELETE failed")
            return Response({
                "error": "Delete Failed", 
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectWeekAllocationDetailAPIView(APIView):
    """
    Retrieve, update, partially update, or delete a specific project week allocation.
    URL: /api/project-week-allocations/<int:pk>/
    """
    permission_classes = [AllowAny]  # Change to IsAuthenticated in production

    def get_object(self, pk):
        """
        Fetch the object safely with optimized related lookups.
        """
        try:
            return ProjectWeekAllocation.objects.select_related('project', 'department').get(pk=pk)
        except ProjectWeekAllocation.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Database error in ProjectWeekAllocation lookup: {str(e)}")
            raise e

    def get(self, request, pk):
        try:
            allocation = self.get_object(pk)
            if not allocation:
                return Response(
                    {"error": "Not Found", "message": f"Project week allocation with ID {pk} not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ProjectWeekAllocationSerializer(allocation, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            logger.exception(f"GET failed for ProjectWeekAllocation {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            allocation = self.get_object(pk)
            if not allocation:
                return Response(
                    {"error": "Not Found", "message": "Project week allocation not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ProjectWeekAllocationSerializer(
                allocation,
                data=request.data,
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(
                {"error": "Validation Error", "message": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(f"PUT failed for ProjectWeekAllocation {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        try:
            allocation = self.get_object(pk)
            if not allocation:
                return Response(
                    {"error": "Not Found", "message": "Project week allocation not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ProjectWeekAllocationSerializer(
                allocation,
                data=request.data,
                partial=True,
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(
                {"error": "Validation Error", "message": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(f"PATCH failed for ProjectWeekAllocation {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        try:
            allocation = self.get_object(pk)
            if not allocation:
                return Response(
                    {"error": "Not Found", "message": "Project week allocation not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            with transaction.atomic():
                # Step 1: Cleanup dependent actual data
                ra_count = ResourceAllocation.objects.filter(week_allocation=allocation).delete()[0]
                pa_count = ProjectAssignment.objects.filter(week_allocation=allocation).delete()[0]

                # Step 2: Delete the planned allocation
                allocation.delete()

            return Response(
                {
                    "message": "Allocation and related records deleted successfully",
                    "resource_allocations_removed": ra_count,
                    "project_assignments_removed": pa_count
                }, 
                status=status.HTTP_200_OK # Changed to 200 so we can return the cleanup summary
            )
        except Exception as e:
            logger.exception(f"DELETE failed for ProjectWeekAllocation {pk}")
            return Response(
                {"error": "Internal Server Error", "message": f"Could not perform cleanup: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ExternalCapacityListCreate(APIView):
    """
    List all external capacities (GET) or create a new one (POST)
    URL: /api/external-capacities/
    """

    def get_permissions(self):
        """
        Different permissions for GET vs POST
        """
        if self.request.method == 'GET':
            permission = ModuleViewPermission()
        else:
            permission = ModulePreparePermission()

        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            # Optimization: select_related for foreign keys to prevent N+1 queries
            capacities = ExternalCapacity.objects.all().select_related('supplier', 'project')

            # --- 1. ID Filtering ---
            supplier_id = request.query_params.get('supplier')
            if supplier_id:
                try:
                    capacities = capacities.filter(supplier_id=int(supplier_id))
                except ValueError:
                    return Response({
                        "error": "Validation Error", 
                        "message": "supplier must be a valid integer ID"
                    }, status=status.HTTP_400_BAD_REQUEST)

            project_id = request.query_params.get('project')
            if project_id:
                try:
                    capacities = capacities.filter(project_id=int(project_id))
                except ValueError:
                    return Response({
                        "error": "Validation Error", 
                        "message": "project must be a valid integer ID"
                    }, status=status.HTTP_400_BAD_REQUEST)

            # --- 2. Date Filtering (Strict Monday Check) ---
            week_monday = request.query_params.get('week_monday')
            if week_monday:
                try:
                    week_date = datetime.strptime(week_monday, '%Y-%m-%d').date()
                    if week_date.weekday() != 0:  # 0 = Monday
                        return Response({
                            "error": "Validation Error", 
                            "message": "week_monday must be a Monday"
                        }, status=status.HTTP_400_BAD_REQUEST)
                    capacities = capacities.filter(week_monday=week_date)
                except ValueError:
                    return Response({
                        "error": "Validation Error", 
                        "message": "week_monday must be YYYY-MM-DD"
                    }, status=status.HTTP_400_BAD_REQUEST)

            # --- 3. Date Range Filtering ---
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            parsed_start = parsed_end = None

            try:
                if start_date:
                    parsed_start = datetime.strptime(start_date, '%Y-%m-%d').date()
                    capacities = capacities.filter(week_monday__gte=parsed_start)
                if end_date:
                    parsed_end = datetime.strptime(end_date, '%Y-%m-%d').date()
                    capacities = capacities.filter(week_monday__lte=parsed_end)
                
                if parsed_start and parsed_end and parsed_start > parsed_end:
                    return Response({
                        "error": "Validation Error", 
                        "message": "start_date cannot be after end_date"
                    }, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({
                    "error": "Validation Error", 
                    "message": "Range dates must be in YYYY-MM-DD format"
                }, status=status.HTTP_400_BAD_REQUEST)

            # --- 4. Minimum Hours Filter ---
            min_hours = request.query_params.get('min_hours')
            if min_hours:
                try:
                    min_h = int(min_hours)
                    if min_h < 0:
                        return Response({
                            "error": "Validation Error", 
                            "message": "min_hours must be non-negative"
                        }, status=status.HTTP_400_BAD_REQUEST)
                    capacities = capacities.filter(hours__gte=min_h)
                except ValueError:
                    return Response({
                        "error": "Validation Error", 
                        "message": "min_hours must be an integer"
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Ordering & Serialization
            capacities = capacities.order_by('-week_monday', 'supplier__name')
            serializer = ExternalCapacitySerializer(capacities, many=True, context={'request': request})
            return Response(serializer.data)

        except Exception as e:
            logger.exception("ExternalCapacity GET failed")
            return Response({
                "error": "Internal Server Error", 
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = ExternalCapacitySerializer(data=request.data, context={'request': request})

            if serializer.is_valid():
                capacity = serializer.save()
                # Return freshly created data with full context
                return Response(
                    ExternalCapacitySerializer(capacity, context={'request': request}).data,
                    status=status.HTTP_201_CREATED
                )

            return Response({
                "error": "Validation Error", 
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("ExternalCapacity POST failed")
            return Response({
                "error": "Internal Server Error", 
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ExternalCapacityDetail(APIView):
    """
    Retrieve, update or delete an ExternalCapacity instance.
    URL: /api/external-capacities/<int:pk>/
    """

    def get_permissions(self):
        """
        Apply different permissions based on HTTP method:
        - GET → view permission
        - PUT/PATCH/DELETE → prepare permission
        """
        if self.request.method == 'GET':
            permission = ModuleViewPermission()
        else:
            permission = ModulePreparePermission()

        permission.module = "CAPACITY"
        return [permission]

    def get_object(self, pk):
        """
        Fetch the ExternalCapacity or return None.
        Optimized with select_related for supplier and project.
        """
        try:
            return ExternalCapacity.objects.select_related('supplier', 'project').get(pk=pk)
        except ExternalCapacity.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Database error in ExternalCapacity lookup: {str(e)}")
            raise e

    def get(self, request, pk):
        try:
            capacity = self.get_object(pk)
            if capacity is None:
                return Response(
                    {"error": "Not Found", "message": f"External capacity with ID {pk} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ExternalCapacitySerializer(capacity, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            logger.exception(f"ExternalCapacityDetail GET failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            capacity = self.get_object(pk)
            if capacity is None:
                return Response(
                    {"error": "Not Found", "message": "External capacity not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ExternalCapacitySerializer(
                capacity,
                data=request.data,
                partial=False,
                context={'request': request}
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(
                {"error": "Validation Error", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(f"ExternalCapacityDetail PUT failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        try:
            capacity = self.get_object(pk)
            if capacity is None:
                return Response(
                    {"error": "Not Found", "message": "External capacity not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ExternalCapacitySerializer(
                capacity,
                data=request.data,
                partial=True,
                context={'request': request}
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(
                {"error": "Validation Error", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(f"ExternalCapacityDetail PATCH failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        try:
            capacity = self.get_object(pk)
            if capacity is None:
                return Response(
                    {"error": "Not Found", "message": "External capacity not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            capacity.delete()
            return Response(
                {"message": "External capacity deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            logger.exception(f"ExternalCapacityDetail DELETE failed for ID {pk}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class ExternalCapacityBulkCreate(APIView):
    """
    Bulk create ExternalCapacity records.
    URL: POST /api/external-capacities/bulk/
    Features: Specific error messaging, Planned Demand validation, and Supplier budget updates.
    """

    def get_permissions(self):
        permission = ModulePreparePermission()
        permission.module = "CAPACITY"
        return [permission]
        
    def post(self, request):
        try:
            data = request.data

            # --- 1. Basic Structure Validation ---
            if not isinstance(data, list):
                return Response({
                    "error": "Validation Error",
                    "message": "Request body must be a JSON array."
                }, status=status.HTTP_400_BAD_REQUEST)

            if not data:
                return Response({
                    "error": "Validation Error",
                    "message": "Empty array not allowed."
                }, status=status.HTTP_400_BAD_REQUEST)

            errors = []
            valid_items_to_save = []
            seen_keys = set()  # For intra-batch duplicate prevention

            # --- 2. Iterative Validation ---
            for index, item in enumerate(data):
                item_errors = {}
                
                # Extract your specific keys
                project_code = item.get('project_code_input')
                dept_id = item.get('dept_id')
                supplier_id = item.get('supplier_id')
                week_monday_str = item.get('week_monday')
                hours = float(item.get('hours', 0) or 0)
                notes = str(item.get('notes', ''))

                # Field Presence Validation
                if not project_code: item_errors['project'] = "Project code is required"
                if not dept_id: item_errors['department'] = "Department ID is required"
                if not supplier_id: item_errors['supplier'] = "Supplier ID is required"
                if hours <= 0: item_errors['hours'] = "Hours must be greater than 0"

                # Date Formatting
                week_monday = None
                try:
                    if week_monday_str:
                        week_monday = datetime.strptime(week_monday_str, "%Y-%m-%d").date()
                    else:
                        item_errors['week_monday'] = "Week Monday is required"
                except (ValueError, TypeError):
                    item_errors['week_monday'] = f"Invalid date format '{week_monday_str}' (Use YYYY-MM-DD)"

                if item_errors:
                    errors.append({"index": index, "sent_data": item, "errors": item_errors})
                    continue

                # --- 3. Database & Planned Demand Logic ---
                try:
                    # A. Resolve Project Code to ID
                    project_obj = Project.objects.get(project_code__iexact=str(project_code).strip())

                    # B. Logic: Check for Planned Demand (ProjectWeekAllocation)
                    if not ProjectWeekAllocation.objects.filter(
                        project=project_obj,
                        department_id=dept_id,
                        week_monday=week_monday
                    ).exists():
                        item_errors['week_monday'] = f"No planned demand found for Project {project_code} on {week_monday_str}"

                    # C. Check for Duplicate in the same request batch
                    dupe_key = (project_obj.id, dept_id, week_monday, supplier_id)
                    if dupe_key in seen_keys:
                        item_errors['duplicate'] = f"Duplicate row for {project_code} / Supplier {supplier_id} on {week_monday_str}"
                    seen_keys.add(dupe_key)

                    # D. Check for existing record in DB
                    if ExternalCapacity.objects.filter(
                        project=project_obj,
                        dept_id=dept_id,
                        week_monday=week_monday,
                        supplier_id=supplier_id
                    ).exists():
                        item_errors['duplicate'] = f"External capacity already exists for {project_code} / Supplier {supplier_id} on {week_monday_str}"

                    # E. Map to Serializer format if clean
                    if not item_errors:
                        valid_items_to_save.append({
                            "project": project_obj.id,  # Match 'project' PrimaryKeyRelatedField
                            "dept": dept_id,           # Match 'dept' PrimaryKeyRelatedField
                            "supplier": supplier_id,    # Match 'supplier' PrimaryKeyRelatedField
                            "week_monday": week_monday,
                            "hours": hours,
                            "notes": notes
                        })

                except Project.DoesNotExist:
                    item_errors['project'] = f"Project code '{project_code}' not found"
                except Exception as e:
                    item_errors['system'] = str(e)

                if item_errors:
                    errors.append({"index": index, "sent_data": item, "errors": item_errors})

            # --- 4. Specific Error Response ---
            if errors:
                # Find the first specific error message to return at the top level
                first_item_errors = errors[0].get('errors', {})
                first_message = next(iter(first_item_errors.values())) if first_item_errors else "Validation failed"

                return Response({
                    "error": "Validation Error",
                    "message": first_message,  # Specific message like "No planned demand..."
                    "error_details": errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # --- 5. Atomic Save & Supplier Updates ---
            serializer = ExternalCapacitySerializer(data=valid_items_to_save, many=True)
            if not serializer.is_valid():
                return Response({
                    "error": "Serializer Error",
                    "message": "Type validation failed",
                    "error_details": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                created_records = serializer.save()

                # Trigger budget recalculations for affected suppliers
                affected_suppliers = set(cap.supplier for cap in created_records)
                for supplier in affected_suppliers:
                    if hasattr(supplier, 'update_budgeted_hours'):
                        supplier.update_budgeted_hours()

            return Response({
                "message": f"Successfully created {len(created_records)} external capacity records.",
                "total_requested": len(data),
                "created_count": len(created_records)
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception("ExternalCapacityBulkCreate failed")
            return Response({
                "error": "Internal Server Error",
                "message": f"Bulk creation aborted: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST', 'PUT', 'PATCH'])
@authentication_classes([])
@permission_classes([AllowAny])
def debug_view(request):
    """
    Open endpoint for testing connectivity, headers, and CORS.
    """
    try:
        # Log the hit for server-side confirmation
        logger.info(f"Debug view accessed: {request.method} from {request.META.get('REMOTE_ADDR')}")

        return Response({
            "status": "success",
            "message": "Public access confirmed",
            "method": request.method,
            "user": str(request.user),
            "auth_status": "No authentication required"
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception("Debug view failed")
        return Response({
            "error": "Internal Server Error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProjectWeekAllocationBulkCreate(APIView):
    """
    Bulk create OR increment existing ProjectWeekAllocations.
    - New allocation → create
    - Existing allocation → add manhours to current value via F() expression
    """

    def get_permissions(self):
        permission = ModulePreparePermission()
        permission.module = "CAPACITY"
        return [permission]

    def post(self, request):
        try:
            data = request.data

            # --- 1. Basic Structure Validation ---
            if not isinstance(data, list):
                return Response({
                    "error": "Validation Error",
                    "message": "Request body must be a JSON array."
                }, status=status.HTTP_400_BAD_REQUEST)

            if not data:
                return Response({
                    "error": "Validation Error",
                    "message": "Empty array not allowed."
                }, status=status.HTTP_400_BAD_REQUEST)

            if len(data) > 200:
                return Response({
                    "error": "Constraint Error",
                    "message": "Maximum 200 items per bulk request for performance safety."
                }, status=status.HTTP_400_BAD_REQUEST)

            # --- 2. Initial Parsing & Per-Item Validation ---
            errors = []
            to_create = []
            to_update = []  # list of (existing_obj, added_manhours, notes)
            seen_keys = set()
            added_by_pd = defaultdict(float)  # track total hours added per Project+Dept

            for idx, item in enumerate(data):
                item_errors = {}

                # Flexible input field capturing
                project_code = (item.get('project_code') or item.get('project_code_input') or '').strip()
                dept_name = (item.get('department_name') or item.get('department_name_input') or '').strip()
                week_str = item.get('week_monday')
                manhours = item.get('manhours')
                notes = (item.get('notes') or '').strip()

                # Basic validation
                if not project_code: item_errors['project_code'] = 'Required'
                if not dept_name: item_errors['department_name'] = 'Required'
                if not week_str: item_errors['week_monday'] = 'Required'
                
                if manhours is None:
                    item_errors['manhours'] = 'Required'
                else:
                    try:
                        manhours = float(manhours)
                        if manhours < 0:
                            item_errors['manhours'] = 'Must be non-negative'
                    except (ValueError, TypeError):
                        item_errors['manhours'] = 'Must be a valid number'

                try:
                    week_monday = datetime.strptime(week_str, "%Y-%m-%d").date()
                except (ValueError, TypeError):
                    item_errors['week_monday'] = 'Invalid date format. Use YYYY-MM-DD'

                if item_errors:
                    errors.append({"index": idx, "data": item, "errors": item_errors})
                    continue

                # Database resolution
                try:
                    department = Department.objects.get(name__iexact=dept_name)
                    
                    pd_alloc = ProjectDepartmentAllocation.objects.select_related('project').get(
                        project__project_code__iexact=project_code,
                        department=department
                    )
                    project = pd_alloc.project
                except Department.DoesNotExist:
                    item_errors['department_name'] = f"Department '{dept_name}' not found"
                    errors.append({"index": idx, "data": item, "errors": item_errors})
                    continue
                except ProjectDepartmentAllocation.DoesNotExist:
                    item_errors['project_code'] = f"No allocation for '{project_code}' in '{dept_name}'"
                    errors.append({"index": idx, "data": item, "errors": item_errors})
                    continue
                except Exception as e:
                    item_errors['non_field_error'] = f"Lookup error: {str(e)}"
                    errors.append({"index": idx, "data": item, "errors": item_errors})
                    continue

                # Local Duplicate Check (prevent same week appearing twice in one CSV/JSON batch)
                key = (project.id, department.id, week_monday)
                if key in seen_keys:
                    item_errors['non_field_error'] = f"Duplicate week {week_monday} for this project in this request"
                    errors.append({"index": idx, "data": item, "errors": item_errors})
                    continue
                seen_keys.add(key)

                # Preparation for Capacity Check
                added_by_pd[(project.id, department.id)] += manhours

                # Check if we update or create
                existing = ProjectWeekAllocation.objects.filter(
                    project=project,
                    department=department,
                    week_monday=week_monday
                ).first()

                if existing:
                    to_update.append((existing, manhours, notes))
                else:
                    to_create.append(
                        ProjectWeekAllocation(
                            project=project,
                            department=department,
                            week_monday=week_monday,
                            manhours=manhours,
                            notes=notes
                        )
                    )

            # --- 3. Global Capacity Limit Check ---
            # We must ensure the SUM of all weeks doesn't exceed the Department Allocation limit
            if not errors and (to_create or to_update):
                for (proj_id, dept_id), added_val in added_by_pd.items():
                    pd_ref = ProjectDepartmentAllocation.objects.get(project_id=proj_id, department_id=dept_id)
                    
                    current_total = ProjectWeekAllocation.objects.filter(
                        project_id=proj_id,
                        department_id=dept_id
                    ).aggregate(total=Sum('manhours'))['total'] or 0.0

                    if float(current_total) + added_val > float(pd_ref.estimated_manhours):
                        return Response({
                            "error": "Capacity Exceeded",
                            "message": f"Bulk import for Project {pd_ref.project.project_code} in {pd_ref.department.name} "
                                       f"would exceed the estimated limit ({current_total + added_val} > {pd_ref.estimated_manhours})"
                        }, status=status.HTTP_400_BAD_REQUEST)

            # --- 4. Final Error Check ---
            if errors:
                return Response({
                    "status": "error",
                    "total_requested": len(data),
                    "error_count": len(errors),
                    "error_details": errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # --- 5. Atomic Save ---
            with transaction.atomic():
                created_objs = ProjectWeekAllocation.objects.bulk_create(to_create)
                
                updated_count = 0
                for obj, add_hours, new_notes in to_update:
                    obj.manhours = F('manhours') + add_hours
                    # Notes are updated only if provided, otherwise keep old ones
                    if new_notes:
                        obj.notes = new_notes
                    obj.save(update_fields=['manhours', 'notes'])
                    updated_count += 1

            return Response({
                "status": "success",
                "total_requested": len(data),
                "created": len(created_objs),
                "updated": updated_count,
                "message": "All allocations processed successfully."
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception("ProjectWeekAllocation Bulk Create Failed")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class ProjectAssignmentBulkCreateAPIView(APIView):
    """
    Bulk create ProjectAssignments + optional ResourceAllocations.
    URL: POST /api/project-assignments/bulk/
    Features: Atomic transactions, multi-level capacity enforcement, and joining date validation.
    """
    permission_classes = [ModulePreparePermission]

    def get_permissions(self):
        permission = ModulePreparePermission()
        permission.module = "CAPACITY"
        return [permission]

    def post(self, request):
        try:
            data = request.data

            # --- 1. Basic Structure Validation ---
            if not isinstance(data, list):
                return Response({
                    "error": "Validation Error",
                    "message": "Request body must be a JSON array of objects."
                }, status=status.HTTP_400_BAD_REQUEST)

            if not data:
                return Response({
                    "error": "Validation Error",
                    "message": "Empty array not allowed."
                }, status=status.HTTP_400_BAD_REQUEST)

            # if len(data) > 100:
            #     return Response({
            #         "error": "Constraint Error",
            #         "message": "Maximum 100 items allowed per bulk request for performance safety."
            #     }, status=status.HTTP_400_BAD_REQUEST)

            errors = []
            assignments_to_create = []
            allocations_to_create = []
            assignments_to_update = []
            allocations_to_update = []
            seen_keys = set()  # (resource_id, project_id, department_id, week_monday)

            # Caches and Accumulators
            planned_week_cache = {}
            resource_week_hours = defaultdict(float)  # (res_id, week) -> hours
            dept_project_hours = defaultdict(float)   # (proj_id, dept_id) -> hours

            # --- 2. Iterative Validation and Mapping ---
            for index, item in enumerate(data):
                item_errors = {}

                # Field Extraction
                project_code = item.get('project_code_input')
                department_name = item.get('department_name')
                week_monday_str = item.get('week_monday')
                resource_id = item.get('resource_id')
                resource_name = item.get('resource_name')
                hours = float(item.get('hours', 0) or 0)
                is_lead = bool(item.get('is_lead', False))
                notes = str(item.get('notes', ''))

                # Basic Presence Check
                if not project_code: item_errors['project_code'] = "Required"
                if not department_name: item_errors['department_name'] = "Required"
                if not week_monday_str: item_errors['week_monday'] = "Required"
                if not resource_id and not resource_name:
                    item_errors['resource'] = "Either resource_id or resource_name required"

                try:
                    week_monday = datetime.strptime(week_monday_str, "%Y-%m-%d").date()
                except (ValueError, TypeError):
                    item_errors['week_monday'] = "Invalid format. Use YYYY-MM-DD"

                if hours < 0: item_errors['hours'] = "Must be >= 0"

                if item_errors:
                    errors.append({"index": index, "sent_data": item, "errors": item_errors})
                    continue

                # Database Resolution Logic
                try:
                    # A. Lookup Dept
                    dept_obj = Department.objects.get(name__iexact=department_name.strip())
                    
                    # B. Lookup Project (Must be allocated to this dept)
                    pd_alloc = ProjectDepartmentAllocation.objects.select_related('project').get(
                        project__project_code__iexact=str(project_code).strip(),
                        department=dept_obj
                    )
                    proj_obj = pd_alloc.project

                    # C. Lookup Resource
                    if resource_id:
                        res_obj = Resource.objects.get(id=resource_id, is_active=True)
                    else:
                        res_obj = Resource.objects.get(name__iexact=resource_name.strip(), is_active=True)

                    # D. Joining Date Check
                    if res_obj.joining_date:
                        res_monday = res_obj.joining_date - timedelta(days=res_obj.joining_date.weekday())
                        if week_monday < res_monday:
                            item_errors['week_monday'] = f"Before joining date ({res_obj.joining_date})"

                    # E. Planned Demand Check
                    cache_key = (proj_obj.id, dept_obj.id, week_monday)
                    if cache_key not in planned_week_cache:
                        planned_week_cache[cache_key] = ProjectWeekAllocation.objects.get(
                            project=proj_obj, department=dept_obj, week_monday=week_monday
                        )
                    
                    week_alloc_obj = planned_week_cache[cache_key]

                    # F. Request Duplicate Check
                    dupe_key = (res_obj.id, proj_obj.id, dept_obj.id, week_monday)
                    if dupe_key in seen_keys:
                        item_errors['duplicate'] = "Duplicate assignment in this request batch"
                    seen_keys.add(dupe_key)

                    # G. Database Duplicate Check
                    # if ProjectAssignment.objects.filter(
                    #     resource=res_obj, project=proj_obj, department=dept_obj, week_monday=week_monday
                    # ).exists():
                    #     item_errors['duplicate'] = "Employee is already assigned to this project/week/dept"

                    existing_asgn = ProjectAssignment.objects.filter(
                        resource=res_obj, project=proj_obj, department=dept_obj, week_monday=week_monday
                    ).first()

                    existing_alloc = ResourceAllocation.objects.filter(
                        resource=res_obj, project=proj_obj, department=dept_obj, week_monday=week_monday
                    ).first()

                except Department.DoesNotExist:
                    item_errors['department_name'] = "Department not found"
                except ProjectDepartmentAllocation.DoesNotExist:
                    item_errors['project_code'] = "Project not allocated to this department"
                except Resource.DoesNotExist:
                    item_errors['resource'] = "Resource not found or inactive"
                except Resource.MultipleObjectsReturned:
                    item_errors['resource'] = "Multiple resources found with this name. Use resource_id."
                except ProjectWeekAllocation.DoesNotExist:
                    item_errors['week_monday'] = "No planned demand found for this project/week/dept"
                except Exception as e:
                    item_errors['system'] = str(e)

                if item_errors:
                    errors.append({"index": index, "sent_data": item, "errors": item_errors})
                    continue

                # Accumulate for capacity checks
                resource_week_hours[(res_obj.id, week_monday)] += hours
                dept_project_hours[(proj_obj.id, dept_obj.id)] += hours

                # Stage Objects
                if existing_asgn:
                    existing_asgn.is_lead = is_lead
                    existing_asgn.notes = notes
                    assignments_to_update.append(existing_asgn)
                else:
                    assignments_to_create.append(ProjectAssignment(
                        week_allocation=week_alloc_obj, resource=res_obj, project=proj_obj,
                        department=dept_obj, is_lead=is_lead, notes=notes, week_monday=week_monday
                    ))

                if hours > 0:
                    if existing_alloc:
                        existing_alloc.hours += int(hours)
                        allocations_to_update.append(existing_alloc)
                    else:
                        allocations_to_create.append(ResourceAllocation(
                            week_allocation=week_alloc_obj, resource=res_obj, project=proj_obj,
                            department=dept_obj, week_monday=week_monday, hours=int(hours)
                        ))

            # --- 3. Capacity Enforcement ---
            if not errors:
                # Check A: Individual Employee Over-allocation
                for (rid, week), val in resource_week_hours.items():
                    res = Resource.objects.get(id=rid)
                    current_h = ResourceAllocation.objects.filter(resource=res, week_monday=week).aggregate(total=Sum('hours'))['total'] or 0
                    if float(current_h) + val > float(res.effective_availability_per_week):
                        return Response({
                            "error": "Resource Capacity Exceeded",
                            "message": f"{res.name} cannot exceed {res.effective_availability_per_week}h/week. (Current: {current_h}h, Request: {val}h)"
                        }, status=status.HTTP_400_BAD_REQUEST)
                # NEW Check C: Weekly Project/Dept Demand Capacity
                # We aggregate total hours requested PER project, PER dept, PER week in this batch

                batch_weekly_demand = defaultdict(float)
                for alloc in allocations_to_create:
                    batch_key = (alloc.project_id, alloc.department_id, alloc.week_monday)
                    batch_weekly_demand[batch_key] += hours

                for alloc in allocations_to_update:
                    batch_key = (alloc.project_id, alloc.department_id, alloc.week_monday)
                    batch_weekly_demand[batch_key] += hours

                for (pid, did, week), requested_hours in batch_weekly_demand.items():
                    # 1. Get the planned limit for this specific week
                    try:
                        week_alloc = planned_week_cache.get((pid, did, week))
                        if not week_alloc:
                            week_alloc = ProjectWeekAllocation.objects.get(
                                project_id=pid, department_id=did, week_monday=week
                            )

                        # man_hours is the limit for this specific week
                        max_allowed = float(week_alloc.manhours or 0)
                    except ProjectWeekAllocation.DoesNotExist:
                        continue # Already handled in iterative validation, but safe to skip

                    # 2. Get hours already assigned in the database for this week
                    existing_hours = ResourceAllocation.objects.filter(
                        project_id=pid, 
                        department_id=did, 
                        week_monday=week
                    ).aggregate(total=Sum('hours'))['total'] or 0

                    # 3. Validation Logic
                    if float(existing_hours) + requested_hours > max_allowed:
                        return Response({
                            "error": "Weekly Demand Exceeded",
                            "message": (
                                f"Cannot assign {requested_hours}h. Project requires {max_allowed}h for "
                                f"week {week}, but {existing_hours}h are already allocated."
                            )
                        }, status=status.HTTP_400_BAD_REQUEST)
 
                # Check B: Departmental Project Budget
                for (pid, did), val in dept_project_hours.items():
                    da = ProjectDepartmentAllocation.objects.select_related('department').get(project_id=pid, department_id=did)
                    cur_int = ResourceAllocation.objects.filter(project_id=pid, department_id=did).aggregate(t=Sum('hours'))['t'] or 0
                    cur_ext = ExternalCapacity.objects.filter(project_id=pid).aggregate(t=Sum('hours'))['t'] or 0 # Global external
                    
                    if float(cur_int) + float(cur_ext) + val > float(da.estimated_manhours):
                        return Response({
                            "error": "Budget Exceeded",
                            "message": f"Project exceeds {da.department.name} budget limit of {da.estimated_manhours}h."
                        }, status=status.HTTP_400_BAD_REQUEST)

            # --- 4. Atomic Execution ---
            if errors:
                # Extract the first actual error message string for the top-level "message"
                # This navigates: first error dict -> 'errors' dict -> first value
                first_error_item = errors[0].get('errors', {})
                first_message = next(iter(first_error_item.values())) if first_error_item else "Validation failed"

                return Response({
                    "error": "Validation Error",
                    "message": first_message,  # Direct message string here
                    "error_details": errors    # Keep full details for debugging/frontend mapping
                }, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                if assignments_to_create: ProjectAssignment.objects.bulk_create(assignments_to_create)
                if allocations_to_create: ResourceAllocation.objects.bulk_create(allocations_to_create)
                if assignments_to_update: ProjectAssignment.objects.bulk_update(assignments_to_update, ['is_lead', 'notes'])
                if allocations_to_update: ResourceAllocation.objects.bulk_update(allocations_to_update, ['hours'])
            return Response({
                "message": f"Successfully created {len(assignments_to_create)} assignments and {len(allocations_to_create)} allocations and {len(assignments_to_update)} Updated assignment and {len(allocations_to_update)} Updated allocation",
                "total_requested": len(data),
                "created_count": len(assignments_to_create)
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception("Bulk Assignment Create Failed")
            return Response({
                "error": "Internal Server Error",
                "message": f"Bulk operation aborted: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ResourceWeeklyUtilizationView(APIView):
    """
    Get weekly utilization for a specific internal resource in a date range.
    URL: /api/resource-weekly-utilization/?resource_id=5&start=2026-01-01&end=2026-03-31
    """
    permission_classes = [ModuleViewPermission]

    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            # --- 1. Parameter Extraction & Validation ---
            resource_id = request.query_params.get('resource_id')
            if not resource_id:
                return Response({
                    "error": "Validation Error",
                    "message": "resource_id parameter is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Optimized resource fetch with departments pre-loaded
                resource = Resource.objects.prefetch_related('departments').get(
                    id=int(resource_id), 
                    is_internal=True
                )
            except (ValueError, Resource.DoesNotExist):
                return Response({
                    "error": "Not Found",
                    "message": f"Internal resource with ID {resource_id} not found"
                }, status=status.HTTP_404_NOT_FOUND)

            # --- 2. Date Range Logic ---
            start_str = request.query_params.get('start')
            end_str = request.query_params.get('end')
            today = timezone.now().date()

            try:
                start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else today - timedelta(weeks=26)
                end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else today + timedelta(weeks=26)
            except (ValueError, TypeError) as e:
                return Response({
                    "error": "Validation Error",
                    "message": f"Invalid date format. Use YYYY-MM-DD: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

            if start_date > end_date:
                start_date, end_date = end_date, start_date

            # Align to Mondays
            start_monday = start_date - timedelta(days=start_date.weekday())
            end_monday = end_date - timedelta(days=end_date.weekday())
            
            mondays = []
            current = start_monday
            while current <= end_monday:
                mondays.append(current)
                current += timedelta(days=7)

            if not mondays:
                return Response({"data": [], "message": "No weeks found in the specified range."})

            # --- 3. Allocation Retrieval ---
            allocations = ResourceAllocation.objects.filter(
                resource=resource,
                week_monday__in=mondays
            ).select_related('project').values(
                'week_monday', 'project__project_code', 'project__name', 'hours'
            )

            # Build week lookup map
            week_map = defaultdict(lambda: {"allocated": 0.0, "projects": {}})
            for alloc in allocations:
                week = alloc['week_monday']
                hours = float(alloc['hours'] or 0.0)
                proj_code = alloc['project__project_code'] or "N/A"
                proj_name = alloc['project__name'] or "Unknown Project"

                week_map[week]["allocated"] += hours
                if proj_code not in week_map[week]["projects"]:
                    week_map[week]["projects"][proj_code] = {
                        "project_code": proj_code,
                        "project_name": proj_name,
                        "hours": 0.0
                    }
                week_map[week]["projects"][proj_code]["hours"] += hours

            # --- 4. Result Construction ---
            capacity = float(resource.effective_availability_per_week or 45.0)
            weeks_result = []
            total_allocated = 0.0
            total_idle = 0.0

            for monday in mondays:
                data = week_map.get(monday, {"allocated": 0.0, "projects": {}})
                allocated = float(data["allocated"])
                idle = float(max(0.0, capacity - allocated))

                total_allocated += allocated
                total_idle += idle

                weeks_result.append({
                    "week_monday": str(monday),
                    "calendar_week": f"CW{monday.isocalendar()[1]:02d}",
                    "week_display": monday.strftime("%b %d, %Y"),
                    "allocated_hours": round(allocated, 1),
                    "idle_hours": round(idle, 1),
                    "utilization_pct": round((allocated / capacity) * 100, 1) if capacity > 0 else 0.0,
                    "projects": [
                        {
                            "project_code": code,
                            "project_name": details["project_name"],
                            "allocated_hours": round(details["hours"], 1)
                        }
                        for code, details in data["projects"].items()
                    ]
                })

            # Final Department path resolution
            dept_obj = resource.departments.first()
            dept_path = "Unassigned"
            if dept_obj:
                dept_path = getattr(dept_obj, 'get_full_path', lambda: dept_obj.name)()

            return Response({
                "resource": {
                    "id": resource.id,
                    "name": resource.name,
                    "role": resource.role,
                    "role_name": resource.get_role_display() if hasattr(resource, 'get_role_display') else resource.role,
                    "department": dept_path,
                    "weekly_capacity": round(capacity, 1)
                },
                "date_range": {
                    "start": str(start_monday),
                    "end": str(end_monday),
                    "total_weeks": len(mondays)
                },
                "summary": {
                    "total_allocated_hours": round(total_allocated, 1),
                    "total_idle_hours": round(total_idle, 1),
                    "average_weekly_utilization_pct": round((total_allocated / (len(mondays) * capacity)) * 100, 1) if mondays and capacity > 0 else 0.0
                },
                "weeks": weeks_result
            })

        except Exception as e:
            logger.exception(f"Resource utilization fetch failed for ID {request.query_params.get('resource_id')}")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class ProjectListCreateAPIView(APIView):
    """
    List all projects (GET) or create a new project (POST).
    URL: /api/projects/
    """
    
    def get_permissions(self):
        """
        Apply module-based permissions per method.
        """
        if self.request.method == 'GET':
            perm = ModuleViewPermission()
            perm.module = "CAPACITY"
            return [perm]

        if self.request.method == 'POST':
            perm = ModulePreparePermission()
            perm.module = "CAPACITY"
            return [perm]

        return super().get_permissions()

    def get(self, request):
        try:
            # Query all projects. Use select_related if your serializer 
            # accesses foreign keys (e.g., project manager or status objects)
            projects = Project.objects.all().order_by('-id')
            
            serializer = ProjectSerializer1(projects, many=True, context={'request': request})
            return Response(serializer.data)

        except Exception as e:
            logger.exception("ProjectListCreateAPIView GET failed")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = ProjectSerializer(data=request.data, context={'request': request})
            
            if serializer.is_valid():
                # Wrap save in a try-except to catch DB-level unique constraint violations
                # (e.g., if project_code is already taken but not checked by serializer)
                try:
                    project = serializer.save()
                    return Response(
                        ProjectSerializer(project, context={'request': request}).data, 
                        status=status.HTTP_201_CREATED
                    )
                except Exception as save_error:
                    logger.error(f"Database save error in Project creation: {str(save_error)}")
                    return Response({
                        "error": "Database Error",
                        "message": "Could not save project. This project code might already exist."
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Standardized validation error response
            return Response({
                "error": "Validation Error",
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("ProjectListCreateAPIView POST failed")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class ProjectDepartmentAllocationAPIView(APIView):
    """
    Assign a project to a department with an optional 'auto-allocate' feature 
    that spreads manhours evenly across the project duration.
    """
    permission_classes = [ModulePreparePermission]

    def get_permissions(self):
        permission = ModulePreparePermission()
        permission.module = "CAPACITY"
        return [permission]

    def post(self, request, department_id):
        try:
            # 1. Fetch Department
            try:
                department = Department.objects.get(id=department_id)
            except Department.DoesNotExist:
                return Response({
                    "error": "Not Found",
                    "message": f"Department with ID {department_id} not found."
                }, status=status.HTTP_404_NOT_FOUND)

            # 2. Extract and Validate Data
            data = request.data.copy()
            data['department'] = department.id
            
            # Pop the custom flag so the serializer doesn't reject the payload
            auto_allocate = data.pop('ishoursweek_allocate', False)

            serializer = ProjectDepartmentAllocationSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    "error": "Validation Error",
                    "message": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # 3. Transactional Operation
            with transaction.atomic():
                allocation = serializer.save()

                if auto_allocate:
                    # --- Auto-allocation logic ---
                    if not allocation.start_monday or not allocation.end_monday:
                        raise ValueError("Start and End Monday dates are required for auto-allocation.")

                    if allocation.estimated_manhours <= 0:
                        raise ValueError("Estimated manhours must be greater than 0 for auto-allocation.")

                    # Generate list of mondays
                    weeks = []
                    current = allocation.start_monday
                    while current <= allocation.end_monday:
                        weeks.append(current)
                        current += timedelta(days=7)

                    if not weeks:
                        raise ValueError("The provided date range contains no valid weeks.")

                    # Calculate distribution
                    total_mh = float(allocation.estimated_manhours)
                    count = len(weeks)
                    mh_per_week = round(total_mh / count, 1)

                    week_allocations = []
                    remainder = total_mh

                    for i, monday in enumerate(weeks):
                        if i == count - 1:
                            # Last week absorbs any rounding differences
                            mh = round(remainder, 1)
                        else:
                            mh = mh_per_week
                            remainder -= mh

                        week_allocations.append(
                            ProjectWeekAllocation(
                                project=allocation.project,
                                department=department,
                                week_monday=monday,
                                manhours=mh,
                                notes="Auto-allocated during department assignment"
                            )
                        )

                    # Defensive check: Ensure we don't overwrite existing plans
                    duplicate_exists = ProjectWeekAllocation.objects.filter(
                        project=allocation.project,
                        department=department,
                        week_monday__in=[w.week_monday for w in week_allocations]
                    ).exists()

                    if duplicate_exists:
                        raise ValueError("Weekly allocations already exist for this range. Manual adjustment required.")

                    ProjectWeekAllocation.objects.bulk_create(week_allocations)

                # Refresh to catch any DB-level triggers or computed fields
                allocation.refresh_from_db()

            return Response(
                ProjectDepartmentAllocationSerializer(allocation).data,
                status=status.HTTP_201_CREATED
            )

        except ValueError as ve:
            # Catch business logic errors from the atomic block
            return Response({
                "error": "Business Logic Error",
                "message": str(ve)
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("ProjectDepartmentAllocation POST failed")
            return Response({
                "error": "Internal Server Error",
                "message": f"An error occurred while creating the allocation: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectDepartmentAllocationDetail(APIView):
    """
    Retrieve, partially update or delete a ProjectDepartmentAllocation instance.
    URL: /api/projects/<int:project_id>/department-allocations/<int:department_id>/
    """

    def get_permissions(self):
        """
        GET: VIEW permission
        PATCH/DELETE: PREPARER or ADMIN permission
        """
        if self.request.method == 'GET':
            permission = ModuleViewPermission()
        else:
            permission = ModulePreparePermission()

        permission.module = "CAPACITY"
        return [permission]

    def get_allocation(self):
        """Fetch the allocation record safely"""
        try:
            return ProjectDepartmentAllocation.objects.get(
                project_id=self.kwargs['project_id'],
                department_id=self.kwargs['department_id']
            )
        except (ProjectDepartmentAllocation.DoesNotExist, ValueError, KeyError):
            return None

    def get_parent_project(self):
        """Fetch the parent Project record safely"""
        try:
            return Project.objects.get(id=self.kwargs['project_id'])
        except (Project.DoesNotExist, ValueError, KeyError):
            return None

    def get(self, request, project_id, department_id):
        try:
            allocation = self.get_allocation()
            if allocation is None:
                return Response({
                    "error": "Not Found",
                    "message": f"No allocation found for project {project_id} in department {department_id}"
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = ProjectDepartmentAllocationSerializer(allocation, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            logger.exception(f"GET Allocation failed for Project {project_id}")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, project_id, department_id):
        try:
            allocation = self.get_allocation()
            if allocation is None:
                return Response({
                    "error": "Not Found",
                    "message": "Allocation record not found."
                }, status=status.HTTP_404_NOT_FOUND)

            project = self.get_parent_project()
            if project is None:
                return Response({
                    "error": "Not Found",
                    "message": "Parent project not found."
                }, status=status.HTTP_404_NOT_FOUND)

            total_project_mh = float(project.total_manhours or 0)

            serializer = ProjectDepartmentAllocationSerializer(
                allocation,
                data=request.data,
                partial=True,
                context={'request': request}
            )

            if not serializer.is_valid():
                return Response({
                    "error": "Validation Error",
                    "message": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # --- Business Logic Validation: Remaining Hours ---
            new_estimated = serializer.validated_data.get('estimated_manhours')
            if new_estimated is not None:
                new_estimated = float(new_estimated)
                
                # Sum estimated hours of all OTHER departments for this project
                other_sum = ProjectDepartmentAllocation.objects.filter(
                    project_id=project_id
                ).exclude(
                    department_id=department_id
                ).aggregate(total=Sum('estimated_manhours'))['total'] or 0.0
                
                other_sum = float(other_sum)
                proposed_total = other_sum + new_estimated

                if proposed_total > total_project_mh:
                    return Response({
                        "error": "Capacity Error",
                        "message": "The proposed estimated manhours exceed the project's total manhours limit.",
                        "details": {
                            "total_project_limit": total_project_mh,
                            "already_allocated_elsewhere": other_sum,
                            "available_remaining": max(0.0, total_project_mh - other_sum),
                            "proposed_amount": new_estimated
                        }
                    }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data)

        except Exception as e:
            logger.exception(f"PATCH Allocation failed for Project {project_id}")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, project_id, department_id):
        try:
            allocation = self.get_allocation()
            if allocation is None:
                return Response({
                    "error": "Not Found",
                    "message": "Allocation record not found."
                }, status=status.HTTP_404_NOT_FOUND)

            with transaction.atomic():
                # Step 1: Cleanup leaf planned data
                week_count = ProjectWeekAllocation.objects.filter(
                    project_id=project_id,
                    department_id=department_id,
                ).delete()[0]

                # Step 2: Cleanup resource utilization records
                util_count = ResourceAllocation.objects.filter(
                    project_id=project_id,
                    department_id=department_id,
                ).delete()[0]

                # Step 3: Cleanup team assignments
                assign_count = ProjectAssignment.objects.filter(
                    project_id=project_id,
                    department_id=department_id,
                ).delete()[0]

                # Final Step: Delete the main link
                allocation.delete()

            return Response({
                "message": "Department allocation and all related data removed successfully.",
                "cleanup_stats": {
                    "planned_weeks_removed": week_count,
                    "utilization_records_removed": util_count,
                    "assignments_removed": assign_count
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception(f"DELETE Allocation failed for Project {project_id}")
            return Response({
                "error": "Delete Failed",
                "message": f"Could not perform the multi-table cleanup: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResourceAllocationListDelete(APIView):
    """
    DELETE /api/resource-allocation-delete/
    
    Bulk deletes ResourceAllocation records and their corresponding ProjectAssignments.
    Safety: Rejects if the IDs belong to multiple different Projects, Departments, or Resources.
    """

    def get_permissions(self):
        permission = ModulePreparePermission()
        permission.module = "CAPACITY"
        return [permission]

    def delete(self, request):
        try:
            ids_list = request.data.get('ids')

            # --- 1. Payload Validation ---
            if not ids_list:
                return Response({
                    "error": "Validation Error",
                    "message": "Missing 'ids' list in request body"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Handle string-formatted list input (e.g., from certain CSV/Form tools)
            if isinstance(ids_list, str):
                try:
                    ids_list = [int(i.strip()) for i in ids_list.strip('[] ').split(',') if i.strip()]
                except (ValueError, TypeError):
                    return Response({
                        "error": "Validation Error",
                        "message": "Invalid format for IDs. Must be a JSON array of integers."
                    }, status=status.HTTP_400_BAD_REQUEST)

            if not isinstance(ids_list, (list, tuple)) or not ids_list:
                return Response({
                    "error": "Validation Error",
                    "message": "ids must be a non-empty list of integers"
                }, status=status.HTTP_400_BAD_REQUEST)

            # --- 2. Atomic Integrity Block ---
            with transaction.atomic():
                # Fetch allocations with related fields to minimize queries during the loop
                allocations = ResourceAllocation.objects.filter(
                    id__in=ids_list
                ).select_related('project', 'department', 'resource')

                # Check if everything exists
                found_ids = set(allocations.values_list('id', flat=True))
                missing_ids = set(ids_list) - found_ids

                if missing_ids:
                    return Response({
                        "error": "Not Found",
                        "message": f"Operation aborted. Some IDs were not found: {sorted(list(missing_ids))}"
                    }, status=status.HTTP_404_NOT_FOUND)

                # --- 3. Safety Constraint: Context Consistency ---
                # We extract unique IDs to ensure we aren't deleting across multiple projects/resources at once
                project_ids = set(allocations.values_list('project_id', flat=True))
                dept_ids = set(allocations.values_list('department_id', flat=True))
                res_ids = set(allocations.values_list('resource_id', flat=True))

                if len(project_ids) > 1 or len(dept_ids) > 1 or len(res_ids) > 1:
                    return Response({
                        "error": "Safety Constraint Violation",
                        "message": "Bulk deletion is restricted to one Project, Department, and Resource at a time.",
                        "details": {
                            "detected_projects": list(project_ids),
                            "detected_departments": list(dept_ids),
                            "detected_resources": list(res_ids),
                        }
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Capture context for the response message
                p_id = next(iter(project_ids))
                d_id = next(iter(dept_ids))
                r_id = next(iter(res_ids))

                # --- 4. Synchronized Deletion ---
                # Build the conditions to find matching ProjectAssignments
                delete_conditions = Q()
                for alloc in allocations:
                    delete_conditions |= Q(
                        resource_id=alloc.resource_id,
                        week_monday=alloc.week_monday,
                        project_id=alloc.project_id,
                        department_id=alloc.department_id,
                    )

                # Delete Assignments first (following database dependency flow)
                pa_deleted_count, _ = ProjectAssignment.objects.filter(delete_conditions).delete()

                # Delete the specific ResourceAllocations requested
                ra_deleted_count, _ = allocations.delete()

                return Response({
                    "message": "Bulk deletion successful",
                    "summary": {
                        "resource_allocations_removed": ra_deleted_count,
                        "project_assignments_removed": pa_deleted_count,
                        "context": {
                            "project_id": p_id,
                            "department_id": d_id,
                            "resource_id": r_id
                        }
                    }
                }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception("ResourceAllocationListDelete failed")
            return Response({
                "error": "Internal Server Error",
                "message": f"Deletion process failed and was rolled back: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectWeekAllocationUpdate(APIView):
    """
    PATCH /api/project-week-allocations/<int:pk>/
    Updates manhours for a specific week allocation record while enforcing department budgets.
    """

    def get_permissions(self):
        permission = ModulePreparePermission()
        permission.module = "CAPACITY"
        return [permission]

    def patch(self, request, pk):
        try:
            # 1. Get the record we want to update
            allocation = get_object_or_404(ProjectWeekAllocation, pk=pk)

            project_id = allocation.project_id
            department_id = allocation.department_id

            if not department_id:
                return Response({
                    "error": "Data Integrity Error",
                    "message": "This allocation has no department linked — cannot validate budget."
                }, status=status.HTTP_400_BAD_REQUEST)

            # 2. Get and validate new manhours
            raw_manhours = request.data.get('manhours')
            if raw_manhours is None:
                return Response({
                    "error": "Validation Error",
                    "message": "Field 'manhours' is required."
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Use float to handle decimal hours (e.g., 7.5 hours)
                new_manhours = float(raw_manhours)
                if new_manhours < 0:
                    raise ValueError
            except (ValueError, TypeError):
                return Response({
                    "error": "Validation Error",
                    "message": "manhours must be a non-negative number."
                }, status=status.HTTP_400_BAD_REQUEST)

            # 3. Fetch Department-level budget
            try:
                dept_alloc = ProjectDepartmentAllocation.objects.get(
                    project_id=project_id,
                    department_id=department_id
                )
                budget = float(dept_alloc.estimated_manhours or 0.0)
            except ProjectDepartmentAllocation.DoesNotExist:
                return Response({
                    "error": "Configuration Error",
                    "message": "No department allocation (budget) found for this project + department."
                }, status=status.HTTP_400_BAD_REQUEST)

            # 4. Calculate current total (excluding the record being updated)
            # Use float casting to ensure mathematical compatibility
            current_others_total = float(ProjectWeekAllocation.objects.filter(
                project_id=project_id,
                department_id=department_id
            ).exclude(
                pk=pk
            ).aggregate(
                total=Sum('manhours')
            )['total'] or 0.0)

            # 5. Compute what the new total would be
            projected_total = current_others_total + new_manhours

            # 6. Check against budget
            if projected_total > budget:
                remaining = max(0.0, budget - current_others_total)
                return Response({
                    "error": "Capacity Exceeded",
                    "message": f"Cannot update: New total ({projected_total}h) would exceed department budget ({budget}h).",
                    "details": {
                        "budget_limit": budget,
                        "current_usage_others": current_others_total,
                        "available_capacity": remaining,
                        "requested_value": new_manhours,
                        "exceeds_by": round(projected_total - budget, 2)
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            # 7. Atomic Update
            with transaction.atomic():
                old_value = allocation.manhours
                allocation.manhours = new_manhours
                allocation.save(update_fields=['manhours'])

                serializer = ProjectWeekAllocationSerializer(
                    allocation,
                    context={'request': request}
                )

                return Response({
                    "message": "Manhours updated successfully",
                    "data": serializer.data,
                    "budget_stats": {
                        "limit": budget,
                        "new_total_usage": projected_total,
                        "remaining": round(budget - projected_total, 2)
                    }
                }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception(f"Manhours update failed for Allocation PK {pk}")
            return Response({
                "error": "Internal Server Error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ResourceFreeNotificationsAPIView(APIView):
    """
    Identifies internal resources who are becoming 'free' (idle) 
    based on their most recent project allocations.
    """
    
    def get_permissions(self):
        permission = ModuleViewPermission()
        permission.module = "CAPACITY"
        return [permission]

    def get(self, request):
        try:
            today = timezone.now().date()
            current_monday = today - timedelta(days=today.weekday())
            prev_monday = current_monday - timedelta(days=7)
            next_monday = current_monday + timedelta(days=7)

            # 1. Efficiently fetch resources with preloaded departments
            resources = Resource.objects.filter(
                is_active=True,
                is_internal=True,
                leaving_date__isnull=True,
            ).prefetch_related('departments')

            # 2. Optimization: Get the latest allocation date for ALL resources in ONE query
            # This avoids the N+1 problem (hitting DB inside the for-loop)
            latest_allocs = ResourceAllocation.objects.filter(
                hours__gt=0
            ).values('resource_id').annotate(
                latest_monday=Max('week_monday')
            )
            
            # Map for O(1) lookup: {resource_id: latest_monday}
            alloc_map = {item['resource_id']: item['latest_monday'] for item in latest_allocs}

            free_today = []
            free_next = []
            not_assigned_or_idle = []

            for resource in resources:
                latest = alloc_map.get(resource.id)
                depts = [d.name for d in resource.departments.all()]

                if latest is None:
                    # Never assigned to anything
                    msg = "has not been assigned to any project yet"
                    not_assigned_or_idle.append(self._build(resource, msg, None, depts))
                    continue

                if latest > current_monday:
                    # Resource still has future work assigned
                    continue

                elif latest == current_monday:
                    # Work ends this week; free from next Monday
                    msg = f"is becoming free from next Monday ({next_monday:%Y-%m-%d})"
                    free_next.append(self._build(resource, msg, latest, depts))

                elif latest == prev_monday:
                    # Work ended last week; free from today
                    msg = f"is becoming free from today (week: {current_monday:%Y-%m-%d})"
                    free_today.append(self._build(resource, msg, latest, depts))

                else:  # latest < prev_monday
                    # Work ended some time ago
                    msg = f"has no recent assignment (last work week: {latest:%Y-%m-%d})"
                    not_assigned_or_idle.append(self._build(resource, msg, latest, depts))

            # Sorting by name
            for lst in [free_today, free_next, not_assigned_or_idle]:
                lst.sort(key=lambda x: x["resource_name"].lower())

            counts = {
                "free_from_today": len(free_today),
                "free_from_next_monday": len(free_next),
                "not_assigned_or_idle": len(not_assigned_or_idle),
            }

            return Response({
                "success": True,
                "metadata": {
                    "today": today.strftime("%Y-%m-%d"),
                    "current_week_monday": current_monday.strftime("%Y-%m-%d"),
                    "previous_week_monday": prev_monday.strftime("%Y-%m-%d"),
                    "next_week_monday": next_monday.strftime("%Y-%m-%d"),
                },
                "notifications": {
                    "free_from_today": free_today,
                    "free_from_next_monday": free_next,
                    "not_assigned_or_idle": not_assigned_or_idle,
                },
                "counts": counts,
                "total_notifications": sum(counts.values()),
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception("ResourceFreeNotifications fetch failed")
            return Response({
                "error": "Internal Server Error",
                "message": f"Could not calculate resource availability: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _format_depts(self, depts):
        if not depts:
            return ""
        return f" – {', '.join(depts)}"

    def _build(self, resource, suffix, last_date, depts):
        return {
            "resource_id": resource.id,
            "resource_name": resource.name,
            "message": f"{resource.name} {suffix}{self._format_depts(depts)}",
            "departments": depts,
            "last_working_monday": last_date.strftime("%Y-%m-%d") if last_date else None,
        }



class AvailablePSRProjectsAPIView(APIView):
    """
    GET /api/capacity/available-psr-projects/
    Returns PSR projects that do NOT yet exist in the Capacity Project table.
    """
    
    def get_permissions(self):
        # Allowing both modules to access this bridge view
        permission = ModuleViewPermission()
        permission.module = ["CAPACITY", "PROCUREMENT"]
        return [permission]

    def get(self, request):
        try:
            # 1. Get list of project codes already existing in Capacity
            # We assume 'project_code' in Capacity matches 'co_no' in PSR
            existing_codes = Project.objects.values_list('project_code', flat=True)

            # 2. Filter PSR projects NOT in existing_codes
            # Using .exclude() is more performant than manual list comprehension
            available_psr = PSRProject.objects.exclude(
                co_no__in=existing_codes
            ).order_by('co_no')

            data = []
            for p in available_psr:
                try:
                    data.append({
                        "psr_id": p.id, # Used as 'psr_project' reference for creation
                        "co_no": p.co_no,
                        "project_name": p.project_name,
                        
                        # Basic info with fallback for nulls
                        "location": p.location or "",
                        "project_manager_id": p.project_manager_id or "",
                        "project_manager_email": p.project_manager_email or "",
                        "sales_person": p.sales_person or "",
                        "sales_person_email": p.sales_person_email or "",
                        "cw_no": p.cw_no or "",
                        "current_phase": p.current_phase or "",
                        "settlement_period": p.settlement_period or "",
                        
                        # Financials (Ensuring float conversion for JSON compatibility)
                        "currency": p.currency,
                        "exchange_rate": float(p.exchange_rate or 1.0),
                        "sales_value_foreign_curr": float(p.sales_value_foreign_curr or 0.0),
                        "sales_value_inr": float(p.sales_value or 0.0),
                        
                        # Percentages
                        "ebit_percentage": float(p.ebit_percentage or 0.0),
                        "sgna_percentage": float(p.sgna_percentage or 0.0),
                        "eff_percentage": float(p.eff_percentage or 0.0),
                        "ter_percentage": float(p.ter_percentage or 0.0),
                        
                        # Calculated values
                        "ebit_value": float(p.ebit_value or 0.0),
                        "sgna_value": float(p.sgna_value or 0.0),
                        "cost_with_sgna": float(p.cost_with_sgna or 0.0),
                        "hk": float(p.hk or 0.0),
                        "direct_margin_value": float(p.direct_margin_value or 0.0),
                        "direct_margin_percentage": float(p.direct_margin_percentage or 0.0),
                        "ter_value": float(p.ter_value or 0.0),
                        "eff_value": float(p.eff_value or 0.0),
                        "actual_budget": float(p.actual_budget or 0.0),
                        "factor": float(p.factor or 1.0),
                        "budget": float(p.budget or 0.0),
                        
                        # Timestamps
                        "created_at": p.created_at.isoformat() if p.created_at else None,
                        "updated_at": p.updated_at.isoformat() if p.updated_at else None,
                    })
                except Exception as item_error:
                    # Log individual record failures so one bad row doesn't crash the whole list
                    logger.warning(f"Error processing PSR Project ID {p.id}: {str(item_error)}")
                    continue

            return Response({
                "count": len(data),
                "results": data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception("AvailablePSRProjectsAPIView failed")
            return Response({
                "error": "Internal Server Error",
                "message": f"Failed to fetch available PSR projects: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




from datetime import datetime, timedelta
from django.db.models import Sum, Count, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Sum
# Assuming these are your models
# from .models import Department, Resource, ResourceAllocation, ExternalCapacity, ProjectDepartmentAllocation

class DepartmentWeeklyReportView(APIView):

    def get_monday(self, date_str=None):
        """Helper to find the Monday of the given date's week or current week."""
        if date_str:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            target_date = datetime.now().date()

        # weekday() returns 0 for Monday
        monday = target_date - timedelta(days=target_date.weekday())
        return monday

    def get(self, request):
        # 1. Extract and process optional payload
        date_input = request.query_params.get('date')
        dept_names = request.query_params.getlist('departments') # Expecting a list of names

        week_monday = self.get_monday(date_input)
        current_date = datetime.now().date()

        # 2. Get Departments
        if dept_names:
            departments = Department.objects.filter(name__in=dept_names)
        else:
            departments = Department.objects.all()

        response_data = []

        for dept in departments:
            # --- Count 1: Resources (Active/Joined) ---
            # Resource joined before 'week_monday' and leaving after 'current_date'
            # --- Count 1: Resources (Active/Joined) ---
            count1 = Resource.objects.filter(
                # Move the Q object to the front of the filter
                (Q(leaving_date__gt=week_monday) | Q(leaving_date__isnull=True)),
                departments=dept,
                joining_date__lte=week_monday
            ).distinct().count()

            # --- Count 2 & Internal Hours: ResourceAllocation ---
            allocation_qs = ResourceAllocation.objects.filter(
                department=dept,
                week_monday=week_monday
            )
            count2 = allocation_qs.values('resource_id').distinct().count()
            total_internal_hours = allocation_qs.aggregate(total=Sum('hours'))['total'] or 0

            # --- Count 3 & External Hours: ExternalCapacity ---
            external_qs = ExternalCapacity.objects.filter(
                dept=dept,
                week_monday=week_monday
            )
            count3 = external_qs.values('supplier_id').distinct().count()
            total_external_hours = external_qs.aggregate(total=Sum('hours'))['total'] or 0

            # --- Total Manhours: ProjectDepartmentAllocation ---
            # Filtering where the range covers the selected week
            # --- Total Manhours: ProjectDepartmentAllocation ---
            total_ma_hours = ProjectDepartmentAllocation.objects.filter(
                department=dept,
                start_monday__lte=week_monday,
                end_monday__gte=week_monday
            ).aggregate(total=Sum('estimated_manhours'))['total'] or 0  # Changed 'manhours' to 'estimated_manhours'

            # --- Calculations ---
            free_capacity = (count1 * 45) - total_internal_hours
            total_count = count2 + count3
            total_used_hours = total_internal_hours + total_external_hours

            response_data.append({
                "department_name": dept.name,
                "internal_hours": total_internal_hours,
                "external_hours": total_external_hours,
                "internal_count": count2,
                "external_count": count3,
                "total_count": total_count,
                "total_used_hours": total_used_hours,
                "free_capacity": free_capacity,
                "total_required_mahours": total_ma_hours
            })

        return Response(response_data, status=status.HTTP_200_OK)

 

