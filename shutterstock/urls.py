from django.urls import path
from .views import getDownloadRecords, activatePhotostockAccount, getPhotostockAccounts, connectShutterstock, disconnectShutterstock, shutterstockLogin, createPhotostockAccount, deletePhotostockAccount, editPhotostockAccount
from .bot import Bot

urlpatterns = [
    path('shutterstock/api/connectShutterstock',
         connectShutterstock, name='connectShutterstock'),
    path('shutterstock/api/disconnectShutterstock',
         disconnectShutterstock, name='disconnectShutterstock'),
    path('shutterstock/api/getUrl',
         shutterstockLogin, name='shutterstockLogin'),
    path('shutterstock/api/bot',
         Bot, name='bot'),
    path('shutterstock/api/createPhotostockAccount',
         createPhotostockAccount, name='createPhotostockAccount'),
    path('shutterstock/api/deletePhotostockAccount',
         deletePhotostockAccount, name='deletePhotostockAccount'),
    path('shutterstock/api/editPhotostockAccount',
         editPhotostockAccount, name='editPhotostockAccount'),
    path('shutterstock/api/getPhotostockAccounts',
         getPhotostockAccounts, name='getPhotostockAccounts'),
    path('shutterstock/api/activatePhotostockAccount',
         activatePhotostockAccount, name='activatePhotostockAccount'),
    path('shutterstock/api/getDownloadRecords',
         getDownloadRecords, name='getDownloadRecords'),
]
