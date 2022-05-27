from django.contrib import admin
from django.urls import path
from . import views

app_name = "transaksi_pembelian"

urlpatterns = [
    path('read/', views.read_transaksi_pembelian_aset, name='read_transaksi_pembelian_aset'),
    path('create/', views.create_transaksi_pembelian_aset, name='create_transaksi_pembelian_aset'),

]