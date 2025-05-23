# Generated by Django 5.2 on 2025-04-28 10:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('user_type', models.CharField(choices=[('customer', 'Customer'), ('provider', 'Service Provider')], default='customer')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience', models.IntegerField()),
                ('description', models.TextField()),
                ('charge_per_hour', models.DecimalField(decimal_places=2, max_digits=10)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
                ('services_offered', models.ManyToManyField(to='accounts.service')),
            ],
        ),
    ]
