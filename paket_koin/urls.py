from unicodedata import name
from django.contrib import admin
from django.urls import path
from .views import paket_koin, pembelian_paket_koin, transaksi_pembelian_koin, buat_paket_koin, ubah_paket_koin

urlpatterns = [
    path('', paket_koin, name='paket-koin'),
    path('transaksi-pembelian-koin/', transaksi_pembelian_koin, name='transaksi-pembelian-koin'),
    path('buat-paket-koin/', buat_paket_koin, name='buat-paket-koin'),
    path('ubah-paket-koin/', ubah_paket_koin, name='ubah-paket-koin'),
    path('pembelian-paket-koin/', pembelian_paket_koin, name='pembelian-paket-koin')
]