from django.contrib import admin
from django.urls import path
from .views import read_transaksi_pembelian

app_name = "koleksi_aset"
urlpatterns = [
    path('menuBuatTransaksiPembelian/', menu_create_transaksi_pembelian, name='menu_create_transaksi_pembelian'),
    path('readTransaksiPembelian/', read_transaksi_pembelian, name='read_transaksi_pembelian'),
]