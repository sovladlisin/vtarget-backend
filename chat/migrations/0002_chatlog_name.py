# Generated by Django 3.0.3 on 2021-06-11 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatlog',
            name='name',
            field=models.CharField(default='Не указано', max_length=600),
        ),
    ]