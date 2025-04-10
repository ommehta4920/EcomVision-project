# Generated by Django 4.2.18 on 2025-04-10 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_delete_price_track'),
    ]

    operations = [
        migrations.CreateModel(
            name='price_track',
            fields=[
                ('track_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('desired_price', models.CharField(max_length=8)),
                ('last_price', models.CharField(max_length=8)),
                ('tracking_status', models.CharField(choices=[('1', 'Active'), ('2', 'Completed')], default='1', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.categories')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.products')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user_details')),
            ],
        ),
    ]
