from django import forms
from main.models import ApartmentDetail


class ApartmentDetailForm(forms.ModelForm):
    class Meta:
        model = ApartmentDetail
        fields = "__all__"
        #fields = ['registredQt', 'livedQt', 'totalArea', 'personalAccount', 'serialNumber']
