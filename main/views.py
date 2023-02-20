from django.shortcuts import render, redirect
from main.forms import *
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from main.calculation import calculate_fees
from main.excells import generate_excel_file
from main.pdf_generator import generate_pdf


def index(request):
    context = {
        'title': 'ТСЖ Радуга',
        'apartments': Apartment.objects.all(),
        'apartment_details': ApartmentDetail.objects.all(),
        'apartment_fees': ApartmentFee.objects.all(),
    }
    return render(request, 'main/index.html', context)


def update(request, id):
    form = ApartmentDetailForm(instance=ApartmentDetail.objects.get(serialNumber=id))
    counterform = ApartmentCounterForm(instance=ApartmentCounter.objects.get(serialNumber=id))
    chargeform = ApartmentChargeForm(instance=ApartmentCharge.objects.get(serialNumber=id))
    optionsform = ApartmentOptionsForm(instance=ApartmentOption.objects.get(serialNumber=id))
    prev_url = f"/update/{int(id) - 1}"
    next_url = f"/update/{int(id) + 1}"
    if request.method == 'POST':
        if 'details' in request.POST:
            form = ApartmentDetailForm(request.POST, instance=ApartmentDetail.objects.get(serialNumber=id))
            if form.is_valid():
                form.save()
                return redirect('index')
            else:
                print(form.errors)
        elif 'counters' in request.POST:
            counterform = ApartmentCounterForm(request.POST, instance=ApartmentCounter.objects.get(serialNumber=id))
            if counterform.is_valid():
                counterform.save()
                return redirect('index')
            else:
                print(counterform.errors)
        elif 'charge' in request.POST:
            chargeform = ApartmentChargeForm(request.POST, instance=ApartmentCharge.objects.get(serialNumber=id))
            if chargeform.is_valid():
                chargeform.save()
                return redirect('index')
            else:
                print(chargeform.errors)
        elif 'options' in request.POST:
            optionsform = ApartmentOptionsForm(request.POST, instance=ApartmentOption.objects.get(serialNumber=id))
            if optionsform.is_valid():
                optionsform.save()
                return redirect('index')
            else:
                print(optionsform.errors)
    context = {
        'form': form,
        'counterform': counterform,
        'chargeform': chargeform,
        'optionsform': optionsform,
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
    # Get all apartment fees
    apartment_fees = ApartmentFee.objects.all()

    # Generate the Excel file and return the response
    response = generate_excel_file(apartment_fees)
    return response


def apartment_receipt(request):
    # ... your code to get the data for the PDF goes here ...
    data = {'some': 'data'}

    # generate the PDF response using the imported generate_pdf() function
    pdf = generate_pdf(data)

    # return the PDF response
    return pdf
