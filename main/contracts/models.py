import django
from django.db import models
from django.db.models import Sum, Max
from django.conf import settings
from django.utils import timezone
from dateutil import relativedelta
from datetime import datetime
from datetime import date

# from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from accounts.models import *
from .services import GregorianToShamsi
# Create your models here.

class CompanyType(models.Model):
    companytypeid = models.AutoField(db_column='CompanyTypeID', primary_key=True)  
    companytype = models.CharField(db_column='CompanyType', unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  

    def __str__(self) -> str:
        return self.companytype
    
    class Meta:
        db_table = 'tbl_CompanyType'
        verbose_name = 'CompanyType'
        verbose_name_plural = 'CompanyTypes'

        
class Company(models.Model):
    companyid = models.AutoField(db_column='CompanyID', primary_key=True)  
    companytypeid = models.ForeignKey(CompanyType, models.DO_NOTHING, db_column='CompanyTypeID')  
    company = models.CharField(db_column='Company', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')  
    tel = models.CharField(db_column='Tel', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  
    fax = models.CharField(db_column='Fax', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  
    email = models.CharField(db_column='Email', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  
    address = models.CharField(db_column='Address', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  

    def __str__(self) -> str:
        return self.company
    
    class Meta:
        db_table = 'tbl_Company'
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Personeltype(models.Model):
    personeltypeid = models.AutoField(db_column='PersonelTypeID', primary_key=True)  
    personeltype = models.CharField(db_column='PersonelType', unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  

    def __str__(self) -> str:
        return self.personeltype
    
    class Meta:
        db_table = 'tbl_PersonelType'
        verbose_name = 'PersonalType'
        verbose_name_plural = 'PersonalTypes'

        
class Personel(models.Model):
    personelid = models.IntegerField(db_column='PersonelID', primary_key=True)  
    name = models.CharField(db_column='Name', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  
    family = models.CharField(db_column='Family', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  
    personeltypeid = models.ForeignKey(Personeltype, models.DO_NOTHING, db_column='PersonelTypeID')  
    tel = models.CharField(db_column='Tel', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  
    activity = models.CharField(db_column='Activity', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  
    active = models.BooleanField(db_column='Active')  

    def __str__(self) -> str:
        return '%s %s' % (self.name, self.family)
    
    class Meta:
        db_table = 'tbl_Personel'
        verbose_name = 'Personal'
        verbose_name_plural = 'Personals'        
      
   
class ContractType(models.Model):
    contracttypeid = models.AutoField(db_column='ContractTypeID', primary_key=True)  
    contracttype = models.CharField(db_column='ContractType', unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  

    def __str__(self) -> str:
        return self.contracttype

    class Meta:
        db_table = 'tbl_ContractType'
        verbose_name = 'ContractType'
        verbose_name_plural = 'ContractTypes'
        
        
class Country(models.Model):
    countryid = models.AutoField(db_column='CountryID', primary_key=True)  
    country = models.CharField(db_column='Country', unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  

    def __str__(self):
        return self.country
    
    class Meta:
        db_table = 'tbl_Country'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class Currency(models.Model):
    currencyid = models.AutoField(db_column='CurrencyID', primary_key=True)  
    # countryid = models.ForeignKey(Country, models.DO_NOTHING, db_column='CountryID')  
    country =  models.CharField(db_column='Country', max_length=50, null=True, db_collation='SQL_Latin1_General_CP1_CI_AS')  
    currency = models.CharField(db_column='Currency', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  

    def __str__(self) -> str:
        return self.currency
    
    class Meta:
        db_table = 'tbl_Currency'
        # unique_together = (('country', 'currency'),)
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'


class Contract(models.Model):
    contractid = models.AutoField(db_column='ContractID', primary_key=True)  
    contractno = models.CharField(db_column='ContractNo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  
    contracttypeid = models.ForeignKey(ContractType, related_name="ContractType_Contract", on_delete=models.CASCADE, db_column='ContractTypeID')  
    projectmanagerid = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="ProjectManager_Contract", on_delete=models.CASCADE, db_column='ProjectManagerID')  
    customerid = models.ForeignKey(Company, related_name="Customer_Contract", on_delete=models.CASCADE, db_column='CustomerID')  
    coordinatorid = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="Coordinator_Contract", on_delete=models.CASCADE, db_column='CoordinatorID', blank=True, null=True)  
    currencyid = models.ForeignKey(Currency, related_name="Currency_Contract", on_delete=models.CASCADE, db_column='CurrencyID', blank=True, null=True)  
    contract = models.CharField(db_column='Contract', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS')  
    startoperationdate = models.DateField(db_column='StartOperationDate', blank=True, null=True)  
    finishdate = models.DateField(db_column='FinishDate', blank=True, null=True)  
    notificationdate = models.DateField(db_column='NotificationDate', blank=True, null=True)  
    validationdate = models.DateField(db_column='ValidationDate', blank=True, null=True)  
    planstartdate = models.DateField(db_column='PlanStartDate', blank=True, null=True)  
    startdate = models.DateField(db_column='StartDate', blank=True, null=True)  
    duration = models.IntegerField(db_column='Duration', blank=True, null=True)  
    prepaymentpercent = models.FloatField(db_column='PrePaymentPercent', blank=True, null=True)  
    insurancepercent = models.FloatField(db_column='InsurancePercent', blank=True, null=True)  
    perforcebondpercent = models.FloatField(db_column='PerforceBondPercent', blank=True, null=True)  
    withholdingtaxpercent = models.FloatField(db_column='WithholdingTaxPercent', blank=True, null=True)  
    contractamount_r = models.BigIntegerField(db_column='ContractAmount_R', blank=True, null=True)  
    contractamount_fc = models.BigIntegerField(db_column='ContractAmount_FC', blank=True, null=True)  
    schedulelevel = models.SmallIntegerField(db_column='ScheduleLevel')  
    version = models.IntegerField(db_column='Version')  
    currencybprice = models.IntegerField(db_column='CurrencyBPrice', blank=True, null=True)  
    currencyuprice = models.IntegerField(db_column='CurrencyUPrice', blank=True, null=True)  
    attachmentcontractprice1_r = models.BigIntegerField(db_column='AttachmentContractPrice1_R', blank=True, null=True)  
    attachmentcontractprice1_fc = models.BigIntegerField(db_column='AttachmentContractPrice1_FC', blank=True, null=True)  
    attachmentcontractprice2_r = models.BigIntegerField(db_column='AttachmentContractPrice2_R', blank=True, null=True)  
    attachmentcontractprice2_fc = models.BigIntegerField(db_column='AttachmentContractPrice2_FC', blank=True, null=True)  
    attachmentcontractprice3_r = models.BigIntegerField(db_column='AttachmentContractPrice3_R', blank=True, null=True)  
    attachmentcontractprice3_fc = models.BigIntegerField(db_column='AttachmentContractPrice3_FC', blank=True, null=True)  
    attachmentcontractprice4_r = models.BigIntegerField(db_column='AttachmentContractPrice4_R', blank=True, null=True)  
    attachmentcontractprice4_fc = models.BigIntegerField(db_column='AttachmentContractPrice4_FC', blank=True, null=True)  
    attachmentcontractprice5_r = models.BigIntegerField(db_column='AttachmentContractPrice5_R', blank=True, null=True)  
    attachmentcontractprice5_fc = models.BigIntegerField(db_column='AttachmentContractPrice5_FC', blank=True, null=True) 
    location = models.CharField(db_column='Location', max_length=20, null=True)
    latitude =  models.FloatField(db_column='Latitude', null=True)
    longitude =  models.FloatField(db_column='Longitude', null=True)
    iscompleted = models.BooleanField(db_column='IsCompleted', blank=True, null=True)  
    completeddate = models.IntegerField(db_column='CompletedDate', blank=True, null=True)  
 
    def contractamount_r_(self):
        return f"{self.contractamount_r:,}"

    def contractamount_fc_(self):
        return f"{self.contractamount_fc:,}"
    
    def extraWorkPrice_r(self):
        addendumamount_r_sum = Addendum.objects.filter(
            contractid__exact=self.contractid).aggregate(Sum('addendumamount_r'))['addendumamount_r__sum']
        result = (addendumamount_r_sum or 0)
        return f"{result:,}"

    def totalprice_r(self):
        addendumamount_r_sum = Addendum.objects.filter(
            contractid__exact=self.contractid).aggregate(Sum('addendumamount_r'))['addendumamount_r__sum']
        result = self.contractamount_r + (addendumamount_r_sum or 0)
        return f"{result:,}"

    def extraWorkPrice_fc(self):
        addendumamount_fc_sum = Addendum.objects.filter(
            contractid__exact=self.contractid).aggregate(Sum('addendumamount_fc'))['addendumamount_fc__sum']
        result = (addendumamount_fc_sum or 0)
        return f"{result:,}"

    def totalprice_fc(self):
        addendumamount_fc_sum = Addendum.objects.filter(
            contractid__exact=self.contractid).aggregate(Sum('addendumamount_fc'))['addendumamount_fc__sum']
        result = self.contractamount_fc + (addendumamount_fc_sum or 0)
        return f"{result:,}"
        
    def projectManager(self):
        # personal = Personel.objects.get(pk=self.projectmanagerid)
        #  self.projectmanagerid.__str__()
        return '%s %s' % (self.projectmanagerid.first_name, self.projectmanagerid.last_name) if self.projectmanagerid is not None else ''
    
    def projectManagerImage(self):
        # image_url = (self.projectmanagerid.user_img.url or "")
        # return mark_safe(f'<img src = "{image_url}" width = "120", alt="img"/>')
        user = get_user_model().objects.get(pk=self.projectmanagerid.id)
        if user.user_img:
            return (user.user_img.url or None)
        else:
            return None
    
    def customer(self):
        # customer = Company.objects.get(pk=self.customerid)
        return self.customerid.company if self.customerid is not None else ''
    
    def currency(self):
        # currency = Currency.objects.get(pk=self.currencyid)
        return self.currencyid.currency if self.currencyid is not None else ''
    
    def startOperationShamsiDate(self):
        return GregorianToShamsi(self.startoperationdate) if self.startoperationdate is not None else ''           

    def notificationShamsiDate(self):
        return GregorianToShamsi(self.notificationdate) if self.notificationdate is not None else ''
    
    def finishShamsiDate(self):
        return GregorianToShamsi(self.finishdate) if self.finishdate is not None else ''

    def planStartShamsiDate(self):
        return GregorianToShamsi(self.planstartdate) if self.planstartdate is not None else ''
    
    def passedDuration(self):
        if not self.iscompleted and self.startdate is not None:
            date_format = "%Y-%m-%d"
            now = datetime.strptime(str(datetime.now().date()), date_format)
            startdate = datetime.strptime(str(self.startdate), date_format)
            months = (now.year - startdate.year) * 12 + (now.month - startdate.month)
            return months
            # relativedelta = (date.today, self.startdate)
            # diff = relativedelta.relativedelta(now, startdate)
            # return diff.months + diff.years * 12
        else:
            return self.duration 

    def approximateFinishShamsiDate(self):
        afteraddendumdate_max = Addendum.objects.filter(
            contractid__exact=self.contractid).aggregate(Max('afteraddendumdate'))['afteraddendumdate__max']
        
        if afteraddendumdate_max is None:
            return GregorianToShamsi(self.finishdate) if self.finishdate is not None else ''
        else:
            return GregorianToShamsi(afteraddendumdate_max)

    def addendumDuration(self):
        afteraddendumdate_max = Addendum.objects.filter(
            contractid__exact=self.contractid).aggregate(Max('afteraddendumdate'))['afteraddendumdate__max']
        
        if afteraddendumdate_max is None:
            return 0
        
        date_format = "%Y-%m-%d"
        now = datetime.strptime(str(afteraddendumdate_max), date_format)
        startdate = datetime.strptime(str(self.finishdate), date_format)
        months = (now.year - startdate.year) * 12 + (now.month - startdate.month)
        return months
    
    def __str__(self) -> str:
        return self.contract
    
    def roles(self):
        roles = Contract.objects.filter(Contract_UserRole__contractid__exact=self.contractid).values(
            'Contract_UserRole__roleid__role').annotate(
                role = F('Contract_UserRole__roleid__role')).values('role')
        # roleid_set__tbljrolepermission__permissionid__permission    permission
        return roles

    def contracttype(self):
        return self.contracttypeid.contracttype if self.contracttypeid is not None else ''
        
    class Meta:
        db_table = 'tbl_Contract'
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'


class ContractUser(models.Model):
    contractuserid = models.AutoField(db_column='ContractUserID', primary_key=True)  
    contractid = models.ForeignKey(Contract, models.DO_NOTHING, db_column='ContractID')  
    userid = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='UserID')  
    type = models.BooleanField(db_column='Type', blank=True, null=True)  
    
    class Meta:
        db_table = 'tbl_JContractUser'
        verbose_name = 'Contract_User'
        verbose_name_plural = 'Contract_Users'


class EpcCorporation(models.Model):
    contractcorporationid = models.AutoField(db_column='ContractCorporationID', primary_key=True)  
    contractid = models.ForeignKey(Contract, related_name="Contract_Corporation", on_delete=models.CASCADE, db_column='ContractID')  
    companyid = models.ForeignKey(Company, related_name="Company_Corporation", on_delete=models.CASCADE, db_column='CompanyID')  
    e_percent = models.FloatField(db_column='E_Percent')  
    p_percent = models.FloatField(db_column='P_Percent')  
    c_percent = models.FloatField(db_column='C_Percent')  
    
    def __str__(self) -> str:
        return '%s: e=%s, p=%s, c=%s' % (self.companyid.company, self.e_percent, self.p_percent, self.c_percent)

    def E(self):
        e = EpcCorporation.objects.filter(contractid__exact=self.contractid, e_percent__gt=0).values(
            'companyid__company', 'e_percent').annotate( value = F('e_percent'), 
                                                        name = F('companyid__company')).values('value', 'name')  
        return (e)
    
    def P(self):
        p = EpcCorporation.objects.filter(contractid__exact=self.contractid, p_percent__gt=0).values(
            'companyid__company', 'p_percent').annotate( value = F('p_percent'), 
                                                        name = F('companyid__company')).values('value', 'name')  
        return (p)

    def C(self):
        c = EpcCorporation.objects.filter(contractid__exact=self.contractid, c_percent__gt=0).values(
            'companyid__company', 'c_percent').annotate( value = F('c_percent'), 
                                                        name = F('companyid__company')).values('value', 'name')  
        return (c)
        
    def company(self):
        return self.companyid.company
    
    class Meta:
        db_table = 'tbl_Corporation'
        verbose_name = 'Contract_Corporation'
        verbose_name_plural = 'Contract_Corporations'

# date.today()
class Addendum(models.Model):
    addendumid = models.AutoField(db_column='AddendumID', primary_key=True)  
    contractid = models.ForeignKey(Contract,related_name="Contract_Addendum", on_delete=models.PROTECT, db_column='ContractID')  
    addendumamount_r = models.BigIntegerField(db_column='AddendumAmount_R', null=True)  
    addendumamount_fc = models.IntegerField(db_column='AddendumAmount_FC', null=True)  
    addendumamountdate = models.DateField(db_column='AddendumAmountDate', default=django.utils.timezone.now, null=True)  
    afteraddendumdate = models.DateField(db_column='AfterAddendumDate', null=True)  

    def afteraddendumshamsidate(self):
        return GregorianToShamsi(self.afteraddendumdate) if self.afteraddendumdate is not None else ''

    class Meta:
        db_table = 'tbl_Addendum'
        verbose_name = 'Contract_Addendum'
        verbose_name_plural = 'Contract_Addendums'


class ContractCurrencies(models.Model):
    contractcurrencyid = models.AutoField(db_column='ContractCurrencyID', primary_key=True)  
    contractid = models.ForeignKey(Contract, models.DO_NOTHING, db_column='ContractID')  
    currencyid = models.IntegerField(db_column='CurrencyID')  
    price = models.IntegerField(db_column='Price')  
    date = models.DateField(db_column='Date')  

    class Meta:
        db_table = 'tbl_JContractCurrencies'
        verbose_name = 'Contract_Currency'
        verbose_name_plural = 'Contract_Currencies'


class ContractConsultant(models.Model):
    contractconsultantid = models.AutoField(db_column='ContractConsultantID', primary_key=True)  
    contractid = models.ForeignKey(Contract, models.DO_NOTHING, db_column='ContractID')  
    consultantid = models.ForeignKey(Company, models.DO_NOTHING, db_column='ConsultantID')  

    def consultant(self):
        try:
            return (self.consultantid.company if self.consultantid.company is not None else '') if self.consultantid is not None else ''
        except:
            return ''
            
        
    class Meta:
        db_table = 'tbl_JContractConsultant'
        verbose_name = 'Contract_Consultant'
        verbose_name_plural = 'Contract_Consultants'
 

class ContractContractor(models.Model):
    contractcontractorid = models.AutoField(db_column='ContractContractorID', primary_key=True)  
    contractid = models.IntegerField(db_column='ContractID')  
    contractorid =models.IntegerField(db_column='ContractorID')  

    class Meta:
        db_table = 'tbl_JContractContractor'


class DateConversion(models.Model):
    shamsidate = models.CharField(db_column='ShamsiDate', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  
    georgiandate = models.CharField(db_column='GeorgianDate', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  
    tmonth = models.CharField(db_column='tMonth', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS')  
    monthtext = models.CharField(db_column='MonthText', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  
    month = models.SmallIntegerField(db_column='Month')  
    year = models.IntegerField(db_column='Year')  

    class Meta:
        db_table = 'tbl_DateConvertion'


class FinancialDocuments(models.Model):
    documentid = models.IntegerField(db_column='DocumentID', primary_key=True)  
    documentno = models.IntegerField(db_column='DocumentNo')  
    doctype = models.CharField(db_column='DocType', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  
    description = models.CharField(db_column='Description', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  
    date = models.CharField(db_column='Date', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  
    contractno = models.CharField(db_column='ContractNo', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  
    contract = models.CharField(db_column='Contract', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  
    definitiveid = models.IntegerField(db_column='DefinitiveID')  
    definitive = models.CharField(db_column='Definitive', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  
    acp = models.BigIntegerField(db_column='ACP')  
    acz = models.BigIntegerField(db_column='ACZ')  
    retrievedate = models.DateField(db_column='RetrieveDate')  
    iscompleted = models.BooleanField(db_column='IsCompleted')  
    tmp = models.BooleanField()
    costcenterid = models.IntegerField(db_column='CostCenterID', blank=True, null=True)  
    costcenter = models.CharField(db_column='CostCenter', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  

    class Meta:
        db_table = 'tbl_FinancialDocuments'

