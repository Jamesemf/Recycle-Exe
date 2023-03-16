from django.urls import path
from . import views


"""
    BARCODEREADER APPLICATION URLS
    (BASED ON '../scanner/')
"""
urlpatterns = [
        path('', views.scanner_page_view, name='barcode_lookup'),
        path('recycle/confirm/', views.recycle_confirm_view, name='recycle_confirm'),
    ]