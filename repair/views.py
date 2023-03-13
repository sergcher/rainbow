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
        return context


class RepairUpdateView(RepairBaseView, TitleMixin, UpdateView):
    """View to update a repair"""
    template_name = 'repair/edit.html'

    def get_context_data(self, **kwargs):
        context = super(RepairUpdateView, self).get_context_data(**kwargs)
        context['title'] = f'Капитальный ремонт квартира № {self.object.id}'
        context['prev_url'] = f"/repair/edit/{self.object.id - 1}"
        context['next_url'] = f"/repair/edit/{self.object.id + 1}"
        context['page_num'] = self.object.id
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
