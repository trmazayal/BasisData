from django.shortcuts import render, redirect, HttpResponse
from django.db import connection
from collections import namedtuple
from login.views import namedtuplefetchall, cekRole

def read_dekorasi(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    cursor.execute(f"select * from aset left join dekorasi on dekorasi.id_aset = aset.id")
    hasil = namedtuplefetchall(cursor)

    data = {
            'list_dekorasi' : hasil,
    }

    role = cekRole(email)
    roleAdmin = False
    rolePengguna = False
    if (role == 'Admin'):
        roleAdmin = True
    if (role == 'Pengguna'):
        rolePengguna = True

    return render(request, "readDekorasi.html", data) 


def read_bibit_tanaman(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    cursor.execute(f"select * from aset left join bibit_tanaman on bibit_tanaman.id_aset = aset.id")
    hasil = namedtuplefetchall(cursor)

    data = {
            'list_bibit_tanaman' : hasil,
    }

    role = cekRole(email)
    roleAdmin = False
    rolePengguna = False
    if (role == 'Admin'):
        roleAdmin = True
    if (role == 'Pengguna'):
        rolePengguna = True

    return render(request, "readBibitTanaman.html", data)


def read_kandang(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    cursor.execute(f"select * from aset left join kandang on kandang.id_aset = aset.id")
    hasil = namedtuplefetchall(cursor)

    data = {
            'list_kandang' : hasil,
    }

    role = cekRole(email)
    roleAdmin = False
    rolePengguna = False
    if (role == 'Admin'):
        roleAdmin = True
    if (role == 'Pengguna'):
        rolePengguna = True

    return render(request, "readKandang.html", data)



def read_hewan(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    cursor.execute(f"select * from aset left join hewan on hewan.id_aset = aset.id")
    hasil = namedtuplefetchall(cursor)

    data = {
            'list_hewan' : hasil,
    }

    role = cekRole(email)
    roleAdmin = False
    rolePengguna = False
    if (role == 'Admin'):
        roleAdmin = True
    if (role == 'Pengguna'):
        rolePengguna = True

    return render(request, "readHewan.html", data)



def read_alat_produksi(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    cursor.execute(f"select * from aset left join alat_produksi on alat_produksi.id_aset = aset.id")
    hasil = namedtuplefetchall(cursor)

    data = {
            'list_alat_produksi' : hasil,
    }

    role = cekRole(email)
    roleAdmin = False
    rolePengguna = False
    if (role == 'Admin'):
        roleAdmin = True
    if (role == 'Pengguna'):
        rolePengguna = True

    return render(request, "readAlatProduksi.html", data)



def read_petak_sawah(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    cursor.execute(f"select * from aset left join petak_sawah on petak_sawah.id_aset = aset.id")
    hasil = namedtuplefetchall(cursor)

    data = {
            'list_petak_sawah' : hasil,
    }

    role = cekRole(email)
    roleAdmin = False
    rolePengguna = False
    if (role == 'Admin'):
        roleAdmin = True
    if (role == 'Pengguna'):
        rolePengguna = True

    return render(request, "readPetakSawah.html", data)
    

