# core/management/commands/generate_psr_snapshot.py

import datetime
from calendar import monthrange
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from psr.models import (
    PSRProject, TimesheetEntry, POData, PSRSubDepartment, CostCategory, PSRSnapshot, GRRData, PCRData
)


class Command(BaseCommand):
    help = "Generate PSR snapshot for projects (all costs in INR)"

    def add_arguments(self, parser):
        parser.add_argument('co_no', type=str, nargs='?', default=None)
        parser.add_argument('--date', type=str, required=False)

    def handle(self, *args, **options):
        co_no = options.get('co_no')
        snapshot_date_str = options.get('date')

        # Determine snapshot date
        if snapshot_date_str:
            try:
                snapshot_date = datetime.datetime.strptime(snapshot_date_str, '%Y-%m-%d').date()
            except ValueError:
                self.stderr.write(self.style.ERROR("Invalid date format. Use YYYY-MM-DD"))
                return
        else:
            # Use today's date if not provided
            snapshot_date = timezone.now().date()

        # Determine which projects to process
        if co_no:
            # Single project mode
            projects = PSRProject.objects.filter(co_no=co_no)
            if not projects.exists():
                self.stderr.write(self.style.ERROR(f"Project {co_no} not found"))
                return
        else:
            # All projects mode
            projects = PSRProject.objects.all()
            if not projects.exists():
                self.stderr.write(self.style.WARNING("No projects found in PSRProject"))
                return

        # Display what we're about to do
        project_count = projects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Generating snapshots for {project_count} project(s) on {snapshot_date}"
            )
        )

        # Process each project
        success_count = 0
        error_count = 0
        
        for project in projects:
            try:
                self.stdout.write(f"\nProcessing {project.co_no}...")
                self.generate_snapshot(project, snapshot_date)
                success_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"? Snapshot generated for {project.co_no}")
                )
            except Exception as e:
                error_count += 1
                self.stderr.write(
                    self.style.ERROR(f"? Error generating snapshot for {project.co_no}: {str(e)}")
                )

        # Summary
        self.stdout.write("\n" + "="*60)
        self.stdout.write(
            self.style.SUCCESS(f"Summary: {success_count} successful, {error_count} errors")
        )
        self.stdout.write("="*60)

    def generate_snapshot(self, project, snapshot_date):
        """Generate snapshot for a single project"""
        
        exchange_rate = project.exchange_rate

        # Calculate last month end date
        first_day_current = snapshot_date.replace(day=1)
        last_day_prev_month = first_day_current - datetime.timedelta(days=1)
        last_month_date = last_day_prev_month.replace(
            day=monthrange(last_day_prev_month.year, last_day_prev_month.month)[1]
        )

        previous_snapshot = PSRSnapshot.objects.filter(
            project=project,
            snapshot_date=last_month_date
        ).first()

        data = {"TIMESHEET": {"HOURS": {}, "COST": {}}, "COST TO GO": {"COST": {}}}

        # Separate totals
        labor_actual_hours = Decimal('0')
        labor_budget_hours = Decimal('0')
        labor_forecast_hours = Decimal('0')
        labor_prognosis_hours = Decimal('0')

        labor_actual_cost = Decimal('0')
        labor_budget_cost = Decimal('0')
        labor_forecast_cost = Decimal('0')
        labor_prognosis_cost = Decimal('0')

        material_actual_cost = Decimal('0')
        material_budget_cost = Decimal('0')
        material_forecast_cost = Decimal('0')
        material_prognosis_cost = Decimal('0')

        # ================================
        # Labor Processing - OPTIMIZED
        # ================================

        # 1. Prefetch all timesheet entries at once
        timesheet_entries = TimesheetEntry.objects.filter(
            co_no__startswith=project.co_no,
            date__lte=snapshot_date
        )

        # 2. Build subdepartment lookup dictionary to avoid N+1 queries
        subdepts_by_role = {}
        subdepts_by_id = {}

        for subdept in PSRSubDepartment.objects.filter(
            department__project=project
        ).select_related('department'):
            key = subdept.role_descrptn.strip().lower()
            if key not in subdepts_by_role:
                subdepts_by_role[key] = subdept
            subdepts_by_id[subdept.id] = subdept

        # 3. Calculate labor actuals using the lookup dictionary
        labor_actuals = {}
        for entry in timesheet_entries:
            key = entry.role_description.strip().lower()
            sub_dept = subdepts_by_role.get(key)

            if sub_dept:
                dept = sub_dept.department
                hours = Decimal(str(entry.hours))
                # cost_inr = hours * dept.hourly_rate * exchange_rate
                cost_inr = hours * dept.hourly_rate

                labor_actuals.setdefault(sub_dept.id, {'hours': Decimal('0'), 'cost_inr': Decimal('0')})
                labor_actuals[sub_dept.id]['hours'] += hours
                labor_actuals[sub_dept.id]['cost_inr'] += cost_inr

        # 4. Prefetch departments and subdepartments in bulk
        departments = project.departments.prefetch_related('sub_departments').all()

        # 5. Extract previous snapshot data once before loops
        previous_snapshot_data = {}
        if previous_snapshot and previous_snapshot.data:
            prev_timesheet_cost = previous_snapshot.data.get("TIMESHEET", {}).get("COST", {})
            for dept_name, sub_depts in prev_timesheet_cost.items():
                previous_snapshot_data[dept_name] = sub_depts

        # 6. Process all departments and subdepartments
        for dept in departments:
            dept_name = dept.name
            data["TIMESHEET"]["HOURS"][dept_name] = {}
            data["TIMESHEET"]["COST"][dept_name] = {}

            prev_dept_data = previous_snapshot_data.get(dept_name, {})

            for sub_dept in dept.sub_departments.all():
                sub_code = sub_dept.code
                sub_dept_id = sub_dept.id
                inkrement = sub_dept.inkrement or ""

                act = labor_actuals.get(sub_dept_id, {'hours': Decimal('0'), 'cost_inr': Decimal('0')})
                actual_hours = act['hours']
                actual_cost_inr = act['cost_inr']

                current_budget_cost_inr = sub_dept.budget_cost
                # rate_inr = dept.hourly_rate * exchange_rate
                rate_inr = dept.hourly_rate
                current_budget_hours = current_budget_cost_inr / rate_inr if rate_inr > 0 else Decimal('0')

                baseline_budget_cost_inr = sub_dept.baseline_budget_cost
                baseline_budget_hours = baseline_budget_cost_inr / rate_inr if rate_inr > 0 else Decimal('0')

                if sub_dept.forecast_override:
                    forecast_hours = sub_dept.forecast_hours
                    forecast_cost_inr = sub_dept.forecast_cost
                else:
                    forecast_hours = current_budget_hours - actual_hours
                    forecast_cost_inr = current_budget_cost_inr - actual_cost_inr
                    
                    sub_dept.forecast_hours = forecast_hours
                    sub_dept.forecast_cost = forecast_cost_inr
                    
                    sub_dept.save(update_fields=["forecast_hours", "forecast_cost"])

                prognosis_hours = actual_hours + forecast_hours
                prognosis_cost_inr = actual_cost_inr + forecast_cost_inr

                last_month_actual_hours = Decimal('0')
                last_month_actual_cost = Decimal('0')
                if prev_dept_data:
                    prev_cost = prev_dept_data.get(sub_code, {})
                    last_month_actual_cost = Decimal(str(prev_cost.get("actuals", 0.0)))
                    last_month_actual_hours = last_month_actual_cost / rate_inr if rate_inr > 0 else Decimal('0')

                balance_pct = round(float((current_budget_cost_inr / prognosis_cost_inr * 100) if prognosis_cost_inr else 0), 2)
                rest_pct = round(float((prognosis_cost_inr / actual_cost_inr * 100) if actual_cost_inr else 0), 2)

                data["TIMESHEET"]["HOURS"][dept_name][sub_code] = {
                    "id": sub_dept_id,
                    "inkrement": inkrement,
                    "baseline_budget": float(baseline_budget_hours),
                    "last_month_actuals": float(last_month_actual_hours),
                    "actuals": float(actual_hours),
                    "budget": float(current_budget_hours),
                    "forecast": float(forecast_hours),
                    "prognosis": float(prognosis_hours),
                    "balance": float(current_budget_hours - prognosis_hours),
                    "balance_percentage": balance_pct,
                    "rest": float(forecast_hours),
                    "rest_percentage": rest_pct,
                }

                data["TIMESHEET"]["COST"][dept_name][sub_code] = {
                    "id": sub_dept_id,
                    "inkrement": inkrement,
                    "baseline_budget": float(baseline_budget_cost_inr),
                    "last_month_actuals": float(last_month_actual_cost),
                    "actuals": float(actual_cost_inr),
                    "budget": float(current_budget_cost_inr),
                    "forecast": float(forecast_cost_inr),
                    "prognosis": float(prognosis_cost_inr),
                    "balance": float(current_budget_cost_inr - prognosis_cost_inr),
                    "balance_percentage": balance_pct,
                    "rest": float(forecast_cost_inr),
                    "rest_percentage": rest_pct,
                }

                labor_actual_hours += actual_hours
                labor_budget_hours += current_budget_hours
                labor_forecast_hours += forecast_hours
                labor_prognosis_hours += prognosis_hours

                labor_actual_cost += actual_cost_inr
                labor_budget_cost += current_budget_cost_inr
                labor_forecast_cost += forecast_cost_inr
                labor_prognosis_cost += prognosis_cost_inr

        # ================================
        # Material Processing - OPTIMIZED
        # ================================

        po_entries = POData.objects.filter(co_no__startswith=project.co_no)

        cost_categories_by_matcode = {}
        cost_categories_by_code = {}
        all_cost_categories = CostCategory.objects.all()

        for cat in all_cost_categories:
            key = (cat.mat_code or "").strip().lower()
            cost_categories_by_matcode.setdefault(key, cat)   # safe even if key == ""
            cost_categories_by_code[cat.code] = cat

        material_actuals = {}
        for entry in po_entries:
            key = entry.mat_code.strip().lower()
            cat = cost_categories_by_matcode.get(key)
            if cat:
                cost_inr = Decimal(str(entry.po_value_inr))
                material_actuals[cat.code] = material_actuals.get(cat.code, Decimal('0')) + cost_inr

        project_cost_categories = project.project_cost_categories.select_related(
            'cost_category'
        ).prefetch_related(
            'rk_actual_adjustments__lines',
            'assembly_actual_adjustments__lines',
            'fv_actual_adjustments__lines'
        ).all()

        pcc_by_cat_code = {}
        for pcc in project_cost_categories:
            pcc_by_cat_code[pcc.cost_category.code] = pcc

        previous_material_data = {}
        if previous_snapshot and previous_snapshot.data:
            prev_cost_to_go = previous_snapshot.data.get("COST TO GO", {}).get("COST", {})
            previous_material_data = prev_cost_to_go

        for cat in all_cost_categories:
            cat_code = cat.code
            pcc = pcc_by_cat_code.get(cat_code)

            if not pcc:
                continue
            
            pcc_id = pcc.id
            inkrement = cat.code

            current_budget_inr = pcc.budget_cost
            baseline_budget_inr = pcc.baseline_budget_cost

            if pcc.actual_override:
                if cat_code == 'RK':
                    actual_inr = material_actuals.get(cat_code, Decimal('0'))
                    latest_adj = pcc.rk_actual_adjustments.all()[:1]
                    if latest_adj:
                        manual_adj = sum(line.amount for line in latest_adj[0].lines.all())
                        actual_inr += manual_adj

                elif cat_code == 'ASSEMBLY SERVICES':
                    actual_inr = material_actuals.get(cat_code, Decimal('0'))
                    latest_adj = pcc.assembly_actual_adjustments.all()[:1]
                    if latest_adj:
                        manual_adj = sum(line.amount for line in latest_adj[0].lines.all())
                        actual_inr += manual_adj

                elif cat_code == 'F+V':
                    actual_inr = material_actuals.get(cat_code, Decimal('0'))
                    latest_adj = pcc.fv_actual_adjustments.all()[:1]
                    if latest_adj:
                        manual_adj = sum(line.amount for line in latest_adj[0].lines.all())
                        actual_inr += manual_adj

                elif cat_code == 'SOKO':
                    actual_inr = material_actuals.get(cat_code, Decimal('0'))
                    latest_adj = pcc.soko_actual_adjustments.all()[:1]
                    if latest_adj:
                        manual_adj = sum(line.amount for line in latest_adj[0].lines.all())
                        actual_inr += manual_adj

                else:
                    actual_inr = material_actuals.get(cat_code, Decimal('0'))

            else:
                actual_inr = material_actuals.get(cat_code, Decimal('0'))

            if pcc.forecast_override:
                forecast_inr = pcc.forecast_cost
            else:
                forecast_inr = current_budget_inr - actual_inr

            prognosis_inr = actual_inr + forecast_inr

            last_month_actual_inr = Decimal('0')
            if previous_material_data:
                prev = previous_material_data.get(cat_code, {})
                last_month_actual_inr = Decimal(str(prev.get("actuals", 0.0)))

            balance_pct = round(float((current_budget_inr / prognosis_inr * 100) if prognosis_inr else 0), 2)
            rest_pct = round(float((prognosis_inr / actual_inr * 100) if actual_inr else 0), 2)

            data["COST TO GO"]["COST"][cat_code] = {
                "id": pcc_id,
                "inkrement": inkrement,
                "baseline_budget": float(baseline_budget_inr),
                "last_month_actuals": float(last_month_actual_inr),
                "actuals": float(actual_inr),
                "budget": float(current_budget_inr),
                "forecast": float(forecast_inr),
                "prognosis": float(prognosis_inr),
                "balance": float(current_budget_inr - prognosis_inr),
                "balance_percentage": balance_pct,
                "rest": float(forecast_inr),
                "rest_percentage": rest_pct,
            }

            material_actual_cost += actual_inr
            material_budget_cost += current_budget_inr
            material_forecast_cost += forecast_inr
            material_prognosis_cost += prognosis_inr



        # ================================
        # GRR Calculations
        # ================================

        grr_entries = GRRData.objects.filter(
            co_no__startswith=project.co_no,
            grr_date__lte=snapshot_date
        )

        total_grr = Decimal('0')
        for entry in grr_entries:
            rate = entry.rate or Decimal('0')
            qty = entry.received_qty or Decimal('0')
            total_grr += rate * qty

        # ================================
        # PCR Calculations
        # ================================

        pcr_entries = PCRData.objects.filter(
            co_no__startswith=project.co_no,
            pcr_date__lte=snapshot_date
        )

        total_pcr = Decimal('0')
        for entry in pcr_entries:
            rate = entry.rate or Decimal('0')
            qty = entry.recp_qty or Decimal('0')
            total_pcr += rate * qty

        # ================================
        # KPI Calculations
        # ================================
        INITIAL_SNAPSHOT_DATE = datetime.date(2023, 11, 1)

        is_initial_view = not PSRSnapshot.objects.filter(
            project=project,
            snapshot_date=INITIAL_SNAPSHOT_DATE
        ).exists()
        
        if is_initial_view:
            snapshot_date = datetime.date(2023, 11, 1)
            total_budget_cost = project.budget
            sales_value = project.sales_value
            eff_value = project.eff_value
            ter_value = project.ter_value
            risk_value = project.risk
            total_actual_cost = Decimal('0')
            total_forecast_cost = total_budget_cost - total_actual_cost
            total_prognosis_cost = total_actual_cost + total_forecast_cost
            sum_prognosis = total_prognosis_cost + eff_value + ter_value + risk_value
            margin = project.sales_value - sum_prognosis
            factor = project.factor
            ebit_value = project.ebit_value
            ebit_percentage = project.ebit_percentage
            net_marginal_income = project.sgna_value + ebit_value
            net_marginal_income_percentage = (net_marginal_income / sales_value) * 100
            
        else:
            total_actual_cost = labor_actual_cost + material_actual_cost

            # total_budget = labor_budget_cost + material_budget_cost
            total_budget_cost = labor_budget_cost + material_budget_cost

            # if project.budget > total_budget:
            #     total_budget_cost = project.budget
            # else:
            #     total_budget_cost = total_budget
            
            # total_forecast = labor_forecast_cost + material_forecast_cost
            
            # if total_forecast == 0:
            #     total_forecast_cost = total_forecast
            
            # else:
            #     # total_forecast_cost = total_budget_cost - total_actual_cost
            #     total_forecast_cost = labor_forecast_cost + material_forecast_cost
            
            total_forecast_cost = labor_forecast_cost + material_forecast_cost
            
            total_prognosis_cost = labor_prognosis_cost + material_prognosis_cost

            # print("Budget ----->", total_budget_cost)
            # pr_total_forecast_cost = total_budget_cost - total_actual_cost
            # print("Forecast --->", pr_total_forecast_cost)
            # total_prognosis_cost = pr_total_forecast_cost + total_actual_cost

            sales_value = project.sales_value
            eff_value = project.eff_value
            ter_value = project.ter_value
            risk_value = project.risk
            sum_prognosis = total_prognosis_cost + eff_value + ter_value + risk_value
            margin = project.sales_value - sum_prognosis
            ebit_value = project.ebit_value
            ebit_percentage = project.ebit_percentage
            # net_marginal_income = project.sgna_value + ebit_value
            net_marginal_income = margin
            net_marginal_income_percentage = (net_marginal_income / sales_value) * 100
            
            factor = project.sales_value / sum_prognosis if sum_prognosis > 0 else Decimal('0')

        # ================================
        # POC Calculation
        # ================================
        poc = (
            (total_grr + total_pcr + labor_actual_cost) / sum_prognosis
            if sum_prognosis > 0
            else Decimal('0')
        )

        # Save snapshot
        snapshot, created = PSRSnapshot.objects.update_or_create(
            project=project,
            snapshot_date=snapshot_date,
            defaults={
                'data': data,

                # Labor
                'labor_actual_hours': labor_actual_hours,
                'labor_budget_hours': labor_budget_hours,
                'labor_forecast_hours': labor_forecast_hours,
                'labor_prognosis_hours': labor_prognosis_hours,
                'labor_actual_cost': labor_actual_cost,
                'labor_budget_cost': labor_budget_cost,
                'labor_forecast_cost': labor_forecast_cost,
                'labor_prognosis_cost': labor_prognosis_cost,

                # Material
                'material_actual_cost': material_actual_cost,
                'material_budget_cost': material_budget_cost,
                'material_forecast_cost': material_forecast_cost,
                'material_prognosis_cost': material_prognosis_cost,

                # New KPI fields
                'sales_value': sales_value,
                'eff_value': eff_value,
                'ter_value': ter_value,
                'risk_value': risk_value,
                'sum_prognosis': sum_prognosis,
                'margin': margin,
                'factor': factor,
                'ebit_value': ebit_value,
                'ebit_percentage': ebit_percentage,
                'net_marginal_income': net_marginal_income,
                'net_marginal_income_percentage': net_marginal_income_percentage,

                # Combined
                'total_actual_cost': total_actual_cost,
                'total_budget_cost': total_budget_cost,
                'total_forecast_cost': total_forecast_cost,
                'total_prognosis_cost': total_prognosis_cost,

                'total_grr': total_grr,
                'total_pcr': total_pcr,
                'poc': poc,
            }
        )
        action = "created" if created else "updated"
        self.stdout.write(self.style.SUCCESS(f"Snapshot {action} successfully for {project.co_no} on {snapshot_date}"))
        