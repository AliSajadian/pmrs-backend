from rest_framework import routers
from django.urls import path, include
from knox import views as knox_views

from .api import *
# PasswordAPIView, RegisterAPI, LoginAPI, LoginExAPI, UserAPI, UserCreateAPI, UserDeleteAPI, \
#     EmployeeImageDownloadListAPIView, UserGroupsAPI, GroupPermissionsAPI, UserPermissionsAPI, FileDownloadListAPIView, UserResetPassword
       
router = routers.DefaultRouter()
router.register('api/auth/users', UserAPI, 'users')
router.register('api/auth/groups', GroupAPI, 'groups')
router.register('api/auth/usergroups', UserGroupsAPI, 'usergroups')
router.register('api/auth/permissions', PermissionAPI, 'permissions')
router.register('api/auth/grouppermissions', GroupPermissionsAPI, 'grouppermissions')

urlpatterns = [
    # path('api/auth', include(routers.urls)),
    path('api/auth', include('knox.urls')),
    path('api/auth/login', LoginAPI.as_view()),
    path("api/auth/changePassword", PasswordAPIView.as_view(), name="changePassword"),
    
    # path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),

    # path('api/auth/user', UserAPI),
    # path('api/auth/adduserex', UserCreateAPI.as_view()),
    # path('api/auth/userex/<int:pk>', UserDeleteAPI.as_view(), name="userex/<pk>/"),
    # path('api/auth/resetpassword/<int:pk>', UserResetPassword.as_view(), name="resetpassword/<pk>/"),
    # path('api/auth/usergroups/<int:pk>', UserGroupsAPI.as_view(), name="usergroups/<pk>/"),
    # path('api/auth/grouppermissions/<int:pk>', GroupPermissionsAPI.as_view(), name="grouppermissions/<pk>/"),
    # path('api/auth/userpermissions/<int:pk>', UserPermissionsAPI.as_view(), name="userpermissions/<pk>/"),
]

# urlpatterns.extend(router)  , name="guestmealdays/(?P<selectedDate>[\w\-]+)/$"
urlpatterns += router.urls

