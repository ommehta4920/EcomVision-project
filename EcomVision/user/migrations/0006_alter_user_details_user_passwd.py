# Generated by Django 5.2 on 2025-04-16 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_price_track'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_details',
            name='user_passwd',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
