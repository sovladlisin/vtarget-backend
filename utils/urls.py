from django.urls import path
from .views import searchVtarget, getRandWord, searchShutterstock, getTagJobStatus, startCollectTagsJob
from .certificates import runLegacyRequest, runLegacyShutterstockGetImages, runLegacyShutterstock
urlpatterns = [
     path('utils/getRandWord',
          getRandWord, name='getRandWord'),
     path('utils/searchVtarget',
          searchVtarget, name='searchVtarget'),
     path('utils/searchShutterstock',
          searchShutterstock, name='searchShutterstock'),
     path('utils/getTagJobStatus',
          getTagJobStatus, name='getTagJobStatus'),
     path('utils/startCollectTagsJob',
          startCollectTagsJob, name='startCollectTagsJob'),

     path('utils/runLegacyRequest',
          runLegacyRequest, name='runLegacyRequest'),
     path('utils/runLegacyShutterstockGetImages',
          runLegacyShutterstockGetImages, name='runLegacyShutterstockGetImages'),
     path('utils/runLegacyShutterstock',
          runLegacyShutterstock, name='runLegacyShutterstock'),
]
