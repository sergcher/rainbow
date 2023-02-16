from django.db import models


class Apartment(models.Model):
    owner = models.CharField(max_length=200)
    serialNumber = models.IntegerField()


class ApartmentDetail(models.Model):
    registredQt = models.IntegerField()
    livedQt = models.IntegerField()
    totalArea = models.FloatField()
    personalAccount = models.IntegerField()
    serialNumber = models.ForeignKey(to=Apartment, on_delete=models.CASCADE)


class ApartmentCounter(models.Model):
    hot_water_previous = models.IntegerField(default=0)
    hot_water_current = models.IntegerField(default=0)
    hot_water_value = models.IntegerField(default=0)
    cold_water_previous = models.IntegerField(default=0)
    cold_water_current = models.IntegerField(default=0)
    cold_water_value = models.IntegerField(default=0)
    electricity_previous = models.IntegerField(default=0)
    electricity_current = models.IntegerField(default=0)
    electricity_value = models.IntegerField(default=0)
    wastewater_value = models.IntegerField(default=0)
    serialNumber = models.ForeignKey(to=Apartment, on_delete=models.CASCADE)


class ApartmentCharge(models.Model):
    electricity_odn = models.FloatField()
    money_deposited = models.FloatField()
    fine = models.FloatField()
    serialNumber = models.ForeignKey(to=Apartment, on_delete=models.CASCADE)


class ApartmentOption(models.Model):
    is_cold_water_meter = models.BooleanField()
    is_hot_water_meter = models.BooleanField()
    is_first_floor = models.BooleanField()
    is_absence_registred = models.BooleanField()
    serialNumber = models.ForeignKey(to=Apartment, on_delete=models.CASCADE)
