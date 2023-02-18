# Generated by Django 4.1.4 on 2023-02-16 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_apartmentoption'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('maintenance', models.FloatField(blank=True, null=True)),
                ('maintenance_over_norm', models.FloatField(blank=True, null=True)),
                ('heating', models.FloatField(blank=True, null=True)),
                ('heating_over_norm', models.FloatField(blank=True, null=True)),
                ('heating_rub', models.FloatField(blank=True, null=True)),
                ('heating_rub_over_norm', models.FloatField(blank=True, null=True)),
                ('hot_water', models.FloatField(blank=True, null=True)),
                ('hot_water_over_norm', models.FloatField(blank=True, null=True)),
                ('cold_water', models.FloatField(blank=True, null=True)),
                ('cold_water_over_norm', models.FloatField(blank=True, null=True)),
                ('sewage', models.FloatField(blank=True, null=True)),
                ('sewage_over_norm', models.FloatField(blank=True, null=True)),
                ('solid_waste', models.FloatField(blank=True, null=True)),
                ('solid_waste_over_norm', models.FloatField(blank=True, null=True)),
                ('electricity', models.FloatField(blank=True, null=True)),
                ('electricity_over_norm', models.FloatField(blank=True, null=True)),
                ('lift', models.FloatField(blank=True, null=True)),
                ('lift_over_norm', models.FloatField(blank=True, null=True)),
                ('big_repair', models.FloatField(blank=True, null=True)),
                ('big_repair_over_norm', models.FloatField(blank=True, null=True)),
                ('electricity_odn', models.FloatField(blank=True, null=True)),
                ('electricity_odn_over_norm', models.FloatField(blank=True, null=True)),
                ('drainage_no_counter_cold_water', models.FloatField(blank=True, null=True)),
                ('drainage_no_counter_cold_water_over_norm', models.FloatField(blank=True, null=True)),
                ('drainage_no_counter_hot_water', models.FloatField(blank=True, null=True)),
                ('drainage_no_counter_hot_water_over_norm', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
