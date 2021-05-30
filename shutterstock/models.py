from django.db import models
from users.models import VkUser
# Create your models here.
import datetime


class ShutterstockUser(models.Model):
    user = models.ForeignKey(
        VkUser, blank=False, null=True, related_name='shutterstock_vk_user', on_delete=models.CASCADE)
    shutterstock_token = models.CharField(max_length=100, default='')


class PhotostockAccount(models.Model):
    username = models.CharField(default='', max_length=300)
    password = models.CharField(default='', max_length=50)
    stock_type = models.IntegerField(default=-1)
    active = models.BooleanField(default=False)
    available_downloads = models.IntegerField(default=999)
    rest_of_days = models.IntegerField(default=999)


class NewUser(models.Model):
    user_id = models.BigIntegerField(default=0)


class UserDownloadRecords(models.Model):
    dates = models.TextField(default='[]')
    user = models.ForeignKey(
        VkUser, blank=False, null=True, related_name='user_records', on_delete=models.CASCADE)
