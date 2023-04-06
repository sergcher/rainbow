from django.shortcuts import redirect, render

from main.calculation import calculate_fees
from main.excel import (export_client_bank, export_excel_apartment_total_file,
                        generate_excel_file)
from main.forms import (ApartmentChargeForm, ApartmentCounterForm,
                        ApartmentDetailForm, Settings, SettingsForm)
from main.models import (Apartment, ApartmentCharge, ApartmentCounter,
                         ApartmentDetail, ApartmentFee)
from main.pdf_generator import generate_pdf
from users.forms import UserLoginForm


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
        'settings_form': form,
    }
    return render(request, 'main/settings_form.html', context)


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
        'settings_form': SettingsForm(instance=Settings.objects.get(id=1)),
        'login_form': UserLoginForm(data=request.POST)
    }
    return render(request, 'main/index.html', context)


def update(request, id):
    form = ApartmentDetailForm(instance=ApartmentDetail.objects.get(serialNumber=id))
    counterform = ApartmentCounterForm(instance=ApartmentCounter.objects.get(serialNumber=id))
    chargeform = ApartmentChargeForm(instance=ApartmentCharge.objects.get(serialNumber=id))
    prev_url = f"/update/{int(id) - 1}"
    next_url = f"/update/{int(id) + 1}"

    shortOwnerName = Apartment.objects.get(serialNumber=id).owner.split()
    shortOwnerName = f"{shortOwnerName[0]} {shortOwnerName[1][0]}.{shortOwnerName[2][0]}."

    if request.method == 'POST':
        if 'details' in request.POST:
            form = ApartmentDetailForm(
                request.POST, instance=ApartmentDetail.objects.get(serialNumber=id)
                )
            if form.is_valid():
                form.save()
                return redirect(request.path_info)
            else:
                print(form.errors)
        elif 'counters' in request.POST:
            counterform = ApartmentCounterForm(
                request.POST, instance=ApartmentCounter.objects.get(
                    serialNumber=id
                    )
                )
            if counterform.is_valid():
                counterform.save()
                return redirect(request.path_info)
            else:
                print(counterform.errors)
        elif 'charge' in request.POST:
            chargeform = ApartmentChargeForm(
                request.POST, instance=ApartmentCharge.objects.get(serialNumber=id)
                )
            if chargeform.is_valid():
                chargeform.save()
                return redirect(request.path_info)
            else:
                print(chargeform.errors)
    context = {
        'form': form,
        'counterform': counterform,
        'chargeform': chargeform,
        'prev_url': prev_url,
        'next_url': next_url,
        'page_num': id,
        'shortOwnerName': shortOwnerName,
        'settings_form': SettingsForm(instance=Settings.objects.get(id=1)),
        'login_form': UserLoginForm(data=request.POST)
    }
    return render(request, 'main/edit.html', context)


def update_fees(request):
    calculate_fees()
    return redirect('index')


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
