from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import *
from django.conf import settings
from knox.models import AuthToken
from .models import *


# from django.contrib.auth import get_user_model
# PmrsUser = get_user_model()

class PmrsUserAdmin(UserAdmin):
    list_display = ('username', 'get_roles', 'email', 'full_name', 'is_active', 'priority', 'img_preview')
    readonly_fields = ['is_staff', 'is_superuser', 'img_preview', 'last_login', 'date_joined']
    list_filter = ['is_active'] 
    search_fields = ['username']
    
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     else:
    #         return qs.filter(user__is_superuser__exact=False)
    
    def get_roles(self, obj):
        return ", ".join([r.role for r in obj.role_set.all()])
    get_roles.short_description = "Roles"

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'priority'
                # 'groups', 'user_permissions'
                )
        }),
        # ('Important dates', {
        #     'fields': ('last_login', 'date_joined')
        # }),
        ('User image', {
            'fields': ( 'img_preview', 'user_img')
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'priority'
                # 'groups', 'user_permissions'
                )
        }),
        # ('Important dates', {
        #     'fields': ('last_login', 'date_joined')
        # }),
        ('User image', {
            'fields': ( 'img_preview', 'user_img')
        })
    )


class UserAdmin(admin.ModelAdmin):
    list_display = ('userid', 'user', 'get_roles', 'active', 'priority')
    list_filter = ['active']
    search_fields = ['user']
    
    def get_roles(self, obj):
        return ", ".join([r.role for r in obj.role_set.all()])
    get_roles.short_description = "Roles"
    
    
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role', 'get_permissions', 'description')
    search_fields = ['role']

    def get_permissions(self, obj):
        return ", ".join([p.permission for p in obj.permission_set.all()])
    get_permissions.short_description = "Permissions"
    
    
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('permission', 'description')
    search_fields = ['permission']
        
    
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'get_contract', 'get_role')
    list_filter = ['userid','contractid','roleid']
    search_fields = ['userid__username']
    
    @admin.display(ordering='UserRole__PmrsUser', description='user')
    def get_user(self, obj):
        return obj.userid.username

    @admin.display(ordering='UserRole__Contract', description='contract')
    def get_contract(self, obj):
        return obj.contractid.contract if obj.contractid is not None else None
        
    @admin.display(ordering='UserRole__Role', description='role')
    def get_role(self, obj):
        return obj.roleid.role


class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('get_role', 'get_permission')
    list_filter = ['permissionid']
    search_fields = ['roleid__role']
    
    @admin.display(ordering='RolePermission__Role', description='role')
    def get_role(self, obj):
        return obj.roleid.role
    
    @admin.display(ordering='RolePermission__Permission', description='permission')
    def get_permission(self, obj):
        return obj.permissionid.permission
 
    
def get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request, app_label)
    
    if not app_dict:
        return
        
    NEW_ADMIN_ORDERING = []
    if app_label:
        for ao in settings.ADMIN_ORDERING:
            if ao[0] == app_label:
                NEW_ADMIN_ORDERING.append(ao)
                break
    
    if not app_label:
        for app_key in list(app_dict.keys()):
            if not any(app_key in ao_app for ao_app in settings.ADMIN_ORDERING):
                app_dict.pop(app_key)
    
    app_list = sorted(
        app_dict.values(), 
        key=lambda x: [ao[0] for ao in settings.ADMIN_ORDERING].index(x['app_label'])
    )
     
    for app, ao in zip(app_list, NEW_ADMIN_ORDERING or settings.ADMIN_ORDERING):
        if app['app_label'] == ao[0]:
            for model in list(app['models']):
                if not model['object_name'] in ao[1]:
                    app['models'].remove(model)
        app['models'].sort(key=lambda x: ao[1].index(x['object_name']))
    return app_list

admin.site.empty_value_display = "(None)"
admin.site.site_header = 'PMRS Admin Panel'
admin.site.site_title = 'PMRS'
admin.site.site_url = None
admin.AdminSite.get_app_list = get_app_list

# admin.site.register(User, UserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(RolePermission, RolePermissionAdmin)

# admin.py
# admin.site.unregister(User)
admin.site.register(PmrsUser, PmrsUserAdmin)
admin.site.unregister(Group)
admin.site.unregister(AuthToken)


