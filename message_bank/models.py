from django.db import models
from users.models import VkUser

# Create your models here.


class MessageBankUnit(models.Model):
    date = models.DateTimeField(default=None, null=True, blank=True)
    date_written = models.CharField(max_length=255, default='')

    body = models.TextField(default='{}')
    fwd_body = models.TextField(default='[]')

    title = models.TextField(default='')


class MessageBankRepostPermission(models.Model):

    user = models.ForeignKey(VkUser, blank=False, null=True,
                             related_name='vk_user_message_bank_permission', on_delete=models.CASCADE)
    is_allowed = models.IntegerField(default=0)
