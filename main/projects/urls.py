from rest_framework import routers
from django.urls import path, include

from .api import *
       
router = routers.DefaultRouter()
router.register('api/reportConfirm', ReportConfirmAPI, basename='reportConfirm')
router.register('api/financialInfos', FinancialInfoAPI, basename='financialInfo')
router.register('api/hses', HseAPI, basename='hse')
router.register('api/progressStates', ProgressStateAPI, basename='progressState')
router.register('api/timeProgressStates', TimeProgressStateAPI, basename='progressState')
router.register('api/invoices', InvoiceAPI, basename='invoice')
router.register('api/financialInvoices', FinancialInvoiceAPI, basename='financialInvoice')
router.register('api/workVolumes', WorkVolumeAPI, basename='workVolume')
router.register('api/pmsProgresses', PmsprogressAPI, basename='pmsProgress')
router.register('api/budgetCosts', BudgetCostAPI, basename='budgetCost')
router.register('api/machineries', MachineryAPI, basename='machinery')
router.register('api/projectPersonals', ProjectPersonalAPI, basename='projectPersonal')
router.register('api/problems', ProblemAPI, basename='problem')
router.register('api/criticalActions', CriticalActionAPI, basename='criticalAction')

urlpatterns = [
    path('api/reportDates', ReportDateAPIEx.as_view()),
    
    path('api/reportConfirm/projectManagerReportConfirm/<int:contract_id>/<int:date_id>/<int:confirmed>/', ReportConfirmAPI.as_view({"post": "projectManagerReportConfirm"})),    
    path('api/financialInfos/contractMonthList/<int:contract_id>/<int:date_id>/', FinancialInfoAPI.as_view({"get": "contractMonthList"})),    
    path('api/hses/contractMonthList/<int:contract_id>/<int:date_id>/', HseAPI.as_view({"get": "contractMonthList"})),    
    path('api/progressStates/contractMonthList/<int:contract_id>/<int:date_id>/', ProgressStateAPI.as_view({"get": "contractMonthList"})),
    path('api/timeProgressStates/contractMonthList/<int:contract_id>/<int:date_id>/', TimeProgressStateAPI.as_view({"get": "contractMonthList"})),
    path('api/invoices/contractMonthList/<int:contract_id>/<int:date_id>/', InvoiceAPI.as_view({"get": "contractMonthList"})),
    path('api/financialInvoices/contractMonthList/<int:contract_id>/<int:date_id>/', FinancialInvoiceAPI.as_view({"get": "contractMonthList"})),
    path('api/workVolumes/contractMonthList/<int:contract_id>/<int:date_id>/', WorkVolumeAPI.as_view({"get": "contractMonthList"})),
    path('api/pmsProgresses/contractMonthList/<int:contract_id>/<int:date_id>/', PmsprogressAPI.as_view({"get": "contractMonthList"})),
    path('api/budgetCosts/contractMonthList/<int:contract_id>/<int:date_id>/', BudgetCostAPI.as_view({"get": "contractMonthList"})),
    path('api/machineries/contractMonthList/<int:contract_id>/<int:date_id>/', MachineryAPI.as_view({"get": "contractMonthList"})),
    path('api/projectPersonals/contractMonthList/<int:contract_id>/<int:date_id>/', ProjectPersonalAPI.as_view({"get": "contractMonthList"})),
    path('api/problems/contractMonthList/<int:contract_id>/<int:date_id>/', ProblemAPI.as_view({"get": "contractMonthList"})),
    path('api/criticalActions/contractMonthList/<int:contract_id>/<int:date_id>/', CriticalActionAPI.as_view({"get": "contractMonthList"})),
]

urlpatterns += router.urls

