# from django.http import Http404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Max, Q
# from django.db.models.functions import Substr
from datetime import datetime

from django.contrib.auth import get_user_model
from contracts.models import *
from contracts.services import GregorianToShamsi
from projects_files.services import SetReportVisit
from projects.models import *
from .serializers import *


class ReportDateAPIEx(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    # READ ContractS
    def get(self, request):
        max_date_id = ReportDate.objects.aggregate(Max('dateid'))['dateid__max']
        date = ReportDate.objects.get(pk=max_date_id)
        y1 = int(date.year)
        m1 = int(date.month)

        now = GregorianToShamsi(datetime.now())
        y2 = int(now[0:4])
        m2 = int(now[5:now.find('-', 5)])
        
        loop = 0
        if((y2 - y1) > 1 or ((y2 - y1) == 0 and (m2 - m1) > 0) or ((y2 -y1) == 1 and (12 - m1 + m2 > 0))):
            loop = 1
        
        while(loop == 1):
            if(y2 == y1):
                m1 = m1 + 1
                date = ReportDate.objects.create(year=str(y1), month=str(m1))
                
                flag = 0
                contracts = Contract.objects.exclude(contract__exact='test').filter(iscompleted__exact=False)
                for contract in contracts:
                    flag = ContractReportDate.objects.filter(contractid__exact=contract.contractid, 
                                                          dateid__year__exact=y2,
                                                          dateid__month__exact=m2).count()
                    if flag == 0:
                        ContractReportDate.objects.create(contractid=contract, dateid=date)
                        
                if(m2 == m1):
                    loop = 0
                    
            elif(y2 - y1 > 0):
                m1 = m1 + 1
                if(m1 > 12):
                    m1 = 1
                    y1 = y1 + 1
                
                date = ReportDate.objects.create(year=str(y1), month=str(m1))

                flag = 0
                contracts = Contract.objects.exclude(contract__exact='test').filter(iscompleted__exact=False)
                for contract in contracts:
                    flag = ContractReportDate.objects.filter(contractid__exact=contract.contractid, 
                                                          dateid__year__exact=y2,
                                                          dateid__month__exact=m2).count()
                    if flag == 0:
                        ContractReportDate.objects.create(contractid=contract, dateid=date)
                
                if(y2 == y1 and m2 == m1):
                    loop = 0
                            
        reportDates = ReportDate.objects.all().order_by('-dateid')
        serializer = ReportDateSerializerEx(reportDates, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    
class ReportConfirmAPI(viewsets.ModelViewSet):
    queryset = ReportConfirm.objects.all()
    serializer_class = ReportConfirmSerializer
    # permission_classes = [
    #     permissions.IsAuthenticated
    # ]

    @action(detail=False, methods=['get'])   
    def getConfirmedReports(self, request, *args, **kwargs):
        try:
            contractId = int(kwargs["contract_id"])
            dateId = int(kwargs["date_id"])
            
            objects = ReportConfirm.objects.filter(
                Q(contractid__exact=contractId, dateid__exact=dateId, user_c__gt=0) | 
                Q(contractid__exact=contractId, dateid__exact=dateId, pm_c__gt=0))
            serializer = ReportsConfirmedSerializer(instance=objects, many=True) 
                
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])   
    def isProjectManagerConfirmedReport(self, request, *args, **kwargs):
        try:
            data = request.data
            contractId = int(data["contractid"])
            dateId = int(data["dateid"])
            type = int(data["type"])
            
            object = ReportConfirm.objects.filter(contractid__exact=contractId, dateid__exact=dateId, pm_c__gt=0)[0]
            
            serializer = ProjectManagerReportConfirmSerializer(instance=object, many=False) \
                if object is not None else {"pm_c":"0", "pmconfirmdate":""}
                
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['post'])   
    def projectManagerReportConfirm(self, request, *args, **kwargs):
        try:
            data = request.data
            contractId = int(data["contractid"])
            dateId = int(data["dateid"])
            confirmed = int(data["confirmed"])
            # userId = int(data["userid"])

            objects = ReportConfirm.objects.filter(contractid__exact=contractId, dateid__exact=dateId)
            if(objects is not None and len(objects) == 15):
                for obj in objects:
                    obj.pm_c = confirmed
                    obj.pmconfirmdate = datetime.now()
                    obj.save()
                # return Response({"status": "success"}, status=status.HTTP_200_OK)
                objects = ReportConfirm.objects.filter(
                    Q(contractid__exact=contractId, dateid__exact=dateId, user_c__gt=0) | 
                    Q(contractid__exact=contractId, dateid__exact=dateId, pm_c__gt=0))
                serializer = ReportsConfirmedSerializer(instance=objects, many=True) 
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else: 
                # contract = Contract.objects.get(pk=contractId)
                # date = ReportDate.objects.get(pk=dateId)
                # user = get_user_model().objects.get(pk=userId)
                # ReportConfirm.objects.create(contractid=contract, 
                #                              dateid=date, 
                #                              pm_c=confirmed, 
                #                              pmconfirmdate = datetime.now(), 
                #                              userId = user)
                return Response({"status": "error", "data": "Err:01"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])   
    def isCoordinatorConfirmedReport(self, request, *args, **kwargs):
        try:
            data = request.data
            contractId = int(data["contractid"])
            dateId = int(data["dateid"])
            type = int(data["type"])
            
            objects = ReportConfirm.objects.filter(contractid__exact=contractId, dateid__exact=dateId, type__exact=type)
            object = objects[0] if (objects is not None and len(objects) > 0) else {"userconfirmer":"", "user_c":"0", "userconfirmdate":""}
            serializer = CoordinatorReportConfirmSerializer(instance=object, many=False) 
                
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # =======
    @action(detail=False, methods=['post'])   
    def coordinatorReportConfirm(self, request, *args, **kwargs):
        try:
            data = request.data
            contractId = int(data["contractid"])
            dateId = int(data["dateid"])
            userId = int(data["userid"])
            confirmed = int(data["confirmed"])
            type = int(data["type"])
            
            objects = ReportConfirm.objects.filter(contractid__exact=contractId, dateid__exact=dateId, type__exact=type)
            object = objects[0] if (objects is not None and len(objects) > 0) else None

            if(object is not None):
                object.user_c = confirmed
                object.userid = userId
                object.userconfirmdate = datetime.now()
                object.save()
            else: 
                contract = Contract.objects.get(pk=contractId)
                date = ReportDate.objects.get(pk=dateId)
                user = get_user_model().objects.get(pk=userId)
                ReportConfirm.objects.create(contractid=contract, dateid=date, userid=user, 
                                             type=type, user_c=confirmed, userconfirmdate = datetime.now())
            
            # object = ReportConfirm.objects.filter(contractid__exact=contractId, dateid__exact=dateId, type__exact=type)[0]
            # serializer = CoordinatorReportConfirmSerializer(instance=object, many=False) \
            #     if object is not None else {"userconfirmer":"", "user_c":"0", "userconfirmdate":""}
            objects = ReportConfirm.objects.filter(
                Q(contractid__exact=contractId, dateid__exact=dateId, user_c__gt=0) | 
                Q(contractid__exact=contractId, dateid__exact=dateId, pm_c__gt=0))
            serializer = ReportsConfirmedSerializer(instance=objects, many=True) 

            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
class FinancialInfoAPI(viewsets.ModelViewSet):
    queryset = FinancialInfo.objects.all()
    serializer_class = FinancialInfoSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    @action(detail=False, methods=['post'])
    def contractMonthList(self, request, *args, **kwargs):
        try:
            data = request.data
            userId = int(data["userid"])
            contractId = int(data["contractid"])
            dateId = int(data["dateid"])
            reportId = int(data["reportid"])
            
            SetReportVisit(userId, contractId, dateId, reportId)            
            
            flg = 1	if FinancialInfo.objects.filter(contractid__exact=contractId, dateid__exact=dateId).count() > 0 else 0

            if flg == 0:
                contract = Contract.objects.get(pk=contractId)
                date = ReportDate.objects.get(pk=dateId)
                FinancialInfo.objects.update_or_create(contractid=contract ,dateid=date)  
                          
            financialinfos = FinancialInfo.objects.filter(contractid__exact=contractId, dateid__exact=dateId)
            serializer = FinancialInfoSerializer(instance=financialinfos[0] if len(financialinfos) > 0 else None, many=False)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def contractMonthReportList(self, request, *args, **kwargs):
        try:
            contractId = int(kwargs["contractid"])
            dateId = int(kwargs["dateid"])
                                    
            financialInfos = FinancialInfo.objects.filter(contractid__exact=contractId, dateid__exact=dateId)
            serializer = FinancialInfoReportSerializer(instance=financialInfos[0] if len(financialInfos) > 0 else None, many=False)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HseAPI(viewsets.ModelViewSet):
    queryset = Hse.objects.all()
    serializer_class = HseSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    
    @action(detail=False, methods=['post'])
    def contractMonthList(self, request, *args, **kwargs):
        try:
            data = request.data
            userId = int(data["userid"])
            contractId = int(data["contractid"])
            dateId = int(data["dateid"])
            reportId = int(data["reportid"])
            
            SetReportVisit(userId, contractId, dateId, reportId)            
            
            flg = 1	if Hse.objects.filter(contractid__exact=contractId, dateid__exact=dateId).count() > 0 else 0

            if flg == 0:
                contract = Contract.objects.get(pk=contractId)
                date = ReportDate.objects.get(pk=dateId)
                Hse.objects.update_or_create(contractid=contract ,dateid=date, totaloperationdays=0,   
                                       withouteventdays=0, deathno=0, woundno=0, disadvantageeventno=0)
                            
            hses = Hse.objects.filter(contractid__exact=contractId, dateid__exact=dateId)
            serializer = HseSerializer(instance=hses[0] if len(hses) > 0 else None, many=False)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def contractMonthReportList(self, request, *args, **kwargs):
        try:
            contractId = int(kwargs["contractid"])
            dateId = int(kwargs["dateid"])
                                    
            hses = Hse.objects.filter(contractid__exact=contractId, dateid__exact=dateId)
            serializer = HseReportSerializer(instance=hses[0] if len(hses) > 0 else None, many=False)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProgressStateAPI(viewsets.ModelViewSet):
    queryset = ProgressState.objects.all()
    serializer_class = ProgressStateSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    @action(detail=True, methods=['post'])
    def contractMonthList(self, request, *args, **kwargs):
        try:
            data = request.data
            userId = int(data["userid"])
            contractId = int(data["contractid"])
            dateId = int(data["dateid"])
            reportId = int(data["reportid"])
            
            SetReportVisit(userId, contractId, dateId, reportId)            
            
            flg = 1	if ProgressState.objects.filter(contractid__exact=contractId, dateid__exact=dateId).count() > 0 else 0

            if flg == 0:
                contract = Contract.objects.get(pk=contractId)
                date = ReportDate.objects.get(pk=dateId)
                ProgressState.objects.update_or_create(contractid=contract ,dateid=date, 
                                                       defaults={
                                                       'plan_replan':'', 'pp_e':0, 'ap_e':0, 'pp_p':0, 'ap_p':0,  
                                                       'pp_c':0, 'ap_c':0, 'pp_t':0, 'ap_t':0, 'pr_t':0, 'pfc_t':0})
            
            progressStates = ProgressState.objects.filter(contractid__exact=contractId, dateid__lte=dateId).order_by('dateid')
            serializer = ProgressStateSerializer(instance=progressStates, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def contractMonthReportList(self, request, *args, **kwargs):
        try:
            contractId = int(kwargs["contractid"])
            dateId = int(kwargs["dateid"])
                   
            progressStates = ProgressState.objects.filter(contractid__exact=contractId, dateid__lte=dateId).order_by('-dateid')[:6:-1]
            serializer = ProgressStateReportSerializer(instance=progressStates, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
 
class TimeProgressStateAPI(viewsets.ModelViewSet):
    queryset = TimeprogressState.objects.all()
    serializer_class = TimeProgressStateSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    @action(detail=True, methods=['post'])
    def contractMonthList(self, request, *args, **kwargs):
        try:
            data = request.data
            userId = int(data["userid"])
            contractId = int(data["contractid"])
            dateId = int(data["dateid"])
            reportId = int(data["reportid"])
            
            SetReportVisit(userId, contractId, dateId, reportId)            
                       
            flg = 1	if TimeprogressState.objects.filter(contractid__exact=contractId, dateid__exact=dateId).count() > 0 else 0

            if flg == 0:
                contract = Contract.objects.get(pk=contractId)
                date = ReportDate.objects.get(pk=dateId)
                TimeprogressState.objects.update_or_create(contractid=contract ,dateid=date, 
                                                           defaults={'plan_replan':'', 'eep_date':None, 'eee_date':None, 
                                                           'epp_date':None, 'epe_date':None, 'ecp_date':None, 
                                                           'ece_date':None, 'epjp_date':None, 'epje_date':None})
            
            timeProgressStates = TimeprogressState.objects.filter(contractid__exact=contractId, dateid__lte=dateId).order_by('dateid')
            serializer = TimeProgressStateSerializer(instance=timeProgressStates, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InvoiceAPI(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    @action(detail=True, methods=['post'])
    def contractMonthList(self, request, *args, **kwargs):
        try:
            data = request.data
            userId = int(data["userid"])
            contractId = int(data["contractid"])
            dateId = int(data["dateid"])
            reportId = int(data["reportid"])
            
            SetReportVisit(userId, contractId, dateId, reportId)            
            
            flg = 1	if Invoice.objects.filter(contractid__exact=contractId, dateid__exact=dateId).count() > 0 else 0

            if flg == 0:
                contract = Contract.objects.get(pk=contractId)
                date = ReportDate.objects.get(pk=dateId)
                financialInfos = FinancialInfo.objects.filter(contractid__exact=contractId, dateid__exact=dateId)
                
                Invoice.objects.update_or_create(contractid=contract ,dateid=date, defaults={'senddate':None, 
                                        'aci_g_r':None, 'aci_n_r':financialInfos[0].lastverifiedinvoice_r if financialInfos and len(financialInfos) > 0 else 0, 
                                        'aci_g_fc':None, 'aci_n_fc':financialInfos[0].lastverifiedinvoice_fc if financialInfos and len(financialInfos) > 0 else 0,
                                        'aca_g_r':None, 'aca_n_r':financialInfos[0].lastverifiedadjustmentinvoice_r if financialInfos and len(financialInfos) > 0 else 0,
                                        'aca_g_fc':None, 'aca_n_fc':financialInfos[0].lastverifiedadjustmentinvoice_fc if financialInfos and len(financialInfos) > 0 else 0,
                                        'ew_g_r':None, 'ew_n_r':financialInfos[0].lastverifiedextraworkinvoice_r if financialInfos and len(financialInfos) > 0 else 0,
                                        'ew_g_fc':None, 'ew_n_fc':financialInfos[0].lastverifiedextraworkinvoice_fc if financialInfos and len(financialInfos) > 0 else 0,
                                        'icc_g_r':None, 'icc_n_r':financialInfos[0].lastclaimedinvoice_r if financialInfos and len(financialInfos) > 0 else 0,
                                        'icc_g_fc':None, 'icc_n_fc':financialInfos[0].lastclaimedinvoice_fc if financialInfos and len(financialInfos) > 0 else 0,
                                        'acc_g_r':None, 'acc_n_r':financialInfos[0].lastclaimedadjustmentinvoice_r if financialInfos and len(financialInfos) > 0 else 0,
                                        'acc_g_fc':None, 'acc_n_fc':financialInfos[0].lastclaimedadjustmentinvoice_fc if financialInfos and len(financialInfos) > 0 else 0,
                                        'ewcc_g_r':None, 'ewcc_n_r':financialInfos[0].lastclaimedextraworkinvoice_r if financialInfos and len(financialInfos) > 0 else 0,
                                        'ewcc_g_fc':None, 'ewcc_n_fc':financialInfos[0].lastclaimedextraworkinvoice_fc if financialInfos and len(financialInfos) > 0 else 0,
                                        'cvat_r':None, 'cvat_fc':None, 'cpi_r':None, 'cpi_fc':None, 'ccpi_a_r':None, 'ccpi_a_fc':None,
                                        'ccpi_a_vat_r':None, 'ccpi_a_vat_fc':None, 'ccpi_a_vat_ew_r':None, 'ccpi_a_vat_ew_fc':None, 
                                        'cp_pp_r':None, 'cp_pp_fc':None, 'pp_pp_r':None, 'pp_pp_fc':None, 'r':None, 'm':None, 'description':None})
            
            invoices = Invoice.objects.filter(contractid__exact=contractId, dateid__lte=dateId).order_by('dateid')
            serializer = InvoiceSerializer(instance=invoices, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def contractMonthReportList1(self, request, *args, **kwargs):
        try:
            contractId = int(kwargs["contractid"])
            dateId = int(kwargs["dateid"])
            
            invoice = Invoice.objects.filter(contractid__exact=contractId, dateid__exact=dateId)
            serializer = InvoiceReport1Serializer(instance=invoice[0] if len(invoice) > 0 else None, many=False)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def contractMonthReportList2(self, request, *args, **kwargs):
        try:
            contractId = int(kwargs["contractid"])
            dateId = int(kwargs["dateid"])
            
            invoices = Invoice.objects.filter(contractid__exact=contractId, dateid__lte=dateId).order_by('-dateid')[:9:-1]
            serializer = InvoiceReport2Serializer(instance=invoices, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FinancialInvoiceAPI(viewsets.ModelViewSet):
    queryset = FinancialInvoice.objects.all()
    serializer_class = FinancialInvoiceSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    @action(detail=True, methods=['post'])
    def contractMonthList(self, request, *args, **kwargs):
        try:
            data = request.data
            userId = int(data["userid"])
            contractId = int(data["contractid"])
            dateId = int(data["dateid"])
            reportId = int(data["reportid"])
            
            SetReportVisit(userId, contractId, dateId, reportId)            
            
            flg = 1	if FinancialInvoice.objects.filter(contractid__exact=contractId, dateid__exact=dateId).count() > 0 else 0

            if flg == 0:
                contract = Contract.objects.get(pk=contractId)
                date = ReportDate.objects.get(pk=dateId)
                FinancialInvoice.objects.update_or_create(contractid=contract ,dateid=date, defaults={'senddate':None, 'invoicetype':'', 'alino':None,
                                             'almino':None, 'aci_g_r':None, 'aci_g_fc':None, 'aca_g_r':None, 'aca_g_fc':None, 
                                             'ew_g_r':None, 'ew_g_fc':None, 'icc_g_r':None, 'icc_g_fc':None, 'acc_g_r':None, 
                                             'acc_g_fc':None, 'ewcc_g_r':None, 'ewcc_g_fc':None, 'aci_n_r':None, 'aci_n_fc':None,
                                             'aca_n_r':None, 'aca_n_fc':None, 'ew_n_r':None, 'ew_n_fc':None, 'icc_n_r':None, 
                                             'icc_n_fc':None, 'acc_n_r':None, 'acc_n_fc':None, 'ewcc_n_r':None, 'ewcc_n_fc':None, 
                                             'cvat_r':None, 'cvat_fc':None, 'cpi_r':None, 'cpi_fc':None, 'ccpi_a_r':None, 
                                             'ccpi_a_fc':None, 'ccpi_a_vat_r':None, 'ccpi_a_vat_fc':None, 'ccpi_a_vat_ew_r':None, 
                                             'ccpi_a_vat_ew_fc':None, 'cp_pp_r':None, 'cp_pp_fc':None, 'pp_pp_r':None, 
                                             'pp_pp_fc':None, 'r':None, 'm':None, 'typevalue':None})
            
            financialInvoices = FinancialInvoice.objects.filter(contractid__exact=contractId, dateid__lte=dateId).order_by('dateid')
            serializer = FinancialInvoiceSerializer(instance=financialInvoices, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def contractMonthReportList(self, request, *args, **kwargs):
        try:
            contractId = int(kwargs["contractid"])
            dateId = int(kwargs["dateid"])
            
            invoices = FinancialInvoice.objects.filter(contractid__exact=contractId, dateid__lte=dateId).order_by('-dateid')[:9:-1]
            serializer = FinancialInvoiceReportSerializer(instance=invoices, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WorkVolumeAPI(viewsets.ModelViewSet):
    queryset = WorkVolume.objects.all()
    serializer_class = WorkvolumeSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    @action(detail=True, methods=['post'])
    def contractMonthList(self, request, *args, **kwargs):
        try:
            data = request.data
            userId = int(data["userid"])
            contractId = int(data["contractid"])
            dateId = int(data["dateid"])
            reportId = int(data["reportid"])
            
            SetReportVisit(userId, contractId, dateId, reportId)            
            
            contract = Contract.objects.get(pk=contractId)
            date = ReportDate.objects.get(pk=dateId)

            flg = 0
            record_count = WorkVolume.objects.filter(contractid__exact=contractId, dateid__exact=dateId).count()
            last_date_id = ReportDate.objects.filter(dateid__lt=dateId).aggregate(Max('dateid'))['dateid__max']

            if WorkVolume.objects.filter(contractid__exact=contractId, dateid__exact=last_date_id).count() > 1:
                flg = 1	
                
            if record_count == 0:
                if flg == 0:
                    WorkVolume.objects.bulk_create([
                        WorkVolume(contractid=contract, dateid=date, work="خاکبرداری(متر مکعب)"),
                        WorkVolume(contractid=contract, dateid=date, work="خاکریزی(متر مکعب)"),
                        WorkVolume(contractid=contract, dateid=date, work="بتن ریزی(متر مکعب)"),
                        WorkVolume(contractid=contract, dateid=date, work="نصب اسکلت فلزی(تن)"),
                        WorkVolume(contractid=contract, dateid=date, work="نصب تجهبزات داخلی(تن)"),
                        WorkVolume(contractid=contract, dateid=date, work="نصب تجهیزات خارجی(تن)"),
                    ])
                else: 
                    workVolumes = WorkVolume.objects.filter(contractid__exact=contractId, dateid__exact=last_date_id)
                    for workvolume in workVolumes:
                        WorkVolume.objects.create(contractid=contract,  
                                                     dateid=date, 
                                                     work=workvolume.work, 
                                                     planestimate=workvolume.planestimate, 
                                                     totalestimate=workvolume.totalestimate,
                                                     executedsofar=workvolume.executedsofar)
                                    
            workVolumes = WorkVolume.objects.filter(contractid__exact=contractId, dateid__exact=dateId)
            serializer = WorkvolumeSerializer(instance=workVolumes, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def contractMonthReportList(self, request, *args, **kwargs):
        try:
            contractId = int(kwargs["contractid"])
            dateId = int(kwargs["dateid"])
            
            workVolumes = WorkVolume.objects.filter(contractid__exact=contractId, dateid__exact=dateId)
            serializer = WorkvolumeSerializer(instance=workVolumes, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PmsprogressAPI(viewsets.ModelViewSet):
    queryset = PmsProgress.objects.all()
    serializer_class = PmsprogressSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    @action(detail=True, methods=['post'])
    def contractMonthList(self, request, *args, **kwargs):
        try:
            data = request.data
            userId = int(data["userid"])
            contractId = int(data["contractid"])
            dateId = int(data["dateid"])
            reportId = int(data["reportid"])
            
            SetReportVisit(userId, contractId, dateId, reportId)            
            
            contract = Contract.objects.get(pk=contractId)
            date = ReportDate.objects.get(pk=dateId)

            flg = 0
            record_count = PmsProgress.objects.filter(contractid__exact=contractId, dateid__exact=dateId).count()
            last_date_id = ReportDate.objects.filter(dateid__lt=dateId).aggregate(Max('dateid'))['dateid__max']

            if PmsProgress.objects.filter(contractid__exact=contractId, dateid__exact=last_date_id).count() > 1:
                flg = 1	
                
            if record_count == 0:
                if flg == 0:
                    PmsProgress.objects.bulk_create([
                        PmsProgress(contractid=contract, dateid=date, item="کل کارهای سیویل"),
                        PmsProgress(contractid=contract, dateid=date, item="کل کارهای نصب"),
                        PmsProgress(contractid=contract, dateid=date, item="نصب اسکلت فلزی"),
                        PmsProgress(contractid=contract, dateid=date, item="بیل مکانیکی"),
                        PmsProgress(contractid=contract, dateid=date, item="نصب تجهیزات مکانیکال"),
                        PmsProgress(contractid=contract, dateid=date, item="نصب تجهیزات برق و ابزار دقیق"),
                        PmsProgress(contractid=contract, dateid=date, item="کل نصب تجهیزات داخلی (بدون در نظرگیری اسکلت فلزی)"),
                        PmsProgress(contractid=contract, dateid=date, item="کل نصب تجهیزات خارجی"),
                    ])
                else: 
                    pmsprogresses = PmsProgress.objects.filter(contractid__exact=contractId, dateid__exact=last_date_id)
                    for pmsprogress in pmsprogresses:
                        PmsProgress.objects.create(contractid=contract,  
                                                     dateid=date, item=pmsprogress.item, 
                                                     lastplanprogress=pmsprogress.lastplanprogress, 
                                                     lastplanvirtualprogress=pmsprogress.lastplanvirtualprogress)
                                    
            Pmsprogresses = PmsProgress.objects.filter(contractid__exact=contractId, dateid__exact=dateId)
            serializer = PmsprogressSerializer(instance=Pmsprogresses, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @action(detail=True, methods=['get'])
    def contractMonthReportList(self, request, *args, **kwargs):
        try:
            contractId = int(kwargs["contractid"])
            dateId = int(kwargs["dateid"])
                   
            Pmsprogresses = PmsProgress.objects.filter(contractid__exact=contractId, dateid__exact=dateId)
            serializer = PmsprogressSerializer(instance=Pmsprogresses, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 

class BudgetCostAPI(viewsets.ModelViewSet):
    queryset = Budgetcost.objects.all()
    serializer_class = BudgetCostSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    @action(detail=True, methods=['post'])
    def contractMonthList(self, request, *args, **kwargs):
        try:
            data = request.data
            userId = int(data["userid"])
            contractId = int(data["contractid"])
            dateId = int(data["dateid"])
            reportId = int(data["reportid"])
            
            SetReportVisit(userId, contractId, dateId, reportId)            
            
            flg = 1	if Budgetcost.objects.filter(contractid__exact=contractId, dateid__exact=dateId).count() > 0 else 0

            if flg == 0:
                contract = Contract.objects.get(pk=contractId)
                date = ReportDate.objects.get(pk=dateId)
                Budgetcost.objects.update_or_create(contractid=contract ,dateid=date, 
                                                    defaults={'bac_r':0, 'bac_fc':0, 'eac_r':0, 'eac_fc':0, 
                                                    'ev_r':0, 'ev_fc':0, 'ac_r':0, 'ac_fc':0, 'description':''})

            budgetCosts = Budgetcost.objects.filter(contractid__exact=contractId, dateid__lte=dateId).order_by('dateid')
            serializer = BudgetCostSerializer(instance=budgetCosts, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['put'])
    def setAdminDescription(self, request, *args, **kwargs):
        try:
            data = request.data
            contractId = int(data["contractid"])
            dateId = int(data["dateid"])
            description = str(data["description"])
            
            budget = Budgetcost.objects.get(contractid__exact=contractId, dateid__exact=dateId)
            budget.description = description
            budget.save()
            
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=True, methods=['get'])
    def contractMonthReportList(self, request, *args, **kwargs):
        try:
            contractId = int(kwargs["contractid"])
            dateId = int(kwargs["dateid"])
                   
            budgetcosts = Budgetcost.objects.filter(contractid__exact=contractId, dateid__lte=dateId).order_by('-dateid')[:6:-1]
            serializer = BudgetCostReportSerializer(instance=budgetcosts, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 

class MachineryAPI(viewsets.ModelViewSet):
    queryset = Machinary.objects.all()
    serializer_class = MachinerySerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    @action(detail=True, methods=['post'])
    def contractMonthList(self, request, *args, **kwargs):
        try:
            data = request.data
            userId = int(data["userid"])
            contractId = int(data["contractid"])
            dateId = int(data["dateid"])
            reportId = int(data["reportid"])
            
            SetReportVisit(userId, contractId, dateId, reportId)            
            
            contract = Contract.objects.get(pk=contractId)
            date = ReportDate.objects.get(pk=dateId)
            
            record_count = Machinary.objects.filter(contractid__exact=contractId, dateid__exact=dateId).count()
            last_date_id = ReportDate.objects.filter(dateid__lt=dateId).aggregate(Max('dateid'))['dateid__max']

            flg = 1	if Machinary.objects.filter(contractid__exact=contractId, dateid__exact=last_date_id).count() > 0 else 0
                
            if record_count == 0:
                if flg == 0:
                    Machinary.objects.bulk_create([
                        Machinary(contractid=contract, dateid=date, machine="تاور کرین"),
                        Machinary(contractid=contract, dateid=date, machine="بولدوزر"),
                        Machinary(contractid=contract, dateid=date, machine="لودر"),
                        Machinary(contractid=contract, dateid=date, machine="بیل مکانیکی"),
                        Machinary(contractid=contract, dateid=date, machine="غلطک"),
                        Machinary(contractid=contract, dateid=date, machine="گریدر"),
                        Machinary(contractid=contract, dateid=date, machine="کمپرسی دو محور"),
                        Machinary(contractid=contract, dateid=date, machine="جرثقیل"),
                        Machinary(contractid=contract, dateid=date, machine="تراک میکسر"),
                        Machinary(contractid=contract, dateid=date, machine="تانکر آبپاش"),
                        Machinary(contractid=contract, dateid=date, machine="تراکتور"),
                        Machinary(contractid=contract, dateid=date, machine="پمپ بتن"),
                        Machinary(contractid=contract, dateid=date, machine="آمبولانس"),
                        Machinary(contractid=contract, dateid=date, machine="ماشین آتشنشانی"),
                        Machinary(contractid=contract, dateid=date, machine="لودر""مینی بوس و اتوبوس"),                        
                        Machinary(contractid=contract, dateid=date, machine="انواع سواری"),
                        Machinary(contractid=contract, dateid=date, machine="دستگاه بچینگ"),
                        Machinary(contractid=contract, dateid=date, machine="دستگاه بلوک زنی"),
                        Machinary(contractid=contract, dateid=date, machine="دستگاه جدول زنی"),
                        Machinary(contractid=contract, dateid=date, machine="تانکر سوخت آب"),
                        Machinary(contractid=contract, dateid=date, machine="چکش مکانیکی"),
                    ])
                else: 
                    machineries = Machinary.objects.filter(contractid__exact=contractId, dateid__exact=last_date_id)
                    for machinery in machineries:
                        Machinary.objects.create(contractid=contract, dateid=date, 
                                                     machine=machinery.machine, activeno=machinery.activeno or 0, 
                                                     inactiveno=machinery.inactiveno or 0, description=machinery.description or '')
            
            machineries = Machinary.objects.filter(contractid__exact=contractId, dateid__exact=dateId)
            serializer = MachinerySerializer(instance=machineries, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
    @action(detail=True, methods=['get'])
    def contractMonthReportList(self, request, *args, **kwargs):
        try:
            contractId = int(kwargs["contractid"])
            dateId = int(kwargs["dateid"])            
            
            machineries = Machinary.objects.filter(contractid__exact=contractId, dateid__exact=dateId)
            serializer = MachinerySerializer(instance=machineries, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectPersonalAPI(viewsets.ModelViewSet):
    queryset = ProjectPersonnel.objects.all()
    serializer_class = ProjectPersonalSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    @action(detail=True, methods=['post'])
    def contractMonthList(self, request, *args, **kwargs):
        try:
            data = request.data
            userId = int(data["userid"])
            contractId = int(data["contractid"])
            dateId = int(data["dateid"])
            reportId = int(data["reportid"])
            
            SetReportVisit(userId, contractId, dateId, reportId)            
                        
            flg = 1	if ProjectPersonnel.objects.filter(contractid__exact=contractId, dateid__exact=dateId).count() > 0 else 0

            if flg == 0:
                contract = Contract.objects.get(pk=contractId)
                date = ReportDate.objects.get(pk=dateId)
                ProjectPersonnel.objects.update_or_create(contractid=contract ,dateid=date, 
                                                          defaults={'dpno':0 ,'dcpno':0 ,'mepno':0})
        
            projectPersonals = ProjectPersonnel.objects.filter(contractid__exact=contractId, dateid__lte=dateId).order_by('dateid')
            serializer = ProjectPersonalSerializer(instance=projectPersonals, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def contractMonthReportList(self, request, *args, **kwargs):
        try:
            contractId = int(kwargs["contractid"])
            dateId = int(kwargs["dateid"])
            
            projectPersonals = ProjectPersonnel.objects.filter(contractid__exact=contractId, dateid__lte=dateId).order_by('-dateid')[:9:-1]
            serializer = ProjectPersonalReportSerializer(instance=projectPersonals, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  

class ProblemAPI(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    @action(detail=True, methods=['post'])
    def contractMonthList(self, request, *args, **kwargs):
        try:
            data = request.data
            userId = int(data["userid"])
            contractId = int(data["contractid"])
            dateId = int(data["dateid"])
            reportId = int(data["reportid"])
            
            SetReportVisit(userId, contractId, dateId, reportId)
            
            problems = Problem.objects.filter(contractid__exact=contractId, dateid__exact=dateId)
            serializer = ProblemSerializer(problems, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @action(detail=True, methods=['get'])
    def contractMonthReportList(self, request, *args, **kwargs):
        try:
            contractId = int(kwargs["contractid"])
            dateId = int(kwargs["dateid"])
            
            problems = Problem.objects.filter(contractid__exact=contractId, dateid__exact=dateId)
            serializer = ProblemSerializer(problems, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
  
class CriticalActionAPI(viewsets.ModelViewSet):
    queryset = CriticalAction.objects.all()
    serializer_class = CriticalActionSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    @action(detail=True, methods=['post'])
    def contractMonthList(self, request, *args, **kwargs):
        try:
            data = request.data
            userId = int(data["userid"])
            contractId = int(data["contractid"])
            dateId = int(data["dateid"])
            reportId = int(data["reportid"])
            
            SetReportVisit(userId, contractId, dateId, reportId)            
            
            criticalActions = CriticalAction.objects.filter(contractid__exact=contractId, dateid__exact=dateId)
            serializer = CriticalActionSerializer(instance=criticalActions, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def contractMonthReportList(self, request, *args, **kwargs):
        try:
            contractId = int(kwargs["contractid"])
            dateId = int(kwargs["dateid"])
            
            criticalActions = CriticalAction.objects.filter(contractid__exact=contractId, dateid__exact=dateId)
            serializer = CriticalActionSerializer(instance=criticalActions, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

