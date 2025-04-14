# Generated by Django 3.2.20 on 2025-04-14 23:34

from django.db import migrations, models
import django.db.models.deletion
import pyuploadcare.dj.models


class Migration(migrations.Migration):

    dependencies = [
        ('dede', '0004_tour_is_featured'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('Image', pyuploadcare.dj.models.ImageField(blank=True, null=True)),
                ('date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pickup_location', models.CharField(max_length=200)),
                ('pickup_time', models.TimeField()),
                ('is_featured', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='IncludedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('icon', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='OptionalActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('daytrip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='optional_activities', to='dede.daytrip')),
            ],
            options={
                'verbose_name_plural': 'Optional Activities',
            },
        ),
        migrations.CreateModel(
            name='ItineraryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('activity', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('daytrip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itinerary_items', to='dede.daytrip')),
            ],
            options={
                'ordering': ['order', 'time'],
            },
        ),
        migrations.AddField(
            model_name='daytrip',
            name='included_items',
            field=models.ManyToManyField(to='dede.IncludedItem'),
        ),
    ]
