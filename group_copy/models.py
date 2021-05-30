from django.db import models
from users.models import VkUser
# Create your models here.


class FutureModerator(models.Model):
    vk_id = models.CharField(max_length=200, default='')
    role = models.CharField(max_length=200, default='')
    group_id = models.CharField(max_length=200, default='')
    is_contact = models.IntegerField(default=0)


class CreatedGroup(models.Model):
    group_id = models.CharField(max_length=200, default='')
    number_of_moderators = models.IntegerField(default=0)
    code = models.CharField(max_length=300, default='')
    user = models.ForeignKey(VkUser, blank=True, null=True,
                             related_name='created_group_owner', on_delete=models.CASCADE)
