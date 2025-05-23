# Generated by Django 3.2.20 on 2025-04-18 16:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dede', '0009_daytripbooking_optional_activities'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='daytrip',
            options={'ordering': ['start_date']},
        ),
        migrations.RemoveField(
            model_name='daytrip',
            name='date',
        ),
        migrations.AddField(
            model_name='daytrip',
            name='end_date',
            field=models.DateField(blank=True, help_text='End date for recurring trips (optional)', null=True),
        ),
        migrations.AddField(
            model_name='daytrip',
            name='recurrence',
            field=models.CharField(choices=[('none', 'One-time Trip'), ('weekend', 'Every Weekend'), ('saturday', 'Every Saturday'), ('sunday', 'Every Sunday')], default='none', help_text='Select if this is a recurring trip', max_length=20),
        ),
        migrations.AddField(
            model_name='daytrip',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now, help_text='Start date for recurring trips or the date for one-time trips'),
            preserve_default=False,
        ),
    ]
