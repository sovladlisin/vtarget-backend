from django.db import models

# Create your models here.


class MessageBankUnit(models.Model):
    date = models.DateTimeField(default=None, null=True, blank=True)
    date_written = models.CharField(max_length=255, default='')

    body = models.TextField(default='{}')
    fwd_body = models.TextField(default='[]')
