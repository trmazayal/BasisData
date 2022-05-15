from django.urls import path

from .views import viewsProduk,viewsProduksi,viewsHistoriProduksiMakanan, createProduk, updateProduk, formUpdateProduk, deleteProduk, createProduksi,deleteProduksi

app_name ='produk'

urlpatterns = [
    path('form_create_produk/', createProduk, name='createProduk'),
    path('read_produk/', viewsProduk, name='produk'),
    path('form_update_produk/<str:id>/', formUpdateProduk, name='formUpdateProduk'),
    path('update_produk/', updateProduk, name='updateProduk'),   
    path('delete_produk/<str:id>/', deleteProduk, name='deleteProduk'), 
     
    path('form_create_produksi/', createProduksi, name='createProduksi'),
    path('read_produksi/', viewsProduksi, name='produksi'),
    # path('form_update_produksi/<str:id>/', formUpdateProduksi, name='formUpdateProduksi'),
    # path('update_produk/', updateProduksi, name='updateProduksi'),
    path('delete_produksi/<str:id>/', deleteProduksi, name='deleteProduksi'),
    
    # path('form_create_histori_produksi_makanan/', createHistoriProduksiMakanan, name='createHistoriProduksiMakanan'),
    path('read_histori_produksi_makanan/', viewsHistoriProduksiMakanan, name='historiProduksiMakanan'),
    
]
