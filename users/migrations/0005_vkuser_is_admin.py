# Generated by Django 3.0.3 on 2020-12-24 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20201107_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='vkuser',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
