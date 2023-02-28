from django.contrib import admin

from main.models import ApartmentDetail, ApartmentCounter, ApartmentCharge
from main.models import Settings, Tariff, Apartment


class ApartmentDetailInline(admin.TabularInline):
    model = ApartmentDetail
    fields = ('serialNumber', 'registredQt', 'livedQt', 'totalArea', 'personalAccount', 'account_number')
    extra = 0


class ApartmentCounterInline(admin.TabularInline):
    model = ApartmentCounter
    extra = 0
    fields = ['hot_water_previous', 'hot_water_current', 'hot_water_value',
              'cold_water_previous', 'cold_water_current', 'cold_water_value',
              'electricity_previous', 'electricity_current', 'electricity_value',
              'wastewater_value']


class ApartmentChargeInline(admin.TabularInline):
    model = ApartmentCharge
    extra = 0
    fields = ['money_deposited', 'fine',
              'recalculation_electricity', 'recalculation_heating_rub',
              'recalculation_hot_water', 'recalculation_cold_water',
              'recalculation_sewage', 'recalculation_solid_waste',
              'balance_start']


@admin.register(Settings)
class Settings(admin.ModelAdmin):
    list_display = ('month_name', 'month_to_pay', 'month_to_date', 'bill', 'pay_up_to')
    fields = ('month_name', 'month_to_pay', 'month_to_date', 'bill', 'pay_up_to')


@admin.register(Tariff)
class Tariff(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'maintenance', 'heating', 'heating_rub', 'hot_water', 'hot_water_odn', 'cold_water',
              'cold_water_odn', 'sewage', 'sewage_odn', 'solid_waste', 'electricity', 'lift', 'electricity_odn')
    search_fields = ('name',)
    ordering = ('name',)
    inlines = (ApartmentDetailInline,)


@admin.register(Apartment)
class Apartment(admin.ModelAdmin):
    list_display = ('owner', 'serialNumber',)
    fields = ('serialNumber', 'owner',)
    search_fields = ('owner', 'serialNumber',)
    ordering = ('serialNumber',)
    inlines = (ApartmentDetailInline, ApartmentCounterInline, ApartmentChargeInline)
