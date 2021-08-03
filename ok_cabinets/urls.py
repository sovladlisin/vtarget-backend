from django.urls import path
from .views import getUserById

urlpatterns = [
    path('ok_cabinets/api/getUserById',
         getUserById, name='getUserById'),
]
