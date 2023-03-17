from django.urls import path
from . import views


"""
    PRODUCTS APPLICATION URLS
    (BASED ON '../product/')
"""
urlpatterns = [
    path('', views.prompt_recycle_product_view, name='product_info'),  # The URL for product information page
    path('create/', views.create_product_view, name='create_product'),  # The URL for creating a product page
    path('dex/', views.product_dex, name='product_dex'),
]