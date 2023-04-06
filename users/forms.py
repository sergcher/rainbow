from django import forms
from django.contrib.auth.forms import AuthenticationForm

from users.models import User


class UserLoginForm(AuthenticationForm):

    attrs_user = {'class': 'card w-100',
                  'style': 'border-color: #D9D9D9;'
                           'padding-left: 10px;'
                           'padding-bottom: 2px;',
                  'placeholder': 'Введите имя пользователя',
                  }

    attrs_pass = {'class': 'card w-100',
                  'style': 'border-color: #D9D9D9;'
                           'padding-left: 10px;'
                           'padding-bottom: 2px;',
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

    class Meta:
        model = User
        fields = ('username', 'password')
