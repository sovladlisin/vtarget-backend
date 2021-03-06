# Generated by Django 3.0.3 on 2021-04-16 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0006_auto_20210416_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='cabinet',
            name='changing_interval',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='chart',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='table',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
