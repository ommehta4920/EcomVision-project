# Generated by Django 4.2.18 on 2025-04-10 04:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_price_track_created_at'),
    ]

    operations = [
        migrations.DeleteModel(
            name='price_track',
        ),
    ]
