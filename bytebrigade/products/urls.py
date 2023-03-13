from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create_product_view, name='create_product'),
    path('', views.prompt_recycle_product_view, name='product_info'),
]