# Generated by Django 3.0.3 on 2020-11-04 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0012_remove_plannedpost_timezone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plannedpost',
            name='posted_vk_id',
        ),
        migrations.AddField(
            model_name='plannedpost',
            name='posted_vk_ids',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
