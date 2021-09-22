from django.urls import path
from .views import getDownloadRecords, activatePhotostockAccount, getPhotostockAccounts, connectShutterstock, disconnectShutterstock, shutterstockLogin, createPhotostockAccount, deletePhotostockAccount, editPhotostockAccount
from .bot import Bot

urlpatterns = [
    path('message_bank/api/bot',
         Bot, name='messageBankBot'),

]
