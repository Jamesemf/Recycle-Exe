from django.urls import path
from . import views
urlpatterns = [
        path('', views.barcode_lookup, name='barcode_lookup'),
        path('recycle/', views.recycle_confirm, name='recycle_confirm'),
        path('recycle/create/', views.create_product, name='create_product'),
        path('bin_map', views.bin_map, name='bin_map')
    ]