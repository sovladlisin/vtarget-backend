# Generated by Django 3.0.3 on 2021-02-25 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shutterstock', '0003_newuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='photostockaccount',
            name='available_downloads',
            field=models.IntegerField(default=999),
        ),
        migrations.AddField(
            model_name='photostockaccount',
            name='rest_of_days',
            field=models.IntegerField(default=999),
        ),
    ]
