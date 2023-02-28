from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from main.calculation import calculate_fees
from main.excells import export_client_bank, generate_excel_file, export_excel_apartment_total_file
from main.forms import SettingsForm, Settings, ApartmentDetailForm, ApartmentCounterForm
from main.forms import ApartmentChargeForm
from main.pdf_generator import generate_pdf
from main.models import Tariff, ApartmentCharge, Apartment, ApartmentDetail, ApartmentFee
from main.models import ApartmentCounter


def index(request):
    filter_criteria = request.GET.get('filter')
    if filter_criteria == 'balance_end_gt_6000':
        apartments = Apartment.objects.filter(apartmentfee__balance_end__gt=6000)
    else:
        apartments = Apartment.objects.all()
    context = {
        'title': 'ТСЖ Радуга',
        'apartments': apartments,
        'apartment_details': ApartmentDetail.objects.all(),
        'apartment_fees': ApartmentFee.objects.all(),
        'apartment_charges': ApartmentCharge.objects.all(),
    }
    return render(request, 'main/index.html', context)


def update(request, id):
    form = ApartmentDetailForm(instance=ApartmentDetail.objects.get(serialNumber=id))
    counterform = ApartmentCounterForm(instance=ApartmentCounter.objects.get(serialNumber=id))
    chargeform = ApartmentChargeForm(instance=ApartmentCharge.objects.get(serialNumber=id))
    prev_url = f"/update/{int(id) - 1}"
    next_url = f"/update/{int(id) + 1}"
    if request.method == 'POST':
        if 'details' in request.POST:
            form = ApartmentDetailForm(request.POST, instance=ApartmentDetail.objects.get(serialNumber=id))
            if form.is_valid():
                form.save()
                return redirect(request.path_info)
            else:
                print(form.errors)
        elif 'counters' in request.POST:
            counterform = ApartmentCounterForm(request.POST, instance=ApartmentCounter.objects.get(serialNumber=id))
            if counterform.is_valid():
                counterform.save()
                return redirect(request.path_info)
            else:
                print(counterform.errors)
        elif 'charge' in request.POST:
            chargeform = ApartmentChargeForm(request.POST, instance=ApartmentCharge.objects.get(serialNumber=id))
            if chargeform.is_valid():
                chargeform.save()
                return redirect(request.path_info)
            else:
                print(chargeform.errors)
    context = {
        'form': form,
        'counterform': counterform,
        'chargeform': chargeform,
        "prev_url": prev_url,
        "next_url": next_url,
        "page_num": id
    }
    return render(request, 'main/edit.html', context)


class TariffBaseView(View):
    model = Tariff
    fields = '__all__'
    success_url = reverse_lazy('main:all')


class TariffListView(TariffBaseView, ListView):
    """View to list all tariffs.
    Use the 'tariff_list' variable in the template
    to access all Tariff objects"""


class TariffDetailView(TariffBaseView, DetailView):
    """View to list the details from one tariff.
    Use the 'tariff' variable in the template to access
    the specific tariff here and in the Views below"""


class TariffCreateView(TariffBaseView, CreateView):
    """View to create a new tariff"""


class TariffUpdateView(TariffBaseView, UpdateView):
    """View to update a tariff"""


class TariffDeleteView(TariffBaseView, DeleteView):
    """View to delete a tariff"""


def update_fees(request):
    calculate_fees()
    return redirect('index')


def settings(request):
    form = SettingsForm(instance=Settings.objects.get(id=1))
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=Settings.objects.get(id=1))
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            print(form.errors)
    context = {
        'form': form,
    }
    return render(request, 'main/settings_form.html', context)


def generate_excel(request):
    filter_criteria = request.GET.get('filter')
    if filter_criteria == 'balance_end_gt_6000':
        apartments = Apartment.objects.filter(apartmentfee__balance_end__gt=6000)
    else:
        apartments = Apartment.objects.all()
    response = generate_excel_file(apartments)
    return response


def generate_excel_apartment_total_file(request):
    response = export_excel_apartment_total_file()
    return response


def generate_txt(request):
    response = export_client_bank()
    return response


def apartment_receipt(request):
    pdf = generate_pdf()
    return pdf
