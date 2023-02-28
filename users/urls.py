from django.contrib.auth import views as auth_views
from django.urls import path

from users.views import login

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
