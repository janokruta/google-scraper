from django.shortcuts import redirect
from django.urls import path

from scraper.views import home, search_result, settings

urlpatterns = [
    path('search', search_result, name='search_result'),
    path('search/', lambda r: redirect('home')),
    path('settings/', settings, name='settings'),
    path('', home, name='home'),
]
