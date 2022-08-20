from django.urls import path, include, re_path
from . import views


urlpatterns = [
    path('', views.getJob),
    path('add/', views.addJob),
]