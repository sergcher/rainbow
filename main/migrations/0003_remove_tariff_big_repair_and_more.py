# Generated by Django 4.1.4 on 2023-02-24 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_apartmentdetail_account_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tariff',
            name='big_repair',
        ),
        migrations.RemoveField(
            model_name='tariff',
            name='big_repair_over_norm',
        ),
        migrations.RemoveField(
            model_name='tariff',
            name='drainage_no_counter_cold_water',
        ),
        migrations.RemoveField(
            model_name='tariff',
            name='drainage_no_counter_cold_water_over_norm',
        ),
        migrations.RemoveField(
            model_name='tariff',
            name='drainage_no_counter_hot_water',
        ),
        migrations.RemoveField(
            model_name='tariff',
            name='drainage_no_counter_hot_water_over_norm',
        ),
        migrations.RemoveField(
            model_name='tariff',
            name='electricity_over_norm',
        ),
        migrations.RemoveField(
            model_name='tariff',
            name='sewage_over_norm',
        ),
    ]