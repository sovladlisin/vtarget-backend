# Generated by Django 3.0.3 on 2021-04-16 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0005_auto_20210415_1827'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chart',
            old_name='is_dev',
            new_name='is_public',
        ),
        migrations.RenameField(
            model_name='table',
            old_name='is_dev',
            new_name='is_public',
        ),
    ]
