from django.urls import path
from .views import getAppList, updateIds, getAppAnalyzeStatus, analyzeApps, getExcelIds

urlpatterns = [
    path('app_stats/api/getAppList',
         getAppList, name='getAppList'),
    path('app_stats/api/updateIds',
         updateIds, name='updateIds'),
    path('app_stats/api/getAppAnalyzeStatus',
         getAppAnalyzeStatus, name='getAppAnalyzeStatus'),
    path('app_stats/api/analyzeApps',
         analyzeApps, name='analyzeApps'),
    path('app_stats/api/getExcelIds',
         getExcelIds, name='getExcelIds'),
]
