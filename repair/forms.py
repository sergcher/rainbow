from django import forms

from .models import CapitalRepair


class CapitalRepairForm(forms.ModelForm):
    attrs = {'class': 'card w-100',
             'style': 'border-color: #D9D9D9; '
                      'padding-left: 10px;'
                      'padding-bottom: 2px;'
             }

    error_messages = {
        'invalid': 'Для ввода дробных чисел используйте точку'
    }

    debt = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )

    fine = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
        )

    paid = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )

    recalculation = forms.FloatField(
        widget=forms.TextInput(attrs=attrs),
        error_messages=error_messages,
        initial=0
    )

    class Meta:
        model = CapitalRepair
        fields = "__all__"
