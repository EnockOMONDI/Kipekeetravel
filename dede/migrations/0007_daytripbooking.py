# Generated by Django 3.2.20 on 2025-04-15 00:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dede', '0006_auto_20250414_2337'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayTripBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('travel_date', models.DateField()),
                ('number_of_people', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Number of people must be at least 1'), django.core.validators.MaxValueValidator(1000, message='Number of people cannot exceed 1000')])),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('special_requirements', models.TextField(blank=True, null=True)),
                ('booking_status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='pending', max_length=20)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('partial', 'Partial'), ('paid', 'Paid'), ('refunded', 'Refunded')], default='pending', max_length=20)),
                ('deposit_paid', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('booking_reference', models.CharField(blank=True, max_length=20, unique=True)),
                ('daytrip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='dede.daytrip')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Day Trip Booking',
                'verbose_name_plural': 'Day Trip Bookings',
                'ordering': ['-created_at'],
            },
        ),
    ]
