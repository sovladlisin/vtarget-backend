# Generated by Django 3.0.3 on 2021-06-24 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_vkuser_date_shutter_banned'),
    ]

    operations = [
        migrations.AddField(
            model_name='vkuser',
            name='medals',
            field=models.TextField(default='[]'),
        ),
    ]
