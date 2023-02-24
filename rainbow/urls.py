from django.contrib import admin
from django.urls import path, include
from main import views

from main.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', index, name='index'),
    path('update/<int:id>', views.update),
    path('users/', include('users.urls', namespace='users')),
]
