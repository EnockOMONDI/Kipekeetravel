# Generated by Django 3.2.20 on 2025-04-02 17:07

from django.db import migrations
import pyuploadcare.dj.models


class Migration(migrations.Migration):

    dependencies = [
        ('dede', '0003_auto_20250402_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='gallery_image1',
            field=pyuploadcare.dj.models.ImageField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='destination',
            name='gallery_image2',
            field=pyuploadcare.dj.models.ImageField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='destination',
            name='gallery_image3',
            field=pyuploadcare.dj.models.ImageField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tour',
            name='Image',
            field=pyuploadcare.dj.models.ImageField(blank=True, null=True),
        ),
    ]
