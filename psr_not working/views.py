# core/views.py
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.management import call_command, CommandError
from rest_framework.generics import CreateAPIView
from rest_framework.filters import OrderingFilter
from accounts.models import UserModulePermission
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from decimal import Decimal, InvalidOperation
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Max, Q
from accounts.models import CustomUser
from collections import defaultdict
from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics
from django.db import transaction
from django.utils import timezone
from datetime import datetime
from psr.models import *
from io import StringIO
import pandas as pd
import tempfile
import logging
import os
from rest_framework.exceptions import PermissionDenied

# from psr.serializers import (PSRProjectListSerializer,
#                           TimesheetImportSerializer,
#                           PODataImportSerializer,
#                           ProjectCreateSerializer,
#                           ProjectBasicSerializer,
#                           ProjectUpdateSerializer,
#                           PSRSnapshotKPISerializer,
#                           MonthlyCumulativeKPISerializer,
#                           RKActualAdjustmentSerializer,
#                           AssemblyActualAdjustmentSerializer,
#                           FVActualAdjustmentSerializer,
#                           SOKOActualAdjustmentSerializer,
#                           PSRBudgetChangeRequestSerializer,
#                         #   PSRForecastChangeRequestCreateSerializer,
#                         #   PSRForecastChangeRequestSerializer,
#                           UserDropdownSerializer,
#                           ProjectPaymentSerializer,
#                           )
from .serializers import *
logger = logging.getLogger(__name__)


# Helpers (put in utils.py or here for simplicity)
def has_psr_permission(user, perm_code):
    return UserModulePermission.objects.filter(
        user=user,
        module__code='PSR',
        permission__code=perm_code,
        is_active=True
    ).exists()

def get_psr_approvers():
    return list(CustomUser.objects.filter(
        usermodulepermission__module__code='PSR',
        usermodulepermission__permission__code='APPROVER',
        usermodulepermission__is_active=True
    ))

def get_psr_admin():
    admin = CustomUser.objects.filter(
        usermodulepermission__module__code='PSR',
        usermodulepermission__permission__code='ADMIN',
        usermodulepermission__is_active=True
    ).first()
    return admin




class PSRProjectListAPIView(APIView):
    # Lists All Projects Under the model / table PSRProject
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = PSRProject.objects.all().order_by("co_no")
        serializer = PSRProjectListSerializer(projects, many=True)
        return Response(serializer.data)


class UpdateAllPSRSnapshotsAPIView(APIView):
    # Updates / Generates PSR Snapshot for all the existing Projects in PSRProject
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            call_command('generate_psr_snapshot')

            logger.info(f"All PSR snapshots updated on {timezone.now().date()} by {request.user.username}")

            return Response({
                "status": "success",
                "message": "PSR snapshots have been successfully generated/updated for all projects (today's date)"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Failed to update all PSR snapshots: {str(e)}", exc_info=True)
            return Response({
                "status": "error",
                "message": "Failed to update PSR snapshots. Please contact support.",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GeneratePSRSnapshotAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data or {}
        co_no = data.get('project')
        date_str = data.get('date')

        if co_no and not isinstance(co_no, str):
            return Response(
                {"status": "error", "message": "'project' must be a string"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if date_str and not isinstance(date_str, str):
            return Response(
                {"status": "error", "message": "'date' must be a string in YYYY-MM-DD format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            args = []
            kwargs = {}

            if co_no:
                args.append(co_no.strip())

            if date_str:
                kwargs['date'] = date_str.strip()

            call_command('generate_psr_snapshot', *args, **kwargs)

            target = f"project {co_no}" if co_no else "all projects"
            target_date = date_str if date_str else timezone.now().date().isoformat()

            logger.info(f"PSR snapshot generated | target={target} | date={target_date} | user={request.user.username}")

            return Response({
                "status": "success",
                "message": f"PSR snapshot successfully generated for {target}",
                "date": target_date,
                "project": co_no or None
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception(f"PSR snapshot generation failed | co_no={co_no} | date={date_str}")
            return Response({
                "status": "error",
                "message": "Failed to generate PSR snapshot"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ImportTimesheetAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = TimesheetImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        excel_file = serializer.validated_data["file"]
        dry_run = serializer.validated_data.get("dry_run", False)

        # Save temp file
        suffix = os.path.splitext(excel_file.name)[1]
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            for chunk in excel_file.chunks():
                tmp.write(chunk)
            temp_path = tmp.name

        # Try reading with both engines
        df = None
        for engine in ["xlrd", "openpyxl"]:
            try:
                df = pd.read_excel(
                    temp_path,
                    sheet_name="Data",
                    skiprows=2,
                    engine=engine
                )
                break
            except Exception:
                continue

        if df is None or df.empty:
            return Response(
                {"detail": "Could not read Excel file or sheet is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        required_columns = [
            'Date', 'EmpCd', 'EmpName',
            'RoleDescrptn', 'CoNo', 'Hours'
        ]
        missing = [c for c in required_columns if c not in df.columns]
        if missing:
            return Response(
                {
                    "detail": "Missing required columns",
                    "missing": missing,
                    "available": list(df.columns)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Keep only required columns
        df = df[required_columns].copy()

        # Drop rows missing critical fields
        df.dropna(subset=['Date', 'EmpCd', 'CoNo', 'Hours'], inplace=True)

        # Clean fields
        df['CoNo'] = df['CoNo'].astype(str).str.strip()
        df['EmpCd'] = df['EmpCd'].astype(str).str.strip()
        df['EmpName'] = df['EmpName'].astype(str).str.strip()
        df['RoleDescrptn'] = df['RoleDescrptn'].astype(str).str.strip()

        # Convert Hours to numeric
        df['Hours'] = pd.to_numeric(df['Hours'], errors='coerce')

        # Drop invalid rows
        df.dropna(subset=['Hours'], inplace=True)
        df = df[df['CoNo'].notna()]
        df = df[df['CoNo'] != '']
        df = df[df['CoNo'] != 'nan']

        if df.empty:
            return Response(
                {"detail": "No valid data after cleaning"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prepare objects
        entries = []
        for _, row in df.iterrows():
            entries.append(TimesheetEntry(
                date=pd.to_datetime(row['Date']).date(),
                emp_cd=row['EmpCd'],
                emp_name=row['EmpName'],
                role_description=row['RoleDescrptn'],
                co_no=row['CoNo'],
                hours=row['Hours']
            ))

        if dry_run:
            return Response({
                "dry_run": True,
                "rows_detected": len(df),
                "records_to_import": len(entries)
            })

        start_time = timezone.now()

        with transaction.atomic():
            deleted_count, _ = TimesheetEntry.objects.all().delete()

            TimesheetEntry.objects.bulk_create(
                entries,
                batch_size=5000,
                ignore_conflicts=True
            )

        duration = (timezone.now() - start_time).total_seconds()

        return Response({
            "status": "success",
            "deleted_existing": deleted_count,
            "imported": len(entries),
            "duration_seconds": round(duration, 2)
        }, status=status.HTTP_201_CREATED)


class ImportPODataAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)    

    def post(self, request):
        serializer = PODataImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        excel_file = serializer.validated_data["file"]
        dry_run = serializer.validated_data.get("dry_run", False)

        # Save temp file
        suffix = os.path.splitext(excel_file.name)[1]
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            for chunk in excel_file.chunks():
                tmp.write(chunk)
            temp_path = tmp.name

        # Read Excel
        df = None
        for engine in ["openpyxl", "xlrd"]:
            try:
                df = pd.read_excel(
                    temp_path,
                    sheet_name="Sheet1",
                    skiprows=2,
                    engine=engine
                )
                break
            except Exception:
                continue

        if df is None or df.empty:
            return Response(
                {"detail": "Could not read Excel or file is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        required_cols = [
            'PoNo', 'Po.Date', 'SrNo', 'CONo',
            'ProjName', 'MatCode', 'POValue in Local Curr'
        ]
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            return Response(
                {"detail": f"Missing required columns: {missing}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Clean
        df = df[required_cols + ['ItemCode', 'Description', 'SupplierName']].copy()
        df.dropna(subset=['CONo', 'POValue in Local Curr'], inplace=True)
        df['CONo'] = df['CONo'].astype(str).str.strip()
        df['POValue in Local Curr'] = pd.to_numeric(
            df['POValue in Local Curr'], errors='coerce'
        )
        df.dropna(subset=['POValue in Local Curr'], inplace=True)

        if df.empty:
            return Response(
                {"detail": "No valid data after cleaning"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prepare objects
        entries = []
        for _, row in df.iterrows():
            entries.append(POData(
                po_no=str(row['PoNo']).strip() if pd.notna(row['PoNo']) else "",
                po_date=row['Po.Date'] if pd.notna(row['Po.Date']) else None,
                sr_no=int(row['SrNo']) if pd.notna(row['SrNo']) and str(row['SrNo']).isdigit() else None,
                co_no=row['CONo'],
                project_name=str(row['ProjName']).strip() if pd.notna(row['ProjName']) else "",
                mat_code=str(row['MatCode']).strip() if pd.notna(row['MatCode']) else "UNKNOWN",
                po_value_inr=row['POValue in Local Curr'],
                item_code=str(row.get('ItemCode', '')).strip(),
                description=str(row.get('Description', '')).strip(),
                supplier_name=str(row.get('SupplierName', '')).strip(),
            ))

        if dry_run:
            return Response({
                "dry_run": True,
                "rows_detected": len(df),
                "records_to_import": len(entries)
            })

        start = timezone.now()

        with transaction.atomic():
            deleted_count, _ = POData.objects.all().delete()

            batch_size = 5000
            imported = 0

            for i in range(0, len(entries), batch_size):
                batch = entries[i:i + batch_size]
                created = POData.objects.bulk_create(
                    batch,
                    batch_size=batch_size,
                    update_conflicts=True,
                    update_fields=['po_value_inr', 'updated_at'],
                    unique_fields=['co_no', 'po_no', 'sr_no'],
                )
                imported += len(created)

        duration = (timezone.now() - start).total_seconds()

        return Response({
            "status": "success",
            "deleted_existing": deleted_count,
            "imported": imported,
            "duration_seconds": round(duration, 2)
        }, status=status.HTTP_201_CREATED)


SECTION_ORDER = [
    ("PROJECT_MANAGEMENT", ["PM", "POM"]),

    ("MECHANICAL_DESIGN", ["PEM", "KMA/KHP", "DET", "DOK", "2D", "SIM", "QC", "LAY"]),

    ("ELECTRICAL_DESIGN", ["PEC", "KEL"]),

    ("IN_HOUSE_COMMISSIONING", ["KES", "IBS", "IBSS"]),

    ("ON_SITE_COMMISSIONING", ["IBK"]),

    ("MECHANICAL_INSTALLATION", ["PAM", "MMA/MHP", "A+I(M)"]),

    ("ELECTRICAL_INSTALLATION", ["INS", "A+I(E)"]),
]

def reorder_section_data(section_data):
    ordered = {}
    for section, dept_order in SECTION_ORDER:
        if section not in section_data:
            continue

        ordered[section] = {}
        for dept in dept_order:
            if dept in section_data[section]:
                ordered[section][dept] = section_data[section][dept]

    return ordered


class ProjectPSRSnapshotTimesheetView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, co_no, snapshot_date=None):
        project = get_object_or_404(PSRProject, co_no=co_no)

        if snapshot_date:
            snapshot = get_object_or_404(PSRSnapshot, project=project, snapshot_date=snapshot_date)
            # Check if this specific snapshot is the latest
            latest_snapshot = PSRSnapshot.objects.filter(project=project).order_by('-snapshot_date').first()
            is_latest = (snapshot.id == latest_snapshot.id) if latest_snapshot else False
        else:
            snapshot = PSRSnapshot.objects.filter(project=project).order_by('-snapshot_date').first()
            if not snapshot:
                return Response({"error": "No snapshots available for this project"}, status=status.HTTP_404_NOT_FOUND)
            is_latest = True  # When no date specified, we always fetch latest

        timesheet_data = snapshot.data.get("TIMESHEET", {"HOURS": {}, "COST": {}})

        # List of keys that are percentages (keep 2 decimals)
        PERCENTAGE_KEYS = {
            'balance_percentage',
            'rest_percentage',
            # Add any future percentage keys here
        }

        def round_value(value, key=None):
            if isinstance(value, float):
                if key in PERCENTAGE_KEYS:
                    return round(value, 2)
                else:
                    return round(value, 1)
            return value

        def round_nested(obj):
            if isinstance(obj, dict):
                return {k: round_nested(v) if k not in PERCENTAGE_KEYS else round_value(v, k) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [round_nested(item) for item in obj]
            elif isinstance(obj, float):
                return round_value(obj)
            else:
                return obj

        # Apply rounding to entire TIMESHEET structure
        rounded_timesheet = {}

        for main_section in ["HOURS", "COST"]:
            raw_section_data = timesheet_data.get(main_section, {})

            # First round values
            rounded_section_data = {
                section: {
                    dept: {
                        sub_code: round_nested(values)
                        for sub_code, values in sub_depts.items()
                    }
                    for dept, sub_depts in section_data.items()
                }
                for section, section_data in raw_section_data.items()
            }

            # Then reorder
            rounded_timesheet[main_section] = reorder_section_data(rounded_section_data)

        return Response({
            "project": project.co_no,
            "snapshot_date": snapshot.snapshot_date,
            "is_latest": is_latest,
            "timesheet": rounded_timesheet
        }, status=status.HTTP_200_OK)


COST_TO_GO_ORDER = [
    "KTFT", "KTES", "KTEP", "KTMA", "KTHP", "ZKE", "F+V", "SOKO", "RK", "ASSEMBLE SERVICES", "DESIGN SERVICES", "FACTORY EQUIPMENTS CONSUMABLES", "STATIONARY", "QC (QUALITY CHECKING SERVICES)",
]


def reorder_cost_to_go(cost_data):
    ordered = {}

    # Add items in fixed order
    for key in COST_TO_GO_ORDER:
        if key in cost_data:
            ordered[key] = cost_data[key]

    # Optional: append any unexpected keys at the end (prevents data loss)
    for key, value in cost_data.items():
        if key not in ordered:
            ordered[key] = value

    return ordered


class ProjectPSRSnapshotCostToGoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, co_no, snapshot_date=None):
        project = get_object_or_404(PSRProject, co_no=co_no)

        if snapshot_date:
            snapshot = get_object_or_404(PSRSnapshot, project=project, snapshot_date=snapshot_date)
            # Check if this specific snapshot is the latest
            latest_snapshot = PSRSnapshot.objects.filter(project=project).order_by('-snapshot_date').first()
            is_latest = (snapshot.id == latest_snapshot.id) if latest_snapshot else False
        else:
            snapshot = PSRSnapshot.objects.filter(project=project).order_by('-snapshot_date').first()
            if not snapshot:
                return Response({"error": "No snapshots available for this project"}, status=status.HTTP_404_NOT_FOUND)
            is_latest = True  # When no date specified, we always fetch latest

        # Return only COST TO GO data
        raw_cost_to_go = snapshot.data.get("COST TO GO", {"COST": {}})

        ordered_cost_to_go = {
            "COST": reorder_cost_to_go(raw_cost_to_go.get("COST", {}))
        }

        return Response({
            "project": project.co_no,
            "snapshot_date": snapshot.snapshot_date,
            "is_latest": is_latest,
            "cost_to_go": ordered_cost_to_go,
        }, status=status.HTTP_200_OK)


class ProjectSnapshotTimesheetHistoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, co_no):
        project = get_object_or_404(PSRProject, co_no=co_no)

        snapshots = PSRSnapshot.objects.filter(project=project).order_by('snapshot_date')

        if not snapshots.exists():
            return Response(
                {"detail": "No snapshots available for this project."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get optional department filter from query params
        selected_department = request.GET.get('department')  # e.g. ?department=Engineering
        # You can also accept 'dept' as alias if you prefer
        # selected_department = request.GET.get('department') or request.GET.get('dept')

        HOURS = []
        COST = []

        for snapshot in snapshots:
            month_year = snapshot.snapshot_date.strftime('%B %Y')
            date_str = snapshot.snapshot_date.strftime('%d-%b-%Y')

            data = snapshot.data or {}
            timesheet_hours = data.get("TIMESHEET", {}).get("HOURS", {})
            timesheet_cost = data.get("TIMESHEET", {}).get("COST", {})

            # -- Decide which data to use -------------------------------
            if selected_department:
                # Filter for specific department
                dept_hours = timesheet_hours.get(selected_department, {})
                dept_cost = timesheet_cost.get(selected_department, {})

                # Sum all sub-departments for the selected department
                actual_h = sum(float(v.get("actuals", 0)) for v in dept_hours.values())
                budget_h = sum(float(v.get("budget", 0)) for v in dept_hours.values())
                forecast_h = sum(float(v.get("forecast", 0)) for v in dept_hours.values())
                prognosis_h = sum(float(v.get("prognosis", 0)) for v in dept_hours.values())

                actual_c = sum(float(v.get("actuals", 0)) for v in dept_cost.values())
                budget_c = sum(float(v.get("budget", 0)) for v in dept_cost.values())
                forecast_c = sum(float(v.get("forecast", 0)) for v in dept_cost.values())
                prognosis_c = sum(float(v.get("prognosis", 0)) for v in dept_cost.values())

            else:
                # Use pre-calculated totals (faster & more reliable)
                actual_h = float(snapshot.labor_actual_hours)
                budget_h = float(snapshot.labor_budget_hours)
                forecast_h = float(snapshot.labor_forecast_hours)
                prognosis_h = float(snapshot.labor_prognosis_hours)

                actual_c = float(snapshot.labor_actual_cost)
                budget_c = float(snapshot.labor_budget_cost)
                forecast_c = float(snapshot.labor_forecast_cost)
                prognosis_c = float(snapshot.labor_prognosis_cost)

            # -- Append to response arrays -----------------------------
            HOURS.append({
                "month": date_str,
                "actual_hours": actual_h,
                "budget_hours": budget_h,
                "forecast_hours": forecast_h,
                "prognosis_hours": prognosis_h,
            })

            COST.append({
                "month": date_str,
                "actual_cost": actual_c,
                "budget_cost": budget_c,
                "forecast_cost": forecast_c,
                "prognosis_cost": prognosis_c,
            })

        return Response({
            "project": project.co_no,
            "project_name": project.project_name,
            "HOURS": HOURS,
            "COST": COST,
            # Optional: you can add this for frontend debugging/info
            # "filtered_department": selected_department if selected_department else "All (Total)",
        })


class ProjectSnapshotCostToGoHistoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, co_no):
        project = get_object_or_404(PSRProject, co_no=co_no)

        snapshots = PSRSnapshot.objects.filter(project=project).order_by('snapshot_date')

        if not snapshots.exists():
            return Response(
                {"detail": "No snapshots available for this project."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Optional filter by cost category (e.g. ?category=RK or ?category=MAT1)
        selected_category = request.GET.get('department') or request.GET.get('cost_category')

        history = []

        for snapshot in snapshots:
            month_year = snapshot.snapshot_date.strftime('%B %Y')
            date_str = snapshot.snapshot_date.strftime('%d-%b-%Y')

            data = snapshot.data or {}
            cost_to_go = data.get("COST TO GO", {}).get("COST", {})

            if selected_category:
                # Specific category selected ? get data only for that category
                cat_data = cost_to_go.get(selected_category, {})

                actual_c   = float(cat_data.get("actuals", 0))
                budget_c   = float(cat_data.get("budget", 0))
                forecast_c = float(cat_data.get("forecast", 0))
                prognosis_c = float(cat_data.get("prognosis", 0))

            else:
                # No filter ? use pre-calculated total material values
                actual_c   = float(snapshot.material_actual_cost)
                budget_c   = float(snapshot.material_budget_cost)
                forecast_c = float(snapshot.material_forecast_cost)
                prognosis_c = float(snapshot.material_prognosis_cost)

            month_data = {
                "month": date_str,
                "actual_cost": actual_c,
                "budget_cost": budget_c,
                "forecast_cost": forecast_c,
                "prognosis_cost": prognosis_c,
            }

            history.append(month_data)

        return Response({
            "project": project.co_no,
            "project_name": project.project_name,
            "cost_to_go_history": history,
            # Optional - useful for debugging / frontend display
            # "filtered_category": selected_category if selected_category else "All (Total)",
        })



class SubDepartmentBudgetUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        sub_dept = get_object_or_404(PSRSubDepartment, pk=pk)
        user = request.user

        new_hours_str = request.data.get('budget_hours')
        note = request.data.get('note', '').strip()

        if new_hours_str is None:
            return Response({"detail": "budget_hours is required."}, status=400)

        if not note:
            return Response({"detail": "note (reason for change) is required."}, status=400)

        try:
            new_hours = Decimal(str(new_hours_str))
            if new_hours < 0:
                raise ValueError("Negative value not allowed")
        except (InvalidOperation, ValueError):
            return Response({"detail": "budget_hours must be a valid positive number."}, status=400)

        is_admin = has_psr_permission(user, 'ADMIN')

        if is_admin:
            # -- Direct update for Admin --
            with transaction.atomic():
                previous_hours = sub_dept.budget_hours

                sub_dept.budget_hours = new_hours
                # sub_dept.budget_cost = (
                #     new_hours
                #     * sub_dept.department.hourly_rate
                #     * sub_dept.department.project.exchange_rate
                # )

                sub_dept.budget_cost = (
                    new_hours
                    * sub_dept.department.hourly_rate
                )

                sub_dept.save()

                SubDepartmentBudgetAdjustment.objects.create(
                    sub_department=sub_dept,
                    adjusted_by=user,
                    note=note,
                    previous_budget_hours=previous_hours,
                    new_budget_hours=new_hours
                )

            # Regenerate snapshot
            project = sub_dept.department.project
            latest_snapshot = project.psr_snapshots.order_by('-snapshot_date').first()
            snapshot_date = None
            if latest_snapshot:
                call_command(
                    'generate_psr_snapshot',
                    str(project.co_no),
                    '--date',
                    latest_snapshot.snapshot_date.strftime('%Y-%m-%d')
                )
                snapshot_date = latest_snapshot.snapshot_date.strftime('%Y-%m-%d')

            return Response({
                "detail": "Budget hours updated successfully (Admin direct update).",
                "baseline_budget_hours": float(sub_dept.baseline_budget_hours),
                "current_budget_hours": float(new_hours),
                "snapshot_regenerated": snapshot_date
            }, status=200)

        else:
            # -- Preparer / Approver ? create request --
            if not (has_psr_permission(user, 'PREPARER') or has_psr_permission(user, 'APPROVER')):
                return Response({"detail": "You are not authorized to request budget changes in PSR."}, status=403)

            # Prevent duplicate pending requests
            if PSRBudgetChangeRequest.objects.filter(
                sub_department=sub_dept,
                status__in=['PENDING_APPROVERS', 'PENDING_ADMIN']
            ).exists():
                return Response(
                    {"detail": "A change request is already pending for this sub-department."},
                    status=409  # Conflict
                )

            # Create approval request
            request_obj = PSRBudgetChangeRequest.objects.create(
                submitter=user,
                sub_department=sub_dept,
                proposed_budget_hours=new_hours,
                note=note,
                status='PENDING_APPROVERS'
            )

            if has_psr_permission(user, 'APPROVER'):
                PSRApprovalAction.objects.create(
                    request=request_obj,
                    approver=user,
                    stage='APPROVER',
                    action='APPROVE',
                    comment='Auto-approved (submitter is approver)'
                )

            return Response({
                "detail": "Budget change request submitted successfully. Awaiting approval.",
                "request_id": request_obj.id,
                "status": request_obj.status,
                "proposed_budget_hours": float(new_hours),
                "target": str(sub_dept)
            }, status=201)


class ProjectCostCategoryBudgetUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        pcc = get_object_or_404(ProjectCostCategory, pk=pk)
        user = request.user

        new_cost_str = request.data.get('budget_cost')
        note = request.data.get('note', '').strip()

        if new_cost_str is None:
            return Response({"detail": "budget_cost is required."}, status=400)

        if not note:
            return Response({"detail": "note (reason for change) is required."}, status=400)

        try:
            new_cost = Decimal(str(new_cost_str))
            if new_cost < 0:
                raise ValueError("Negative value not allowed")
        except (InvalidOperation, ValueError):
            return Response({"detail": "budget_cost must be a valid positive number."}, status=400)

        is_admin = has_psr_permission(user, 'ADMIN')

        if is_admin:
            # -- Direct update for Admin --
            with transaction.atomic():
                previous_cost = pcc.budget_cost

                pcc.budget_cost = new_cost
                pcc.save()

                ProjectCostCategoryBudgetAdjustment.objects.create(
                    project_cost_category=pcc,
                    adjusted_by=user,
                    note=note,
                    previous_budget_cost=previous_cost,
                    new_budget_cost=new_cost
                )

            # Regenerate snapshot
            project = pcc.project
            latest_snapshot = project.psr_snapshots.order_by('-snapshot_date').first()
            snapshot_date = None
            if latest_snapshot:
                call_command(
                    'generate_psr_snapshot',
                    str(project.co_no),
                    '--date',
                    latest_snapshot.snapshot_date.strftime('%Y-%m-%d')
                )
                snapshot_date = latest_snapshot.snapshot_date.strftime('%Y-%m-%d')

            return Response({
                "detail": "Budget cost updated successfully (Admin direct update).",
                "baseline_budget_cost": float(pcc.baseline_budget_cost),
                "current_budget_cost": float(new_cost),
                "snapshot_regenerated": snapshot_date
            }, status=200)

        else:
            # -- Preparer / Approver ? create request --
            if not (has_psr_permission(user, 'PREPARER') or has_psr_permission(user, 'APPROVER')):
                return Response({"detail": "You are not authorized to request budget changes in PSR."}, status=403)

            # Prevent duplicate pending requests
            if PSRBudgetChangeRequest.objects.filter(
                project_cost_category=pcc,
                status__in=['PENDING_APPROVERS', 'PENDING_ADMIN']
            ).exists():
                return Response(
                    {"detail": "A change request is already pending for this cost category."},
                    status=409
                )

            # Create approval request
            request_obj = PSRBudgetChangeRequest.objects.create(
                submitter=user,
                project_cost_category=pcc,
                proposed_budget_cost=new_cost,
                note=note,
                status='PENDING_APPROVERS'
            )

            if has_psr_permission(user, 'APPROVER'):
                PSRApprovalAction.objects.create(
                    request=request_obj,
                    approver=user,
                    stage='APPROVER',
                    action='APPROVE',
                    comment='Auto-approved (submitter is approver)'
                )

            return Response({
                "detail": "Budget change request submitted successfully. Awaiting approval.",
                "request_id": request_obj.id,
                "status": request_obj.status,
                "proposed_budget_cost": float(new_cost),
                "target": str(pcc)
            }, status=201)


class SubDepartmentForecastOverrideView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        sub_dept = get_object_or_404(PSRSubDepartment, pk=pk)
        user = request.user

        note = request.data.get('note', '').strip()
        lines_data = request.data.get('lines', [])

        if not note:
            return Response(
                {"detail": "Note (reason) is required for forecast override."},
                status=400
            )

        if not lines_data or not isinstance(lines_data, list):
            return Response(
                {"detail": "Lines (list of description + hours) is required."},
                status=400
            )

        total_hours = Decimal('0')

        for line in lines_data:
            hours_str = line.get('hours')
            if hours_str is None:
                return Response(
                    {"detail": "Each line must have 'hours'."},
                    status=400
                )
            total_hours += Decimal(str(hours_str))

        with transaction.atomic():
            previous_forecast = sub_dept.forecast_hours

            sub_dept.forecast_override = True
            sub_dept.forecast_hours = total_hours

            dept = sub_dept.department
            project = dept.project

            sub_dept.forecast_cost = total_hours * dept.hourly_rate
            sub_dept.forecast_overridden_by = user
            sub_dept.forecast_overridden_at = timezone.now()
            sub_dept.save()

            adjustment = ForecastAdjustment.objects.create(
                sub_department=sub_dept,
                adjusted_by=user,
                note=note,
                previous_forecast_hours=previous_forecast,
                new_forecast_hours=total_hours
            )

            for line in lines_data:
                ForecastAdjustmentLine.objects.create(
                    adjustment=adjustment,
                    description=line['description'],
                    hours=Decimal(str(line['hours']))
                )

        # Regenerate snapshot
        latest_snapshot = project.psr_snapshots.order_by('-snapshot_date').first()
        snapshot_date = None

        if latest_snapshot:
            call_command(
                'generate_psr_snapshot',
                str(project.co_no),
                '--date',
                latest_snapshot.snapshot_date.strftime('%Y-%m-%d')
            )
            snapshot_date = latest_snapshot.snapshot_date.strftime('%Y-%m-%d')

        return Response({
            "detail": "Forecast override applied successfully.",
            "warning": "Manual forecast override is now active.",
            "total_forecast_hours": float(total_hours),
            "adjustment_id": adjustment.id,
            "snapshot_regenerated": snapshot_date
        }, status=200)


class SubDepartmentGetForecastOverrideView(APIView):
    permission_classes = [IsAuthenticated]  # or AllowAny as needed

    def get(self, request, pk):
        sub_dept = get_object_or_404(PSRSubDepartment, pk=pk)

        if not sub_dept.forecast_override:
            return Response({
                "forecast_override": False,
                "detail": "No manual forecast override is active. Using auto-calculated forecast (Budget - Actual)."
            }, status=status.HTTP_200_OK)

        # Use the correct field name   likely 'adjustment_date' or 'created_at'
        latest_adjustment = sub_dept.forecast_adjustments.order_by('-adjustment_date').first()
        # OR if it's auto_now_add on created_at:
        # latest_adjustment = sub_dept.forecast_adjustments.order_by('-created_at').first()

        if not latest_adjustment:
            return Response({
                "forecast_override": True,
                "detail": "Override flag is set but no adjustment record found.",
                "current_forecast_hours": float(sub_dept.forecast_hours),
                "current_forecast_cost": float(sub_dept.forecast_cost),
            }, status=status.HTTP_200_OK)

        lines = []
        for line in latest_adjustment.lines.all():
            lines.append({
                "description": line.description,
                "hours": float(line.hours)
            })

        return Response({
            "forecast_override": True,
            "current_forecast_hours": float(sub_dept.forecast_hours),
            "current_forecast_cost": float(sub_dept.forecast_cost),
            "adjustment": {
                "id": latest_adjustment.id,
                "note": latest_adjustment.note,
                "previous_forecast_hours": float(latest_adjustment.previous_forecast_hours),
                "new_forecast_hours": float(latest_adjustment.new_forecast_hours),
                "adjusted_by": latest_adjustment.adjusted_by.username if latest_adjustment.adjusted_by else None,
                "adjusted_at": latest_adjustment.adjustment_date.isoformat() if hasattr(latest_adjustment, 'adjustment_date') else latest_adjustment.created_at.isoformat(),
                "lines": lines
            }
        }, status=status.HTTP_200_OK)


class ProjectCostCategoryForecastOverrideView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        pcc = get_object_or_404(ProjectCostCategory, pk=pk)
        user = request.user

        note = request.data.get('note', '').strip()
        lines_data = request.data.get('lines', [])

        if not note:
            return Response(
                {"detail": "Note (reason) is required."},
                status=400
            )

        if not lines_data or not isinstance(lines_data, list):
            return Response(
                {"detail": "Lines list is required."},
                status=400
            )

        total_amount = Decimal('0')

        for line in lines_data:
            amount_str = line.get('amount')
            if amount_str is None:
                return Response(
                    {"detail": "Each line must have 'amount'."},
                    status=400
                )
            total_amount += Decimal(str(amount_str))

        with transaction.atomic():
            previous_forecast = pcc.forecast_cost

            pcc.forecast_override = True
            pcc.forecast_cost = total_amount
            pcc.forecast_overridden_by = user
            pcc.forecast_overridden_at = timezone.now()
            pcc.save()

            adjustment = MaterialForecastAdjustment.objects.create(
                project_cost_category=pcc,
                adjusted_by=user,
                note=note,
                previous_forecast_cost=previous_forecast,
                new_forecast_cost=total_amount
            )

            for line in lines_data:
                MaterialForecastAdjustmentLine.objects.create(
                    adjustment=adjustment,
                    description=line['description'],
                    amount=Decimal(str(line['amount']))
                )

        # Regenerate snapshot
        project = pcc.project
        latest_snapshot = project.psr_snapshots.order_by('-snapshot_date').first()
        snapshot_date = None

        if latest_snapshot:
            call_command(
                'generate_psr_snapshot',
                str(project.co_no),
                '--date',
                latest_snapshot.snapshot_date.strftime('%Y-%m-%d')
            )
            snapshot_date = latest_snapshot.snapshot_date.strftime('%Y-%m-%d')

        return Response({
            "detail": "Material forecast override applied successfully.",
            "total_forecast_cost": float(total_amount),
            "adjustment_id": adjustment.id,
            "snapshot_regenerated": snapshot_date
        }, status=200)


class ProjectCostCategoryGetForecastOverrideView(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def get(self, request, pk):
        pcc = get_object_or_404(ProjectCostCategory, pk=pk)

        # Check if override is active
        if not pcc.forecast_override:
            return Response({
                "forecast_override": False,
                "detail": "No manual forecast override is active. Using auto-calculated forecast (Budget - Actual)."
            }, status=status.HTTP_200_OK)

        # ? CORRECT related_name: 'forecast_adjustments'
        latest_adjustment = pcc.forecast_adjustments.order_by('-adjustment_date').first()

        if not latest_adjustment:
            return Response({
                "forecast_override": True,
                "detail": "Override flag is set but no adjustment record found.",
                "current_forecast_cost": float(pcc.forecast_cost),
            }, status=status.HTTP_200_OK)

        # Serialize lines
        lines = []
        for line in latest_adjustment.lines.all():
            lines.append({
                "description": line.description,
                "amount": float(line.amount)
            })

        return Response({
            "forecast_override": True,
            "current_forecast_cost": float(pcc.forecast_cost),
            "adjustment": {
                "id": latest_adjustment.id,
                "note": latest_adjustment.note,
                "previous_forecast_cost": float(latest_adjustment.previous_forecast_cost),
                "new_forecast_cost": float(latest_adjustment.new_forecast_cost),
                "adjusted_by": latest_adjustment.adjusted_by.username if latest_adjustment.adjusted_by else None,
                "adjusted_at": latest_adjustment.adjustment_date.isoformat(),
                "lines": lines
            }
        }, status=status.HTTP_200_OK)


SUB_DEPT_DETAILS = {
    "PM": ("Project Management PRO", 
           "Project Manager", 
           "PROJECT_MANAGEMENT"),
    "POM": ("Site Manager BSTL", 
            "OnSide Manager", 
            "PROJECT_MANAGEMENT"),
    "PEM": ("Mechanical design coordinator MEC", 
            "Project Mechanical design Engineering Manager", 
            "MECHANICAL_DESIGN"),
    "KMA/KHP": ("Engineering Mechanical & Pneumatic Design KMA_KHP", 
                "Mechanical Design ", 
                "MECHANICAL_DESIGN"),
    "DET": ("Engineering Detailing DET", 
            "Detailing ", 
            "MECHANICAL_DESIGN"),
    "DOK": ("Documentation DOK_SERV", 
            "Documentation", 
            "MECHANICAL_DESIGN"),
    "SIM": ("Simulation", 
            "Simulation", 
            "MECHANICAL_DESIGN"),
    "2D": ("2D Detailing", 
           "2D Detailing", 
           "MECHANICAL_DESIGN"),
    "QC": ("Quality Checking", 
           "Quality Checking", 
           "MECHANICAL_DESIGN"),
    "LAY": ("Layout",
            "Layout",
            "MECHANICAL_DESIGN"),
    "PEC": ("Electrics coordinator-ELK ", 
            "Project Controls Engineering Manager", 
            "ELECTRICAL_DESIGN"),
    "KEL": ("Engineering Electrical Design KEL", 
            "Electrical Design", 
            "ELECTRICAL_DESIGN"),
    "KES": ("Electrical Design SPecial Software KES_KESs", 
            "Software  Design", 
            "IN_HOUSE_COMMISSIONING"),
    "IBS": ("Engineering Software & Commisioning Coordinator IBS", 
            "Software  Commissioning", 
            "IN_HOUSE_COMMISSIONING"),
    "IBSS": ("Commissioning & Special Software IBS_IBSs TKSY", 
             "Software  Commissioning", 
             "IN_HOUSE_COMMISSIONING"),
    "IBK": ("Engineering Software & Commissioning at customer site IBK_IBKs", 
            "Commissioning on site", 
            "ON_SITE_COMMISSIONING"),
    "PAM": ("", 
            "Manager Assembly & Installation", 
            "MECHANICAL_INSTALLATION"),
    "MMA/MHP": ("Mechanical,Pneumatic,Hydrauic Assembly on TKSY Shop Floor MMA_VMA_MHP", 
            "Mechanical Assembly", 
            "MECHANICAL_INSTALLATION"),
    "A+I(M)": ("Mechanical ,Pneumatic,Hydraulic Assembly On site AIM", 
            "Mechanical Assembly  on site", 
            "MECHANICAL_INSTALLATION"),
    "INS": ("Electrical Installation INS Inhouse", 
            "Electrical Installation", 
            "ELECTRICAL_INSTALLATION"),
    "A+I(E)": ("Electrical Installation on Site AIE", 
            "Electrical Installation  on site", 
            "ELECTRICAL_INSTALLATION"),
}


# class ProjectCreateView(CreateAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = ProjectCreateSerializer

#     @transaction.atomic
#     def perform_create(self, serializer):
#         # Save project   this triggers save() override which calculates all derived fields
#         project = serializer.save()

#         # === Create Departments, SubDepartments, ProjectCostCategories ===
#         dept_budgets = self.request.data.get('department_budgets', {})
#         sub_budgets = self.request.data.get('sub_department_budgets', {})  # Now expects budget_cost
#         cost_cat_budgets = self.request.data.get('cost_category_budgets', {})

#         departments_map = {}

#         # Create Departments
#         for dept_name, payload in dept_budgets.items():
#             hourly_rate = Decimal(str(payload.get('hourly_rate', '2000.00')))
#             # budget_hours no longer used here   kept for reference
#             # budget_hours = Decimal(str(payload.get('budget_hours', '0')))

#             dept = PSRDepartment.objects.create(
#                 project=project,
#                 name=dept_name,
#                 hourly_rate=hourly_rate,
#                 budget_hours=0,  # Will be updated via sub-department totals if needed
#             )
#             departments_map[dept_name] = dept

#         for code, (role_descrptn, inkrement, dept_name) in SUB_DEPT_DETAILS.items():
#             budget_cost_str = sub_budgets.get(code, '0')
#             budget_cost = Decimal(str(budget_cost_str)) if budget_cost_str else Decimal('0')

#             department = departments_map.get(dept_name)
#             if not department:
#                 continue

#             # rate_inr = department.hourly_rate * project.exchange_rate
#             rate_inr = department.hourly_rate
#             budget_hours = budget_cost / rate_inr if rate_inr > 0 else Decimal('0')

#             PSRSubDepartment.objects.create(
#                 department=department,
#                 code=code,
#                 role_descrptn=role_descrptn,
#                 inkrement=inkrement,
#                 baseline_budget_cost=budget_cost,
#                 budget_hours=budget_hours,
#                 budget_cost=budget_cost,  # Direct storage
#             )
        
#         for dept in project.departments.all():
#             total_dept_cost = sum(sub.budget_cost for sub in dept.sub_departments.all())
#             dept.budget_cost = total_dept_cost
#             dept.save()

#         # Create ProjectCostCategory with baseline (unchanged)
#         for cost_cat in CostCategory.objects.all():
#             budget_cost = Decimal(str(cost_cat_budgets.get(cost_cat.code, '0')))

#             ProjectCostCategory.objects.create(
#                 project=project,
#                 cost_category=cost_cat,
#                 baseline_budget_cost=budget_cost,
#                 budget_cost=budget_cost,
#             )

#         # === Generate First PSR Snapshot ===
#         snapshot_date = project.created_at.date()

#         try:
#             call_command(
#                 'generate_psr_snapshot',
#                 str(project.co_no),
#                 '--date',
#                 snapshot_date.strftime('%Y-%m-%d')
#             )
#         except Exception as e:
#             print(f"Warning: Could not generate initial snapshot: {e}")

#         return project

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)

#         full_serializer = ProjectCreateSerializer(serializer.instance)
#         return Response({
#             "detail": "Project created successfully with initial financial plan and first PSR snapshot.",
#             "project": full_serializer.data
#         }, status=status.HTTP_201_CREATED, headers=headers)

class ProjectCreateView(CreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ProjectCreateSerializer

    def _create_project_components(self, project, setup_data):
        """
        Reusable method to create departments, sub-departments, cost categories,
        and initial snapshot from the initialization data.
        """
        dept_budgets = setup_data.get("department_budgets", {})
        sub_budgets = setup_data.get("sub_department_budgets", {})
        cost_cat_budgets = setup_data.get("cost_category_budgets", {})

        departments_map = {}

        # ---------------- Departments
        for dept_name, payload in dept_budgets.items():
            hourly_rate = Decimal(str(payload.get("hourly_rate", "2000.00")))
            dept = PSRDepartment.objects.create(
                project=project,
                name=dept_name,
                hourly_rate=hourly_rate,
                budget_hours=0,
            )
            departments_map[dept_name] = dept

        # ---------------- SubDepartments
        for code, (role_descrptn, inkrement, dept_name) in SUB_DEPT_DETAILS.items():
            budget_cost_str = sub_budgets.get(code, "0")
            budget_cost = (
                Decimal(str(budget_cost_str)) if budget_cost_str else Decimal("0")
            )

            department = departments_map.get(dept_name)
            if not department:
                continue

            rate_inr = department.hourly_rate
            budget_hours = budget_cost / rate_inr if rate_inr > 0 else Decimal("0")

            PSRSubDepartment.objects.create(
                department=department,
                code=code,
                role_descrptn=role_descrptn,
                inkrement=inkrement,
                baseline_budget_cost=budget_cost,
                budget_hours=budget_hours,
                budget_cost=budget_cost,
            )

        # ---------------- Rollup Departments
        for dept in project.departments.all():
            total_dept_cost = sum(sub.budget_cost for sub in dept.sub_departments.all())
            dept.budget_cost = total_dept_cost
            dept.save()

        # ---------------- Cost Categories
        for cost_cat in CostCategory.objects.all():
            budget_cost = Decimal(str(cost_cat_budgets.get(cost_cat.code, "0")))
            ProjectCostCategory.objects.create(
                project=project,
                cost_category=cost_cat,
                baseline_budget_cost=budget_cost,
                budget_cost=budget_cost,
            )

        # ---------------- Snapshot
        snapshot_date = project.created_at.date()
        try:
            call_command(
                "generate_psr_snapshot",
                str(project.co_no),
                "--date",
                snapshot_date.strftime("%Y-%m-%d"),
            )
        except Exception as e:
            logger.error(f"Snapshot generation failed: {e}")

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user

        # 1. Save the project (Removed status=... because field doesn't exist)
        project = serializer.save()

        # ✅ ADMIN → Direct Full Creation
        if has_psr_permission(user, "ADMIN"):
            # If you still need a way to track if a project is "Live", 
            # you would do it via the Request table status.
            creation_request = PSRProjectCreationRequest.objects.create(
                project=project,
                submitter=user,
                status="APPROVED", # Admin bypasses pending states
                data=self.request.data,
            )
            # Create components immediately
            self._create_project_components(project, self.request.data)

        # ✅ PREPARER / APPROVER → Approval Request Flow
        elif has_psr_permission(user, "PREPARER") or has_psr_permission(user, "APPROVER"):
            creation_request = PSRProjectCreationRequest.objects.create(
                project=project,
                submitter=user,
                status="PENDING_APPROVERS",
                data=self.request.data,
            )

            # Assign Approvers
            approvers = get_psr_approvers()
            for approver in approvers:
                if approver == user:
                    continue 
                PSRProjectApprovalAction.objects.create(
                    request=creation_request, approver=approver, stage="APPROVER"
                )

            # Assign Admin
            admin = get_psr_admin()
            if admin:
                PSRProjectApprovalAction.objects.create(
                    request=creation_request, approver=admin, stage="ADMIN"
                )

        else:
            raise PermissionDenied("You are not allowed to create projects.")

        return project
    
    
    
class ProjectDetailView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get(self, request, co_no):
        project = get_object_or_404(PSRProject, co_no=co_no)

        if project.project_manager:
            project_manager_name = f"{project.project_manager.first_name} {project.project_manager.last_name}"
        else:
            project_manager_name = ""
        
        # Base project data
        data = {
            "co_no": project.co_no,
            "project_name": project.project_name,
            "location": project.location,
            "project_manager": project_manager_name,
            "project_manager_email": project.project_manager_email,
            "sales_person": project.sales_person,
            "sales_person_email": project.sales_person_email,
            "settlement_period": project.settlement_period,
            "sales_value_foreign_curr": float(project.sales_value_foreign_curr),
            "sales_value": float(project.sales_value),
            "direct_margin_percentage": float(project.direct_margin_percentage),
            "sgna_percentage": float(project.sgna_percentage),
            "ter_percentage": float(project.ter_percentage),
            "eff_percentage": float(project.eff_percentage),
            "risk": float(project.risk),
            "budget": float(project.budget),
            "currency": project.currency,
            "exchange_rate": float(project.exchange_rate),
        }

        # Departments with rates and budget_hours
        department_budgets = {}
        for dept in project.departments.all():
            department_budgets[dept.name] = {
                "hourly_rate": float(dept.hourly_rate)
            }
        data["department_budgets"] = department_budgets

        # SubDepartments with budget_hours
        sub_department_budgets = {}
        for sub in PSRSubDepartment.objects.filter(department__project=project):
            sub_department_budgets[sub.code] = float(sub.budget_cost)
        data["sub_department_budgets"] = sub_department_budgets

        # Cost categories with budget_cost
        cost_category_budgets = {}
        for pcc in project.project_cost_categories.all():
            cost_category_budgets[pcc.cost_category.code] = float(pcc.budget_cost)
        data["cost_category_budgets"] = cost_category_budgets

        return Response(data, status=status.HTTP_200_OK)


from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from accounts.models import CustomUser
from psr.models import (
    PSRProject, PSRDepartment, PSRSubDepartment,
    ProjectCostCategory, PSRSnapshot
)

# class ProjectUpdateView(APIView):
#     permission_classes = [IsAuthenticated]

#     @transaction.atomic
#     def patch(self, request, co_no):
#         project = get_object_or_404(PSRProject, co_no=co_no)

#         # ===============================
#         # Update main project fields
#         # ===============================
#         project_fields = [
#             'project_name',
#             'location',
#             'project_manager',          # FK handled separately
#             'project_manager_email',
#             'sales_person',
#             'sales_person_email',
#             'sales_value_foreign_curr',
#             'direct_margin_percentage',
#             'ter_percentage',
#             'eff_percentage',
#             'risk',
#             'currency',
#             'exchange_rate',
#         ]

#         for field in project_fields:
#             if field not in request.data:
#                 continue

#             value = request.data[field]

#             if field == 'project_manager':
#                 if value is None:
#                     project.project_manager = None
#                 else:
#                     project.project_manager = get_object_or_404(CustomUser, id=value)

#             elif field in [
#                 'sales_value_foreign_curr',
#                 'direct_margin_percentage',
#                 'ter_percentage',
#                 'eff_percentage',
#                 'risk',
#                 'exchange_rate',
#             ]:
#                 setattr(project, field, Decimal(str(value)) if value is not None else None)

#             else:
#                 setattr(project, field, value)

#         project.save()  # triggers recalculation safely

#         # ===============================
#         # Update departments
#         # ===============================
#         if 'department_budgets' in request.data:
#             for dept_code, values in request.data['department_budgets'].items():
#                 dept = get_object_or_404(
#                     PSRDepartment,
#                     project=project,
#                     name=dept_code
#                 )
#                 if 'hourly_rate' in values:
#                     dept.hourly_rate = Decimal(str(values['hourly_rate']))
#                 dept.save()

#         # ===============================
#         # Update sub-departments
#         # ===============================
#         if 'sub_department_budgets' in request.data:
#             for code, cost in request.data['sub_department_budgets'].items():
#                 sub = get_object_or_404(
#                     PSRSubDepartment,
#                     department__project=project,
#                     code=code
#                 )
#                 sub.budget_cost = Decimal(str(cost))

#                 rate = sub.department.hourly_rate
#                 exchange = project.exchange_rate
#                 # sub.budget_hours = (
#                 #     sub.budget_cost / (rate * exchange)
#                 #     if rate and exchange else Decimal('0')
#                 # )

#                 sub.budget_hours = (
#                     sub.budget_cost / rate 
#                     if rate and exchange else Decimal('0')
#                 )

#                 sub.save()

#         # ===============================
#         # Update cost categories
#         # ===============================
#         if 'cost_category_budgets' in request.data:
#             for code, cost in request.data['cost_category_budgets'].items():
#                 pcc = get_object_or_404(
#                     ProjectCostCategory,
#                     project=project,
#                     cost_category__code=code
#                 )
#                 pcc.budget_cost = Decimal(str(cost))
#                 pcc.save()

#         # ===============================
#         # Regenerate PSR snapshot
#         # ===============================
#         latest_snapshot = (
#             PSRSnapshot.objects
#             .filter(project=project)
#             .order_by('-snapshot_date')
#             .first()
#         )

#         if latest_snapshot:
#             snapshot_date = latest_snapshot.snapshot_date
#             try:
#                 call_command(
#                     'generate_psr_snapshot',
#                     str(project.co_no),
#                     '--date',
#                     snapshot_date.strftime('%Y-%m-%d')
#                 )
#             except Exception as e:
#                 print(f"Warning: Snapshot regeneration failed: {e}")

#         return Response(
#             {
#                 "detail": "Project updated successfully.",
#                 "co_no": project.co_no
#             },
#             status=status.HTTP_200_OK
#         )



from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.management import call_command
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


import logging
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.management import call_command
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Import your models and helpers here
# from .models import PSRProject, PSRProjectCreationRequest, PSRProjectApprovalAction, PSRDepartment, PSRSubDepartment, ProjectCostCategory, PSRSnapshot
# from .serializers import PSRProjectCreationRequestSerializer

logger = logging.getLogger(__name__)

class ProjectUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def patch(self, request, co_no):
        # Use select_for_update to prevent race conditions during the workflow
        project = get_object_or_404(PSRProject.objects.select_for_update(), co_no=co_no)
        user = request.user

        # ==============================
        # ✅ ADMIN → DIRECT UPDATE
        # ==============================
        if has_psr_permission(user, "ADMIN"):
            # 1. Update main project fields
            self._apply_project_updates(project, request.data)
            # 2. Update Depts/Sub-Depts/Cost Cats & Trigger Snapshot
            self._apply_component_updates(project, request.data)
            
            project.refresh_from_db()
            return Response({
                "detail": "Project updated directly and snapshot regenerated.",
                "co_no": project.co_no
            }, status=status.HTTP_200_OK)

        # ==============================
        # ✅ NON-ADMIN → WORKFLOW
        # ==============================
        # FIX: Ensure status is never " "
        creation_request, created = PSRProjectCreationRequest.objects.get_or_create(
            project=project,
            defaults={
                'submitter': user, 
                'data': request.data, 
                'status': 'PENDING_APPROVERS'
            }
        )

        # Reset to pending if it's an update to an existing request
        creation_request.status = "PENDING_APPROVERS"
        creation_request.data = request.data
        creation_request.submitter = user
        creation_request.save()

        # Clear old actions to restart the approval chain
        creation_request.approval_actions.all().delete()

        # Assign Approvers
        approvers = get_psr_approvers()
        for approver in approvers:
            if approver != user:
                PSRProjectApprovalAction.objects.create(
                    request=creation_request, 
                    approver=approver, 
                    stage="APPROVER"
                )

        # Assign Admin
        admin = get_psr_admin()
        if admin:
            PSRProjectApprovalAction.objects.create(
                request=creation_request, 
                approver=admin, 
                stage="ADMIN"
            )

        return Response({
            "detail": "Update request submitted.",
            "status": creation_request.status
        }, status=status.HTTP_202_ACCEPTED)

    def _apply_project_updates(self, project, update_data):
        fields_to_map = [
            'project_name', 'location', 'project_manager_email',
            'sales_person', 'sales_person_email', 'currency',
            'sales_value_foreign_curr', 'direct_margin_percentage',
            'ter_percentage', 'eff_percentage', 'risk', 'exchange_rate',
            'settlement_period'
        ]

        for field in fields_to_map:
            if field in update_data:
                value = update_data[field]
                if field in ['sales_value_foreign_curr', 'exchange_rate', 'direct_margin_percentage', 'risk', 'ter_percentage', 'eff_percentage']:
                    setattr(project, field, Decimal(str(value)) if value is not None else Decimal('0'))
                else:
                    setattr(project, field, value)

        if 'project_manager' in update_data:
            pm_id = update_data['project_manager']
            project.project_manager = CustomUser.objects.filter(id=pm_id).first()

        project.save()

    def _apply_component_updates(self, project, data):
        # 1. Departments
        if 'department_budgets' in data:
            for dept_name, payload in data['department_budgets'].items():
                PSRDepartment.objects.filter(project=project, name=dept_name).update(
                    hourly_rate=Decimal(str(payload.get("hourly_rate", "2000.00")))
                )

        # 2. Sub-Departments
        if 'sub_department_budgets' in data:
            for code, cost_value in data['sub_department_budgets'].items():
                sub = PSRSubDepartment.objects.filter(department__project=project, code=code).first()
                if sub:
                    sub.budget_cost = Decimal(str(cost_value))
                    # Re-fetch hourly rate from dept (handling the .update() from step 1)
                    sub.department.refresh_from_db()
                    rate = sub.department.hourly_rate
                    sub.budget_hours = sub.budget_cost / rate if rate > 0 else Decimal("0")
                    sub.save()

        # 3. Cost Categories
        if 'cost_category_budgets' in data:
            for code, cost_value in data['cost_category_budgets'].items():
                ProjectCostCategory.objects.filter(project=project, cost_category__code=code).update(
                    budget_cost=Decimal(str(cost_value))
                )

        # 4. Rollups (CRITICAL FIX: refresh_from_db)
        for dept in project.departments.all():
            dept.refresh_from_db() # Sync hourly_rate from SQL update
            dept.budget_cost = sum(sub.budget_cost for sub in dept.sub_departments.all())
            dept.save()

        # 5. Snapshot Regeneration (CRITICAL FIX: on_commit)
        latest_snapshot = PSRSnapshot.objects.filter(project=project).order_by('-snapshot_date').first()
        snapshot_date_str = latest_snapshot.snapshot_date.strftime('%Y-%m-%d') if latest_snapshot else None
        co_no_str = str(project.co_no)

        def trigger_snapshot():
            try:
                args = [co_no_str]
                if snapshot_date_str:
                    args.extend(['--date', snapshot_date_str])
                call_command("generate_psr_snapshot", *args)
                logger.info(f"Snapshot regenerated for {co_no_str}")
            except Exception as e:
                logger.error(f"Error regenerating snapshot: {e}")

        # The command runs only after the SQL transaction is committed
        print("Scheduling snapshot regeneration after transaction commit...")
        transaction.on_commit(trigger_snapshot)

# class ProjectUpdateView(APIView):
#     permission_classes = [IsAuthenticated]

#     @transaction.atomic
#     def patch(self, request, co_no):
#         project = get_object_or_404(PSRProject, co_no=co_no)
#         user = request.user

#         # ==============================
#         # ✅ ADMIN → DIRECT UPDATE
#         # ==============================
#         if has_psr_permission(user, "ADMIN"):
#             # 1. Update main project fields (EBIT, etc via save())
#             self._apply_project_updates(project, request.data)
#             # 2. Update Depts/Sub-Depts/Cost Cats & Trigger Snapshot
#             self._apply_component_updates(project, request.data)
#             project.refresh_from_db()
#             return Response({
#                 "detail": "Project updated directly and snapshot regenerated.",
#                 "co_no": project.co_no
#             }, status=status.HTTP_200_OK)

#         # ==============================
#         # ✅ NON-ADMIN → WORKFLOW
#         # ==============================
#         creation_request, created = PSRProjectCreationRequest.objects.get_or_create(
#             project=project,
#             defaults={'submitter': user, 'data': request.data}
#         )

#         creation_request.status = "PENDING_APPROVERS"
#         creation_request.data = request.data
#         creation_request.submitter = user
#         creation_request.save()

#         creation_request.approval_actions.all().delete()

#         # Assign Approvers & Admin
#         approvers = get_psr_approvers()
#         for approver in approvers:
#             if approver != user:
#                 PSRProjectApprovalAction.objects.create(
#                     request=creation_request, approver=approver, stage="APPROVER"
#                 )

#         admin = get_psr_admin()
#         if admin:
#             PSRProjectApprovalAction.objects.create(
#                 request=creation_request, approver=admin, stage="ADMIN"
#             )

#         return Response({"detail": "Update request submitted."}, status=status.HTTP_202_ACCEPTED)

#     def _apply_project_updates(self, project, update_data):
#         """
#         Maps JSON data fields to PSRProject model fields.
#         """
#         fields_to_map = [
#             'project_name', 'location', 'project_manager_email',
#             'sales_person', 'sales_person_email', 'currency',
#             'sales_value_foreign_curr', 'direct_margin_percentage',
#             'ter_percentage', 'eff_percentage', 'risk', 'exchange_rate',
#             'settlement_period'
#         ]

#         for field in fields_to_map:
#             if field in update_data:
#                 value = update_data[field]
#                 if field in ['sales_value_foreign_curr', 'exchange_rate', 'direct_margin_percentage', 'risk', 'ter_percentage', 'eff_percentage']:
#                     setattr(project, field, Decimal(str(value)) if value is not None else Decimal('0'))
#                 else:
#                     setattr(project, field, value)

#         if 'project_manager' in update_data:
#             pm_id = update_data['project_manager']
#             project.project_manager = CustomUser.objects.filter(id=pm_id).first()

#         project.save()

#     def _apply_component_updates(self, project, data):
#         """
#         Updates budgets and triggers the snapshot regeneration.
#         """
#         # 1. Departments
#         if 'department_budgets' in data:
#             for dept_name, payload in data['department_budgets'].items():
#                 PSRDepartment.objects.filter(project=project, name=dept_name).update(
#                     hourly_rate=Decimal(str(payload.get("hourly_rate", "2000.00")))
#                 )

#         # 2. Sub-Departments
#         if 'sub_department_budgets' in data:
#             for code, cost_value in data['sub_department_budgets'].items():
#                 sub = PSRSubDepartment.objects.filter(department__project=project, code=code).first()
#                 if sub:
#                     sub.budget_cost = Decimal(str(cost_value))
#                     rate = sub.department.hourly_rate
#                     # Recalculate hours
#                     sub.budget_hours = sub.budget_cost / rate if rate > 0 else Decimal("0")
#                     sub.save()

#         # 3. Cost Categories
#         if 'cost_category_budgets' in data:
#             for code, cost_value in data['cost_category_budgets'].items():
#                 ProjectCostCategory.objects.filter(project=project, cost_category__code=code).update(
#                     budget_cost=Decimal(str(cost_value))
#                 )

#         # 4. Rollups
#         for dept in project.departments.all():
#             dept.budget_cost = sum(sub.budget_cost for sub in dept.sub_departments.all())
#             dept.save()

#         # 5. Snapshot Regeneration (The Missing Piece)
#         latest_snapshot = PSRSnapshot.objects.filter(project=project).order_by('-snapshot_date').first()
        
#         # We always want a snapshot. If one exists, update it. If not, generate for today.
#         try:
#             snapshot_date_str = latest_snapshot.snapshot_date.strftime('%Y-%m-%d') if latest_snapshot else None
            
#             args = [str(project.co_no)]
#             if snapshot_date_str:
#                 args.extend(['--date', snapshot_date_str])

#             call_command("generate_psr_snapshot", *args)
#         except Exception as e:
#             print(f"Error regenerating snapshot: {e}")


class ProjectKPIDetailsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, co_no):
        project = get_object_or_404(PSRProject, co_no=co_no)
        serializer = ProjectBasicSerializer(project)
        return Response(serializer.data)


class ProjectStatusUpdateView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, co_no):
        project = get_object_or_404(PSRProject, co_no=co_no)
        serializer = ProjectUpdateSerializer(
            project,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                "detail": "Project updated successfully",
                "data": ProjectBasicSerializer(project).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectLatestSnapshotKPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, co_no):
        project = get_object_or_404(PSRProject, co_no=co_no)
        snapshot = PSRSnapshot.objects.filter(project=project).order_by('-snapshot_date').first()
        if not snapshot:
            return Response({"detail": "No snapshot available"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PSRSnapshotKPISerializer(snapshot)
        return Response({
            "project": project.co_no,
            "snapshot_date": snapshot.snapshot_date,
            "kpi": serializer.data
        })


class ProjectSnapshotHistoryKPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, co_no):
        project = get_object_or_404(PSRProject, co_no=co_no)
        snapshots = PSRSnapshot.objects.filter(project=project).order_by('snapshot_date')
        if not snapshots.exists():
            return Response({"detail": "No snapshots available"}, status=status.HTTP_404_NOT_FOUND)

        history = []
        for snapshot in snapshots:
            serializer = PSRSnapshotKPISerializer(snapshot)
            history.append({
                "snapshot_date": snapshot.snapshot_date.strftime('%Y-%m-%d'),
                "kpi": serializer.data
            })

        return Response({
            "project": project.co_no,
            "project_name": project.project_name,
            "history": history
        })


class LandingPageAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        projects = PSRProject.objects.all()

        # Initialize aggregated totals
        total_sales_value = Decimal('0')
        total_budget = Decimal('0')
        total_ter = Decimal('0')
        total_eff = Decimal('0')
        total_actual = Decimal('0')
        total_forecast = Decimal('0')
        total_prognosis = Decimal('0')
        total_factors = Decimal('0')
        total_ebit_values = Decimal('0')
        total_ebit_percentages = Decimal('0')
        total_net_marginal_income = Decimal('0')
        total_net_marginal_income_percentages = Decimal('0')
        project_count = 0

        # Get latest snapshot for each project
        for project in projects:
            # Get the latest snapshot for this project
            latest_snapshot = PSRSnapshot.objects.filter(
                project=project
            ).order_by('-snapshot_date').first()

            # Add project values
            total_sales_value += project.sales_value or Decimal('0')

            # Add snapshot values if snapshot exists
            if latest_snapshot:
                
                total_budget += latest_snapshot.total_budget_cost or Decimal('0')
                total_ter += latest_snapshot.ter_value or Decimal('0')
                total_eff += latest_snapshot.eff_value or Decimal('0')
                total_actual += latest_snapshot.total_actual_cost or Decimal('0')
                total_forecast += latest_snapshot.total_forecast_cost or Decimal('0')
                total_prognosis += latest_snapshot.total_prognosis_cost or Decimal('0')
                total_ebit_values += latest_snapshot.ebit_value or Decimal('0')
                total_net_marginal_income += latest_snapshot.net_marginal_income or Decimal('0')
                
                # Add factor for averaging
                total_factors += latest_snapshot.factor or Decimal('0')
                total_ebit_percentages += latest_snapshot.ebit_percentage or Decimal('0')
                total_net_marginal_income_percentages += latest_snapshot.net_marginal_income_percentage or Decimal('0')
                project_count += 1

        # Calculate average factor
        average_factor = total_factors / project_count if project_count > 0 else Decimal('0')
        average_ebit_percentage = total_ebit_percentages / project_count if project_count > 0 else Decimal('0')
        average_net_marginal_income_percentage = total_net_marginal_income_percentages / project_count if project_count > 0 else Decimal('0')

        # Format the response - only the 8 fields for landing page
        return Response({
            "total_sales_value": float(total_sales_value),
            "total_budget": float(total_budget),
            "total_ter": float(total_ter),
            "total_eff": float(total_eff),
            "total_actual": float(total_actual),
            "total_forecast": float(total_forecast),
            "total_prognosis": float(total_prognosis),
            "average_factor": float(average_factor),
            "average_ebit_percentage": float(average_ebit_percentage),
            "average_net_marginal_income_percentage": float(average_net_marginal_income_percentage)
        }, status=status.HTTP_200_OK)


class AllProjectsLatestSnapshotView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Get all projects that have at least one snapshot
        projects_with_snapshots = PSRProject.objects.filter(
            psr_snapshots__isnull=False
        ).distinct()

        project_data = []

        for project in projects_with_snapshots:
            snapshot = project.psr_snapshots.order_by('-snapshot_date').first()
            if snapshot:  # Should always exist due to filter
                data = {
                    "project_id": project.id,
                    "co_no": project.co_no,
                    "project_name": project.project_name,
                    "sales_value": float(project.sales_value),
                    "total_budget_cost": float(snapshot.total_budget_cost),
                    "ter_value": float(snapshot.ter_value),
                    "eff_value": float(snapshot.eff_value),
                    "total_actual_cost": float(snapshot.total_actual_cost),
                    "total_forecast_cost": float(snapshot.total_forecast_cost),
                    "total_prognosis_cost": float(snapshot.total_prognosis_cost),
                    "margin": float(snapshot.margin),
                    "factor": float(snapshot.factor),
                    "ebit_value": float(snapshot.ebit_value),
                    "ebit_percentage": float(snapshot.ebit_percentage),
                    "net_marginal_income": float(snapshot.net_marginal_income),
                    "net_marginal_income_percentage": float(snapshot.net_marginal_income_percentage),
                }
                project_data.append(data)

        return Response({
            "count": len(project_data),
            "projects_latest_snapshots": project_data
        })


class MonthlyCumulativeKPIHistoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Get all snapshots ordered by date
        snapshots = PSRSnapshot.objects.all().order_by('snapshot_date')

        # Group by month (YYYY-MM)
        monthly_data = defaultdict(lambda: {
            'sales_value': Decimal('0'),
            'total_budget_cost': Decimal('0'),
            'ter_value': Decimal('0'),
            'eff_value': Decimal('0'),
            'total_actual_cost': Decimal('0'),
            'total_forecast_cost': Decimal('0'),
            'total_prognosis_cost': Decimal('0'),
            'margin': Decimal('0'),
            'factor_sum': Decimal('0'),
            'factor_count': 0,
            'ebit_value': Decimal('0'),
            'ebit_percentage_sum': Decimal('0'),
            'ebit_percentage_count': 0,
            'net_marginal_income': Decimal('0'),
            'net_marginal_income_percentage_sum': Decimal('0'),
            'net_marginal_income_percentage_count': 0,
        })

        for snapshot in snapshots:
            month_key = snapshot.snapshot_date.strftime('%Y-%m')
            month_name = snapshot.snapshot_date.strftime('%B %Y')

            data = monthly_data[month_key]
            data['sales_value'] += snapshot.project.sales_value
            data['total_budget_cost'] += snapshot.total_budget_cost
            data['ter_value'] += snapshot.ter_value
            data['eff_value'] += snapshot.eff_value
            data['total_actual_cost'] += snapshot.total_actual_cost
            data['total_forecast_cost'] += snapshot.total_forecast_cost
            data['total_prognosis_cost'] += snapshot.total_prognosis_cost
            data['margin'] += snapshot.margin
            data['factor_sum'] += snapshot.factor
            data['factor_count'] += 1
            data['ebit_value'] += snapshot.ebit_value
            data['ebit_percentage_sum'] += snapshot.ebit_percentage
            data['ebit_percentage_count'] += 1
            data['net_marginal_income'] += snapshot.net_marginal_income
            data['net_marginal_income_percentage_sum'] += snapshot.net_marginal_income_percentage
            data['net_marginal_income_percentage_count'] += 1

        # Build final list in reverse chronological order
        history = []
        for month_key in sorted(monthly_data.keys(), reverse=True):
            month_name = datetime.strptime(month_key, '%Y-%m').strftime('%B %Y')
            data = monthly_data[month_key]
            average_factor = data['factor_sum'] / data['factor_count'] if data['factor_count'] > 0 else Decimal('0')
            average_ebit_percentage = data['ebit_percentage_sum'] / data['ebit_percentage_count'] if data['ebit_percentage_count'] > 0 else Decimal('0')
            average_net_marginal_income = data['net_marginal_income_percentage_sum'] / data['net_marginal_income_percentage_count'] if data['net_marginal_income_percentage_count'] > 0 else Decimal ('0')

            history.append({
                "month": month_name,
                "sales_value": data['sales_value'],
                "total_budget_cost": data['total_budget_cost'],
                "ter_value": data['ter_value'],
                "eff_value": data['eff_value'],
                "total_actual_cost": data['total_actual_cost'],
                "total_forecast_cost": data['total_forecast_cost'],
                "total_prognosis_cost": data['total_prognosis_cost'],
                "margin": data['margin'],
                "factor": round(average_factor, 4),
                "ebit_value": data['ebit_value'],
                "ebit_percentage": round(average_ebit_percentage, 2),
                "net_marginal_income": data['net_marginal_income'],
                "net_marginal_income_percentage": round(average_net_marginal_income, 2),
            })

        serializer = MonthlyCumulativeKPISerializer(history, many=True)
        return Response({
            "months_count": len(history),
            "cumulative_kpi_history": serializer.data
        })


class RKActualOverrideView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        pcc = get_object_or_404(ProjectCostCategory, pk=pk)
        
        # Validate it's RK
        if pcc.cost_category.code != 'RK':
            return Response(
                {"detail": "This endpoint is only for RK (Travel Costs) category."},
                status=status.HTTP_400_BAD_REQUEST
            )

        note = request.data.get('note')
        lines = request.data.get('lines', [])

        if not note:
            return Response({"detail": "Note is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not lines or len(lines) == 0:
            return Response({"detail": "At least one line with description and amount is required."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Get the latest adjustment or create new
            adjustment = pcc.rk_actual_adjustments.order_by('-adjusted_at').first()
            
            if adjustment:
                # Update existing
                adjustment.note = note
                adjustment.adjusted_by = request.user
                adjustment.adjusted_at = timezone.now()
                adjustment.save()
                
                # Delete old lines
                adjustment.lines.all().delete()
            else:
                # Create new if none exists
                adjustment = RKActualAdjustment.objects.create(
                    project_cost_category=pcc,
                    adjusted_by=request.user,
                    note=note
                )

            # Add all sent lines (full replacement)
            total_amount = Decimal('0')
            for line in lines:
                amount = Decimal(str(line.get('amount', '0')))
                # if amount <= 0:
                #     return Response({"detail": "Each line must have positive amount."}, status=status.HTTP_400_BAD_REQUEST)
                
                RKActualAdjustmentLine.objects.create(
                    adjustment=adjustment,
                    description=line.get('description', ''),
                    amount=amount
                )
                total_amount += amount

            # Set override flag
            pcc.actual_override = True
            pcc.save()

        # Regenerate latest snapshot
        latest_snapshot = pcc.project.psr_snapshots.order_by('-snapshot_date').first()
        if latest_snapshot:
            call_command('generate_psr_snapshot', str(pcc.project.co_no), '--date', latest_snapshot.snapshot_date.strftime('%Y-%m-%d'))

        serializer = RKActualAdjustmentSerializer(adjustment)
        return Response({
            "detail": "RK actuals updated successfully",
            "current_total_actuals": float(total_amount),
            "adjustment": serializer.data
        }, status=status.HTTP_200_OK)


class RKGetActualOverrideView(APIView):
    """
    GET: Retrieve current manual actual override status for RK
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        pcc = get_object_or_404(ProjectCostCategory, pk=pk)

        if pcc.cost_category.code != 'RK':
            return Response(
                {"detail": "This endpoint is only for RK category."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate current PO actual
        po_entries = POData.objects.filter(
            co_no__startswith=pcc.project.co_no,
            mat_code__iexact=pcc.cost_category.mat_code.strip()
        )
        po_actual_amount = sum(Decimal(str(entry.po_value_inr)) for entry in po_entries)

        response_data = {
            "actual_override": pcc.actual_override,
            "po_actual_amount": float(po_actual_amount),
        }

        if not pcc.actual_override:
            # No override ? PO is the truth
            response_data.update({
                "detail": "No manual override active. Using PO actual amount.",
                "current_total_actuals": float(po_actual_amount),
            })
            return Response(response_data, status=status.HTTP_200_OK)

        # Override is active ? try to get manual adjustment
        latest_adjustment = pcc.rk_actual_adjustments.order_by('-adjusted_at').first()

        if latest_adjustment:
            # We have manual lines ? use them
            total_manual = sum(line.amount for line in latest_adjustment.lines.all())
            lines = [
                {"description": line.description, "amount": float(line.amount)}
                for line in latest_adjustment.lines.all()
            ]

            response_data.update({
                "detail": "Manual override active. Using manual total (PO shown for reference).",
                "current_total_actuals": float(total_manual),
                "adjustment": {
                    "id": latest_adjustment.id,
                    "note": latest_adjustment.note,
                    "adjusted_by": latest_adjustment.adjusted_by.username if latest_adjustment.adjusted_by else None,
                    "adjusted_at": latest_adjustment.adjusted_at.isoformat(),
                    "lines": lines
                }
            })
        else:
            # Flag is True, but no record yet ? fallback to PO
            response_data.update({
                "detail": "Override flag is set, but no manual adjustment record found yet. Falling back to PO actual amount.",
                "current_total_actuals": float(po_actual_amount),
            })

        return Response(response_data, status=status.HTTP_200_OK)


class AssemblyActualOverrideView(APIView):
    """
    PATCH: Update or create manual actual override for Assembly Services category
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        pcc = get_object_or_404(ProjectCostCategory, pk=pk)
        
        # Validate it's Assembly Services
        if pcc.cost_category.code != 'ASSEMBLY SERVICES':  
            return Response(
                {"detail": "This endpoint is only for Assembly Services category."},
                status=status.HTTP_400_BAD_REQUEST
            )

        note = request.data.get('note')
        lines = request.data.get('lines', [])

        if not note:
            return Response({"detail": "Note is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not lines or len(lines) == 0:
            return Response(
                {"detail": "At least one line with description and amount is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # Get the latest adjustment or create new
            adjustment = pcc.assembly_actual_adjustments.order_by('-adjusted_at').first()
            
            if adjustment:
                # Update existing adjustment
                adjustment.note = note
                adjustment.adjusted_by = request.user
                adjustment.adjusted_at = timezone.now()
                adjustment.save()
                
                # Delete old lines (full replacement)
                adjustment.lines.all().delete()
            else:
                # Create new adjustment
                adjustment = AssemblyActualAdjustment.objects.create(
                    project_cost_category=pcc,
                    adjusted_by=request.user,
                    note=note
                )

            # Add all new lines from request
            total_amount = Decimal('0')
            for line in lines:
                amount = Decimal(str(line.get('amount', '0')))
                # if amount <= 0:
                #     return Response(
                #         {"detail": "Each line must have positive amount."},
                #         status=status.HTTP_400_BAD_REQUEST
                #     )
                
                AssemblyActualAdjustmentLine.objects.create(
                    adjustment=adjustment,
                    description=line.get('description', ''),
                    amount=amount
                )
                total_amount += amount

            # Activate override flag
            pcc.actual_override = True
            pcc.save()

        # Regenerate the latest snapshot to reflect changes immediately
        latest_snapshot = pcc.project.psr_snapshots.order_by('-snapshot_date').first()
        if latest_snapshot:
            call_command(
                'generate_psr_snapshot',
                str(pcc.project.co_no),
                '--date',
                latest_snapshot.snapshot_date.strftime('%Y-%m-%d')
            )

        serializer = AssemblyActualAdjustmentSerializer(adjustment)
        return Response({
            "detail": "Assembly Services actuals updated successfully",
            "current_total_actuals": float(total_amount),
            "adjustment": serializer.data
        }, status=status.HTTP_200_OK)


class AssemblyGetActualOverrideView(APIView):
    """
    GET: Retrieve current manual actual override status for Assembly Services
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        pcc = get_object_or_404(ProjectCostCategory, pk=pk)

        if pcc.cost_category.code != 'ASSEMBLY SERVICES':
            return Response(
                {"detail": "This endpoint is only for Assembly Services category."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate current PO actual
        po_entries = POData.objects.filter(
            co_no__startswith=pcc.project.co_no,
            mat_code__iexact=pcc.cost_category.mat_code.strip()
        )
        po_actual_amount = sum(Decimal(str(entry.po_value_inr)) for entry in po_entries)

        response_data = {
            "actual_override": pcc.actual_override,
            "po_actual_amount": float(po_actual_amount),
        }

        if not pcc.actual_override:
            # No override ? PO is the truth
            response_data.update({
                "detail": "No manual override active. Using PO actual amount.",
                "current_total_actuals": float(po_actual_amount),
            })
            return Response(response_data, status=status.HTTP_200_OK)

        # Override is active ? try to get manual adjustment
        latest_adjustment = pcc.assembly_actual_adjustments.order_by('-adjusted_at').first()

        if latest_adjustment:
            # We have manual lines ? use them
            total_manual = sum(line.amount for line in latest_adjustment.lines.all())
            lines = [
                {"description": line.description, "amount": float(line.amount)}
                for line in latest_adjustment.lines.all()
            ]

            response_data.update({
                "detail": "Manual override active. Using manual total (PO shown for reference).",
                "current_total_actuals": float(total_manual),
                "adjustment": {
                    "id": latest_adjustment.id,
                    "note": latest_adjustment.note,
                    "adjusted_by": latest_adjustment.adjusted_by.username if latest_adjustment.adjusted_by else None,
                    "adjusted_at": latest_adjustment.adjusted_at.isoformat(),
                    "lines": lines
                }
            })
        else:
            # Flag is True, but no record yet ? fallback to PO
            response_data.update({
                "detail": "Override flag is set, but no manual adjustment record found yet. Falling back to PO actual amount.",
                "current_total_actuals": float(po_actual_amount),
            })

        return Response(response_data, status=status.HTTP_200_OK)


class FVActualOverrideView(APIView):
    """
    PATCH: Update or create manual actual override for F+V category
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        pcc = get_object_or_404(ProjectCostCategory, pk=pk)
        
        # Validate it's F+V
        if pcc.cost_category.code != 'F+V':
            return Response(
                {"detail": "This endpoint is only for F+V category."},
                status=status.HTTP_400_BAD_REQUEST
            )

        note = request.data.get('note')
        lines = request.data.get('lines', [])

        if not note:
            return Response({"detail": "Note is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not lines or len(lines) == 0:
            return Response(
                {"detail": "At least one line with description and amount is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # Get the latest adjustment or create new
            adjustment = pcc.fv_actual_adjustments.order_by('-adjusted_at').first()
            
            if adjustment:
                # Update existing adjustment
                adjustment.note = note
                adjustment.adjusted_by = request.user
                adjustment.adjusted_at = timezone.now()
                adjustment.save()
                
                # Delete old lines (full replacement)
                adjustment.lines.all().delete()
            else:
                # Create new adjustment
                adjustment = FVActualAdjustment.objects.create(
                    project_cost_category=pcc,
                    adjusted_by=request.user,
                    note=note
                )

            # Add all new lines from request
            total_amount = Decimal('0')
            for line in lines:
                amount = Decimal(str(line.get('amount', '0')))
                # if amount <= 0:
                #     return Response(
                #         {"detail": "Each line must have positive amount."},
                #         status=status.HTTP_400_BAD_REQUEST
                #     )
                
                FVActualAdjustmentLine.objects.create(
                    adjustment=adjustment,
                    description=line.get('description', ''),
                    amount=amount
                )
                total_amount += amount

            # Activate override flag
            pcc.actual_override = True
            pcc.save()

        # Regenerate the latest snapshot
        latest_snapshot = pcc.project.psr_snapshots.order_by('-snapshot_date').first()
        if latest_snapshot:
            call_command(
                'generate_psr_snapshot',
                str(pcc.project.co_no),
                '--date',
                latest_snapshot.snapshot_date.strftime('%Y-%m-%d')
            )

        serializer = FVActualAdjustmentSerializer(adjustment)
        return Response({
            "detail": "F+V actuals updated successfully",
            "current_total_actuals": float(total_amount),
            "adjustment": serializer.data
        }, status=status.HTTP_200_OK)


class FVGetActualOverrideView(APIView):
    """
    GET: Retrieve current manual actual override status for F+V
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        pcc = get_object_or_404(ProjectCostCategory, pk=pk)

        if pcc.cost_category.code != 'F+V':
            return Response(
                {"detail": "This endpoint is only for F+V category."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate current PO actual
        po_entries = POData.objects.filter(
            co_no__startswith=pcc.project.co_no,
            mat_code__iexact=pcc.cost_category.mat_code.strip()
        )
        po_actual_amount = sum(Decimal(str(entry.po_value_inr)) for entry in po_entries)

        response_data = {
            "actual_override": pcc.actual_override,
            "po_actual_amount": float(po_actual_amount),
        }

        if not pcc.actual_override:
            response_data.update({
                "detail": "No manual override active. Using PO actual amount.",
                "current_total_actuals": float(po_actual_amount),
            })
            return Response(response_data, status=status.HTTP_200_OK)

        # Override is active ? try to get manual adjustment
        latest_adjustment = pcc.fv_actual_adjustments.order_by('-adjusted_at').first()

        if latest_adjustment:
            total_manual = sum(line.amount for line in latest_adjustment.lines.all())
            lines = [
                {"description": line.description, "amount": float(line.amount)}
                for line in latest_adjustment.lines.all()
            ]

            response_data.update({
                "detail": "Manual override active. Using manual total (PO shown for reference).",
                "current_total_actuals": float(total_manual),
                "adjustment": {
                    "id": latest_adjustment.id,
                    "note": latest_adjustment.note,
                    "adjusted_by": latest_adjustment.adjusted_by.username if latest_adjustment.adjusted_by else None,
                    "adjusted_at": latest_adjustment.adjusted_at.isoformat(),
                    "lines": lines
                }
            })
        else:
            response_data.update({
                "detail": "Override flag is set, but no manual adjustment record found yet. Falling back to PO actual amount.",
                "current_total_actuals": float(po_actual_amount),
            })

        return Response(response_data, status=status.HTTP_200_OK)


class SOKOActualOverrideView(APIView):
    """
    PATCH: Update or create manual actual override for SOKO category
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        pcc = get_object_or_404(ProjectCostCategory, pk=pk)
        
        # Validate it's SOKO
        if pcc.cost_category.code != 'SOKO':
            return Response(
                {"detail": "This endpoint is only for SOKO category."},
                status=status.HTTP_400_BAD_REQUEST
            )

        note = request.data.get('note')
        lines = request.data.get('lines', [])

        if not note:
            return Response({"detail": "Note is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not lines or len(lines) == 0:
            return Response(
                {"detail": "At least one line with description and amount is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # Get the latest adjustment or create new
            adjustment = pcc.soko_actual_adjustments.order_by('-adjusted_at').first()
            
            if adjustment:
                # Update existing adjustment
                adjustment.note = note
                adjustment.adjusted_by = request.user
                adjustment.adjusted_at = timezone.now()
                adjustment.save()
                
                # Delete old lines (full replacement)
                adjustment.lines.all().delete()
            else:
                # Create new adjustment
                adjustment = SOKOActualAdjustment.objects.create(
                    project_cost_category=pcc,
                    adjusted_by=request.user,
                    note=note
                )

            # Add all new lines from request
            total_amount = Decimal('0')
            for line in lines:
                amount = Decimal(str(line.get('amount', '0')))
                # if amount <= 0:
                #     return Response(
                #         {"detail": "Each line must have positive amount."},
                #         status=status.HTTP_400_BAD_REQUEST
                #     )
                
                SOKOActualAdjustmentLine.objects.create(
                    adjustment=adjustment,
                    description=line.get('description', ''),
                    amount=amount
                )
                total_amount += amount

            # Activate override flag
            pcc.actual_override = True
            pcc.save()

        # Regenerate the latest snapshot
        latest_snapshot = pcc.project.psr_snapshots.order_by('-snapshot_date').first()
        if latest_snapshot:
            call_command(
                'generate_psr_snapshot',
                str(pcc.project.co_no),
                '--date',
                latest_snapshot.snapshot_date.strftime('%Y-%m-%d')
            )

        serializer = SOKOActualAdjustmentSerializer(adjustment)
        return Response({
            "detail": "SOKO actuals updated successfully",
            "current_total_actuals": float(total_amount),
            "adjustment": serializer.data
        }, status=status.HTTP_200_OK)


class SOKOGetActualOverrideView(APIView):
    """
    GET: Retrieve current manual actual override status for SOKO
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        pcc = get_object_or_404(ProjectCostCategory, pk=pk)

        if pcc.cost_category.code != 'SOKO':
            return Response(
                {"detail": "This endpoint is only for SOKO category."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate current PO actual
        po_entries = POData.objects.filter(
            co_no__startswith=pcc.project.co_no,
            mat_code__iexact=pcc.cost_category.mat_code.strip()
        )
        po_actual_amount = sum(Decimal(str(entry.po_value_inr)) for entry in po_entries)

        response_data = {
            "actual_override": pcc.actual_override,
            "po_actual_amount": float(po_actual_amount),
        }

        if not pcc.actual_override:
            response_data.update({
                "detail": "No manual override active. Using PO actual amount.",
                "current_total_actuals": float(po_actual_amount),
            })
            return Response(response_data, status=status.HTTP_200_OK)

        # Override is active ? try to get manual adjustment
        latest_adjustment = pcc.soko_actual_adjustments.order_by('-adjusted_at').first()

        if latest_adjustment:
            total_manual = sum(line.amount for line in latest_adjustment.lines.all())
            lines = [
                {"description": line.description, "amount": float(line.amount)}
                for line in latest_adjustment.lines.all()
            ]

            response_data.update({
                "detail": "Manual override active. Using manual total (PO shown for reference).",
                "current_total_actuals": float(total_manual),
                "adjustment": {
                    "id": latest_adjustment.id,
                    "note": latest_adjustment.note,
                    "adjusted_by": latest_adjustment.adjusted_by.username if latest_adjustment.adjusted_by else None,
                    "adjusted_at": latest_adjustment.adjusted_at.isoformat(),
                    "lines": lines
                }
            })
        else:
            response_data.update({
                "detail": "Override flag is set, but no manual adjustment record found yet. Falling back to PO actual amount.",
                "current_total_actuals": float(po_actual_amount),
            })

        return Response(response_data, status=status.HTTP_200_OK)


class MyPendingBudgetApprovalsView(APIView):
    def get(self, request):
        user = request.user
        is_approver = has_psr_permission(user, 'APPROVER')
        is_admin = has_psr_permission(user, 'ADMIN')

        if not (is_approver or is_admin):
            return Response({"detail": "Not authorized"}, status=403)

        if is_approver:
            # Show requests pending approvers where THIS user hasn't acted yet
            queryset = PSRBudgetChangeRequest.objects.filter(status='PENDING_APPROVERS') \
                .exclude(approval_actions__approver=user, approval_actions__action__isnull=False) \
                .order_by('-created_at')
        else:  # Admin
            queryset = PSRBudgetChangeRequest.objects.filter(status='PENDING_ADMIN') \
                .order_by('-created_at')

        serializer = PSRBudgetChangeRequestSerializer(queryset, many=True)
        return Response(serializer.data)


class MySubmittedBudgetRequestsView(APIView):
    def get(self, request):
        queryset = PSRBudgetChangeRequest.objects.filter(submitter=request.user) \
            .order_by('-created_at')
        serializer = PSRBudgetChangeRequestSerializer(queryset, many=True)
        return Response(serializer.data)


class PSRBudgetChangeRequestDetailView(APIView):
    def get(self, request, pk):
        request_obj = get_object_or_404(PSRBudgetChangeRequest, pk=pk)

        # Basic permission: submitter or involved in approval or admin
        if (request_obj.submitter != request.user and
            not request_obj.approval_actions.filter(approver=request.user).exists() and
            not has_psr_permission(request.user, 'ADMIN')):
            return Response({"detail": "Not authorized"}, status=403)

        serializer = PSRBudgetChangeRequestSerializer(request_obj)
        return Response(serializer.data)


class PSRBudgetChangeRequestActionView(APIView):
    def patch(self, request, pk):
        change_request = get_object_or_404(PSRBudgetChangeRequest, pk=pk)
        user = request.user

        action = request.data.get('action')
        comment = request.data.get('comment', '')

        if action not in ['APPROVE', 'REJECT']:
            return Response({"detail": "action must be APPROVE or REJECT"}, status=400)

        with transaction.atomic():
            # Determine current stage
            if change_request.status == 'PENDING_APPROVERS':
                if not has_psr_permission(user, 'APPROVER'):
                    return Response({"detail": "Only Approvers can act here"}, status=403)
                
                stage = 'APPROVER'
                
                # Check if this user already acted
                if change_request.approval_actions.filter(approver=user, stage=stage, action__isnull=False).exists():
                    return Response({"detail": "You have already acted on this request"}, status=400)

                # Create action
                PSRApprovalAction.objects.create(
                    request=change_request,
                    approver=user,
                    stage=stage,
                    action=action,
                    comment=comment
                )

                # Check if approver stage complete
                approvers_approved = change_request.approval_actions.filter(
                    stage='APPROVER', action='APPROVE'
                ).count()

                required = 2

                if approvers_approved >= required:
                    change_request.status = 'PENDING_ADMIN'
                    change_request.save()

            elif change_request.status == 'PENDING_ADMIN':
                stage = 'ADMIN'
                if not has_psr_permission(user, 'ADMIN'):
                    return Response({"detail": "Only Admin can act here"}, status=403)

                if change_request.approval_actions.filter(approver=user, stage=stage, action__isnull=False).exists():
                    return Response({"detail": "Admin already acted"}, status=400)

                PSRApprovalAction.objects.create(
                    request=change_request,
                    approver=user,
                    stage=stage,
                    action=action,
                    comment=comment
                )

                if action == 'APPROVE':
                    # Final apply
                    if change_request.sub_department:
                        sub_dept = change_request.sub_department
                        old_hours = sub_dept.budget_hours
                        sub_dept.budget_hours = change_request.proposed_budget_hours
                        # sub_dept.budget_cost = (sub_dept.budget_hours *
                        #                        sub_dept.department.hourly_rate *
                        #                        sub_dept.department.project.exchange_rate)

                        sub_dept.budget_cost = (sub_dept.budget_hours *
                                               sub_dept.department.hourly_rate)

                        sub_dept.save()

                        SubDepartmentBudgetAdjustment.objects.create(
                            sub_department=sub_dept,
                            adjusted_by=user,
                            note=change_request.note,
                            previous_budget_hours=old_hours,
                            new_budget_hours=sub_dept.budget_hours
                        )
                        self._regenerate_latest_snapshot(sub_dept.department.project)

                    elif change_request.project_cost_category:
                        pcc = change_request.project_cost_category
                        old_cost = pcc.budget_cost
                        pcc.budget_cost = change_request.proposed_budget_cost
                        pcc.save()

                        ProjectCostCategoryBudgetAdjustment.objects.create(
                            project_cost_category=pcc,
                            adjusted_by=user,
                            note=change_request.note,
                            previous_budget_cost=old_cost,
                            new_budget_cost=pcc.budget_cost
                        )
                        self._regenerate_latest_snapshot(pcc.project)

                    change_request.status = 'APPROVED'
                    change_request.save()

                else:
                    change_request.status = 'REJECTED'
                    change_request.save()

            else:
                return Response({"detail": "Request is not in a pending state"}, status=400)

        serializer = PSRBudgetChangeRequestSerializer(change_request)
        return Response(serializer.data)

    def _regenerate_latest_snapshot(self, project):
        latest = project.psr_snapshots.order_by('-snapshot_date').first()
        if latest:
            call_command(
                'generate_psr_snapshot',
                str(project.co_no),
                '--date',
                latest.snapshot_date.strftime('%Y-%m-%d')
            )


class UserDropdownView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserDropdownSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(is_active=True).order_by('first_name', 'last_name')


# GET (list) + POST (create) on the same endpoint
class ProjectPaymentsListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectPaymentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['id']
    ordering = ['id']

    def get_queryset(self):
        co_no = self.kwargs['co_no']
        return ProjectPayment.objects.filter(project__co_no=co_no)

    def perform_create(self, serializer):
        co_no = self.kwargs['co_no']
        project = get_object_or_404(PSRProject, co_no=co_no)
        serializer.save(project=project)


# PATCH (partial update) + GET detail + PUT (full update)
class ProjectPaymentDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProjectPaymentSerializer
    lookup_field = 'pk'  # Payment's primary key

    def get_queryset(self):
        co_no = self.kwargs['co_no']
        return ProjectPayment.objects.filter(project__co_no=co_no) \
                   .select_related('project')


class ProjectPaymentSummaryView(APIView):
    def get(self, request, co_no):
        project = get_object_or_404(PSRProject, co_no=co_no)

        aggregates = project.payments.aggregate(
            invoice_amount=Sum(
                'amount_in_foreign_curr',
                filter=Q(invoice_no__isnull=False) & ~Q(invoice_no='')
            ),
            received_po_amount=Sum('received_amount')
        )

        invoice_amount = aggregates['invoice_amount'] or 0
        received_po_amount = aggregates['received_po_amount'] or 0

        data = {
            "sales_value_foreign_curr": project.sales_value_foreign_curr,
            "invoice_amount": invoice_amount,
            "received_po_amount": received_po_amount,
            "balance_po_amount": invoice_amount - received_po_amount,
        }

        return Response(data)


class ProjectPaymentsGraphView(APIView):
    """
    New API endpoint for graph data (cumulative expected vs received amounts).
    URL example: /projects/<co_no>/payments/graph/
    Only GET is needed.
    """

    def get(self, request, co_no, *args, **kwargs):
        project = get_object_or_404(PSRProject, co_no=co_no)
        
        # Fetch all payments for the project once
        payments = ProjectPayment.objects.filter(project=project)

        # ============ Cumulative Expected ============
        expected_payments = payments.filter(expected_receive_date__isnull=False)\
                                   .order_by('expected_receive_date')
        
        expected_amount = {}
        cumulative_expected = Decimal('0.00')
        index_expected = 1
        prev_date = None
        daily_amount = Decimal('0.00')

        for pay in expected_payments:
            date_str = pay.expected_receive_date.strftime('%Y-%m-%d')
            amt = pay.amount_in_foreign_curr or Decimal('0.00')
            
            if date_str == prev_date:
                daily_amount += amt
            else:
                # Save previous day’s cumulative before moving to new date
                if prev_date is not None:
                    cumulative_expected += daily_amount
                    expected_amount[str(index_expected)] = {
                        "amount_in_foreign_curr": f"{cumulative_expected:.2f}",
                        "expected_receive_date": prev_date
                    }
                    index_expected += 1
                
                prev_date = date_str
                daily_amount = amt
        
        # Don't forget the last group
        if prev_date is not None:
            cumulative_expected += daily_amount
            expected_amount[str(index_expected)] = {
                "amount_in_foreign_curr": f"{cumulative_expected:.2f}",
                "expected_receive_date": prev_date
            }

        # ============ Cumulative Received ============
        received_payments = payments.filter(actual_receive_date__isnull=False)\
                                   .order_by('actual_receive_date')
        
        received_amount = {}
        cumulative_received = Decimal('0.00')
        index_received = 1
        prev_date_r = None
        daily_received = Decimal('0.00')

        for pay in received_payments:
            date_str = pay.actual_receive_date.strftime('%Y-%m-%d')
            amt = pay.received_amount or Decimal('0.00')
            
            if date_str == prev_date_r:
                daily_received += amt
            else:
                if prev_date_r is not None:
                    cumulative_received += daily_received
                    received_amount[str(index_received)] = {
                        "received_amount": f"{cumulative_received:.2f}",
                        "actual_receive_date": prev_date_r
                    }
                    index_received += 1
                
                prev_date_r = date_str
                daily_received = amt
        
        if prev_date_r is not None:
            cumulative_received += daily_received
            received_amount[str(index_received)] = {
                "received_amount": f"{cumulative_received:.2f}",
                "actual_receive_date": prev_date_r
            }

        # Final response structure (following your example format and spelling)
        data = {
            "expected-amount": expected_amount,
            "recieved-amount": received_amount
        }

        return Response(data)









# ============== Forecast Approval Process =============#
# If Abhijeet sir requests to implement the Forecast Approval Process, 
# just replace the above APIs with the below ones 

# APIs to be swapped: SubDepartmentForecastOverrideView, ProjectCostCategoryForecastOverrideView

# APIs have been tested thoroughly and had been implemented in the frontend earlier.
# Made some slight changes in the Angular code 

# Apps: my-pending-req, my-submitted-req

# swapped the endpoints from
# forecast-override-requests ---> budget-change-requests

# Just uncomment the commented serializers, urls and the 
# below APIs for implementing the Approval process for reimplementing it.

# models.py and admin.py remains the same without any changes.

"""
class ProjectCostCategoryForecastOverrideView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        pcc = get_object_or_404(ProjectCostCategory, pk=pk)
        user = request.user

        note = request.data.get('note', '').strip()
        lines_data = request.data.get('lines', [])

        if not note:
            return Response({"detail": "Note (reason) is required."}, status=400)

        if not lines_data or not isinstance(lines_data, list):
            return Response({"detail": "Lines list is required."}, status=400)
\
        is_admin = has_psr_permission(user, 'ADMIN')

        if is_admin:
            # -- Direct override for Admin --
            total_amount = Decimal('0')
            for line in lines_data:
                amount_str = line.get('amount')
                if amount_str is None:
                    return Response({"detail": "Each line must have 'amount'."}, status=400)
                amount = Decimal(str(amount_str))
                total_amount += amount


            with transaction.atomic():
                previous_forecast = pcc.forecast_cost

                pcc.forecast_override = True
                pcc.forecast_cost = total_amount
                pcc.forecast_overridden_by = user
                pcc.forecast_overridden_at = timezone.now()
                pcc.save()

                adjustment = MaterialForecastAdjustment.objects.create(
                    project_cost_category=pcc,
                    adjusted_by=user,
                    note=note,
                    previous_forecast_cost=previous_forecast,
                    new_forecast_cost=total_amount
                )

                for line in lines_data:
                    MaterialForecastAdjustmentLine.objects.create(
                        adjustment=adjustment,
                        description=line['description'],
                        amount=Decimal(str(line['amount']))
                    )

            # Regenerate snapshot
            project = pcc.project
            latest_snapshot = project.psr_snapshots.order_by('-snapshot_date').first()
            snapshot_date = None
            if latest_snapshot:
                call_command(
                    'generate_psr_snapshot',
                    str(project.co_no),
                    '--date',
                    latest_snapshot.snapshot_date.strftime('%Y-%m-%d')
                )
                snapshot_date = latest_snapshot.snapshot_date.strftime('%Y-%m-%d')

            return Response({
                "detail": "Material forecast override applied successfully (Admin direct).",
                "total_forecast_cost": float(total_amount),
                "adjustment_id": adjustment.id,
                "snapshot_regenerated": snapshot_date
            }, status=200)

        else:
            # -- Preparer / Approver ? create request --
            if not (has_psr_permission(user, 'PREPARER') or has_psr_permission(user, 'APPROVER')):
                return Response({"detail": "You are not authorized to request forecast overrides in PSR."}, status=403)

            # Prevent duplicate pending forecast requests
            if PSRForecastChangeRequest.objects.filter(
                project_cost_category=pcc,
                status__in=['PENDING_APPROVERS', 'PENDING_ADMIN']
            ).exists():
                return Response(
                    {"detail": "A forecast override request is already pending for this cost category."},
                    status=409
                )

            # Validate using serializer
            serializer = PSRForecastChangeRequestCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Create request
            request_obj = serializer.save(
                submitter=user,
                status='PENDING_APPROVERS'
            )

            return Response({
                "detail": "Forecast override request submitted successfully. Awaiting approval.",
                "request_id": request_obj.id,
                "status": request_obj.status,
                "proposed_forecast_cost": float(request_obj.proposed_forecast_cost),
                "target": str(pcc)
            }, status=201)







class SubDepartmentForecastOverrideView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        sub_dept = get_object_or_404(PSRSubDepartment, pk=pk)
        user = request.user

        note = request.data.get('note', '').strip()
        lines_data = request.data.get('lines', [])

        if not note:
            return Response({"detail": "Note (reason) is required for forecast override."}, status=400)

        if not lines_data or not isinstance(lines_data, list):
            return Response({"detail": "Lines (list of description + hours) is required."}, status=400)

        is_admin = has_psr_permission(user, 'ADMIN')

        if is_admin:
            # -- Direct override for Admin --
            total_hours = Decimal('0')
            for line in lines_data:
                hours_str = line.get('hours')
                if hours_str is None:
                    return Response({"detail": "Each line must have 'hours'."}, status=400)
                hours = Decimal(str(hours_str))
                total_hours += hours

            with transaction.atomic():
                previous_forecast = sub_dept.forecast_hours

                sub_dept.forecast_override = True
                sub_dept.forecast_hours = total_hours
                dept = sub_dept.department
                project = dept.project
                # sub_dept.forecast_cost = total_hours * dept.hourly_rate * project.exchange_rate
                sub_dept.forecast_cost = total_hours * dept.hourly_rate
                sub_dept.forecast_overridden_by = user
                sub_dept.forecast_overridden_at = timezone.now()
                sub_dept.save()

                adjustment = ForecastAdjustment.objects.create(
                    sub_department=sub_dept,
                    adjusted_by=user,
                    note=note,
                    previous_forecast_hours=previous_forecast,
                    new_forecast_hours=total_hours
                )

                for line in lines_data:
                    ForecastAdjustmentLine.objects.create(
                        adjustment=adjustment,
                        description=line['description'],
                        hours=Decimal(str(line['hours']))
                    )

            # Regenerate snapshot
            project = sub_dept.department.project
            latest_snapshot = project.psr_snapshots.order_by('-snapshot_date').first()
            snapshot_date = None
            if latest_snapshot:
                call_command(
                    'generate_psr_snapshot',
                    str(project.co_no),
                    '--date',
                    latest_snapshot.snapshot_date.strftime('%Y-%m-%d')
                )
                snapshot_date = latest_snapshot.snapshot_date.strftime('%Y-%m-%d')

            return Response({
                "detail": "Forecast override applied successfully (Admin direct).",
                "warning": "Manual forecast override is now active.",
                "total_forecast_hours": float(total_hours),
                "adjustment_id": adjustment.id,
                "snapshot_regenerated": snapshot_date
            }, status=200)

        else:
            # -- Preparer / Approver ? create request --
            if not (has_psr_permission(user, 'PREPARER') or has_psr_permission(user, 'APPROVER')):
                return Response({"detail": "You are not authorized to request forecast overrides in PSR."}, status=403)

            # Prevent duplicate pending forecast requests
            if PSRForecastChangeRequest.objects.filter(
                sub_department=sub_dept,
                status__in=['PENDING_APPROVERS', 'PENDING_ADMIN']
            ).exists():
                return Response(
                    {"detail": "A forecast override request is already pending for this sub-department."},
                    status=409
                )

            # Validate using serializer
            serializer = PSRForecastChangeRequestCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Create request
            request_obj = serializer.save(
                submitter=user,
                status='PENDING_APPROVERS'
            )

            return Response({
                "detail": "Forecast override request submitted successfully. Awaiting approval.",
                "request_id": request_obj.id,
                "status": request_obj.status,
                "proposed_forecast_hours": float(request_obj.proposed_forecast_hours),
                "target": str(sub_dept)
            }, status=201)

"""




# class MyPendingForecastApprovalsView(APIView):
#     def get(self, request):
#         user = request.user
#         is_approver = has_psr_permission(user, 'APPROVER')
#         is_admin = has_psr_permission(user, 'ADMIN')

#         if not (is_approver or is_admin):
#             return Response({"detail": "Not authorized"}, status=403)

#         if is_approver:
#             # Show forecast requests pending approvers where THIS user hasn't acted yet
#             queryset = PSRForecastChangeRequest.objects.filter(status='PENDING_APPROVERS') \
#                 .exclude(approval_actions__approver=user, approval_actions__action__isnull=False) \
#                 .order_by('-created_at')
#         else:  # Admin
#             queryset = PSRForecastChangeRequest.objects.filter(status='PENDING_ADMIN') \
#                 .order_by('-created_at')

#         serializer = PSRForecastChangeRequestSerializer(queryset, many=True)
#         return Response(serializer.data)





# class MySubmittedForecastRequestsView(APIView):
#     def get(self, request):
#         queryset = PSRForecastChangeRequest.objects.filter(submitter=request.user) \
#             .order_by('-created_at')
#         serializer = PSRForecastChangeRequestSerializer(queryset, many=True)
#         return Response(serializer.data)




# class PSRForecastChangeRequestDetailView(APIView):
#     def get(self, request, pk):
#         request_obj = get_object_or_404(PSRForecastChangeRequest, pk=pk)

#         # Permission: submitter or someone who has acted on it or admin
#         if (request_obj.submitter != request.user and
#             not request_obj.approval_actions.filter(approver=request.user).exists() and
#             not has_psr_permission(request.user, 'ADMIN')):
#             return Response({"detail": "Not authorized"}, status=403)

#         serializer = PSRForecastChangeRequestSerializer(request_obj)
#         return Response(serializer.data)




# class PSRForecastChangeRequestActionView(APIView):
#     def patch(self, request, pk):
#         change_request = get_object_or_404(PSRForecastChangeRequest, pk=pk)
#         user = request.user

#         action = request.data.get('action')
#         comment = request.data.get('comment', '')

#         if action not in ['APPROVE', 'REJECT']:
#             return Response({"detail": "action must be APPROVE or REJECT"}, status=400)

#         with transaction.atomic():
#             if change_request.status == 'PENDING_APPROVERS':
#                 stage = 'APPROVER'
#                 if change_request.approval_actions.filter(approver=user, stage=stage, action__isnull=False).exists():
#                     return Response({"detail": "You have already acted on this request"}, status=400)

#                 PSRForecastApprovalAction.objects.create(
#                     request=change_request,
#                     approver=user,
#                     stage=stage,
#                     action=action,
#                     comment=comment
#                 )

#                 approvers_approved = change_request.approval_actions.filter(
#                     stage='APPROVER', action='APPROVE'
#                 ).count()

#                 # Determine required number (simplified   adjust if needed)
#                 required = 2 if change_request.submitter != get_psr_approvers()[0] else 1

#                 if approvers_approved >= required:
#                     change_request.status = 'PENDING_ADMIN'
#                     change_request.save()

#             elif change_request.status == 'PENDING_ADMIN':
#                 stage = 'ADMIN'
#                 if not has_psr_permission(user, 'ADMIN'):
#                     return Response({"detail": "Only Admin can act here"}, status=403)

#                 if change_request.approval_actions.filter(approver=user, stage=stage, action__isnull=False).exists():
#                     return Response({"detail": "Admin already acted"}, status=400)

#                 PSRForecastApprovalAction.objects.create(
#                     request=change_request,
#                     approver=user,
#                     stage=stage,
#                     action=action,
#                     comment=comment
#                 )

#                 if action == 'APPROVE':
#                     # Final apply - forecast override
#                     if change_request.sub_department:
#                         sub_dept = change_request.sub_department
#                         previous_forecast = sub_dept.forecast_hours

#                         sub_dept.forecast_override = True
#                         sub_dept.forecast_hours = change_request.proposed_forecast_hours
#                         dept = sub_dept.department
#                         project = dept.project
#                         # sub_dept.forecast_cost = (
#                         #     change_request.proposed_forecast_hours
#                         #     * dept.hourly_rate
#                         #     * project.exchange_rate
#                         # )
                        
#                         sub_dept.forecast_cost = (
#                             change_request.proposed_forecast_hours
#                             * dept.hourly_rate
#                         )
                        
#                         sub_dept.forecast_overridden_by = user
#                         sub_dept.forecast_overridden_at = timezone.now()
#                         sub_dept.save()

#                         adjustment = ForecastAdjustment.objects.create(
#                             sub_department=sub_dept,
#                             adjusted_by=user,
#                             note=change_request.note,
#                             previous_forecast_hours=previous_forecast,
#                             new_forecast_hours=change_request.proposed_forecast_hours
#                         )

#                         # Create lines from request
#                         for req_line in change_request.lines.all():
#                             ForecastAdjustmentLine.objects.create(
#                                 adjustment=adjustment,
#                                 description=req_line.description,
#                                 hours=req_line.hours
#                             )

#                         self._regenerate_latest_snapshot(project)

#                     elif change_request.project_cost_category:
#                         pcc = change_request.project_cost_category
#                         previous_forecast = pcc.forecast_cost

#                         pcc.forecast_override = True
#                         pcc.forecast_cost = change_request.proposed_forecast_cost
#                         pcc.forecast_overridden_by = user
#                         pcc.forecast_overridden_at = timezone.now()
#                         pcc.save()

#                         adjustment = MaterialForecastAdjustment.objects.create(
#                             project_cost_category=pcc,
#                             adjusted_by=user,
#                             note=change_request.note,
#                             previous_forecast_cost=previous_forecast,
#                             new_forecast_cost=change_request.proposed_forecast_cost
#                         )

#                         for req_line in change_request.lines.all():
#                             MaterialForecastAdjustmentLine.objects.create(
#                                 adjustment=adjustment,
#                                 description=req_line.description,
#                                 amount=req_line.amount
#                             )

#                         self._regenerate_latest_snapshot(pcc.project)

#                     change_request.status = 'APPROVED'
#                     change_request.save()

#                 else:
#                     change_request.status = 'REJECTED'
#                     change_request.save()

#             else:
#                 return Response({"detail": "Request is not in a pending state"}, status=400)

#         serializer = PSRForecastChangeRequestSerializer(change_request)
#         return Response(serializer.data)

#     def _regenerate_latest_snapshot(self, project):
#         latest = project.psr_snapshots.order_by('-snapshot_date').first()
#         if latest:
#             call_command(
#                 'generate_psr_snapshot',
#                 str(project.co_no),
#                 '--date',
#                 latest.snapshot_date.strftime('%Y-%m-%d')
#             )


from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class PSRProjectCreationWorkflowView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """
        Handles:
        1. List pending requests for Approvers/Admins
        2. List user's own submitted requests
        3. Get Detail of a single request
        """
        user = request.user
        
        # Detail View
        if pk:
            request_obj = get_object_or_404(PSRProjectCreationRequest, pk=pk)
            return Response(PSRProjectCreationRequestSerializer(request_obj).data)

        # Filtering logic
        view_type = request.query_params.get('view', 'pending')
        
        if view_type == 'submitted':
            queryset = PSRProjectCreationRequest.objects.filter(submitter=user)
        else:
            # Default to "My Inbox" (Pending actions)
            if has_psr_permission(user, "APPROVER"):
                queryset = PSRProjectCreationRequest.objects.filter(
                    status="PENDING_APPROVERS",
                    approval_actions__approver=user,
                    approval_actions__action__isnull=True,
                    approval_actions__stage="APPROVER"
                ).distinct()
            elif has_psr_permission(user, "ADMIN"):
                queryset = PSRProjectCreationRequest.objects.filter(
                    status="PENDING_ADMIN",
                    approval_actions__approver=user,
                    approval_actions__action__isnull=True,
                    approval_actions__stage="ADMIN"
                ).distinct()
            else:
                queryset = PSRProjectCreationRequest.objects.none()

        serializer = PSRProjectCreationRequestSerializer(queryset, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def patch(self, request, pk):
        """Processes Approval/Rejection"""
        creation_request = get_object_or_404(PSRProjectCreationRequest, pk=pk)
        action = request.data.get("action")
        comment = request.data.get("comment", "")

        if action not in ["APPROVE", "REJECT"]:
            return Response({"detail": "Invalid action."}, status=400)

        # Logic Mapping to reduce nested IFs
        handlers = {
            "PENDING_APPROVERS": self._handle_approver_stage,
            "PENDING_ADMIN": self._handle_admin_stage,
        }

        handler = handlers.get(creation_request.status)
        if handler:
            print(f"DEBUG: Current Status is '{creation_request.status}', triggering handler: {handler.__name__}")
        else:
            print(f"DEBUG: No handler found for status: '{creation_request.status}'")
            return Response({"detail": "Request not in a pending state."}, status=400)
        # if not handler:
        #     return Response({"detail": "Request not in a pending state."}, status=400)

        return handler(request, creation_request, action, comment)

    def _handle_approver_stage(self, request, creation_request, action, comment):
        if not has_psr_permission(request.user, "APPROVER"):
            return Response({"detail": "Forbidden"}, status=403)

        # Update action
        updated = PSRProjectApprovalAction.objects.filter(
            request=creation_request, approver=request.user, stage="APPROVER", action__isnull=True
        ).update(action=action, comment=comment, timestamp=timezone.now())

        if not updated:
            return Response({"detail": "Already acted or not assigned."}, status=400)

        if action == "REJECT":
            self._set_final_status(creation_request, "REJECTED")
        else:
            # Check threshold
            required = 1 if has_psr_permission(creation_request.submitter, "APPROVER") else 2
            approvals = creation_request.approval_actions.filter(stage="APPROVER", action="APPROVE").count()
            
            if approvals >= required:
                creation_request.status = "PENDING_ADMIN"
                creation_request.save()

        return Response(PSRProjectCreationRequestSerializer(creation_request).data)


    
    def _handle_admin_stage(self, request, creation_request, action, comment):
        if not has_psr_permission(request.user, "ADMIN"):
            return Response({"detail": "Forbidden"}, status=403)

        # 1. Update the approval action
        PSRProjectApprovalAction.objects.filter(
            request=creation_request, approver=request.user, stage="ADMIN"
        ).update(action=action, comment=comment, timestamp=timezone.now())

        if action == "REJECT":
            self._set_final_status(creation_request, "REJECTED")
        else:
            self._set_final_status(creation_request, "APPROVED")
            
            # --- SYNC DATA ---
            from .views import ProjectUpdateView 
            project_instance = creation_request.project
            
            if project_instance:
                updater = ProjectUpdateView()
                
                # ✅ STEP 1: Update main fields (Name, Manager, etc.)
                updater._apply_project_updates(project_instance, creation_request.data)
                
                # ✅ STEP 2: Update budgets & Trigger Snapshot (The missing link!)
                # This call contains the 'call_command("generate_psr_snapshot")' logic
                updater._apply_component_updates(project_instance, creation_request.data)
                
                # Refresh to ensure calculations are updated
                project_instance.refresh_from_db()
            
            # 2. If it was a brand new project with no components, create them
            if not project_instance.departments.exists():
                from .views import ProjectCreateView
                ProjectCreateView()._create_project_components(project_instance, creation_request.data)

        return Response(PSRProjectCreationRequestSerializer(creation_request).data)

    def _set_final_status(self, creation_request, status_val):
        creation_request.status = status_val
        creation_request.save()
        
        # If you don't have a 'status' field in PSRProject, 
        # just remove the project.status lines below.
        # project = creation_request.project
        # project.save()



import matplotlib
matplotlib.use('Agg') # Prevents GUI/Tkinter errors
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import matplotlib.pyplot as plt
import pandas as pd
from django.template.loader import render_to_string
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# REPLACED: from weasyprint import HTML
from xhtml2pdf import pisa 
import json
import base64
import requests
import urllib.parse
import matplotlib
matplotlib.use('Agg') # Important: Must be before pyplot
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch  # <--- THIS IS THE MISSING LINE
import numpy as np
import io
import base64
class ProcurementSummaryView(APIView):
    
    def get_combined_data(self, request, co_no):
        target_date = request.query_params.get('date')
        if not target_date:
            raise ValueError("Query parameter 'date' is required.")

        # 1. Setup the request object with the date in GET params
        raw_request = request._request
        query_dict = raw_request.GET.copy()
        query_dict['date'] = target_date
        raw_request.GET = query_dict

        # 2. Call each view with ONLY the arguments they expect in their URL path
        # If the URL pattern is '.../<str:co_no>/', only pass co_no.
        # If the Snapshot view pattern is '.../<str:co_no>/<str:snapshot_date>/', pass both.
        
        details_resp = ProjectKPIDetailsView.as_view()(raw_request, co_no=co_no)
        
        history_resp = ProjectSnapshotCostToGoHistoryView.as_view()(raw_request, co_no=co_no)
        
        # This one likely expects the date in the path based on your API URL
        # /psr/api/projects/30747/snapshot/cost-to-go/2023-11-01/
        snapshot_resp = ProjectPSRSnapshotCostToGoView.as_view()(
            raw_request, 
            co_no=co_no, 
            snapshot_date=target_date  # Only pass it here
        )

        return {
            "project_details": details_resp.data,
            "cost_to_go_history": history_resp.data,
            "snapshot_at_date": snapshot_resp.data
        }



    def generate_beautiful_matplotlib(self, history_data):
        try:
            # 1. Data Prep
            history_list = history_data.get('cost_to_go_history', [])
            if not history_list:
                return None

            labels = [item.get('month', '') for item in history_list]
            budget = [item.get('budget_cost', 0) / 1000000 for item in history_list]
            actual = [item.get('actual_cost', 0) / 1000000 for item in history_list]
            forecast = [item.get('forecast_cost', 0) / 1000000 for item in history_list]
            prognosis = [item.get('prognosis_cost', 0) / 1000000 for item in history_list]

            # 2. Layout Setup - Optimized for Half-Page Box
            x = np.arange(len(labels))
            width = 0.18  # Increased width slightly so bars aren't invisible in smaller size
            
            colors = ['#163079', '#00A0F5', '#00E3E3', '#000000']
            data_sets = [budget, actual, forecast, prognosis]
            names = ['Budget', 'Actual', 'Forecast', 'Prognosis']

            # Change: Use a boxier aspect ratio (8x5 or 10x6) for half-page fitting
            # fig, ax = plt.subplots(figsize=(10, 6), dpi=100) 
            fig, ax = plt.subplots(figsize=(14, 4), dpi=100)            
            # 3. Plotting with Rounded Ends
            for i, data in enumerate(data_sets):
                offset = (i - 1.5) * (width + 0.02)
                bars = ax.bar(x + offset, data, width, label=names[i], color=colors[i], zorder=3)
                
                for bar in bars:
                    height = bar.get_height()
                    if height <= 0: continue # Avoid drawing invisible rounded caps
                    
                    bbox = FancyBboxPatch(
                        (bar.get_x(), 0), bar.get_width(), height,
                        # Change: Smaller rounding_size looks better on smaller charts
                        boxstyle="round,pad=0,rounding_size=0.1", 
                        ec="none", fc=colors[i], zorder=3
                    )
                    ax.add_patch(bbox)
                bars.remove()

            # 4. Styling
            ax.set_facecolor('white')
            ax.set_ylabel('₹ Millions', color='#6c757d', fontsize=11, fontweight='bold')
            
            ax.yaxis.grid(True, linestyle=(0, (5, 5)), color='#e9ecef', zorder=0)
            ax.xaxis.grid(False)
            
            for spine in ['top', 'right', 'left']:
                ax.spines[spine].set_visible(False)
            ax.spines['bottom'].set_color('#e9ecef')

            ax.set_xticks(x)
            ax.set_xticklabels(labels, color='#6c757d', fontsize=10) # Slightly larger font for readability
            
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f'₹{int(x)}M'))
            
            # Legend: Moved slightly up to save vertical space
            ax.legend(
                loc='upper center', bbox_to_anchor=(0.5, -0.18),
                ncol=4, frameon=False, handletextpad=0.5,
                handlelength=1.0, fontsize=10
            )

            # Change: Tighter rect to ensure it fits the half-page container without waste
            plt.tight_layout(rect=[0, 0, 1, 1])
            # 5. Convert to Base64
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
            plt.close(fig)
            return base64.b64encode(buf.getvalue()).decode('utf-8')

        except Exception as e:
            print(f"Matplotlib Error: {e}")
            return None

    def get(self, request, co_no, *args, **kwargs):
        try:
            data = self.get_combined_data(request, co_no) 
            graph_base64 = self.generate_beautiful_matplotlib(data['cost_to_go_history']) # USE THIS
            returned_date = data['snapshot_at_date'].get('snapshot_date')
            print(f"DEBUG: Requested Date: {request.query_params.get('date')}")
            print(f"DEBUG: API Returned Date: {returned_date}")

            if str(returned_date) != str(request.query_params.get('date')):
                print("WARNING: Data mismatch! The API is returning a different date.")
            # Extracting the source dictionary
            snapshot_data = data['snapshot_at_date']['cost_to_go']['COST']

            # Enriching the dict with the calculated difference
            for key, val in snapshot_data.items():
                val['actual_difference'] = val.get('actuals', 0) - val.get('last_month_actuals', 0)

            # --- PRINT THE DICTIONARY TO CONSOLE ---
            # import json
            # print("\n--- DATA DICTIONARY FOR TEMPLATE ---")
            # # We use indent=4 to make it readable in your terminal
            # print(json.dumps(snapshot_data, indent=4))
            # print("-------------------------------------\n")

            context = {
                "details": data['project_details'],
                "snapshot": snapshot_data,
                "snapshot_date": data['snapshot_at_date']['snapshot_date'],
                "graph_image": graph_base64
            }
            
            html_string = render_to_string('procurement_report.html', context)
            result = io.BytesIO()
            pisa_status = pisa.CreatePDF(io.BytesIO(html_string.encode("UTF-8")), dest=result)
            
            if not pisa_status.err:
                response = HttpResponse(result.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = f'inline; filename="Procurement_Report_{co_no}.pdf"'
                return response
            
            return Response({"error": "PDF conversion error"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HoursCostSummaryView(APIView):
    
    def get_combined_data(self, request, co_no):
        target_date = request.query_params.get('date')
        if not target_date:
            return Response({"error": "Query parameter 'date' is required."}, status=400)

        # Use the existing request - don't manually override raw_request.GET 
        # unless ProjectKPIDetailsView specifically requires 'date' in the QueryParams.
        
        # 1. Project Details
        details_resp = ProjectKPIDetailsView.as_view()(request, co_no=co_no)
        
        # 2. History (The URL without the date in the path)
        history_resp = ProjectPSRSnapshotTimesheetView.as_view()(request, co_no=co_no)
        
        # 3. Snapshot at specific date (The URL WITH the date in the path)
        snapshot_resp = ProjectPSRSnapshotTimesheetView.as_view()(
            request, 
            co_no=co_no, 
            snapshot_date=target_date 
        )

        return Response({
            "project_details": details_resp.data,
            "cost_to_go_history": history_resp.data,
            "snapshot_at_date": snapshot_resp.data
        })



    def generate_beautiful_matplotlib(self, history_data):
        try:
            # 1. Data Prep
            history_list = history_data.get('cost_to_go_history', [])
            if not history_list:
                return None

            labels = [item.get('month', '') for item in history_list]
            budget = [item.get('budget_cost', 0) / 1000000 for item in history_list]
            actual = [item.get('actual_cost', 0) / 1000000 for item in history_list]
            forecast = [item.get('forecast_cost', 0) / 1000000 for item in history_list]
            prognosis = [item.get('prognosis_cost', 0) / 1000000 for item in history_list]

            # 2. Layout Setup - Optimized for Half-Page Box
            x = np.arange(len(labels))
            width = 0.18  # Increased width slightly so bars aren't invisible in smaller size
            
            colors = ['#163079', '#00A0F5', '#00E3E3', '#000000']
            data_sets = [budget, actual, forecast, prognosis]
            names = ['Budget', 'Actual', 'Forecast', 'Prognosis']

            # Change: Use a boxier aspect ratio (8x5 or 10x6) for half-page fitting
            # fig, ax = plt.subplots(figsize=(10, 6), dpi=100) 
            fig, ax = plt.subplots(figsize=(14, 4), dpi=100)            
            # 3. Plotting with Rounded Ends
            for i, data in enumerate(data_sets):
                offset = (i - 1.5) * (width + 0.02)
                bars = ax.bar(x + offset, data, width, label=names[i], color=colors[i], zorder=3)
                
                for bar in bars:
                    height = bar.get_height()
                    if height <= 0: continue # Avoid drawing invisible rounded caps
                    
                    bbox = FancyBboxPatch(
                        (bar.get_x(), 0), bar.get_width(), height,
                        # Change: Smaller rounding_size looks better on smaller charts
                        boxstyle="round,pad=0,rounding_size=0.1", 
                        ec="none", fc=colors[i], zorder=3
                    )
                    ax.add_patch(bbox)
                bars.remove()

            # 4. Styling
            ax.set_facecolor('white')
            ax.set_ylabel('₹ Millions', color='#6c757d', fontsize=11, fontweight='bold')
            
            ax.yaxis.grid(True, linestyle=(0, (5, 5)), color='#e9ecef', zorder=0)
            ax.xaxis.grid(False)
            
            for spine in ['top', 'right', 'left']:
                ax.spines[spine].set_visible(False)
            ax.spines['bottom'].set_color('#e9ecef')

            ax.set_xticks(x)
            ax.set_xticklabels(labels, color='#6c757d', fontsize=10) # Slightly larger font for readability
            
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f'₹{int(x)}M'))
            
            # Legend: Moved slightly up to save vertical space
            ax.legend(
                loc='upper center', bbox_to_anchor=(0.5, -0.18),
                ncol=4, frameon=False, handletextpad=0.5,
                handlelength=1.0, fontsize=10
            )

            # Change: Tighter rect to ensure it fits the half-page container without waste
            plt.tight_layout(rect=[0, 0, 1, 1])
            # 5. Convert to Base64
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
            plt.close(fig)
            return base64.b64encode(buf.getvalue()).decode('utf-8')

        except Exception as e:
            print(f"Matplotlib Error: {e}")
            return None

    def get(self, request, co_no, *args, **kwargs):
        try:
            data = self.get_combined_data(request, co_no) 
            graph_base64 = self.generate_beautiful_matplotlib(data['cost_to_go_history']) # USE THIS
            returned_date = data['snapshot_at_date'].get('snapshot_date')
            print(f"DEBUG: Requested Date: {request.query_params.get('date')}")
            print(f"DEBUG: API Returned Date: {returned_date}")

            if str(returned_date) != str(request.query_params.get('date')):
                print("WARNING: Data mismatch! The API is returning a different date.")
            # Extracting the source dictionary
            snapshot_data = data['snapshot_at_date']['cost_to_go']['COST']

            # Enriching the dict with the calculated difference
            for key, val in snapshot_data.items():
                val['actual_difference'] = val.get('actuals', 0) - val.get('last_month_actuals', 0)

            # --- PRINT THE DICTIONARY TO CONSOLE ---
            # import json
            # print("\n--- DATA DICTIONARY FOR TEMPLATE ---")
            # # We use indent=4 to make it readable in your terminal
            # print(json.dumps(snapshot_data, indent=4))
            # print("-------------------------------------\n")

            context = {
                "details": data['project_details'],
                "snapshot": snapshot_data,
                "snapshot_date": data['snapshot_at_date']['snapshot_date'],
                "graph_image": graph_base64
            }
            
            html_string = render_to_string('procurement_report.html', context)
            result = io.BytesIO()
            pisa_status = pisa.CreatePDF(io.BytesIO(html_string.encode("UTF-8")), dest=result)
            
            if not pisa_status.err:
                response = HttpResponse(result.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = f'inline; filename="Procurement_Report_{co_no}.pdf"'
                return response
            
            return Response({"error": "PDF conversion error"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
