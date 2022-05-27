from django.contrib import admin
from django.urls import path
from . import views

app_name = "koleksi_aset"

urlpatterns = [
    path('read/', views.read_koleksi_aset, name='read_koleksi_aset'),
    path('dekorasi/', views.dekorasi, name='dekorasi'),
    path('bibit-tanaman/', views.bibit_tanaman, name='bibit_tanaman'),
    path('kandang/', views.kandang, name='kandang'),
    path('hewan/', views.hewan, name='hewan'),
    path('alat-produksi/', views.alat_produksi, name='alat_produksi'),
    path('petak-sawah/', views.petak_sawah, name='petak_sawah'),
]