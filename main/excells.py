from openpyxl import Workbook
from django.http import HttpResponse


def generate_excel_file(apartment_fees):
    # Create a new workbook
    wb = Workbook()

    # Select the active worksheet
    ws = wb.active

    # Write the headers
    headers = ['Maintenance', 'Electricity ODN', 'Lift', 'Maintenance Full', 'Solid Waste', 'Electricity', 'Heating', 'Heating RUB', 'Hot Water', 'Hot Water ODN', 'Cold Water', 'Cold Water ODN', 'Sewage', 'Maintenance Total', 'Accrued Expenses', 'Recalculation', 'Balance Start', 'Balance End', 'Paid', 'Fine', 'Total']
    ws.append(headers)

    # Write the data for each apartment fee
    for i, fee in enumerate(apartment_fees):
        data = [fee.maintenance, fee.electricity_odn, fee.lift, fee.maintenance_full, fee.solid_waste, fee.electricity, fee.heating, fee.heating_rub, fee.hot_water, fee.hot_water_odn, fee.cold_water, fee.cold_water_odn, fee.sewage, fee.maintenance_total, fee.accrued_expenses, fee.recalculation, fee.balance_start, fee.balance_end, fee.paid, fee.fine, fee.total]
        ws.append(data)

    # Create a response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=apartment_fees.xlsx'

    # Write the Excel file to the response
    wb.save(response)

    return response
