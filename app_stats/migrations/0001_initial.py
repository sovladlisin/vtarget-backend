# Generated by Django 3.0.3 on 2021-07-01 10:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppsIds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(default='[]')),
                ('ids', models.TextField(default='[]')),
                ('in_progress', models.BooleanField(default=False)),
                ('last_updated', models.DateField(default=datetime.date(2021, 3, 24))),
                ('progress', models.CharField(default='', max_length=200)),
            ],
        ),
    ]