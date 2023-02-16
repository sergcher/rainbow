from django.contrib import admin
from django.urls import path
from main import views

from main.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('update/<int:id>', views.update),
]
