from django.db import models
from users.models import VkUser
# Create your models here.


class Medal(models.Model):
    title = models.CharField(max_length=200, default='')
    description_gold = models.CharField(max_length=400, default='')
    description_silver = models.CharField(max_length=400, default='')
    description_copper = models.CharField(max_length=400, default='')
    description_diamond = models.CharField(max_length=400, default='')
    name = models.CharField(max_length=400, default='')


class Cabinet(models.Model):
    user = models.ForeignKey(
        VkUser, blank=False, null=False, related_name='user', on_delete=models.CASCADE)

    title = models.CharField(max_length=400, default='')
    start_date = models.CharField(max_length=400, default='')
    end_date = models.CharField(max_length=400, default='')

    changing_interval = models.IntegerField(default=-1)
    secondary_user = models.ForeignKey(
        VkUser, blank=True, null=True, related_name='cabinet_secondary_user', on_delete=models.CASCADE)


class Chart(models.Model):
    cabinet = models.ForeignKey(
        Cabinet, blank=False, null=False, related_name='chart_cabinet', on_delete=models.CASCADE)

    is_public = models.BooleanField(default=False)
    chart_type = models.CharField(max_length=400, default='')
    key = models.CharField(max_length=400, default='')
    title = models.CharField(max_length=400, default='')

    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    w = models.IntegerField(default=0)
    h = models.IntegerField(default=0)

    x_p = models.IntegerField(default=0)
    y_p = models.IntegerField(default=0)
    w_p = models.IntegerField(default=0)
    h_p = models.IntegerField(default=0)

    entities = models.CharField(max_length=9000, default='')
    kpi = models.BigIntegerField(default=0)
    unified = models.BooleanField(default=True)
    unified_color = models.CharField(max_length=400, default='')
    kpi_color = models.CharField(max_length=400, default='')
    smooth = models.BooleanField(default=True)
    pie_type = models.BigIntegerField(default=0)
    is_client = models.BooleanField(default=True)
    start_date = models.CharField(max_length=400, default='')
    end_date = models.CharField(max_length=400, default='')
    meta = models.CharField(max_length=9000, default='')


class Table(models.Model):
    cabinet = models.ForeignKey(
        Cabinet, blank=False, null=False, related_name='table_cabinet', on_delete=models.CASCADE)

    is_public = models.BooleanField(default=False)

    entities = models.CharField(max_length=9000, default='')
    custom_keys = models.CharField(max_length=9000, default='')

    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    w = models.IntegerField(default=0)
    h = models.IntegerField(default=0)

    x_p = models.IntegerField(default=0)
    y_p = models.IntegerField(default=0)
    w_p = models.IntegerField(default=0)
    h_p = models.IntegerField(default=0)

    is_collapsed = models.BooleanField(default=True)
    title = models.CharField(max_length=400, default='')
    is_client_table = models.BooleanField(default=True)
