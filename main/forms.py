from django import forms

from main.models import (ApartmentCharge, ApartmentCounter, ApartmentDetail,
                         Settings, Tariff)


class TariffChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class ApartmentDetailForm(forms.ModelForm):
    attrs = {'class': 'card',
             'style': 'border-color: #D9D9D9; '
                      'padding-left: 10px;'
                      'padding-bottom: 2px;'
             }

    error_messages = {
        'invalid': 'Для ввода дробных чисел используйте точку'
    }

    registredQt = forms.IntegerField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0,
        label='Количество зарегистрированных:'
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
        label='Общая площадь:'
    )

    personalAccount = forms.IntegerField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0,
        label='Лицевой счет:'
    )

    account_number = forms.CharField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0,
        label='Единый лиц. счёт в ГИС ЖКХ:'
    )

    tariff = TariffChoiceField(
        queryset=Tariff.objects.all(),
        widget=forms.Select(attrs=attrs),
        error_messages=error_messages,
        required=False,
        empty_label=None,
        label='Действующий тариф:'
    )

    class Meta:
        model = ApartmentDetail
        fields = ('registredQt', 'livedQt', 'totalArea',
                  'personalAccount', 'account_number',
                  'serialNumber', 'tariff')
        labels = {
            'registredQt': 'Количество зарегистрированных', 'livedQt': 'Количество проживающих',
            'totalArea': 'Общая площадь', 'personalAccount': 'Лицевой счет',
            'account_number': 'Единый лицевой счет в ГИС ЖКХ', 'tariff': 'Действующий тариф'
        }


class ApartmentCounterForm(forms.ModelForm):
    class Meta:
        model = ApartmentCounter
        fields = "__all__"


class ApartmentChargeForm(forms.ModelForm):
    class Meta:
        model = ApartmentCharge
        fields = ('money_deposited', 'fine', 'balance_start', 'recalculation_electricity',
                  'recalculation_heating_rub', 'recalculation_hot_water',
                  'recalculation_cold_water',
                  'recalculation_sewage', 'recalculation_solid_waste', 'serialNumber')
        labels = {
            'money_deposited': 'Оплачено', 'fine': 'Пеня',
            'balance_start': 'Сальдо начало',
            'recalculation_electricity': 'Перерасчет электроэнергия',
            'recalculation_heating_rub': 'Перерасчет подогрев воды',
            'recalculation_hot_water': 'Перерасчет горячая вода',
            'recalculation_cold_water': 'Перерасчет холодная вода',
            'recalculation_sewage': 'Перерасчет канализация',
            'recalculation_solid_waste': 'Перерасчет обращение с ТКО',
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
            'month_name': 'Месяц:', 'month_to_pay': 'К оплате на (месяц):',
            'month_to_date': 'К оплате на (дата):',
            'bill': 'Счет-извещение:', 'pay_up_to': 'Оплатить до:'
        }
