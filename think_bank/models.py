from django.db import models
from users.models import VkUser
# Create your models here.


class Post(models.Model):
    # владелец поста в банке креативов
    user = models.ForeignKey(
        VkUser, blank=False, null=False, related_name='vkuser_id', on_delete=models.CASCADE)
    post_id = models.BigIntegerField(default=0)
    owner_id = models.BigIntegerField(default=0)
    owner_name = models.CharField(default='Не указано', max_length=1000)
    owner_img_link = models.CharField(default='Не указано', max_length=1000)
    from_id = models.BigIntegerField(default=0)
    date = models.CharField(default='Не указано', max_length=300)
    text = models.CharField(default='Не указано', max_length=30000)
    comments_count = models.BigIntegerField(default=0)
    likes_count = models.BigIntegerField(default=0)
    reposts_count = models.BigIntegerField(default=0)
    views_count = models.BigIntegerField(default=0)
    attachments = models.CharField(default='Не указано', max_length=30000)

    date_added = models.CharField(default='', max_length=200)


class VkUserPermissions(models.Model):
    owner = models.ForeignKey(
        VkUser, blank=False, null=False, related_name='owner', on_delete=models.CASCADE)
    viewer = models.ForeignKey(
        VkUser, blank=False, null=False, related_name='viewer', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, blank=False, null=False, related_name='comment_post', on_delete=models.CASCADE)
    user = models.ForeignKey(
        VkUser, blank=False, null=False, related_name='comment_owner', on_delete=models.CASCADE)
    comment = models.CharField(default='', max_length=300)
    date = models.CharField(default='', max_length=200)
