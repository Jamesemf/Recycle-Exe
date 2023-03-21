from django.urls import path
from . import views


"""
    BINS APPLICATION URLS
    (BASED ON '../bin/')
"""
urlpatterns = [
    # path('bin_map', views.bin_map, name='bin_map'),
    path('map/', views.bin_map_view, name='bin_map'),
    path('nav/', views.bin_nav_view, name='bin_nav'),
]