from django.urls import path

from . import views

urlpatterns = [
    path('', views.getTransactions, name='index'),
    path('leaderboard/', views.getLeaderboard, name='leaderboard'),
    path('instruction/', views.instruction_view, name='instruction'),
]