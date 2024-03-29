from django.urls import path
from .views import toggleUserAdminRole, getUserMedals, getAllUsers, shutterUnbanUser, shutterBanUser, checkServiceRequest, editServiceInfo, getServiceInfo, login, addPostToken, deletePostToken, getServiceRequests, applyServiceRequest, acceptServiceRequest, denyServiceRequest

# urlpatterns = [path('api/vkUserPermissions',
#                     getPermissions, name='vkUserPermissions')]
urlpatterns = [
    path('auth/toggleUserAdminRole',
         toggleUserAdminRole, name='toggleUserAdminRole'),
    path('auth/login',
         login, name='login'),
    path('auth/addPostToken',
         addPostToken, name='addPostToken'),
    path('auth/deletePostToken',
         deletePostToken, name='deletePostToken'),


    path('auth/getAllUsers',
         getAllUsers, name='getAllUsers'),

    path('auth/getUserMedals',
         getUserMedals, name='getUserMedals'),


    path('auth/getServiceRequests',
         getServiceRequests, name='getServiceRequests'),
    path('auth/applyServiceRequest',
         applyServiceRequest, name='applyServiceRequest'),
    path('auth/acceptServiceRequest',
         acceptServiceRequest, name='acceptServiceRequest'),
    path('auth/denyServiceRequest',
         denyServiceRequest, name='denyServiceRequest'),
    path('auth/editServiceInfo',
         editServiceInfo, name='editServiceInfo'),
    path('auth/getServiceInfo',
         getServiceInfo, name='getServiceInfo'),
    path('auth/checkServiceRequest',
         checkServiceRequest, name='checkServiceRequest'),
    path('auth/shutterBanUser',
         shutterBanUser, name='shutterBanUser'),
    path('auth/shutterUnbanUser',
         shutterUnbanUser, name='shutterUnbanUser'),
]
