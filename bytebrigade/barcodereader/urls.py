from django.urls import path
from . import views
urlpatterns = [
        path('', views.scanner_page_view, name='barcode_lookup'),
        path('recycle/confirm/', views.recycle_confirm_view, name='recycle_confirm'),
        path('recycle/create/', views.create_product_view, name='create_product'),
        path('recycle/product/', views.prompt_recycle_product_view, name='prompt_product')
    ]