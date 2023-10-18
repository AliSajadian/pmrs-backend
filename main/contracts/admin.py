from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
PmrsUser = get_user_model()


class CompanyInline(admin.StackedInline):
    model = Company
    exclude = ["fax", "address"]

class CompanyTypeAdmin(admin.ModelAdmin):
    inlines = [
        CompanyInline,
    ]
    
admin.site.register(CompanyType, CompanyTypeAdmin)  

# @admin.register(CompanyType)
# class CompanyTypeAdmin(admin.ModelAdmin):
#     list_display = ('companytypeid', 'companytype') 
  
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('companyid', 'company', 'get_companyType')
    list_filter = ['companytypeid']
    search_fields = ['company']
    
    @admin.display(ordering='Company__CompanyType', description='company type')
    def get_companyType(self, obj):
        return obj.companytypeid.companytype

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('countryid', 'country') 
    
@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('currencyid', 'currency', 'get_country') 
    
    @admin.display(ordering='Currency__Country', description='country')
    def get_country(self, obj):
        return obj.countryid.country

# class PersonelInline(admin.TabularInline):
#     model = Personel
#     exclude = ["tel", "activity"]

# class PersoneltypeAdmin(admin.ModelAdmin):
#     inlines = [
#         PersonelInline,
#     ]
    
# admin.site.register(Personeltype, PersoneltypeAdmin)  

# @admin.register(Personeltype)
# class PersoneltypeAdmin(admin.ModelAdmin):
#     list_display = ('personeltypeid', 'personeltype') 
  
@admin.register(Personel)
class PersonelAdmin(admin.ModelAdmin):
    list_display = ('personelid', 'name', 'family', 'get_personelType')
    list_filter = ['personeltypeid']
    search_fields = ['family']
    
    @admin.display(ordering='Personel__Personeltype', description='personal type')
    def get_personelType(self, obj):
        return obj.personeltypeid.personeltype
    
@admin.register(ContractType)
class ContractTypeAdmin(admin.ModelAdmin):
    list_display = ('contracttypeid', 'contracttype') 
  
@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contractno', 'contract', 'get_contractType', 'duration')
    
    @admin.display(ordering='Contract__ContractType', description='contract type')
    def get_contractType(self, obj):
        return obj.contracttypeid.contracttype
    
# @admin.register(ContractUser)
# class ContractUserAdmin(admin.ModelAdmin):
#     list_display = ('contractuserid', 'get_user', 'get_contract')
#     list_filter = ['userid']
#     search_fields = ['contractid__contract']
    
#     @admin.display(ordering='ContractUser__Tblcontract', description='contract')
#     def get_contract(self, obj):
#         return obj.contractid.contract
    
#     @admin.display(ordering='ContractUser__PmrsUser', description='user')
#     def get_user(self, obj):
#         return obj.userid.username
    
@admin.register(EpcCorporation)
class EpcCorporationAdmin(admin.ModelAdmin):
    list_display = ('contractcorporationid', 'get_contract', 'get_company', 'e_percent', 'p_percent', 'c_percent') 
    list_filter = ['contractid']
    search_fields = ['companyid__company']
    
    @admin.display(ordering='EpcCorporation__Contract', description='contract')
    def get_contract(self, obj):
        return obj.contractid.contract
    
    @admin.display(ordering='EpcCorporation__Company', description='company')
    def get_company(self, obj):
        return obj.companyid.company
    
@admin.register(ContractConsultant)
class ContractConsultantAdmin(admin.ModelAdmin):
    list_display = ('contractconsultantid', 'get_contract', 'get_consultant') 
    list_filter = ['contractid', 'consultantid']
    search_fields = ['consultantid__company']
    
    @admin.display(ordering='ContractConsultant__Contract', description='contract')
    def get_contract(self, obj):
        return obj.contractid.contract
    
    @admin.display(ordering='ContractConsultant__Company', description='consultant')
    def get_consultant(self, obj):
        return obj.consultantid.company

# @admin.register(ContractCurrencies)
# class ContractCurrenciesAdmin(admin.ModelAdmin):
#     list_display = ('contractcurrencyid', 'get_contract', 'get_currency', 'price', 'date') 
    
#     @admin.display(ordering='ContractCurrencies__Contract', description='contract')
#     def get_contract(self, obj):
#         return obj.contractid.contract
    
#     @admin.display(ordering='ContractCurrencies__Currency', description='currency')
#     def get_currency(self, obj):
#         curr = Currency.objects.get(pk=obj.currencyid)
#         return curr.currency

@admin.register(Addendum)
class AddendumAdmin(admin.ModelAdmin):
    list_display = ('addendumid', 'get_contract', 'addendumamount_r', 'addendumamount_fc', 'addendumamountdate', 'afteraddendumdate') 
    
    @admin.display(ordering='Addendum__Contract', description='contract')
    def get_contract(self, obj):
        return obj.contractid.contract
