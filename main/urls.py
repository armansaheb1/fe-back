"""fexchange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('balance', views.balance.as_view() ),
    path('deposit', views.deposit.as_view() ),
    path('withdraw', views.withdraw.as_view() ),
    path('pin', views.pined.as_view() ),
    path('get_price', views.get_price.as_view() ),
    path('l_close', views.l_close.as_view() ),
    path('l_cancel', views.l_cancel.as_view() ),
    path('m_close', views.m_close.as_view() ),
    path('tp_cancel', views.tp_cancel.as_view() ),
    path('sl_cancel', views.sl_cancel.as_view() ),
    path('tpsl_send', views.tpsl_send.as_view() ),
    path('balances', views.balances.as_view() ),
    path('users', views.users.as_view() ),
    path('token', views.token.as_view() ),
    path('symbols', views.symbols.as_view() ),
    path('positions', views.positions.as_view() ),
    path('orders', views.orders.as_view() ),
    path('closeorders', views.closeorders.as_view() ),
    path('allorders', views.allorders.as_view() ),
    path('fav', views.fav.as_view() ),
    path('buy', views.buy.as_view() ),
    path('sell', views.sell.as_view() ),
    path('historicalsell', views.historicalsell.as_view() ),
    path('historicalbuy', views.historicalbuy.as_view() ),
]
