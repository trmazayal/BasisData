from django.shortcuts import render, redirect, HttpResponse
from django.db import connection
from collections import namedtuple
from login.views import namedtuplefetchall, cekRole

def read_koleksi_dekorasi(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    cursor.execute(f"select * from aset left join transaksi_pembelian on transaksi_pembelian.id_aset = aset.id where transaksi_pembelian.id_aset like 'DK%'")
    hasil = namedtuplefetchall(cursor)

    data = {
            'list_koleksi_dekorasi' : hasil,
    }

    role = cekRole(email)
    roleAdmin = False
    rolePengguna = False
    if (role == 'Admin'):
        roleAdmin = True
    if (role == 'Pengguna'):
        rolePengguna = True

    return render(request, "readKoleksiDekorasi.html", data) 


def read_bibit_tanaman(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

     cursor.execute(f"select * from aset left join transaksi_pembelian on transaksi_pembelian.id_aset = aset.id where transaksi_pembelian.id_aset like 'BT%'")
    hasil = namedtuplefetchall(cursor)

    data = {
            'list_koleksi_bibit_tanaman' : hasil,
    }

    role = cekRole(email)
    roleAdmin = False
    rolePengguna = False
    if (role == 'Admin'):
        roleAdmin = True
    if (role == 'Pengguna'):
        rolePengguna = True

    return render(request, "readKoleksiBibitTanaman.html", data)


def read_kandang(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

     cursor.execute(f"select * from aset left join transaksi_pembelian on transaksi_pembelian.id_aset = aset.id where transaksi_pembelian.id_aset like 'KD%'")
    hasil = namedtuplefetchall(cursor)

    data = {
            'list_koleksi_kandang' : hasil,
    }

    role = cekRole(email)
    roleAdmin = False
    rolePengguna = False
    if (role == 'Admin'):
        roleAdmin = True
    if (role == 'Pengguna'):
        rolePengguna = True

    return render(request, "readKoleksiKandang.html", data)



def read_hewan(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    cursor.execute(f"select * from aset left join transaksi_pembelian on transaksi_pembelian.id_aset = aset.id where transaksi_pembelian.id_aset like 'HW%'")
    hasil = namedtuplefetchall(cursor)

    data = {
            'list_koleksi_hewan' : hasil,
    }

    role = cekRole(email)
    roleAdmin = False
    rolePengguna = False
    if (role == 'Admin'):
        roleAdmin = True
    if (role == 'Pengguna'):
        rolePengguna = True

    return render(request, "readKoleksiHewan.html", data)



def read_alat_produksi(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    cursor.execute(f"select * from aset left join transaksi_pembelian on transaksi_pembelian.id_aset = aset.id where transaksi_pembelian.id_aset like 'AP%'")
    hasil = namedtuplefetchall(cursor)

    data = {
            'list_koleksi_alat_produksi' : hasil,
    }

    role = cekRole(email)
    roleAdmin = False
    rolePengguna = False
    if (role == 'Admin'):
        roleAdmin = True
    if (role == 'Pengguna'):
        rolePengguna = True

    return render(request, "readKoleksiAlatProduksi.html", data)



def read_petak_sawah(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    cursor.execute(f"select * from aset left join transaksi_pembelian on transaksi_pembelian.id_aset = aset.id where transaksi_pembelian.id_aset like 'PS%'")
    hasil = namedtuplefetchall(cursor)

    data = {
            'list_koleksi_petak_sawah' : hasil,
    }

    role = cekRole(email)
    roleAdmin = False
    rolePengguna = False
    if (role == 'Admin'):
        roleAdmin = True
    if (role == 'Pengguna'):
        rolePengguna = True

    return render(request, "readKoleksiPetakSawah.html", data)
    
