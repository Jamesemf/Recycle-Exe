from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


"""
    ACCOUNT APPLICATION URLS
    (BASED ON '../account/')
"""
urlpatterns = [
    path('', views.account, name='account'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registration/', views.register, name='registration'),
    path('password/', views.password, name='password'),
    path('password/reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/emailsent', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password/change', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('addUserGoal/', views.addUserGoal, name='addUserGoal'),
]