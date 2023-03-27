import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from main.models import Apartment, ApartmentDetail
from repair.excel import (export_excel_repair_total_file,
                          repair_export_client_bank,
                          repair_generate_excel_file)
from repair.models import CapitalRepair
from repair.pdf_repair import repair_generate_pdf
from repair.forms import CapitalRepairForm
from users.forms import UserLoginForm
from main.forms import (Settings, SettingsForm)


def repair_list(request):
    return render(request, 'repair/repair_list.html', {
        'repairs': CapitalRepair.objects.all(),
        'apartments': Apartment.objects.all(),
        'details': ApartmentDetail.objects.all(),
    })


def edit_repair(request, pk):
    repair = get_object_or_404(CapitalRepair, pk=pk)
    if request.method == "POST":
        repair_form = CapitalRepairForm(request.POST, instance=repair)
        if repair_form.is_valid():
            repair_form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "repairListChanged": None,
                        "showMessage": f"Данные по квартире №{repair.serialNumber} изменены."
                    })
                }
            )
    else:
        repair_form = CapitalRepairForm(instance=repair)
    return render(request, 'repair/edit.html', {
        'repair_form': repair_form,
        'repair': repair,
        'title': f'КАПИТАЛЬНЫЙ РЕМОНТ КВАРТИРА №{repair.serialNumber}',
    })


class RepairBaseView(View):
    model = CapitalRepair
    fields = '__all__'
    success_url = reverse_lazy('repair:repair_list')


class RepairListView(TitleMixin, ListView):
    template_name = 'repair/index.html'
    title = 'Капитальный ремонт'
    queryset = CapitalRepair.objects.all()
    ordering = 'serialNumber'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RepairListView, self).get_context_data()
        context['details'] = ApartmentDetail.objects.all()
        context['apartments'] = Apartment.objects.all()
        context['repairs'] = CapitalRepair.objects.all()
        context['settings_form'] = SettingsForm(instance=Settings.objects.get(id=1))
        context['login_form'] = UserLoginForm()
        return context


def repair_generate_txt(request):
    response = repair_export_client_bank()
    return response


def repair_generate_excel(request):
    apartments = Apartment.objects.all()
    response = repair_generate_excel_file(apartments)
    return response


def generate_excel_repair_total_file(request):
    response = export_excel_repair_total_file()
    return response


def repairs_receipt(request):
    pdf = repair_generate_pdf()
    return pdf
