from django.urls import path

from tariff.views import (TariffListView, TariffCreateView,
                          TariffDeleteView, TariffUpdateView)

app_name = 'tariff'

urlpatterns = [
    path('', TariffListView.as_view(), name='tariff_list'),
    path('create/', TariffCreateView.as_view(), name='tariff_create'),
    path('<int:pk>/update/', TariffUpdateView.as_view(), name='tariff_update'),
    path('<int:pk>/delete/', TariffDeleteView.as_view(), name='tariff_delete'),
]
