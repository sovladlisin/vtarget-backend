from django.urls import path
from .views import getAppList, updateIds, getAppAnayzeStatus, analyzeApps

urlpatterns = [
    path('app_stats/api/getAppList',
         getAppList, name='getAppList'),
    path('app_stats/api/updateIds',
         updateIds, name='updateIds'),
    path('app_stats/api/getAppAnayzeStatus',
         getAppAnayzeStatus, name='getAppAnayzeStatus'),
    path('app_stats/api/analyzeApps',
         analyzeApps, name='analyzeApps'),
]
