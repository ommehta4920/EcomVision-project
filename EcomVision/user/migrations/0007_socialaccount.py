# Generated by Django 5.1.6 on 2025-04-16 14:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_user_details_user_passwd'),
    ]

    operations = [
        migrations.CreateModel(
            name='Socialaccount',
            fields=[
                ('socailaccount_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('provider', models.CharField(max_length=200)),
                ('uid', models.CharField(max_length=200)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('extra_data', models.JSONField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user_details')),
            ],
        ),
    ]
