from django.urls import path
from .bot import Bot
from .views import copyRequest
urlpatterns = [path('bot-moderators', Bot, name='bot_moderators'),
               path('api/copyGroup', copyRequest, name='bot_moderators'),
               ]
