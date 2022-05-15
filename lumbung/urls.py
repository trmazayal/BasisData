from django.contrib import admin
from django.urls import path
from .views import produksi_tanaman, transaksi_upgrade_lumbung, histori_produksi_tanaman, upgrade_lumbung

urlpatterns = [
    path('transaksi-upgrade-lumbung/', transaksi_upgrade_lumbung, name='transaksi-upgrade-lumbung'),
    path('histori-produksi-tanaman/', histori_produksi_tanaman, name='histori-produksi-tanaman'),
    path('upgrade-lumbung/', upgrade_lumbung, name='upgrade-lumbung'),
    path('produksi-tanaman/', produksi_tanaman, name='produksi-tanaman'),
]