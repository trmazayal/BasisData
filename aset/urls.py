from django.contrib import admin
from django.urls import path
from .views import menu_lihat_aset, read_dekorasi, read_bibit_tanaman, read_hewan, read_kandang, read_alat_produksi, read_petak_sawah

app_name = "aset"
urlpatterns = [
    path('menuLihatAset/', menu_lihat_aset, name='menu_read_aset'),
    path('readDekorasi/', read_dekorasi, name='read_dekorasi'),
    path('readBibitTanaman/', read_bibit_tanaman, name='read_bibit_tanaman'),
    path('readHewan/', read_hewan, name='read_hewan'),
    path('readKandang/', read_kandang, name='read_kandang'),
    path('readAlatProduksi/', read_alat_produksi, name='read_alat_produksi'),
    path('readPetakSawah/', read_petak_sawah, name='read_petak_sawah'),
    path('createDekorasi/', create_dekorasi, name='create_dekorasi'),
    path('createBibitTanaman/', create_bibit_tanaman, name='create_bibit_tanaman'),
    path('createHewan/', create_hewan, name='create_hewan'),
    path('createKandang/', create_kandang, name='create_kandang'),
    path('createAlatProduksi/', create_alat_produksi, name='create_alat_produksi'),
    path('createPetakSawah/', create_petak_sawah, name='create_petak_sawah'),
]