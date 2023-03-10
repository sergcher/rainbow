# Generated by Django 4.1.4 on 2023-03-03 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_tariff_big_repair_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='settings',
            options={'verbose_name': 'setting', 'verbose_name_plural': 'settings'},
        ),
        migrations.AlterModelOptions(
            name='tariff',
            options={'verbose_name': 'tariff', 'verbose_name_plural': 'tariffs'},
        ),
        migrations.AddField(
            model_name='tariff',
            name='capital_repair',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
