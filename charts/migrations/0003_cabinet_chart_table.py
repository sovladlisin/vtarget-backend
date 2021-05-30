# Generated by Django 3.0.3 on 2021-04-15 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_servicerequest_date_until'),
        ('charts', '0002_auto_20210319_1904'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=400)),
                ('start_date', models.CharField(default='', max_length=400)),
                ('end_date', models.CharField(default='', max_length=400)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='users.VkUser')),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entities', models.CharField(default='', max_length=9000)),
                ('custom_keys', models.CharField(default='', max_length=9000)),
                ('x', models.IntegerField(default=0)),
                ('y', models.IntegerField(default=0)),
                ('w', models.IntegerField(default=0)),
                ('h', models.IntegerField(default=0)),
                ('is_collapsed', models.BooleanField(default=True)),
                ('title', models.CharField(default='', max_length=400)),
                ('is_client_table', models.BooleanField(default=True)),
                ('cabinet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table_cabinet', to='charts.Cabinet')),
            ],
        ),
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_dev', models.BooleanField(default=True)),
                ('type', models.CharField(default='', max_length=400)),
                ('key', models.CharField(default='', max_length=400)),
                ('title', models.CharField(default='', max_length=400)),
                ('x', models.IntegerField(default=0)),
                ('y', models.IntegerField(default=0)),
                ('w', models.IntegerField(default=0)),
                ('h', models.IntegerField(default=0)),
                ('entities', models.CharField(default='', max_length=9000)),
                ('kpi', models.BigIntegerField(default=0)),
                ('unified', models.BooleanField(default=True)),
                ('unified_color', models.CharField(default='', max_length=400)),
                ('kpi_color', models.CharField(default='', max_length=400)),
                ('smooth', models.BooleanField(default=True)),
                ('pie_type', models.BigIntegerField(default=0)),
                ('is_client', models.BooleanField(default=True)),
                ('start_date', models.CharField(default='', max_length=400)),
                ('end_date', models.CharField(default='', max_length=400)),
                ('meta', models.CharField(default='', max_length=9000)),
                ('cabinet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chart_cabinet', to='charts.Cabinet')),
            ],
        ),
    ]
