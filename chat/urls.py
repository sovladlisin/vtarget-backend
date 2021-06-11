from django.urls import path
from .views import createChatLog, deleteChatLog, postChatLog, getChatLog, getAllChatLogs

urlpatterns = [
    path('chat/api/createChatLog',
         createChatLog, name='createChatLog'),
    path('chat/api/deleteChatLog',
         deleteChatLog, name='deleteChatLog'),
    path('chat/api/postChatLog',
         postChatLog, name='postChatLog'),
    path('chat/api/getChatLog',
         getChatLog, name='getChatLog'),
    path('chat/api/getAllChatLogs',
         getAllChatLogs, name='getAllChatLogs'),
]
