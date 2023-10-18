from rest_framework import serializers

from projects.models import *


#=========== Contract Serializers ============
class ReportDateSerializerEx(serializers.ModelSerializer):
    shamsiDate = serializers.ReadOnlyField()
    class Meta:
        model = ReportDate
        fields = ('dateid', 'shamsiDate')
        

class ReportConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportConfirm
        fields = '__all__'  

        
class FinancialInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialInfo
        fields = '__all__'


class HseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hse
        fields = '__all__'
        
         
class ProgressStateSerializer(serializers.ModelSerializer):
    # row_number = serializers.ReadOnlyField() , "row_number"
    year = serializers.ReadOnlyField()
    month = serializers.ReadOnlyField()
    class Meta:
        model = ProgressState
        fields = ("progressstateid", "contractid", "dateid", "plan_replan", "pp_e", "ap_e", "pp_p", 
                    "ap_p", "pp_c", "ap_c", "pp_t", "ap_t", "pr_t", "pfc_t", "year", "month")         
         
         
class TimeProgressStateSerializer(serializers.ModelSerializer):
    year = serializers.ReadOnlyField()
    month = serializers.ReadOnlyField()
    eep_shamsiDate = serializers.ReadOnlyField()
    eee_shamsiDate = serializers.ReadOnlyField()
    epp_shamsiDate = serializers.ReadOnlyField()
    epe_shamsiDate = serializers.ReadOnlyField()
    ecp_shamsiDate = serializers.ReadOnlyField()
    ece_shamsiDate = serializers.ReadOnlyField()
    epjp_shamsiDate = serializers.ReadOnlyField()
    epje_shamsiDate = serializers.ReadOnlyField()
    class Meta:
        model = TimeprogressState
        fields = ("timeprogressstateid", "contractid", "dateid", "plan_replan", "eep_date", "eee_date", 
                    "epp_date", "epe_date", "ecp_date", "ece_date", "epjp_date", "epje_date", "year", "month",
                    "eep_shamsiDate", "eee_shamsiDate", "epp_shamsiDate", "epe_shamsiDate", "ecp_shamsiDate", 
                    "ece_shamsiDate", "epjp_shamsiDate", "epje_shamsiDate")


class InvoiceSerializer(serializers.ModelSerializer):
    # row_number = serializers.ReadOnlyField() , "row_number"
    class Meta:
        model = Invoice
        fields = ("invoiceid", "contractid", "dateid", "senddate", "aci_g_r", "aci_g_fc", "aca_g_r", "aca_g_fc", 
                    "ew_g_r", "ew_g_fc", "icc_g_r", "icc_g_fc", "acc_g_r", "acc_g_fc", "ewcc_g_r", "ewcc_g_fc", 
                    "aci_n_r", "aci_n_fc", "aca_n_r", "aca_n_fc", "ew_n_r", "ew_n_fc", "icc_n_r", "icc_n_fc", 
                    "acc_n_r", "acc_n_fc", "ewcc_n_r", "ewcc_n_fc", "cvat_r", "cvat_fc", "cpi_r", "cpi_fc", 
                    "ccpi_a_r", "ccpi_a_fc", "ccpi_a_vat_r", "ccpi_a_vat_fc", "ccpi_a_vat_ew_r", "ccpi_a_vat_ew_fc", 
                    "cp_pp_r", "cp_pp_fc", "pp_pp_r", "pp_pp_fc", "r", "m", "description")


class InvoiceExSerializer(serializers.ModelSerializer):
    # row_number = serializers.ReadOnlyField() , "row_number"
    class Meta:
        model = FinancialInvoice
        fields = ("invoiceid", "contractid", "dateid", "senddate", "invoicetype", "alino", "almino", "aci_g_r", 
                    "aci_g_fc", "aca_g_r", "aca_g_fc", "ew_g_r", "ew_g_fc", "icc_g_r", "icc_g_fc", "acc_g_r", 
                    "acc_g_fc", "ewcc_g_r", "ewcc_g_fc", "aci_n_r", "aci_n_fc", "aca_n_r", "aca_n_fc", "ew_n_r", 
                    "ew_n_fc", "icc_n_r", "icc_n_fc", "acc_n_r", "acc_n_fc", "ewcc_n_r", "ewcc_n_fc", "cvat_r", 
                    "cvat_fc", "cpi_r", "cpi_fc", "ccpi_a_r", "ccpi_a_fc", "ccpi_a_vat_r", "ccpi_a_vat_fc", 
                    "ccpi_a_vat_ew_r", "ccpi_a_vat_ew_fc", "cp_pp_r", "cp_pp_fc", "pp_pp_r", "pp_pp_fc", "r", "m", 
                    "typevalue")


class WorkvolumeSerializer(serializers.ModelSerializer):
    # row_number = serializers.ReadOnlyField() , "row_number"
    class Meta:
        model = WorkVolume
        fields = ("workvolumeid", "contractid", "dateid", "work", "planestimate", "totalestimate", "executedsofar")

    
class PmsprogressSerializer(serializers.ModelSerializer):
    # row_number = serializers.ReadOnlyField() , "row_number"
    class Meta:
        model = PmsProgress
        fields = ("pmsprogressid", "contractid", "dateid", "item", "lastplanprogress", "lastplanvirtualprogress")


class BudgetCostSerializer(serializers.ModelSerializer):
    # row_number = serializers.ReadOnlyField() , "row_number"
    year = serializers.ReadOnlyField()
    month = serializers.ReadOnlyField()

    class Meta:
        model = Budgetcost
        fields = ("budgetcostid", "contractid", "dateid", "bac_r", "bac_fc", 
                    "eac_r", "eac_fc", "ev_r", "ev_fc", "ac_r", "ac_fc", "description", "year", "month")


class MachinerySerializer(serializers.ModelSerializer):
    # row_number = serializers.ReadOnlyField() , "row_number"
    class Meta:
        model = Machinary
        fields = ("machinaryid", "contractid", "dateid", "machine", "activeno", "inactiveno", "description")


class ProjectPersonalSerializer(serializers.ModelSerializer):
    tpno = serializers.ReadOnlyField()
    year = serializers.ReadOnlyField()
    month = serializers.ReadOnlyField()

    # row_number = serializers.ReadOnlyField() , "row_number"
    class Meta:
        model = ProjectPersonnel
        fields = ("projectpersonelid", "contractid", "dateid", "dpno", "dcpno", "mepno", "tpno", "description", "year", "month")


class ProblemSerializer(serializers.ModelSerializer):
    # row_number = serializers.ReadOnlyField() , "row_number"
    class Meta:
        model = Problem
        fields = ("problemid", "contractid", "dateid", "problem")


class CriticalActionSerializer(serializers.ModelSerializer):
    # row_number = serializers.ReadOnlyField() , "row_number"
    class Meta:
        model = CriticalAction
        fields = ("criticalactionid", "contractid", "dateid", "criticalaction")
