from django.db import models
from users.models import VkUser
# Create your models here.


class AvailableGroup(models.Model):
    name = models.CharField(max_length=600, default='')
    group_id = models.CharField(max_length=100, default='')
    group_img = models.CharField(max_length=600, default='')
    user = models.ForeignKey(
        VkUser, blank=False, null=True, related_name='group_owner', on_delete=models.CASCADE)


class SavedPost(models.Model):
    user = models.ForeignKey(
        VkUser, blank=False, null=True, related_name='publisher', on_delete=models.CASCADE)
    message = models.CharField(max_length=4000)
    attachments = models.CharField(max_length=4000)


class PlannedPost(models.Model):
    target_groups_id = models.CharField(default='', max_length=500)
    post = models.ForeignKey(
        SavedPost, blank=False, null=True, related_name='target_post', on_delete=models.CASCADE)

    from_group = models.IntegerField(default=1)
    mark_as_ads = models.IntegerField(default=0)
    close_comments = models.IntegerField(default=0)
    mute_notifications = models.IntegerField(default=0)

    posted_vk_ids = models.CharField(default='', max_length=1000)

    time_add = models.CharField(default='', max_length=100)
    time_delete = models.CharField(default='', max_length=100)
    every_day_marker = models.BooleanField(default=True)
    days_add = models.CharField(default='', max_length=500)
    days_delete = models.CharField(default='', max_length=500)

    on_delete = models.BooleanField(default=False)

    last_day_added = models.IntegerField(default=-1)
    last_day_deleted = models.IntegerField(default=-1)
