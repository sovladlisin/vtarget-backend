from django.db import models
import datetime
from users.models import VkUser
# Create your models here.


class AccountDuplicateJob(models.Model):
    data = models.TextField(default="[]")
    owner = models.ForeignKey(
        VkUser, blank=False, null=True, related_name='account_duplicate_job_owner', on_delete=models.CASCADE)
    in_progress = models.BooleanField(default=False)
    last_updated = models.DateField(default=datetime.date(2021, 3, 24))
    progress = models.CharField(default='', max_length=200)
