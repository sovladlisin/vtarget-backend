# Generated by Django 3.0.3 on 2021-04-15 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0003_cabinet_chart_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chart',
            old_name='type',
            new_name='chart_type',
        ),
    ]
