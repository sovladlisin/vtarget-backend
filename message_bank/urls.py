from django.urls import path
from .bot import Bot

urlpatterns = [
    path('message_bank/api/bot',
         Bot, name='messageBankBot'),

]
