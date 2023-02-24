from django import forms
from main.models import *


class ApartmentDetailForm(forms.ModelForm):
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
                  'recalculation_heating_rub', 'recalculation_hot_water', 'recalculation_cold_water',
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
    class Meta:
        model = Settings
        fields = ['month_name', 'month_to_pay', 'month_to_date', 'bill', 'pay_up_to']
        labels = {
            'month_name': 'Месяц', 'month_to_pay': 'К оплате на (месяц)', 'month_to_date': 'К оплате на (дата)',
            'bill': 'Счет-извещение', 'pay_up_to': 'Оплатить до'
        }
