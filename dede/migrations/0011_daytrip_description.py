# Generated by Django 3.2.20 on 2025-04-18 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dede', '0010_auto_20250418_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='daytrip',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
