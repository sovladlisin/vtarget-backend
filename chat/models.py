from django.db import models
from users.models import VkUser
# Create your models here.


class ChatLog(models.Model):
    log = models.TextField(default='[]')
    key = models.CharField(default='f', max_length=600)
    owner = models.ForeignKey(
        VkUser, blank=False, null=True, related_name='chat_owner', on_delete=models.CASCADE)
    name = models.CharField(default='Не указано', max_length=600)
