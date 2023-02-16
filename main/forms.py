from django import forms
from main.models import ApartmentDetail, ApartmentCounter, ApartmentCharge, ApartmentOption


class ApartmentDetailForm(forms.ModelForm):
    class Meta:
        model = ApartmentDetail
        fields = "__all__"


class ApartmentCounterForm(forms.ModelForm):
    class Meta:
        model = ApartmentCounter
        fields = "__all__"


class ApartmentChargeForm(forms.ModelForm):
    class Meta:
        model = ApartmentCharge
        fields = "__all__"


class ApartmentOptionsForm(forms.ModelForm):
    class Meta:
        model = ApartmentOption
        fields = "__all__"
