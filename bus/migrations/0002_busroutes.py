# Generated by Django 5.0.1 on 2024-01-18 20:20

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusRoutes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('source', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('bus', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='source_destination', to='bus.busdetails')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
