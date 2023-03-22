from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from tariff.forms import TariffForm
from tariff.models import Tariff

import json


class TariffBaseView(View):
    model = Tariff
    fields = '__all__'
    success_url = reverse_lazy('tariff:tariff_list')


def tariff_list(request):
    return render(request, 'tariff/tariff_list.html', {
        'tariff_list': Tariff.objects.all(),
    })


class TariffListView(TariffBaseView, TitleMixin, ListView):
    """View to list all tariffs.
    Use the 'tariff_list' variable in the template
    to access all Tariff objects"""
    template_name = 'tariff/index.html'
    title = 'Тарифы'


def add_tariff(request):
    if request.method == "POST":
        tariff_form = TariffForm(request.POST)
        if tariff_form.is_valid():
            tariff = tariff_form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "tariffListChanged": None,
                        "showMessage": f"Тариф {tariff.name} добавлен."
                    })
                })
    else:
        tariff_form = TariffForm()
    return render(request, 'tariff/edit.html', {
        'tariff_form': tariff_form,
        'title': 'СОЗДАНИЕ НОВОГО ТАРИФА',
    })


def edit_tariff(request, pk):
    tariff = get_object_or_404(Tariff, pk=pk)
    if request.method == "POST":
        tariff_form = TariffForm(request.POST, instance=tariff)
        if tariff_form.is_valid():
            tariff_form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "tariffListChanged": None,
                        "showMessage": f"Тариф {tariff.name} изменен."
                    })
                }
            )
    else:
        tariff_form = TariffForm(instance=tariff)
    return render(request, 'tariff/edit.html', {
        'tariff_form': tariff_form,
        'tariff': tariff,
        'title': 'РЕДАКТИРОВАНИЕ ТАРИФА',
    })


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
