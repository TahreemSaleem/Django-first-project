# Generated by Django 2.0.5 on 2018-05-21 06:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('task_management', '0015_auto_20180521_0619'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='target_date',
            new_name='end_date',
        ),
        migrations.AddField(
            model_name='task',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2018, 5, 21, 6, 47, 31, 158359, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
