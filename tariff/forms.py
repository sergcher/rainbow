from django import forms

from .models import Tariff


class TariffForm(forms.ModelForm):
    attrs = {'class': 'card w-100',
             'style': 'border-color: #D9D9D9; '
                      'padding-left: 10px;'
                      'padding-bottom: 2px;'
             }

    error_messages = {
        'invalid': 'For entering decimal numbers, please use a dot (.)'
    }

    name = forms.CharField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages
    )

    maintenance = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )

    heating = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
        )
    heating_rub = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )
    hot_water = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )

    hot_water_odn = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )

    cold_water = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )
    cold_water_odn = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )
    sewage = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )
    sewage_odn = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )
    solid_waste = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )
    electricity = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )
    lift = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )
    electricity_odn = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )
    capital_repair = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )

    class Meta:
        model = Tariff
        fields = "__all__"
