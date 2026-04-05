# procurement/urls.py

from django.urls import path
from .views import *

urlpatterns = [

   #dashboard
    path('dashboard/', DashboardDataView.as_view(), name='get_dashboard_data'),#DOne
 
    # get projects, non-project, capex
    # path('getAllProjects/', ProjectListCreateAPIView.as_view(), name='project_list_create_view'), # Done
    path('getAllProjects/', ProjectListCreateAPIView.as_view(), name='project-list-create'),

    path('projects/<int:pk>/', ProjectBudgetPatchView.as_view(), name='update-budget'),    
    # path('getAllProjects/<int:pk>/', ProjectDetailAPIView.as_view(), name='project-detail'),   
    # # path('getAllProjects/<int:pk>/', ProjectListCreateAPIView.as_view(), name='project_update_view'), 
    # # create project(post)
    # #path('createProject', project_list_create_view, name='project_list_create_view'),#added in above class api
 
    # # get project by id
    # path('getProjectById/<int:pk>/', ProjectDetailAPIView.as_view(), name='project_detail_view'),#done
 
    # update all projects
    # path('updateProject/<int:pk>', project_detail_view, name='project_detail_view'),
    # path('updateNonProject/<int:pk>', project_detail_view, name='project_detail_view'),#added in above api
 
    # get project managers & hod & project names
    # path("getProjectManagers/", ProjectManagerListAPIView.as_view(), name="get-project-managers"),#done
    # path("getHods/", HodListAPIView.as_view(), name="get-hods"),#done
    path("getProjectName/", ProjectNameListAPIView.as_view(), name="get-project-name"),#done
    path('getUsers/', OrganizationalUsersAPIView.as_view(), name='org-users'),
    # graph api's
    path("cashIn/", CashInflowListCreateAPIView.as_view(), name='cash_inflow_view'),#done
    path("cashIn/<int:pk>", CashInflowByProjectAPIView.as_view(), name='cash_inflow_view'),#done
    # path("cashOut/", cash_outflow_view, name='cash_outflow_view'),
    # path('cashflow/', cash_flow_view, name='cash_flow_view'),
    path('draft/', DraftListView.as_view(), name='draft-create'),
    path('draft/<int:pk>/', DraftDetailView.as_view(), name='draft-detail'),    
    path('change-requests/', ChangeRequestListView.as_view(), name='change-request-list'),
    
    path('projectsboards/<int:project_id>/boards/', ProjectBoardListCreateAPIView.as_view(), name='project-board-list'),
    path('project-boards/', ProjectBoardListCreateAPIView.as_view(), name='project-board-create'),
    path('project-boards/<int:pb_id>/', ProjectBoardDetailAPIView.as_view(), name='project-board-detail'),
    path('buyer/dashboard/', BuyerProcurementDashboard.as_view(), name='buyer-procurement-dashboard'),

    path('commercial-requirements/', CommercialRequirementListCreateAPIView.as_view(), name='commercial-requirements-create'),
    path('commercial-requirements/<int:pb_id>/', CommercialRequirementDetailAPIView.as_view(), name='commercial-requirements-detail'),


    # path('commercial-requirements/',CommercialRequirementListCreateAPIView.as_view(), name='commercial_requirement_create'),

    # # Detail and Update endpoint (Combined)
    # path('commercial-requirements/<int:cr_id>/',CommercialRequirementDetailAPIView.as_view(),name='commercial_requirement_detail_update'),

    # List by PB ID (GET) and Create (POST)
    # GET /suppliers/pb/5/ -> list all for PB 5
    # POST /suppliers/ -> create new
    path('supplier/', SupplierListCreateAPIView.as_view(), name='supplier-create'),
    path('supplier/<int:pb_id>/', SupplierDetailAPIView.as_view(), name='supplier-detail'),


    # project board supplier create api
    path('lineitem',LineItemListCreateAPIView.as_view(),name='create_line_item_with_negotiation'),

    path('lineitemall/<int:pb_id>/',LineItemDetailAPIViewAll.as_view(),name='get_all_line_items_by_pb'),
             
    path('lineitem/<int:li_id>/',LineItemDetailAPIView.as_view(),name='get_all_line_items_by_li'),

    path('suppliernegotiationssummary/<int:pb_id>/', SupplierNegotiationSummaryAPIView.as_view()),   
    path('suppliernegotiations/<int:pb_id>/<int:supplier_id>/', SupplierNegotiationSummaryAPIView.as_view(), name='negotiation-list-finalize'),
    # POST: Finalize
    # path("finalizeSupplierNegotiation",SupplierNegotiationAPIView.as_view(),name='finalize_supplier_negotiation'),
    #project board term's create api
    path('procurement-upload/', ProcurementUploadAPIView.as_view(), name='procurement-upload'),
    path('conditions/', TermConditionListCreateAPIView.as_view(), name='condition-list'),
    # path('conditions/<int:pk>/', TermConditionDetailView.as_view(), name='condition-detail'),

    
    path('term-assignments/', TermAssignmentListCreateView.as_view(), name='term-assignment-list-create'),
    path('term-assignments/<int:id>/', TermAssignmentDetailAPIView.as_view(), name='term-assignment-detail'),
    path('term-assignments-pb/<int:pb_id>/<int:supplier_id>/', TermAssignmentDetailAPIViewAll.as_view(), name='term-assignment-detail-pb'),
    path('term-assignments-pb/<int:pb_id>/', TermAssignmentDetailAPIViewAll.as_view(), name='term-assignment-detail-pb'),

    path('approvar/', ApprovarListCreateAPIView.as_view(), name='approvar-create'),
    path('approvar-pb/<int:pb_id>/', ApprovarDetailAPIView.as_view(), name='approvar-detail'),
    path('approvar-id/<int:id>/', ApprovarDetailAPIViewId.as_view(), name='approvar-detail-id'),

    path('pb-summary/<int:pb_id>/', ProjectBoardSummaryAPIView.as_view(), name='pb-summary'),


    path('project-finance/<int:project_id>/', get_single_project_data, name='project-finance-json'),    

    path('approvalsrejection/', ApprovalRejectionAPIView.as_view(), name='approval-list-create'),    
    path('approvalsrejection/<int:pk>/', ApprovalRejectionAPIView.as_view(), name='approvals-detail'),   

    path('initialize-approvlflow/', BulkInitializeWorkflowAPIView.as_view(), name='initialize-workflow'),

    path('change-requests/<int:pk>/', ChangeRequestPatchView.as_view(), name='change-request-patch'),    


    path("projectBoardFullDetails/<int:pb_id>", ProjectBoardFullDetailsView.as_view(), name='project_board_full_details'),
    path('item_description/<int:project_id>/', ProjectExcelFileListView.as_view(), name='project-items-list'),    

    path('procurement_plan_item_list/<int:project_id>/', ProjectProcurementPlanListView.as_view(), name='check_procurement'),
    path('pb-summary-export/<int:pb_id>/', ProjectBoardPDFExportAPIView.as_view()),    
    # path("createProjectBoardApprover", ApproverListCreateView.as_view(), name='create_project_board_approver'),
    # path("getAllApproverByPBId/<int:pb_id>", ApproverListCreateView.as_view(), name='get_all_approvers_by_pb'),
    # path("getApproverDetailsById/<int:mapping_id>", ApproverDetailView.as_view(), name='get_approver_by_id'),
    # path("updateApproverDetails/<int:mapping_id>", ApproverDetailView.as_view(), name='update_approver_details'),

    # Approval Matrix & Workflow
    path("generateApprovalMatrix/<int:pb_id>", GenerateApprovalMatrixView.as_view(), name='generate_approval_matrix'),
    path("myApprovalList/<int:user_id>", MyApprovalListView.as_view(), name='my_approval_list'),
    path("takeApprovalAction", TakeApprovalActionView.as_view(), name='take_approval_action'),
    path('pb_attachements/<int:pb_id>/', ProcurementListByPBView.as_view()),
    path('pb_attachements_delete/<int:pk>/', ProcurementDeleteView.as_view()),
    # Board Details
    path("api/rates/", CurrencyExchangeView.as_view(), name='test'),

]
