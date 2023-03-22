from django.urls import path

from tariff.views import (TariffCreateView, TariffDeleteView, TariffListView,
                          TariffUpdateView, add_tariff, edit_tariff, tariff_list)

app_name = 'tariff'

urlpatterns = [
    path('', TariffListView.as_view(), name='tariff_list_main'),
    path('list/', tariff_list, name='tariff_list'),
    # path('create/', TariffCreateView.as_view(), name='tariff_create'),
    path('add/', add_tariff, name='add_tariff'),
    # path('<int:pk>/update/', TariffUpdateView.as_view(), name='tariff_update'),
    path('<int:pk>/edit', edit_tariff, name='edit_tariff'),
    path('<int:pk>/delete/', TariffDeleteView.as_view(), name='tariff_delete'),
]
