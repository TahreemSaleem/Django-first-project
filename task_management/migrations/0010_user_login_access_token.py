# Generated by Django 2.0.5 on 2018-05-18 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_management', '0009_auto_20180517_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_login',
            name='access_token',
            field=models.CharField(default=None, max_length=30),
        ),
    ]