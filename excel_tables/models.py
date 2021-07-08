from django.db import models
from django.db.models.fields import TextField
from users.models import VkUser
# Create your models here.
import datetime


class ExcelTable(models.Model):
    owner = models.ForeignKey(
        VkUser, blank=False, null=True, related_name='excel_table_vk_user', on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    data = TextField(default='')
    title = models.CharField(default='Не указано', max_length=500)
# Create your models here.
