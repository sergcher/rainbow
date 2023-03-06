from django.contrib import admin
from django.urls import include, path

from main import views
from main.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('', include('main.urls', namespace='main')),
    path('tariff/', include('tariff.urls', namespace='tariff')),
    path('repair/', include('repair.urls', namespace='repair')),
    path('', index, name='index'),
    path('update/<int:id>', views.update),

]
