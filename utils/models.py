from django.db import models
import datetime
# Create your models here.


class CollectTagsJob(models.Model):
    data = models.TextField(default='')
    size = models.IntegerField(default=0)
    in_progress = models.BooleanField(default=False)
    last_updated = models.DateField(default=datetime.date(2021, 3, 24))
    progress = models.CharField(default='', max_length=200)
