from main.models import *


def calculate_area(livedQt, totalArea):
    if livedQt >= 3:
        area_by_norm = (livedQt * 18) + 10
    elif livedQt == 2:
        area_by_norm = 52
    elif livedQt == 1:
        area_by_norm = 43
    else:
        area_by_norm = 0

    if area_by_norm < totalArea:
        area_over_norm = totalArea - area_by_norm
        area_over_norm = round(area_over_norm, 2)
    else:
        area_over_norm = 0
        area_by_norm = totalArea

    return [area_by_norm, area_over_norm]


def round_float(value):
    approximate = 0.01
    return round(value / approximate) * approximate


def calculate_fees():
    # Delete all rows from the ApartmentFee model
    ApartmentFee.objects.all().delete()

    # Cycle through the Apartment model and insert new rows in the ApartmentFee model
    for apartment in Apartment.objects.all():
        apartment_detail = ApartmentDetail.objects.get(serialNumber=apartment.serialNumber)
        tariff = Tariff.objects.get(id=apartment_detail.tariff_id)
        counters = ApartmentCounter.objects.get(serialNumber=apartment.serialNumber)
        charges = ApartmentCharge.objects.get(serialNumber=apartment.serialNumber)

        area_by_norm, area_over_norm = calculate_area(apartment_detail.livedQt, apartment_detail.totalArea)
        solid_waste = round_float(apartment_detail.livedQt * tariff.solid_waste)
        maintenance = round_float((area_by_norm * tariff.maintenance) + (area_over_norm * tariff.maintenance_over_norm))
        lift = round_float((area_by_norm * tariff.lift) + (area_over_norm * tariff.lift_over_norm))
        electricity_odn = round_float((area_by_norm * tariff.electricity_odn) + (area_over_norm * tariff.electricity_odn_over_norm))
        cold_water_odn = round_float((area_by_norm * tariff.cold_water_odn) + (area_over_norm * tariff.cold_water_odn_over_norm))
        hot_water_odn = round_float((area_by_norm * tariff.hot_water_odn) + (area_over_norm * tariff.hot_water_odn_over_norm))
        heating = round_float((area_by_norm * tariff.heating) + (area_over_norm * tariff.heating_over_norm))
        heating_rub = round_float((area_by_norm * tariff.heating_rub) + (area_over_norm * tariff.heating_rub_over_norm))
        hot_water = round_float(counters.hot_water_current * tariff.hot_water)
        cold_water = round_float(counters.cold_water_current * tariff.cold_water)
        sewage = round_float(counters.wastewater_value * tariff.sewage)
        electricity = round_float(counters.electricity_current * tariff.electricity)
        paid = charges.money_deposited
        balance_start = charges.balance_start
        fine = charges.fine
        balance_end = round_float(balance_start - paid)
        accrued_expenses = solid_waste + maintenance + lift + electricity_odn + cold_water_odn + hot_water_odn + heating_rub + hot_water + cold_water + sewage + electricity + fine
        maintenance_full = solid_waste + maintenance + lift + electricity_odn + cold_water_odn
        maintenance_total = solid_waste + maintenance + lift + electricity_odn + cold_water_odn
        total = maintenance_total + maintenance_full

        fee = ApartmentFee(
            solid_waste=solid_waste,
            maintenance=maintenance,
            lift=lift,
            electricity_odn=electricity_odn,
            cold_water_odn=cold_water_odn,
            hot_water_odn=hot_water_odn,
            heating=heating,
            heating_rub=heating_rub,
            hot_water=hot_water,
            cold_water=cold_water,
            sewage=sewage,
            electricity=electricity,
            paid=paid,
            balance_start=balance_start,
            fine=fine,
            balance_end=balance_end,
            accrued_expenses=accrued_expenses,
            maintenance_full=maintenance_full,
            maintenance_total=maintenance_total,
            total=total,
            serialNumber=apartment_detail.serialNumber
        )
        fee.save()
