from django import forms

from main.models import (ApartmentCharge, ApartmentCounter, ApartmentDetail,
                         Settings, Tariff)


class TariffChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class ApartmentDetailForm(forms.ModelForm):
    attrs = {'class': 'form-control',
             'style': 'border-color: #D9D9D9;'
                      'padding-left: 10px;'
                      'padding-bottom: 2px;'
                      'margin-bottom: 15px;'
             }

    attrs_tariff = {'class': 'form-control',
                    'style': 'border-color: #D9D9D9;'
                             'margin-top: 1px;'
                             'height: 33px;'
                             'padding-left: 10px;'
                             'padding-bottom: 2px;'
                             'margin-bottom: 15px;'
                    }

    error_messages = {
        'invalid': 'For entering decimal numbers, please use a dot (.)'
    }

    registredQt = forms.IntegerField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0,
        label='Number of registered:'
    )

    livedQt = forms.IntegerField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0,
        label='Количество проживающих:'
    )

    totalArea = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0,
        label='Apartment size:'
    )

    personalAccount = forms.IntegerField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0,
        label='Personal account:'
    )

    account_number = forms.CharField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0,
        label='Unified personal account:'
    )

    tariff = TariffChoiceField(
        queryset=Tariff.objects.all(),
        widget=forms.Select(attrs=attrs_tariff),
        error_messages=error_messages,
        required=False,
        empty_label=None,
        label='Current tariff:'
    )

    class Meta:
        model = ApartmentDetail
        fields = ('registredQt', 'livedQt', 'totalArea',
                  'personalAccount', 'account_number',
                  'serialNumber', 'tariff')
        labels = {
            'registredQt': 'Number of registered', 'livedQt': 'Number of residents',
            'totalArea': 'Apartment size', 'personalAccount': 'Licence account',
            'account_number': 'Unified personal account', 'tariff': 'Current tariff'
        }


class ApartmentCounterForm(forms.ModelForm):
    attrs = {'class': 'form-control',
             'style': 'border-color: #D9D9D9;'
                      'padding-left: 10px;'
                      'padding-bottom: 2px;'
                      'margin-bottom: 15px;',
             'data-toggle': 'tooltip',
             'data-placement': 'top',
             }

    attrs_previous = {'class': 'form-control',
                      'style': 'border-color: #D9D9D9;'
                               'padding-left: 10px;'
                               'padding-bottom: 2px;'
                               'margin-bottom: 15px;',
                      'data-toggle': 'tooltip',
                      'data-placement': 'top',
                      'title': 'Предыдущее показание',
                      }

    attrs_current = {'class': 'form-control',
                     'style': 'border-color: #D9D9D9;'
                              'padding-left: 10px;'
                              'padding-bottom: 2px;'
                              'margin-bottom: 15px;',
                     'data-toggle': 'tooltip',
                     'data-placement': 'top',
                     'title': 'Введите новое показание',
                     }

    error_messages = {
        'invalid': 'For entering decimal numbers, please use a dot (.)'
    }

    hot_water_previous = forms.IntegerField(
        widget=forms.TextInput(attrs=attrs_previous),
        error_messages=error_messages,
        initial=0,
    )

    hot_water_current = forms.IntegerField(
        widget=forms.TextInput(attrs=attrs_current),
        error_messages=error_messages,
        initial=0
    )

    hot_water_value = forms.IntegerField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )

    electricity_previous = forms.IntegerField(
        widget=forms.TextInput(attrs=attrs_previous),
        error_messages=error_messages,
        initial=0
    )

    electricity_current = forms.IntegerField(
        widget=forms.TextInput(attrs=attrs_current),
        error_messages=error_messages,
        initial=0
    )

    electricity_value = forms.IntegerField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )

    cold_water_previous = forms.IntegerField(
        widget=forms.TextInput(attrs=attrs_previous),
        error_messages=error_messages,
        initial=0
    )

    cold_water_current = forms.IntegerField(
        widget=forms.TextInput(attrs=attrs_current),
        error_messages=error_messages,
        initial=0
    )

    cold_water_value = forms.IntegerField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )

    wastewater_value = forms.IntegerField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )

    class Meta:
        model = ApartmentCounter
        fields = "__all__"


class ApartmentChargeForm(forms.ModelForm):
    attrs = {'class': 'form-control',
             'style': 'border-color: #D9D9D9;'
                      'padding-left: 10px;'
                      'padding-bottom: 2px;'
                      'margin-bottom: 15px;'
             }

    error_messages = {
        'invalid': 'For entering decimal numbers, please use a dot (.)'
    }

    money_deposited = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0,
        label='Paid:'
    )

    fine = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0,
        label='Fine:'
    )

    balance_start = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0,
        label='Balance start:'
    )

    recalculation_electricity = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0,
        label='Recalculating Electricity:'
    )

    recalculation_heating_rub = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0,
        label='Recalculating heating water:'
    )

    recalculation_hot_water = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0,
        label='Recalculating hot water:'
    )

    recalculation_cold_water = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0,
        label='Recalculating Cold water:'
    )

    recalculation_sewage = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0,
        label='Recalculating Sewerage:'
    )

    recalculation_solid_waste = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0,
        label='Recalculating Solid waste management:'
    )

    class Meta:
        model = ApartmentCharge
        fields = ('money_deposited', 'fine', 'balance_start', 'recalculation_electricity',
                  'recalculation_heating_rub', 'recalculation_hot_water',
                  'recalculation_cold_water',
                  'recalculation_sewage', 'recalculation_solid_waste', 'serialNumber')
        labels = {
            'money_deposited': 'Paid', 'fine': 'Fine',
            'balance_start': 'Balance start',
            'recalculation_electricity': 'Recalculating Electricity',
            'recalculation_heating_rub': 'Recalculating hot water',
            'recalculation_hot_water': 'Recalculating hot water',
            'recalculation_cold_water': 'Recalculating Cold water',
            'recalculation_sewage': 'Recalculating sewerage',
            'recalculation_solid_waste': 'Recalculating solid waste management',
        }


class SettingsForm(forms.ModelForm):
    attrs = {'class': 'card w-100',
             'style': 'border-color: #D9D9D9; '
                      'padding-left: 10px;'
                      'padding-bottom: 2px;'
             }

    month_name = forms.CharField(widget=forms.TextInput(attrs=attrs))
    month_to_pay = forms.CharField(widget=forms.TextInput(attrs=attrs))
    month_to_date = forms.CharField(widget=forms.TextInput(attrs=attrs))
    bill = forms.CharField(widget=forms.TextInput(attrs=attrs))
    pay_up_to = forms.CharField(widget=forms.TextInput(attrs=attrs))

    class Meta:
        model = Settings
        fields = ['month_name', 'month_to_pay', 'month_to_date', 'bill', 'pay_up_to']
        labels = {
            'month_name': 'Month:', 'month_to_pay': 'To be paid for (month):',
            'month_to_date': 'To be paid for (date):',
            'bill': 'Notification Bill:', 'pay_up_to': 'Pay before:'
        }
