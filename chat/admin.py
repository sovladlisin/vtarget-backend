from django.contrib import admin
from .models import ChatLog
# Register your models here.


class ChatAdmin(admin.ModelAdmin):
    model = ChatLog


admin.site.register(ChatLog, ChatAdmin)
