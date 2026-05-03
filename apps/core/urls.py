from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('health/', views.health, name='health'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
]
