from django.urls import path
from .bot import Bot
from .views import getMessages
from .views import deleteMessage
urlpatterns = [
    path('message_bank/api/bot',
         Bot, name='messageBankBot'),
    path('message_bank/api/getMessages',
         getMessages, name='getMessages'),
    path('message_bank/api/deleteMessage',
         deleteMessage, name='deleteMessage'),
]