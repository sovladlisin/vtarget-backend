from django.db import models
import datetime
# Create your models here.


class VkUser(models.Model):
    user_id = models.BigIntegerField(default=0)
    user_img = models.CharField(default='Не указано', max_length=300)
    user_name = models.CharField(default='Не указано', max_length=300)
    token = models.CharField(default='', max_length=300)
    post_token = models.CharField(
        default='', max_length=300, blank=True, null=True)
    shutterstock_token = models.CharField(
        default='', max_length=1000, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    date_shutter_banned = models.DateField(default=datetime.date(2009, 5, 3))

    # {tier: 1-4, title: ''}
    medals = models.TextField(default='[]')

    def __str__(self):
        return self.user_name


class ServiceRequest(models.Model):
    user = models.ForeignKey(
        VkUser, blank=False, null=False, related_name='request_user', on_delete=models.CASCADE)
    service_id = models.IntegerField(default=-1)
    is_accepted = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=False)
    is_denied = models.BooleanField(default=False)

    date_until = models.DateField(default=datetime.date(2021, 5, 3))

    def __str__(self):
        return self.user.user_name + str(self.service_id)

class ServiceInfo(models.Model):
    text = models.TextField(default=' ')
    service_id = models.IntegerField(default=-1)

    def __str__(self):
        return self.text