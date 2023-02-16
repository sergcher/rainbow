from django.shortcuts import render, redirect
from main.models import Apartment, ApartmentDetail, ApartmentCounter, ApartmentCharge, ApartmentOption
from main.forms import ApartmentDetailForm, ApartmentCounterForm, ApartmentChargeForm, ApartmentOptionsForm


def index(request):
    context = {
              'title': 'ТСЖ Радуга',
              'apartments': Apartment.objects.all(),
              'apartment_details': ApartmentDetail.objects.all(),
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
