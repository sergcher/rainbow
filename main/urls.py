from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('main/tariffs', views.TariffListView.as_view(), name='all'),
    path('main/<int:pk>/detail', views.TariffDetailView.as_view(), name='tariff_detail'),
    path('main/create/', views.TariffCreateView.as_view(), name='tariff_create'),
    path('main/<int:pk>/update/', views.TariffUpdateView.as_view(), name='tariff_update'),
    path('main/<int:pk>/delete/', views.TariffDeleteView.as_view(), name='tariff_delete'),
    path('update_fees', views.update_fees, name='update_fees'),
    path('settings', views.settings, name='settings'),
    path('generate_excel', views.generate_excel, name='generate_excel'),
    path('apartment_receipt', views.apartment_receipt, name='apartment_receipt'),
]
