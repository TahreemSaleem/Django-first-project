# Generated by Django 2.0.5 on 2018-05-18 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_management', '0012_auto_20180518_0924'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_login',
            old_name='access_token',
            new_name='token',
        ),
    ]
