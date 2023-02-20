from django import forms
from main.models import *


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


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = "__all__"
