from django.urls import path
from . import views

urlpatterns = [
    path('', views.gamekeeperPage, name='gamekeeperPage'),
    path('addBin', views.addBin, name='addBin'),
    path('addGoal', views.addGoal, name='addGoal'),
    path('addShopItem', views.addShopItem, name='addShopItem'),
    path('deleteBin', views.deleteBin, name='deleteBin'),
    path('deleteGoal', views.deleteGoal, name='deleteGoal'),
    path('deleteShopItem', views.deleteShopItem, name='deleteShopItem'),
]