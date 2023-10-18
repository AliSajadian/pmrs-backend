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
    filename = serializers.ReadOnlyField()
    
    class Meta:
        model = ContractDox
        fields = ('contractdoxid', 'contractid', 'dateid', 'contractdate', 'contracttitle',  
                  'contractor', 'contractNo', 'riderno', 'filename', 'description', 'file', 'active')


class ProjectMonthlyDoxSerializers(serializers.ModelSerializer):
    year = serializers.ReadOnlyField()
    month = serializers.ReadOnlyField()
    filename = serializers.ReadOnlyField()
    
    class Meta:
        model = ProjectMonthlyDox
        fields = ('projectmonthlydoxid', 'contractid', 'dateid', 'year', 'month', 'filename', 'description', 'file', 'active')


class ApprovedInvoiceDoxSerializers(serializers.ModelSerializer):
    filename = serializers.ReadOnlyField()
    
    class Meta:
        model = InvoiceDox
        fields = ('invoicedoxid', 'contractid', 'dateid', 'invoiceKind', 'invoiceNo',
                  'invoiceDate', 'sendDate', 'confirmDate', 'sgp_r', 'sgp_fc', 'cgp_r', 'cgp_fc', 
                  'filename', 'description', 'file', 'active')


class ReportDoxSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReportDox
        fields = '__all__'
        

class ReportVisitSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReportVisit
        fields = '__all__'


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
       
        
# class BookingSerializer(ModelSerializer):
#     rooms = PrimaryKeyRelatedField(queryset=Room.objects.all(), many=True)
#     guest = GuestSerializer

#     class Meta:
#         model = Booking
#         fields = ['id', 'guest', 'rooms', 'booking_date', 'arrival_date', 'duration']

#     def validate(self, data):
#             rooms = data['rooms']
#             arrival_date = data['arrival_date']
#             duration = data['duration']

#             # CHECK WHETHER ROOMS LIST ARE BOOKED BEFORE
#             result = check_rooms_is_booked(rooms, arrival_date, duration)
#             if result != '':
#                 raise ValidationError(result)
#             return data    