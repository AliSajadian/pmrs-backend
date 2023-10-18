from rest_framework import routers
from django.urls import path, include

from .api import *
       
router = routers.DefaultRouter()
router.register('api/hseReportDox', HseReportDoxAPI, basename='hseReportDox')
router.register('api/projectDox', ProjectDoxAPI, basename='projectDox')
router.register('api/contractorDox', ContractorDoxAPI, basename='contractorDox')
router.register('api/projectMonthlyDox', ProjectMonthlyDoxAPI, basename='projectMonthlyDox')
router.register('api/approvedInvoiceDox', ApprovedInvoiceDoxAPI, basename='hseReportDox')

router.register('api/reportVisit', ReportVisitAPI, basename='reportVisit')

urlpatterns = [
    path('api/reportdox/', ReportDoxAPI.as_view()),
    path('api/zoneImages/', ZoneImagesAPI.as_view()),
    path('api/zoneImages/<int:pk>/', ZoneImagesAPI.as_view()),    
    path('api/updateZoneImage/<int:pk>/', updateZoneImage),    
    path('api/zoneImages/<int:contract_id>/<int:date_id>/', ZoneImagesAPI.as_view()),    

    path('api/hseReportDox/contractList/<int:contract_id>/', HseReportDoxAPI.as_view({"get": "contractList"})),    
    path('api/hseReportDox/download/<int:id>/', HseReportDoxAPI.as_view({"get": "download"})),    
    path('api/projectDox/contractList/<int:contract_id>/', ProjectDoxAPI.as_view({"get": "contractList"})),    
    path('api/projectDox/download/<int:id>/', ProjectDoxAPI.as_view({"get": "download"})),    
    path('api/contractorDox/contractList/<int:contract_id>/', ContractorDoxAPI.as_view({"get": "contractList"})),    
    path('api/contractorDox/download/<int:id>/', ContractorDoxAPI.as_view({"get": "download"})),    
    path('api/projectMonthlyDox/contractList/<int:contract_id>/', ProjectMonthlyDoxAPI.as_view({"get": "contractList"})),    
    path('api/projectMonthlyDox/download/<int:id>/', ProjectMonthlyDoxAPI.as_view({"get": "download"})),    
    path('api/approvedInvoiceDox/contractMonthList/<int:contract_id>/<int:date_id>/', ApprovedInvoiceDoxAPI.as_view({"get": "contractMonthList"})),    
    path('api/approvedInvoiceDox/download/<int:id>/', ApprovedInvoiceDoxAPI.as_view({"get": "download"})),  
      
    path('api/reportVisit/contractMonthList/<int:contract_id>/<int:date_id>/', ReportVisitAPI.as_view({"get": "contractMonthList"})),    
]

urlpatterns += router.urls

