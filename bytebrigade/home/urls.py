from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='index'),
    path('leaderboard/', views.getLeaderboard, name='leaderboard'),
    path('instruction/', views.instruction_view, name='instruction'),
]