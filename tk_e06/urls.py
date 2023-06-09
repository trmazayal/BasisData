"""tk_e06 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('aset/', include('aset.urls')),
    path('koleksi-aset/', include('koleksi_aset.urls')),
    path('transaksi-pembelian/', include('transaksi_pembelian.urls')),
    path('paket-koin/', include('paket_koin.urls')),
    path('lumbung/', include('lumbung.urls')),
    path('produk/', include('produk.urls')),
    path('', include('histori.urls')),
]