from django.db import models


class Tariff(models.Model):
    name = models.CharField(max_length=200)
    maintenance = models.FloatField(null=True, blank=True)
    maintenance_over_norm = models.FloatField(null=True, blank=True)  # delete
    heating = models.FloatField(null=True, blank=True)
    heating_over_norm = models.FloatField(null=True, blank=True)  # delete
    heating_rub = models.FloatField(null=True, blank=True)
    heating_rub_over_norm = models.FloatField(null=True, blank=True)  # delete
    hot_water = models.FloatField(null=True, blank=True)
    hot_water_over_norm = models.FloatField(null=True, blank=True)  # delete
    hot_water_odn = models.FloatField(null=True, blank=True)
    hot_water_odn_over_norm = models.FloatField(null=True, blank=True)  # delete
    cold_water = models.FloatField(null=True, blank=True)
    cold_water_over_norm = models.FloatField(null=True, blank=True)  # delete
    cold_water_odn = models.FloatField(null=True, blank=True)
    cold_water_odn_over_norm = models.FloatField(null=True, blank=True)  # delete
    sewage = models.FloatField(null=True, blank=True)
    sewage_over_norm = models.FloatField(null=True, blank=True)
    sewage_odn = models.FloatField(null=True, blank=True)
    solid_waste = models.FloatField(null=True, blank=True)
    solid_waste_over_norm = models.FloatField(null=True, blank=True)  # delete
    electricity = models.FloatField(null=True, blank=True)
    electricity_over_norm = models.FloatField(null=True, blank=True)
    lift = models.FloatField(null=True, blank=True)
    lift_over_norm = models.FloatField(null=True, blank=True)  # delete
    big_repair = models.FloatField(null=True, blank=True)
    big_repair_over_norm = models.FloatField(null=True, blank=True)
    electricity_odn = models.FloatField(null=True, blank=True)
    electricity_odn_over_norm = models.FloatField(null=True, blank=True)  # delete
    drainage_no_counter_cold_water = models.FloatField(null=True, blank=True)
    drainage_no_counter_cold_water_over_norm = models.FloatField(null=True, blank=True)
    drainage_no_counter_hot_water = models.FloatField(null=True, blank=True)
    drainage_no_counter_hot_water_over_norm = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Apartment(models.Model):
    owner = models.CharField(max_length=200)
    serialNumber = models.IntegerField()


class ApartmentDetail(models.Model):
    registredQt = models.IntegerField()
    livedQt = models.IntegerField()
    totalArea = models.FloatField()
    personalAccount = models.IntegerField()
    serialNumber = models.ForeignKey(to=Apartment, on_delete=models.CASCADE)
    tariff = models.ForeignKey(to=Tariff, on_delete=models.DO_NOTHING, null=True, blank=True)


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
    electricity_odn = models.FloatField()  #delete
    money_deposited = models.FloatField()
    fine = models.FloatField()
    recalculation = models.FloatField(null=True, blank=True)  #delete
    recalculation_electricity = models.FloatField(null=True, blank=True)
    recalculation_heating_rub = models.FloatField(null=True, blank=True)
    recalculation_hot_water = models.FloatField(null=True, blank=True)
    recalculation_cold_water = models.FloatField(null=True, blank=True)
    recalculation_sewage = models.FloatField(null=True, blank=True)
    recalculation_solid_waste = models.FloatField(null=True, blank=True)
    balance_start = models.FloatField(null=True, blank=True)
    serialNumber = models.ForeignKey(to=Apartment, on_delete=models.CASCADE)


class ApartmentOption(models.Model):
    is_cold_water_meter = models.BooleanField()
    is_hot_water_meter = models.BooleanField()
    is_first_floor = models.BooleanField()
    is_absence_registred = models.BooleanField()
    serialNumber = models.ForeignKey(to=Apartment, on_delete=models.CASCADE)


class ApartmentFee(models.Model):
    maintenance = models.FloatField(null=True, blank=True)
    electricity_odn = models.FloatField(null=True, blank=True)
    lift = models.FloatField(null=True, blank=True)
    maintenance_full = models.FloatField(null=True, blank=True)
    solid_waste = models.FloatField(null=True, blank=True)
    electricity = models.FloatField(null=True, blank=True)
    heating = models.FloatField(null=True, blank=True)
    heating_rub = models.FloatField(null=True, blank=True)
    hot_water = models.FloatField(null=True, blank=True)
    hot_water_odn = models.FloatField(null=True, blank=True)
    cold_water = models.FloatField(null=True, blank=True)
    cold_water_odn = models.FloatField(null=True, blank=True)
    sewage = models.FloatField(null=True, blank=True)
    sewage_odn = models.FloatField(null=True, blank=True)
    maintenance_total = models.FloatField(null=True, blank=True)
    accrued_expenses = models.FloatField(null=True, blank=True)
    recalculation = models.FloatField(null=True, blank=True)
    balance_start = models.FloatField(null=True, blank=True)
    balance_end = models.FloatField(null=True, blank=True)
    paid = models.FloatField(null=True, blank=True)
    fine = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    serialNumber = models.ForeignKey(to=Apartment, on_delete=models.CASCADE)


class Settings(models.Model):
    month_name = models.CharField(max_length=200)
    month_to_pay = models.CharField(max_length=200)
    month_to_date = models.CharField(max_length=200)
    bill = models.CharField(max_length=200)
    pay_up_to = models.CharField(max_length=200)
