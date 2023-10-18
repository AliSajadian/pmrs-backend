from django.db import models
from django.db.models import F
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.utils.html import mark_safe

from contracts.models import Contract
# from django.contrib.auth import get_user_model
# Create your models here.

def upload_to(instance, filename):
    return "posts/{filename}".format(filename=filename)

def upload_path(instance, filename):
    return '/'.join(['user', instance.user_img, filename])
    
class PmrsUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **kwargs):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
            username=username,
            email=self.normalize_email(email), 
            is_staff=True, 
            is_superuser=True, 
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user
class PmrsUser(AbstractUser):
    user_img = models.ImageField(upload_to='user_images', null=True)
    priority = models.SmallIntegerField(db_column='Priority', default=0)  # Field name made lowercase.
    
    objects = PmrsUserManager()
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    
    def img_preview(self): #new
        if(self.user_img and self.user_img.url and hasattr(self.user_img, 'url')):
            image_url = self.user_img.url
            return mark_safe(f'<img src = "{image_url}" width = "120", alt="img"/>')
        else:
            return mark_safe(f'<img src = "/assets/user_images/asft.png" width = "120", alt="img"/>')
    
    def __str__(self):
        return self.username
    
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)


class User(models.Model):
    userid = models.IntegerField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    user = models.CharField(db_column='User', unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    passphrase = models.CharField(db_column='PassPhrase', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    active = models.BooleanField(db_column='Active')  # Field name made lowercase.
    priority = models.SmallIntegerField(db_column='Priority')  # Field name made lowercase.

    def __str__(self) -> str:
        return self.user
    
    class Meta:
        db_table = 'tbl_User'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Userlogin(models.Model):
    loginid = models.AutoField(db_column='LoginID', primary_key=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    enterdate = models.DateTimeField(db_column='EnterDate')  # Field name made lowercase.
    exitdate = models.DateTimeField(db_column='ExitDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'tbl_UserLogin'
        

class Role(models.Model):
    roleid = models.AutoField(db_column='RoleID', primary_key=True)  # Field name made lowercase.
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UserRole')
    role = models.CharField(db_column='Role', unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    def __str__(self) -> str:
        return self.role
    
    class Meta:
        db_table = 'tbl_Role'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
   
        
class Permission(models.Model):
    permissionid = models.AutoField(db_column='PermissionID', primary_key=True)  # Field name made lowercase.
    role = models.ManyToManyField(Role, through='RolePermission')
    permission = models.CharField(db_column='Permission', unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    def __str__(self) -> str:
        return self.permission
    
    class Meta:
        db_table = 'tbl_Permission'
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'


class UserRole(models.Model):
    userroleid = models.AutoField(db_column='UserRoleID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="User_UserRole", on_delete=models.PROTECT, db_column='UserID')  # Field name made lowercase.
    contractid = models.ForeignKey(Contract, related_name="Contract_UserRole", on_delete=models.PROTECT, blank=True, null=True, db_column='ContractID')  # Field name made lowercase.
    roleid = models.ForeignKey(Role, related_name="Role_UserRole", on_delete=models.PROTECT, db_column='RoleID')  # Field name made lowercase.
    all_projects = models.BooleanField(db_column='AllProjects', default=False, null=True)

    def permissions(self):
        # permissions = RolePermission.objects.filter(roleid__exact=self.roleid.roleid).values('permissionid')
        
        permissions = RolePermission.objects.filter(roleid__exact=self.roleid.roleid).values(
            'permissionid__permission').annotate(permission = F('permissionid__permission')).values('permission')
        return permissions
        
    class Meta:
        db_table = 'tbl_JUserRole'
        verbose_name = 'User_Contract_Role'
        verbose_name_plural = 'User_Contracts_Roles'
        

class RolePermission(models.Model):
    rolepermissionid = models.AutoField(db_column='RolePermissionID', primary_key=True)  # Field name made lowercase.
    roleid = models.ForeignKey(Role, related_name="Role_RolePermission", on_delete=models.PROTECT, db_column='RoleID')  # Field name made lowercase.
    permissionid = models.ForeignKey(Permission, related_name="Permission_RolePermission", on_delete=models.PROTECT, db_column='PermissionID')  # Field name made lowercase.

    class Meta:
        db_table = 'tbl_JRolePermission'
        verbose_name = 'Role_Permission'
        verbose_name_plural = 'Role_Permissions'


