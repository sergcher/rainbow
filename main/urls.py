from django.urls import path

from main.views import (update_fees, settings, generate_excel,
                        generate_excel_apartment_total_file, generate_txt, apartment_receipt)

app_name = 'main'

urlpatterns = [
    path('update_fees', update_fees, name='update_fees'),
    path('settings', settings, name='settings'),
    path('generate_excel', generate_excel, name='generate_excel'),
    path('generate_excel_apartment_total_file', generate_excel_apartment_total_file,
         name='generate_excel_apartment_total_file'),
    path('generate_txt', generate_txt, name='generate_txt'),
    path('apartment_receipt', apartment_receipt, name='apartment_receipt'),
]
