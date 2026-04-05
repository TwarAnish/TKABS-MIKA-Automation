# capacity_planning/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import *


router = DefaultRouter()
router.register(r'departments', views.DepartmentViewSet)
# router.register(r'projects', views.ProjectViewSet)
router.register(r'resources', views.ResourceViewSet)
router.register(r'assignments', views.ProjectAssignmentViewSet)
router.register(r'allocations', views.ResourceAllocationViewSet)
router.register(r'planned-demand', views.ProjectWeekAllocationViewSet)
router.register(r'external-capacity', views.ExternalCapacityViewSet)
# router.register(r'suppliers', views.SupplierViewSet)
router.register(r'settings', views.AppSettingsViewSet, basename='settings')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/capacity/summary/', views.CapacitySummaryView.as_view(), name='capacity-summary'),
    path('api/capacity/gaps/', views.CapacityGapsView.as_view(), name='capacity-gaps'),
    path('api/weekly-project-breakdown/', views.WeeklyProjectBreakdownView.as_view(), name='weekly-project-breakdown'),
    path('api/department-weekly-breakdown/', views.DepartmentWeeklyBreakdownView.as_view(), name='department-weekly-breakdown'),
    path('api/department-weekly-detail/', views.DepartmentWeeklyDetailView.as_view(), name='department-weekly-detail'),
    path('api/project-role-utilization/', views.ProjectRoleUtilizationView.as_view(), name='project-role-utilization'),
    path('api/internal-resource-utilization/', views.InternalResourceUtilizationView.as_view(), name='internal-resource-utilization'),
    path('api/employee-summary/', views.EmployeeSummaryView.as_view(), name='employee-summary'),
    path('api/employee-table/', views.EmployeeTableView.as_view(), name='employee-table'),
    path('api/employee-capacity-graph/', views.EmployeeCapacityGraphView.as_view(), name='employee-capacity-graph'),
    path('api/project-summary/', views.ProjectSummaryView.as_view(), name='project-summary'),
    path('api/employee-idle-capacity/', views.EmployeeIdleCapacityView.as_view(), name='employee-idle-capacity'),
    path('api/department-capacity-summary/', views.DepartmentCapacitySummaryView.as_view(), name='department-capacity-summary'),
    path('api/supplier-master/', views.SupplierMasterView.as_view(), name='supplier-master'),
    path('api/free-capacity-employees/<int:deptId>/', views.FreeCapacityEmployeeView.as_view(), name='free-capacity-employees'),
    # path('api/projects/', views.project_list_create, name='project-list-create'),
    path('api/projects/<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
    path('api/employees/', views.employee_list_create, name='employee-list-create'),
    path('api/employees/<int:pk>/', EmployeeDetailAPIView.as_view(), name='employee-detail'),
    path('api/suppliers/', SupplierListCreate.as_view(), name='supplier-list-create'),
    path('api/suppliers/<int:pk>/', SupplierDetail.as_view(), name='supplier-detail'),
    path('api/project-assignments/', views.ProjectAssignmentListCreate.as_view(), name='project-assignment-list-create'),
    path('api/project-assignments/<int:pk>/', views.ProjectAssignmentDetail.as_view(), name='project-assignment-detail'),
    path('api/project-assignments/bulk/', ProjectAssignmentBulkCreateAPIView.as_view(), name='project-assignment-bulk'),
    path('api/resource-allocations/', ResourceAllocationListCreate.as_view(), name='resource-allocation-list-create'),
    path('api/resource-allocations/<int:pk>/',ResourceAllocationDetail.as_view(), name='resource-allocation-detail'),
    path('api/project-week-allocations/', ProjectWeekAllocationListCreate.as_view(), name='project-week-allocation-list-create'),
    path('api/project-week-allocations/<int:pk>/', ProjectWeekAllocationDetailAPIView.as_view(), name='project-week-allocation-detail'),
    path('api/project-week-allocations/bulk/', ProjectWeekAllocationBulkCreate.as_view(), name='project-week-allocation-bulk'),
    path('api/external-capacities/', ExternalCapacityListCreate.as_view(), name='external-capacity-list-create'),
    path('api/external-capacities/<int:pk>/', ExternalCapacityDetail.as_view(), name='external-capacity-detail'),
    path('api/external-capacities/bulk/', ExternalCapacityBulkCreate.as_view(), name='external-capacity-bulk'),
    path('api/debug/', views.debug_view),
    path('api/resource-weekly-utilization/', views.ResourceWeeklyUtilizationView.as_view(), name='resource-weekly-utilization'),
    path('api/all-project-weekly-detail/', GlobalDepartmentWeeklyDetailView.as_view(),name='project-weekly-detail'),    
    
    
    path('api/department-weekly-detail/<int:department_id>/', DepartmentWeeklyDetailView_byDeptId.as_view(),name='department-weekly-detail'),
    path('api/employees_deptId/<int:department_id>/', EmployeeListCreateAPIView.as_view(), name='employee-list-create'),
    path('api/project-summary_deptId/<int:department_id>/',ProjectSummaryView_DeptId.as_view(), name='project-summary'),
    path('api/department-capacity-summary_deptId/<int:department_id>/', DepartmentCapacitySummary_DeptId.as_view(), name='department-capacity-summary'),
    # path('api/projects_deptId/<int:department_id>/', ProjectListCreateAPIView_DeptId.as_view(), name='project-list-create'),
    path('api/projects/', ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('api/departments/<int:department_id>/project-allocations/',views.ProjectDepartmentAllocationAPIView.as_view(),name='department-project-allocation'),

    path('api/projects/<int:project_id>/department-allocations/<int:department_id>/',ProjectDepartmentAllocationDetail.as_view(), name='project-department-allocation-detail'),
    path('api/resource-allocation-delete/', ResourceAllocationListDelete.as_view(), name='resource-allocation-list-delete'),

    path('api/project-week-allocations-update/<int:pk>/', ProjectWeekAllocationUpdate.as_view(), name='project-week-allocation-update'),
    path('api/notifications/resources-free/', ResourceFreeNotificationsAPIView.as_view(), name='free-resources-notifications'),
    path('api/available-psr-projects/', AvailablePSRProjectsAPIView.as_view(), name='available-psr-projects'),
    path('api/reports/department-capacity/', DepartmentWeeklyReportView.as_view(), name='department-report-projects'),
]