from django.urls import path

from repair.views import (RepairListView, edit_repair,
                          generate_excel_repair_total_file,
                          repair_generate_excel, repair_generate_txt,
                          repair_list, repairs_receipt)

app_name = 'repair'

urlpatterns = [
    path('', RepairListView.as_view(), name='repair_list_main'),
    path('list/', repair_list, name='repair_list'),
    path('<int:pk>/edit', edit_repair, name='edit_repair'),
    path('repair_generate_txt', repair_generate_txt, name='repair_generate_txt'),
    path('repair_generate_excel', repair_generate_excel, name='repair_generate_excel'),
    path(
        'generate_excel_repair_total_file', generate_excel_repair_total_file,
        name='generate_excel_repair_total_file'
        ),
    path('repair_receipt', repairs_receipt, name='repair_receipt'),
]
