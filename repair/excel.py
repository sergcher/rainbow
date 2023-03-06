from datetime import datetime
import os

from django.db.models import Sum
from django.http import HttpResponse
from openpyxl import Workbook

from main.models import Apartment, ApartmentDetail, Settings
from repair.models import CapitalRepair


def repair_export_client_bank():
    filename = f'44070_{datetime.today().strftime("%d%m%Y")}_1.txt'
    total = 0
    apartments = Apartment.objects.all()
    settings = Settings.objects.get(id=1)

    date_str = settings.month_to_date
    date_obj = datetime.strptime(date_str, '%d.%m.%Y')
    date_str = datetime.strftime(date_obj, '%m%Y')

    with open(filename, 'w') as f:
        for apartment in apartments:
            apartment_detail = ApartmentDetail.objects.get(serialNumber=apartment.serialNumber)
            capital_repair = CapitalRepair.objects.get(serialNumber=apartment.serialNumber)
            repair_total = capital_repair.total()
            total += repair_total
            f.write(
                f'{apartment_detail.personalAccount}|{apartment.owner.strip()}'
                f'|Междуреченск, Шахтеров проспект, д. 55,{apartment.serialNumber}|12|'
                f'кап.ремонт|{date_str}||{int(repair_total * 100)}' + '\n')
        total = round(total, 2)
        f.write('=|106|' + str(int(total * 100)) + '\n')

    with open(filename, 'rb') as f:
        response = HttpResponse(f.read(), content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

    os.remove(filename)
    return response


def repair_generate_excel_file(apartments):
    wb = Workbook()
    ws = wb.active
    headers = [
         'Квартира', 'ФИО', 'Общ. площ.', 'Долг на нач. месяца', 'Начислено',
         'Пеня', 'Перерасчет', 'Оплачено', 'Итого'
    ]

    ws.append(headers)

    for i, apartment in enumerate(apartments):
        apartment_detail = ApartmentDetail.objects.get(serialNumber=apartment.serialNumber)
        capital_repair = CapitalRepair.objects.get(serialNumber=apartment.serialNumber)
        data = [
            apartment.serialNumber,
            apartment.owner,
            apartment_detail.totalArea,
            capital_repair.debt,
            capital_repair.accrued(),
            capital_repair.fine,
            capital_repair.recalculation,
            capital_repair.paid,
            capital_repair.total()
        ]
        ws.append(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=repair_fees.xlsx'
    wb.save(response)

    return response


def export_excel_repair_total_file():
    wb = Workbook()
    ws = wb.active
    objects = CapitalRepair.objects.all()

    # Долг на начало месяца
    value = CapitalRepair.objects.aggregate(Sum('debt'))['debt__sum']
    data = ['Долг на начало месяца', value]
    ws.append(data)

    # Начислено
    value = sum([obj.accrued() for obj in objects])
    data = ['Начислено', value]
    ws.append(data)

    # Пеня
    value = CapitalRepair.objects.aggregate(Sum('fine'))['fine__sum']
    data = ['Пеня', value]
    ws.append(data)

    # Перерасчет
    value = CapitalRepair.objects.aggregate(Sum('recalculation'))['recalculation__sum']
    data = ['Перерасчет', value]
    ws.append(data)

    # Оплачено
    value = CapitalRepair.objects.aggregate(Sum('paid'))['paid__sum']
    data = ['Оплачено', value]
    ws.append(data)

    # Итого
    value = sum([obj.total() for obj in objects])
    data = ['Итого', value]
    ws.append(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=apartment_fees.xlsx'
    wb.save(response)

    return response
