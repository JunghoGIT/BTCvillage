from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from . import views



app_name ='btc'



urlpatterns = [
    path('/', views.index, name='index'),
    path('createorder/',views.createorder, name='createorder')
]

