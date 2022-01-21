from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from . import views



app_name ='btc'



urlpatterns = [
    path('', views.index, name='index'),
    path('order/create/limit', views.create_order_limit, name='create_order_limit'),
    path('order/contract/market', views.contract_order_market, name='contract_order_market'),
    path('order/list/<int:pk>', views.user_order_list, name='user_order_list'),
    path('order/contract/limit', views.contract_order_limit, name='contract_order_limit'),
    path('order/delete/<int:pk>', views.order_delete, name='order_delete'),
    path('exchange/', views.get_exchange, name='get_exchange')
]

