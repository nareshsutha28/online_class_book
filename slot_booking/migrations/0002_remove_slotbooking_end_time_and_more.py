# Generated by Django 5.1.4 on 2024-12-10 08:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slot_booking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slotbooking',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='slotbooking',
            name='start_time',
        ),
        migrations.AddField(
            model_name='slotbooking',
            name='slot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='slot_booking.teacheravailabilityslot'),
        ),
    ]
