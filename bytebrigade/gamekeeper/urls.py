from django.urls import path
from . import views

urlpatterns = [
    path('', views.gamekeeperPage, name='gamekeeperPage'),
    path('addBin', views.addBin, name='addBin'),
    path('addGoal', views.addGoal, name='addGoal'),
    path('addShopItem', views.addShopItem, name='addShopItem'),
]