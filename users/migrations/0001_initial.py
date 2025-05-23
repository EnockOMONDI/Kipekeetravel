# Generated by Django 3.2.20 on 2025-04-09 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adminside', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBookings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('number_of_adults', models.PositiveIntegerField()),
                ('number_of_children', models.PositiveIntegerField(blank=True, null=True)),
                ('number_of_rooms', models.PositiveIntegerField(default=1)),
                ('booking_date', models.DateField(auto_now_add=True)),
                ('include_travelling', models.BooleanField(default=False)),
                ('special_requests', models.TextField(blank=True, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('total_amount', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminside.package')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-booking_date',),
            },
        ),
    ]
