from django.shortcuts import render, redirect
from main.models import Apartment, ApartmentDetail
from main.forms import ApartmentDetailForm


def index(request):
    context = {
              'title': 'ТСЖ Радуга',
              'apartments': Apartment.objects.all(),
              'apartment_details': ApartmentDetail.objects.all(),
              }
    return render(request, 'main/index.html', context)


def edit(request, id):
    apartmentdetails = ApartmentDetail.objects.get(serialNumber=id)
    return render(request, 'main/edit.html', {'apartmentdetails': apartmentdetails})


def update(request, id):
    form = ApartmentDetailForm(instance=ApartmentDetail.objects.get(serialNumber=id))
    if request.method == 'POST':
        form = ApartmentDetailForm(request.POST, instance=ApartmentDetail.objects.get(serialNumber=id))
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            print(form.errors)
    return render(request, 'main/edit.html', {'form': form})
