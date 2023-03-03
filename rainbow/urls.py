from django.contrib import admin
from django.urls import include, path

from main import views
from main.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('users/', include('users.urls', namespace='users')),
    path('', include('main.urls', namespace='main')),
    path('tariff/', include('tariff.urls', namespace='tariff')),

    path('update/<int:id>', views.update),

]
