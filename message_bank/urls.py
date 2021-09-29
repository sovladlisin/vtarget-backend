from django.urls import path
from .bot import Bot
from .views import getMessages
from .views import deleteMessage, getUserPermissions, updateUserPermission, updateMessageTitle
urlpatterns = [
    path('message_bank/api/bot',
         Bot, name='messageBankBot'),
    path('message_bank/api/getMessages',
         getMessages, name='getMessages'),
    path('message_bank/api/deleteMessage',
         deleteMessage, name='deleteMessage'),
    path('message_bank/api/updateMessageTitle',
         updateMessageTitle, name='updateMessageTitle'),

    path('message_bank/api/getUserPermissions',
         getUserPermissions, name='getUserPermissions'),
    path('message_bank/api/updateUserPermission',
         updateUserPermission, name='updateUserPermission'),
]
