# Generated by Django 3.2.20 on 2025-04-15 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dede', '0007_daytripbooking'),
    ]

    operations = [
        migrations.AddField(
            model_name='daytrip',
            name='group_size',
            field=models.IntegerField(default=30, help_text='Maximum number of participants'),
        ),
    ]
