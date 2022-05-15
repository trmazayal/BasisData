from django.contrib import admin
from django.urls import path
from .views import menu_lihat_koleksi_aset, read_koleksi_dekorasi, read_koleksi_bibit_tanaman, read_koleksi_hewan, read_koleksi_alat_produksi, read_koleksi_petak_sawah

app_name = "koleksi_aset"
urlpatterns = [
    path('menuLihatKoleksiAset/', menu_lihat_koleksi_aset, name='menu_read_koleksi_aset'),
    path('readKoleksiDekorasi/', read_koleksi_dekorasi, name='read_koleksi_dekorasi'),
    path('readKoleksiBibitTanaman/', read_koleksi_bibit_tanaman, name='read_koleksi_bibit_tanaman'),
    path('readKoleksiHewan/', read_koleksi_hewan, name='read_koleksi_hewan'),
    path('readKoleksiKandang/', read_koleksi_hewan name='read_koleksi_kandang'),
    path('readKoleksiAlatProduksi/', read_koleksi_alat_produksi, name='read_koleksi_alat_produksi'),
    path('readKoleksiPetakSawah/', read_koleksi_petak_sawah, name='read_koleksi_petak_sawah'),
]