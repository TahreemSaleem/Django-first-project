# Generated by Django 2.0.5 on 2018-05-16 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_management', '0005_user_e_verication'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='e_verication',
            new_name='e_verification',
        ),
    ]
