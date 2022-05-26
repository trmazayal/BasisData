from unicodedata import name
from django.contrib import admin
from django.urls import path
from .views import delete_paket_koin, form_beli_paket_koin, form_buat_paket_koin, paket_koin, pembelian_paket_koin, transaksi_pembelian_koin, buat_paket_koin, ubah_paket_koin, update_paket_koin

urlpatterns = [
    path('', paket_koin, name='paket-koin'),
    path('transaksi-pembelian-koin/', transaksi_pembelian_koin, name='transaksi-pembelian-koin'),
    path('buat-paket-koin/', buat_paket_koin, name='buat-paket-koin'),
    path('form-buat-paket-koin/', form_buat_paket_koin, name='form-buat-paket-koin'),
    path('ubah-paket-koin/<str:jumlah_koin>/', ubah_paket_koin, name='ubah-paket-koin'),
    path('update-paket-koin/', update_paket_koin, name='update-paket-koin'),
    path('pembelian-paket-koin/<str:jumlah_koin>/', pembelian_paket_koin, name='pembelian-paket-koin'),
    path('form-beli-paket-koin/', form_beli_paket_koin, name='form-beli-paket-koin'),
    path('delete-paket-koin/<str:jumlah_koin>/', delete_paket_koin, name='delete-paket-koin'),
]