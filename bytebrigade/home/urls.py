from django.urls import path
from . import views


"""
    HOME APPLICATION URLS
    (BASED ON ../)
"""
urlpatterns = [
    path('', views.home_view, name='index'),
    path('leaderboard/', views.getLeaderboard, name='leaderboard'),  # URL for the leaderboard page
    path('abouts/', views.instruction_view, name='instruction'),  # URL for the about page
    path('privacy/', views.privacy_policy, name='privacy'),  # URL for the privacy policy page
    path('about-us/', views.about_us_view, name='aboutus'),  # URL for the privacy policy page
    path('license/', views.license_view, name='license'),  # URL for the privacy policy page
]