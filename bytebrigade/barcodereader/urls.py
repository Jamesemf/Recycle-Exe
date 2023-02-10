from django.urls import path
from . import views
urlpatterns = [
        path('', views.barcode_lookup, name='barcode_lookup'),
    ]