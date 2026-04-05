# core/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path("list-projects/", PSRProjectListAPIView.as_view(), name="psr-project-list"),
    path('update-all/', UpdateAllPSRSnapshotsAPIView.as_view(), name='update-all-psr'),
    path('generate-snapshot/', GeneratePSRSnapshotAPIView.as_view(), name='generate-psr-snapshot'),

    path('import/timesheet/', ImportTimesheetAPIView.as_view(), name='import-timesheet'),
    path('import/podata/', ImportPODataAPIView.as_view(), name='import-podata'),
    path('import/grrdata/', ImportGRRDataAPIView.as_view(), name='import-grrdata'),
    path('import/pcrdata/', ImportPCRDataAPIView.as_view(), name='import-pcrdata'),

    path('landing-data/', LandingPageAPIView.as_view(), name='landing-page-summary'),
    
    path('projects/latest-snapshots/', AllProjectsLatestSnapshotView.as_view(), name='all-projects-latest-snapshots'),
    path('projects/history-kpi/', MonthlyCumulativeKPIHistoryView.as_view(), name='monthly-cumulative-kpi-history'),
    
    path('projects/<str:co_no>/snapshot/timesheet/', ProjectPSRSnapshotTimesheetView.as_view(), name='project-snapshot-timesheet'),
    path('projects/<str:co_no>/snapshot/timesheet/<str:snapshot_date>/', ProjectPSRSnapshotTimesheetView.as_view(), name='project-snapshot-timesheet-date'),

    path('projects/<str:co_no>/snapshot/cost-to-go/', ProjectPSRSnapshotCostToGoView.as_view(), name='project-snapshot-cost-to-go'),
    path('projects/<str:co_no>/snapshot/cost-to-go/<str:snapshot_date>/', ProjectPSRSnapshotCostToGoView.as_view(), name='project-snapshot-cost-to-go-date'),
    
    path('projects/<str:co_no>/snapshot-history/timesheet/', ProjectSnapshotTimesheetHistoryView.as_view(), name='project-snapshot-timesheet-history'),
    path('projects/<str:co_no>/snapshot-history/cost-to-go/', ProjectSnapshotCostToGoHistoryView.as_view(), name='project-snapshot-cost-to-go-history'),
    
    path('subdepartments/<int:pk>/budget-update/', SubDepartmentBudgetUpdateView.as_view(), name='subdepartment-budget-update'),
    path('projectcostcategories/<int:pk>/budget-update/', ProjectCostCategoryBudgetUpdateView.as_view(), name='projectcostcategory-budget-update'),
    
    path('subdepartments/<int:pk>/forecast-override/', SubDepartmentForecastOverrideView.as_view(), name='subdepartment-forecast-override'),
    path('subdepartments/<int:pk>/get-forecast-override/', SubDepartmentGetForecastOverrideView.as_view(), name='subdepartment-forecast-override'),
    
    path('projectcostcategories/<int:pk>/forecast-override/', ProjectCostCategoryForecastOverrideView.as_view(), name='projectcostcategory-forecast-override'),
    path('projectcostcategories/<int:pk>/get-forecast-override/', ProjectCostCategoryGetForecastOverrideView.as_view(), name='projectcostcategory-forecast-override-detail'),
    
    path('projects/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/<str:co_no>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/<str:co_no>/update/', ProjectUpdateView.as_view(), name='project-update'),
    
    path('projects/<str:co_no>/details/', ProjectKPIDetailsView.as_view(), name='project-details'),
    path('projects/<str:co_no>/update-status/', ProjectStatusUpdateView.as_view(), name='project-update'),
    path('projects/<str:co_no>/snapshot/latest-kpi/', ProjectLatestSnapshotKPIView.as_view(), name='project-latest-kpi'),
    path('projects/<str:co_no>/snapshot/history-kpi/', ProjectSnapshotHistoryKPIView.as_view(), name='project-history-kpi'),

    path('projectcostcategories/<int:pk>/rk-actual-override/', RKActualOverrideView.as_view(), name='rk-actual-override'),
    path('projectcostcategories/<int:pk>/get-rk-actual-override/', RKGetActualOverrideView.as_view(), name='rk-actual-override-detail'),
    
    path('projects/cost-category/<int:pk>/assembly-override/', AssemblyActualOverrideView.as_view(), name='assembly-actual-override'),
    path('projects/cost-category/<int:pk>/get-assembly-override/', AssemblyGetActualOverrideView.as_view(), name='assembly-get-actual-override'),
    
    path('projects/cost-category/<int:pk>/fv-override/', FVActualOverrideView.as_view(), name='fv-actual-override'),
    path('projects/cost-category/<int:pk>/get-fv-override/', FVGetActualOverrideView.as_view(), name='fv-get-actual-override'),


    path('projects/cost-category/<int:pk>/soko-override/', SOKOActualOverrideView.as_view(), name='soko-actual-override'),
    path('projects/cost-category/<int:pk>/get-soko-override/', SOKOGetActualOverrideView.as_view(), name='soko-get-actual-override'),
    

    path('budget-change-requests/my-pending/', MyPendingBudgetApprovalsView.as_view(), name='psr-my-pending'),
    path('budget-change-requests/my-submitted/', MySubmittedBudgetRequestsView.as_view(), name='psr-my-submitted'),
    path('budget-change-requests/<int:pk>/', PSRBudgetChangeRequestDetailView.as_view(), name='psr-request-detail'),
    path('budget-change-requests/<int:pk>/action/', PSRBudgetChangeRequestActionView.as_view(), name='psr-request-action'),
    
    
    # path('forecast-override-requests/my-pending/', MyPendingForecastApprovalsView.as_view(), name='psr-forecast-my-pending'),
    # path('forecast-override-requests/my-submitted/', MySubmittedForecastRequestsView.as_view(), name='psr-forecast-my-submitted'),
    # path('forecast-override-requests/<int:pk>/', PSRForecastChangeRequestDetailView.as_view(), name='psr-forecast-request-detail'),
    # path('forecast-override-requests/<int:pk>/action/', PSRForecastChangeRequestActionView.as_view(), name='psr-forecast-request-action'),
    
    path('users/dropdown/', UserDropdownView.as_view(), name='user-dropdown'),
    
    
    path('projects/<str:co_no>/payments/', ProjectPaymentsListCreateView.as_view(), name='project-payments-list-create'),
    path('projects/<str:co_no>/payments/<int:pk>/', ProjectPaymentDetailView.as_view(), name='project-payment-detail'),
    path('projects/<str:co_no>/payments/summary/', ProjectPaymentSummaryView.as_view()),
    path('projects/<str:co_no>/payments/graph/', ProjectPaymentsGraphView.as_view(), name='project-payments-graph'),
    
    path('workflow/', PSRProjectCreationWorkflowView.as_view(), name='project-workflow-list'),
    
    # Route for Detail, Approving, or Rejecting a specific request
    path('workflow/<int:pk>/', PSRProjectCreationWorkflowView.as_view(), name='project-workflow-detail'),


    path('projects/<str:co_no>/unified-summary/', ProcurementSummaryView.as_view(), name='procurement-summary'),
    path('projects/<str:co_no>/update-phase/', ProjectPhaseUpdateView.as_view(), name='update-phase'),
]