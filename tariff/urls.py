from django.urls import path

from tariff.views import (TariffListView, add_tariff, edit_tariff,
                          remove_tariff, tariff_list)

app_name = 'tariff'

urlpatterns = [
    path('', TariffListView.as_view(), name='tariff_list_main'),
    path('list/', tariff_list, name='tariff_list'),
    path('add/', add_tariff, name='add_tariff'),
    path('<int:pk>/edit', edit_tariff, name='edit_tariff'),
    path('<int:pk>/delete/', remove_tariff, name='tariff_delete'),
]
