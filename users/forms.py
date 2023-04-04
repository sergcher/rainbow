from django import forms
from django.contrib.auth.forms import AuthenticationForm

from users.models import User


class UserLoginForm(AuthenticationForm):

    attrs_user = {'class': 'form-control',
                  'style': 'border-color: #D9D9D9;'
                           'padding-left: 10px;'
                           'padding-bottom: 2px;'
                           'margin-bottom: 15px;',
                  'placeholder': 'Введите имя пользователя',
                  }

    attrs_pass = {'class': 'form-control',
                  'style': 'border-color: #D9D9D9;'
                           'padding-left: 10px;'
                           'padding-bottom: 2px;'
                           'margin-bottom: 15px;',
                  'placeholder': 'Введите пароль',
                  }

    username = forms.CharField(
        widget=forms.TextInput(attrs=attrs_user)
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs=attrs_pass
        )
    )

    # username = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'form-control py-4', }))
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control py-4',
    #                                                              'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'password')
