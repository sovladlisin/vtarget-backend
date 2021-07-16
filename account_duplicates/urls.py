from django.urls import path
from .views import startAnalysis, getUserJob

urlpatterns = [
    path('account_duplicates/api/startAnalysis',
         startAnalysis, name='startAnalysis'),
    path('account_duplicates/api/getUserJob',
         getUserJob, name='getUserJob'),
]
