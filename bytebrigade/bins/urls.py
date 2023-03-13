from django.urls import path

from . import views

urlpatterns = [
    # path('bin_map', views.bin_map, name='bin_map'),
    path('bin/map/', views.bin_map_view, name='bin_map'),
    path('bin/map/nav/', views.bin_nav_view, name='bin_nav'),
    path('bin/map/arrive/', views.bin_arrived_view, name='bin_arrive')
]