# Generated by Django 4.1.4 on 2023-02-24 10:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=200)),
                ('serialNumber', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_name', models.CharField(max_length=200)),
                ('month_to_pay', models.CharField(max_length=200)),
                ('month_to_date', models.CharField(max_length=200)),
                ('bill', models.CharField(max_length=200)),
                ('pay_up_to', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('maintenance', models.FloatField(blank=True, null=True)),
                ('heating', models.FloatField(blank=True, null=True)),
                ('heating_rub', models.FloatField(blank=True, null=True)),
                ('hot_water', models.FloatField(blank=True, null=True)),
                ('hot_water_odn', models.FloatField(blank=True, null=True)),
                ('cold_water', models.FloatField(blank=True, null=True)),
                ('cold_water_odn', models.FloatField(blank=True, null=True)),
                ('sewage', models.FloatField(blank=True, null=True)),
                ('sewage_over_norm', models.FloatField(blank=True, null=True)),
                ('sewage_odn', models.FloatField(blank=True, null=True)),
                ('solid_waste', models.FloatField(blank=True, null=True)),
                ('electricity', models.FloatField(blank=True, null=True)),
                ('electricity_over_norm', models.FloatField(blank=True, null=True)),
                ('lift', models.FloatField(blank=True, null=True)),
                ('big_repair', models.FloatField(blank=True, null=True)),
                ('big_repair_over_norm', models.FloatField(blank=True, null=True)),
                ('electricity_odn', models.FloatField(blank=True, null=True)),
                ('drainage_no_counter_cold_water', models.FloatField(blank=True, null=True)),
                ('drainage_no_counter_cold_water_over_norm', models.FloatField(blank=True, null=True)),
                ('drainage_no_counter_hot_water', models.FloatField(blank=True, null=True)),
                ('drainage_no_counter_hot_water_over_norm', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApartmentOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_cold_water_meter', models.BooleanField()),
                ('is_hot_water_meter', models.BooleanField()),
                ('is_first_floor', models.BooleanField()),
                ('is_absence_registred', models.BooleanField()),
                ('serialNumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.apartment')),
            ],
        ),
        migrations.CreateModel(
            name='ApartmentFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintenance', models.FloatField(blank=True, null=True)),
                ('electricity_odn', models.FloatField(blank=True, null=True)),
                ('lift', models.FloatField(blank=True, null=True)),
                ('maintenance_full', models.FloatField(blank=True, null=True)),
                ('solid_waste', models.FloatField(blank=True, null=True)),
                ('electricity', models.FloatField(blank=True, null=True)),
                ('heating', models.FloatField(blank=True, null=True)),
                ('heating_rub', models.FloatField(blank=True, null=True)),
                ('hot_water', models.FloatField(blank=True, null=True)),
                ('hot_water_odn', models.FloatField(blank=True, null=True)),
                ('cold_water', models.FloatField(blank=True, null=True)),
                ('cold_water_odn', models.FloatField(blank=True, null=True)),
                ('sewage', models.FloatField(blank=True, null=True)),
                ('sewage_odn', models.FloatField(blank=True, null=True)),
                ('maintenance_total', models.FloatField(blank=True, null=True)),
                ('accrued_expenses', models.FloatField(blank=True, null=True)),
                ('recalculation', models.FloatField(blank=True, null=True)),
                ('balance_start', models.FloatField(blank=True, null=True)),
                ('balance_end', models.FloatField(blank=True, null=True)),
                ('paid', models.FloatField(blank=True, null=True)),
                ('fine', models.FloatField(blank=True, null=True)),
                ('total', models.FloatField(blank=True, null=True)),
                ('serialNumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.apartment')),
            ],
        ),
        migrations.CreateModel(
            name='ApartmentDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registredQt', models.IntegerField()),
                ('livedQt', models.IntegerField()),
                ('totalArea', models.FloatField()),
                ('personalAccount', models.IntegerField()),
                ('serialNumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.apartment')),
                ('tariff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.tariff')),
            ],
        ),
        migrations.CreateModel(
            name='ApartmentCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hot_water_previous', models.IntegerField(default=0)),
                ('hot_water_current', models.IntegerField(default=0)),
                ('hot_water_value', models.IntegerField(default=0)),
                ('cold_water_previous', models.IntegerField(default=0)),
                ('cold_water_current', models.IntegerField(default=0)),
                ('cold_water_value', models.IntegerField(default=0)),
                ('electricity_previous', models.IntegerField(default=0)),
                ('electricity_current', models.IntegerField(default=0)),
                ('electricity_value', models.IntegerField(default=0)),
                ('wastewater_value', models.IntegerField(default=0)),
                ('serialNumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.apartment')),
            ],
        ),
        migrations.CreateModel(
            name='ApartmentCharge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money_deposited', models.FloatField()),
                ('fine', models.FloatField()),
                ('recalculation_electricity', models.FloatField(blank=True, null=True)),
                ('recalculation_heating_rub', models.FloatField(blank=True, null=True)),
                ('recalculation_hot_water', models.FloatField(blank=True, null=True)),
                ('recalculation_cold_water', models.FloatField(blank=True, null=True)),
                ('recalculation_sewage', models.FloatField(blank=True, null=True)),
                ('recalculation_solid_waste', models.FloatField(blank=True, null=True)),
                ('balance_start', models.FloatField(blank=True, null=True)),
                ('serialNumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.apartment')),
            ],
        ),
    ]
