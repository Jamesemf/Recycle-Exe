from django.urls import path

from . import views

urlpatterns = [
    path('bin_map', views.bin_map, name='bin_map'),
]