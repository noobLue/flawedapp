from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sql', views.sql_injection, name='sql')
]