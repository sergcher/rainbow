from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from tariff.models import Tariff


class TariffBaseView(View):
    model = Tariff
    fields = '__all__'
    success_url = reverse_lazy('tariff:tariff_list')


class TariffListView(TariffBaseView, TitleMixin, ListView):
    """View to list all tariffs.
    Use the 'tariff_list' variable in the template
    to access all Tariff objects"""
    template_name = 'tariff/index.html'
    title = 'Тарифы'


class TariffCreateView(TariffBaseView, TitleMixin, CreateView):
    """View to create a new tariff"""
    template_name = 'tariff/edit.html'
    title = 'Новый тариф'


class TariffUpdateView(TariffBaseView, TitleMixin, UpdateView):
    """View to update a tariff"""
    template_name = 'tariff/edit.html'
    title = 'Редактировать тариф'


class TariffDeleteView(TariffBaseView, TitleMixin, DeleteView):
    """View to delete a tariff"""
    template_name = 'tariff/confirm_delete.html'
    title = 'Удалить тариф'
