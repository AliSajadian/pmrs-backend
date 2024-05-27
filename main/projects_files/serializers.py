from rest_framework import serializers

from projects_files.models import *


class HseReportDoxSerializers(serializers.ModelSerializer):
    year = serializers.ReadOnlyField()
    month = serializers.ReadOnlyField()
    filename = serializers.ReadOnlyField()
    
    class Meta:
        model = HseReportDox
        fields = ('hsereportdoxid', 'contractid', 'dateid', 'year', 'month', 'filename', 'description', 'file', 'active')


class ProjectDoxSerializers(serializers.ModelSerializer):
    filename = serializers.ReadOnlyField()
    
    class Meta:
        model = ProjectDox
        fields = ('projectdoxid', 'contractid', 'dateid', 'doctitle', 'dockind', 'docno', 'filename', 'file', 'active')


class ContractorDoxSerializers(serializers.ModelSerializer):
    contractshamsidate = serializers.ReadOnlyField()
    filename = serializers.ReadOnlyField()
    
    class Meta:
        model = ContractorDox
        fields = ('contractordoxid', 'contractid', 'contractdate', 'contractshamsidate',  
                  'contracttitle', 'contractor', 'contractno', 'riderno', 'file', 'filename')


class ProjectMonthlyDoxSerializers(serializers.ModelSerializer):
    year = serializers.ReadOnlyField()
    month = serializers.ReadOnlyField()
    filename = serializers.ReadOnlyField()
    
    class Meta:
        model = ProjectMonthlyDox
        fields = ('projectmonthlydoxid', 'contractid', 'dateid', 'year', 'month', 'filename', 'description', 'file', 'active')


class ApprovedInvoiceDoxSerializers(serializers.ModelSerializer):
    invoiceshamsidate = serializers.ReadOnlyField()
    sendshamsidate = serializers.ReadOnlyField()
    confirmshamsidate = serializers.ReadOnlyField()
    filename = serializers.ReadOnlyField()

    class Meta:
        model = InvoiceDox
        fields = ('invoicedoxid', 'contractid', 'dateid', 'invoicekind', 'invoiceno', 'invoicedate', 
                  'senddate', 'confirmdate', 'invoiceshamsidate', 'sendshamsidate', 'confirmshamsidate',  
                  'sgp_r', 'sgp_fc', 'cgp_r', 'cgp_fc', 'description', 'file', 'filename', 'active')


class ReportDoxSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReportDox
        fields = '__all__'
        

class ReportVisitSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReportVisit
        fields = '__all__'


class ZoneSerializers(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ('zoneid', 'zone')


class ZoneImagesSerializers(serializers.ModelSerializer):
    contract = serializers.ReadOnlyField
    zone = serializers.ReadOnlyField
    imagename1 = serializers.ReadOnlyField
    imagename2 = serializers.ReadOnlyField
    imagename3 = serializers.ReadOnlyField
    
    class Meta:
        model = ZoneImage
        fields = ('zoneimageid', 'zoneid', 'dateid', 'contract', 'zone', 'ppp', 'app', 'img1', 'imagepath1', 
                  'description1', 'img2', 'imagepath2', 'description2', 'img3', 'imagepath3', 'description3')
       

class ProjectZoneImagesSerializers(serializers.Serializer):
    contract = serializers.CharField()
    zone = serializers.CharField()
    ppp = serializers.CharField()
    app = serializers.CharField()
    img = serializers.CharField()
    description = serializers.CharField()

    
class ReportZoneImagesSerializers1(serializers.ModelSerializer):
    zone = serializers.ReadOnlyField
    explanation = serializers.ReadOnlyField

    class Meta:
        model = ZoneImage
        fields = ('zone', 'img1', 'img2', 'img3', 'explanation')
        
        
class ReportVisitSerializers(serializers.ModelSerializer):
    manager = serializers.ReadOnlyField
    class Meta:
        model = ReportVisit
        fields = ('manager', 'financialinfo', 'hse','progressstate', 'timeprogressstate', 'invoice', 
                  'financialinvoice', 'workvolume', 'pmsprogress', 'budget', 'machinary', 'personel', 
                  'problems', 'criticalactions', 'zoneimages', 'projectdox', 'durationdox', 'dashboard_r', 
                  'dashboard_fc', 'imagereport',)
     