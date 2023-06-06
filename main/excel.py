import os
from datetime import datetime

from django.db.models import Sum
from django.http import HttpResponse
from openpyxl import Workbook

from main.models import Apartment, ApartmentDetail, ApartmentFee, Settings


def export_client_bank():
    filename = f'44069_{datetime.today().strftime("%d%m%Y")}_1.txt'
    total = 0
    apartments = Apartment.objects.all()
    settings = Settings.objects.get(id=1)

    date_str = settings.month_to_date
    date_obj = datetime.strptime(date_str, '%d.%m.%Y')
    date_str = datetime.strftime(date_obj, '%m%Y')

    with open(filename, 'w') as f:
        for apartment in apartments:
            apartment_detail = ApartmentDetail.objects.get(serialNumber=apartment.serialNumber)
            apartment_fee = ApartmentFee.objects.get(serialNumber=apartment.serialNumber)
            fee = round(apartment_fee.total, 2)
            total += fee
            f.write(
                f'{apartment_detail.personalAccount}|{apartment.owner.strip()}'
                f'|New York, street, h. 55,{apartment.serialNumber}|11|'
                f'payment|{date_str}||{int(fee * 100)}' + '\n')
        total = round(total, 2)
        f.write('=|106|' + str(int(total * 100)) + '\n')

    with open(filename, 'rb') as f:
        response = HttpResponse(f.read(), content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

    os.remove(filename)
    return response


def generate_excel_file(apartments):
    wb = Workbook()
    ws = wb.active
    headers = [
         '№', 'Owner', 'Number of registered', 'Number of residents', 'Apartment size',
         'Maintenance fee', 'Electricity household needs', 'Cold water household needs',
         'Sewage household needs', 'Hot water household needs', 'Elevator',
         'Maintenance fee total', 'Solid waste management', 'Electricity',
         'Heating Gcal', 'Heating, $.', 'Hot water', 'Cold water', 'Canalization',
         'Total Utilities', 'Current charges', 'Recalculating', 'Balance start',
         'Balance end', 'Paid', 'Fine', 'Total amount due'
    ]

    ws.append(headers)

    for i, apartment in enumerate(apartments):
        apartment_detail = ApartmentDetail.objects.get(serialNumber=apartment.serialNumber)
        apartment_fee = ApartmentFee.objects.get(serialNumber=apartment.serialNumber)
        data = [
            apartment.serialNumber,
            apartment.owner,
            apartment_detail.registredQt,
            apartment_detail.livedQt,
            apartment_detail.totalArea,
            apartment_fee.maintenance,
            apartment_fee.electricity_odn,
            apartment_fee.cold_water_odn,
            apartment_fee.sewage_odn,
            apartment_fee.hot_water_odn,
            apartment_fee.lift,
            apartment_fee.maintenance_full,
            apartment_fee.solid_waste,
            apartment_fee.electricity,
            apartment_fee.heating,
            apartment_fee.heating_rub,
            apartment_fee.hot_water,
            apartment_fee.cold_water,
            apartment_fee.sewage,
            apartment_fee.maintenance_total,
            apartment_fee.accrued_expenses,
            apartment_fee.recalculation,
            apartment_fee.balance_start,
            apartment_fee.balance_end,
            apartment_fee.paid,
            apartment_fee.fine,
            apartment_fee.total
        ]
        ws.append(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=apartment_fees.xlsx'
    wb.save(response)

    return response


def export_excel_apartment_total_file():
    wb = Workbook()
    ws = wb.active

    # Number of registered
    value = ApartmentDetail.objects.aggregate(Sum('registredQt'))['registredQt__sum']
    data = ['Number of registered', value]
    ws.append(data)

    # Number of residents
    value = ApartmentDetail.objects.aggregate(Sum('livedQt'))['livedQt__sum']
    data = ['Number of residents', value]
    ws.append(data)

    # Apartment size
    value = ApartmentDetail.objects.aggregate(Sum('totalArea'))['totalArea__sum']
    data = ['Apartment size', value]
    ws.append(data)

    # Отапливаемая площадь
    value = ApartmentDetail.objects.aggregate(Sum('totalArea'))['totalArea__sum']
    data = ['Heating area', value]
    ws.append(data)

    # Electricity
    value = ApartmentFee.objects.aggregate(Sum('electricity'))['electricity__sum']
    data = ['Electricity', value]
    ws.append(data)

    # Heating
    value = ApartmentFee.objects.aggregate(Sum('heating_rub'))['heating_rub__sum']
    data = ['Heating', value]
    ws.append(data)

    # Hot water
    value = ApartmentFee.objects.aggregate(Sum('hot_water'))['hot_water__sum']
    data = ['Hot water', value]
    ws.append(data)

    # Cold water
    value = ApartmentFee.objects.aggregate(Sum('cold_water'))['cold_water__sum']
    data = ['Cold water', value]
    ws.append(data)

    # Canalization
    value = ApartmentFee.objects.aggregate(Sum('sewage'))['sewage__sum']
    data = ['Canalization', value]
    ws.append(data)

    # Solid waste management
    value = ApartmentFee.objects.aggregate(Sum('solid_waste'))['solid_waste__sum']
    data = ['Solid waste management', value]
    ws.append(data)

    # Maintenance fee
    value = ApartmentFee.objects.aggregate(Sum('maintenance'))['maintenance__sum']
    data = ['Maintenance fee', value]
    ws.append(data)

    # household needs Эл/энергия
    value = ApartmentFee.objects.aggregate(Sum('electricity_odn'))['electricity_odn__sum']
    data = ['household needs Electricity', value]
    ws.append(data)

    # household needs sewage
    value = ApartmentFee.objects.aggregate(Sum('sewage_odn'))['sewage_odn__sum']
    data = ['household needs sewage', value]
    ws.append(data)

    # household needs Cold water
    value = ApartmentFee.objects.aggregate(Sum('cold_water_odn'))['cold_water_odn__sum']
    data = ['household needs cold water', value]
    ws.append(data)

    # household needs Hot water
    value = ApartmentFee.objects.aggregate(Sum('hot_water_odn'))['hot_water_odn__sum']
    data = ['household needs hot water', value]
    ws.append(data)

    # Elevator
    value = ApartmentFee.objects.aggregate(Sum('lift'))['lift__sum']
    data = ['Elevator', value]
    ws.append(data)

    # Сальдо конец
    value = ApartmentFee.objects.aggregate(Sum('balance_end'))['balance_end__sum']
    data = ['Balance end', value]
    ws.append(data)

    # Paid
    value = ApartmentFee.objects.aggregate(Sum('paid'))['paid__sum']
    data = ['Paid', value]
    ws.append(data)

    # Сальдо начало
    value = ApartmentFee.objects.aggregate(Sum('balance_start'))['balance_start__sum']
    data = ['Balance start', value]
    ws.append(data)

    # Fine
    value = ApartmentFee.objects.aggregate(Sum('fine'))['fine__sum']
    data = ['Fine', value]
    ws.append(data)

    # Перерасчет/недопоставка услуг
    value = ApartmentFee.objects.aggregate(Sum('recalculation'))['recalculation__sum']
    data = ['Fine', value]
    ws.append(data)

    # Current charges
    value = ApartmentFee.objects.aggregate(Sum('accrued_expenses'))['accrued_expenses__sum']
    data = ['Current charges', value]
    ws.append(data)

    # Итого
    value = ApartmentFee.objects.aggregate(Sum('total'))['total__sum']
    data = ['Total', value]
    ws.append(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=apartment_fees.xlsx'
    wb.save(response)

    return response
