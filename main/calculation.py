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
    return round(value, 2)


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
        total_area = apartment_detail.totalArea

        #Электроэнегия ОДН
        electricity_odn = round_float(total_area * tariff.electricity_odn)
        #Холодная вода ОДН
        cold_water_odn = round_float(total_area * tariff.cold_water_odn)
        #Сточные вода ОДН
        sewage_odn = round_float(total_area * tariff.sewage_odn)
        #Горячая вода ОДН
        hot_water_odn = round_float(total_area * tariff.hot_water_odn)
        #Лифт
        lift = round_float(total_area * tariff.lift)
        #Обращение с ТКО
        solid_waste = round_float(apartment_detail.livedQt * tariff.solid_waste)
        #Электричество
        electricity = round_float(counters.electricity_value * tariff.electricity)
        #Отопление Гкал
        heating = round_float(total_area * tariff.heating)
        #Отопление руб
        heating_rub = round_float(heating * tariff.heating_rub)
        #Горячая вода
        hot_water = round_float(counters.hot_water_value * tariff.hot_water)
        #Холодная вода
        cold_water = round_float(counters.cold_water_value * tariff.cold_water)
        #Водоотведение
        sewage = round_float(counters.wastewater_value * tariff.sewage)
        #Перерасчет
        recalculation = charges.recalculation_sewage + charges.recalculation_electricity + charges.recalculation_cold_water + charges.recalculation_heating_rub + charges.recalculation_hot_water + charges.recalculation_solid_waste
        #Итого коммунальные услуги
        maintenance_total = round_float(electricity + heating_rub + hot_water + cold_water + sewage + solid_waste + recalculation)
        #Содержание помещения
        maintenance = 0

        #Начислено
        accrued_expenses = solid_waste


        #         (Adoquery1['Sodershanie_jilya']) + (Adoquery1['Otoplenie']) + (Adoquery1['Podogrev_new']) + (
        # Adoquery1['Cold_Water_new']) + (Adoquery1['Canalization']) + (Adoquery1['Musor']) + (Adoquery1['Energy']) + (
        #         Adoquery1['Lift']) + (Adoquery1['Objii_Svet']))) - (Adoquery1['Lgota_schet']) + Adoquery1[
        #                                'Cap_remont'] + Adoquery1['odn_cold_water'] + Adoquery1['odn_hot_water'];

        #Сальдо начало
        balance_start = charges.balance_start

        #maintenance = round_float((area_by_norm * tariff.maintenance) + (area_over_norm * tariff.maintenance_over_norm))
        paid = charges.money_deposited
        fine = charges.fine
        balance_end = round_float(balance_start - paid)
        maintenance_full = solid_waste + maintenance + lift + electricity_odn + cold_water_odn

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
            recalculation=recalculation,
            sewage_odn=sewage_odn,
            serialNumber=apartment_detail.serialNumber
        )
        fee.save()
