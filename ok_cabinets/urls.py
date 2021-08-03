from django.urls import path
from .views import getUserById, getUsersPermissions, changeUserPermissions

urlpatterns = [
    path('ok_cabinets/api/getUserById',
         getUserById, name='getUserById'),
    path('ok_cabinets/api/getUsersPermissions',
         getUsersPermissions, name='getUsersPermissions'),
    path('ok_cabinets/api/changeUserPermissions',
         changeUserPermissions, name='changeUserPermissions'),
]
