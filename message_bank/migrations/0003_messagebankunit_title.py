# Generated by Django 3.0.3 on 2021-09-29 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message_bank', '0002_messagebankrepostpermission'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagebankunit',
            name='title',
            field=models.TextField(default=''),
        ),
    ]
