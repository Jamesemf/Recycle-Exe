from django.urls import path
from . import views
urlpatterns = [
        path('', views.scanner_page_view, name='barcode_lookup'),
        path('recycle/confirm/', views.recycle_confirm_view, name='recycle_confirm'),
        path('recycle/create/', views.create_product_view, name='create_product'),
        path('recycle/product/', views.prompt_recycle_product_view, name='prompt_product'),
        path('bin/map/', views.bin_map_view, name='bin_map'),
        path('bin/map/nav/', views.bin_nav_view, name='bin_nav'),
        path('bin/map/arrive/', views.bin_arrived_view, name='bin_arrive')
    ]