from django.contrib import admin
from django.urls import path
from . import views

app_name = "aset"

urlpatterns = [
    path('read/', views.read_aset, name='read_aset'),
    path('read/dekorasi/', views.read_dekorasi, name='read_dekorasi'),
    path('read/bibit-tanaman/', views.read_bibit_tanaman, name='read_bibit_tanaman'),
    path('read/hewan/', views.read_hewan, name='read_hewan'),
    path('read/kandang/', views.read_kandang, name='read_kandang'),
    path('read/alat-produksi/', views.read_alat_produksi, name='read_alat_produksi'),
    path('read/petak-sawah/', views.read_petak_sawah, name='read_petak_sawah'),
    path('create/', views.create_aset, name='create_aset'),
    path('create/dekorasi/', views.create_dekorasi, name='create_dekorasi'),
    path('create/bibit-tanaman/', views.create_bibit_tanaman, name='create_bibit_tanaman'),
    path('create/hewan/', views.create_hewan, name='create_hewan'),
    path('create/kandang/', views.create_kandang, name='create_kandang'),
    path('create/alat-produksi/', views.create_alat_produksi, name='create_alat_produksi'),
    path('create/petak-sawah/', views.create_petak_sawah, name='create_petak_sawah'),
    path('form_update_dekorasi/<str:id>/', views.formUpdateDekorasi, name='formUpdateDekorasi'),
    path('update/dekorasi/', views.updateDekorasi, name='updateDekorasi'),
    path('form_update_bibit_tanaman/<str:id>/', views.formUpdateBibitTanaman, name='formUpdateBibitTanaman'),
    path('update/bibit-tanaman/', views.updateBibitTanaman, name='updateBibitTanaman'),
    path('form_update_kandang/<str:id>/', views.formUpdateKandang, name='formUpdateKandang'),
    path('update/kandang/', views.updateKandang, name='updateKandang'),
    path('form_update_hewan/<str:id>/', views.formUpdateHewan, name='formUpdateHewan'),
    path('update/hewan/', views.updateHewan, name='updateHewan'),
    path('form_update_alat_produksi/<str:id>/', views.formUpdateAlatProduksi, name='formUpdateAlatProduksi'),
    path('update/alat-produksi/', views.updateAlatProduksi, name='updateAlatProduksi'),
    path('form_update_petak_sawah/<str:id>/', views.formUpdatePetakSawah, name='formUpdatePetakSawah'),
    path('delete/dekorasi/<str:id>/', views.deleteDekorasi, name='deleteDekorasi'),
    path('delete/bibit-tanaman/<str:id>/', views.deleteBibitTanaman, name='deleteBibitTanaman'),
    path('delete/kandang/<str:id>/', views.deleteKandang, name='deleteKandang'),
    path('delete/hewan/<str:id>/', views.deleteHewan, name='deleteHewan'),
    path('delete/alat-produksi/<str:id>/', views.deleteAlatProduksi, name='deleteAlatProduksi'),
    path('delete/petak-sawah/<str:id>/', views.deletePetakSawah, name='deletePetakSawah'),
]