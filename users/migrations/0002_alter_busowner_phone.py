# Generated by Django 5.0.1 on 2024-01-18 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busowner',
            name='phone',
            field=models.IntegerField(max_length=100),
        ),
    ]
