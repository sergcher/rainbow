from django.db import models


class Tariff(models.Model):
    name = models.CharField(max_length=200)
    maintenance = models.FloatField(null=True, blank=True)
    heating = models.FloatField(null=True, blank=True)
    heating_rub = models.FloatField(null=True, blank=True)
    hot_water = models.FloatField(null=True, blank=True)

    hot_water_odn = models.FloatField(null=True, blank=True)

    cold_water = models.FloatField(null=True, blank=True)
    cold_water_odn = models.FloatField(null=True, blank=True)
    sewage = models.FloatField(null=True, blank=True)
    sewage_odn = models.FloatField(null=True, blank=True)
    solid_waste = models.FloatField(null=True, blank=True)
    electricity = models.FloatField(null=True, blank=True)
    lift = models.FloatField(null=True, blank=True)
    electricity_odn = models.FloatField(null=True, blank=True)
    capital_repair = models.FloatField(null=True, blank=True, default=0)

    class Meta:
        verbose_name = 'tariff'
        verbose_name_plural = 'tariffs'

    def __str__(self):
        return self.name
