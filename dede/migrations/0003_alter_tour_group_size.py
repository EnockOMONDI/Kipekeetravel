# Generated by Django 3.2.20 on 2025-04-14 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dede', '0002_booking_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='group_size',
            field=models.IntegerField(blank=True, default=30, null=True),
        ),
    ]
