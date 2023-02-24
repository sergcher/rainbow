from openpyxl import Workbook
from django.http import HttpResponse
from main.models import *


def generate_excel_file(apartments):
    # Create a new workbook
    wb = Workbook()

    # Select the active worksheet
    ws = wb.active

    # Write the headers
    headers = [
         '№', 'ФИО', 'Кол. зарег.', 'Кол. прожив.', 'Общ. площ.', 'Содерж. помещения', 'Эл/эн ОДН', 'ОДН Холодная вода',
         'ОДН Сточные воды', 'ОДН Горячая вода', 'Лифт', 'Содерж. помещ. итого', 'Обращение с ТКО', 'Электр.',
         'Отопление Гкал', 'Отопление, руб.', 'Гор. вода', 'Хол. вода', 'Водоотв.', 'Итого коммунальные услуги',
         'Начислено', 'Перерасчет', 'Сальдо Начало', 'Сальдо Конец', 'Оплачено', 'Пеня', 'Итого к оплате'
    ]

    ws.append(headers)

    # Write the data for each apartment fee
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

    # Create a response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=apartment_fees.xlsx'

    # Write the Excel file to the response
    wb.save(response)

    return response
