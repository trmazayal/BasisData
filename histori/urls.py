"""tk_e06 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from .views import create_pesanan, list_histori_hewan, list_histori_penjualan, list_pesanan, detail_histori_penjualan, detail_pesanan, create_histori_hewan, create_histori_penjualan, update_pesanan, delete_pesanan
app_name='histori'

urlpatterns = [
    path('ListHistoriHewan/', list_histori_hewan, name='list_histori_hewan'),
    path('CreateHistoriHewan/', create_histori_hewan, name='create_histori_hewan'),
    path('ListHistoriPenjualan/', list_histori_penjualan, name='list_histori_penjualan'),
    path('DetailHistoriPenjualan/<id_pesanan>/', detail_histori_penjualan, name='detail_histori_penjualan'),
    path('CreateHistoriPenjualan/', create_histori_penjualan, name='create_histori_penjualan'),
    path('ListPesanan/', list_pesanan, name='list_pesanan'),
    path('DetailPesanan/<id_pesanan>/', detail_pesanan, name='detail_pesanan'),
    path('CreatePesanan/', create_pesanan, name='create_pesanan'),
    path('UpdatePesanan/<id_pesanan>/', update_pesanan, name='update_pesanan'),
    path('DeletePesanan/<id_pesanan>/', delete_pesanan, name="delete_pesanan"),
]
    
    
    
    
    
    
    
