# Generated by Django 5.0.1 on 2024-02-27 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0004_alter_busdetails_busrc_alter_busdetails_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='busschedule',
            name='bus',
        ),
    ]
