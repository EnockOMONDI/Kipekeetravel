# Generated by Django 3.2.20 on 2025-04-09 11:43

from django.db import migrations, models
import django.db.models.deletion
import pyuploadcare.dj.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accomodation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_name', models.CharField(max_length=200)),
                ('hotel_description', models.TextField()),
                ('price_per_room', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('dtn_description', models.TextField()),
                ('Image', pyuploadcare.dj.models.ImageField()),
            ],
        ),
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itinerary_name', models.CharField(default='NULL', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ItineraryDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itinerary_description', models.TextField()),
                ('day_number', models.IntegerField()),
            ],
            options={
                'ordering': ['day_number'],
            },
        ),
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure', models.CharField(max_length=100)),
                ('arrival', models.CharField(max_length=100)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('price_per_person', models.PositiveIntegerField()),
                ('travelling_mode', models.CharField(choices=[('TN', 'Train'), ('FT', 'Flight'), ('BS', 'Bus')], default='FT', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', pyuploadcare.dj.models.ImageField()),
                ('package_name', models.CharField(default='NULL', max_length=200)),
                ('adult_price', models.IntegerField()),
                ('child_price', models.IntegerField()),
                ('description', models.TextField(default='NO DESCRIPTION ADDED')),
                ('inclusive', models.TextField()),
                ('exclusive', models.TextField()),
                ('number_of_days', models.PositiveIntegerField()),
                ('number_of_times_booked', models.PositiveIntegerField(default=0)),
                ('accomodation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminside.accomodation')),
            ],
        ),
    ]
