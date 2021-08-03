from django.db import models
from users.models import VkUser
# Create your models here.


class OKUserPermissions(models.Model):
    user = models.ForeignKey(
        VkUser, blank=False, null=True, related_name='vk_user_ok', on_delete=models.CASCADE)
    permissions = models.TextField(default='[]')
