from django.urls import path

from . import views

urlpatterns = [
    path('product/create/', views.create_product, name='create_product'),
]