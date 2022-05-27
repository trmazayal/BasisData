from django.shortcuts import render, redirect, HttpResponse
from django.db import connection
from collections import namedtuple
from login.views import namedtuplefetchall, cekRole

def read_koleksi_aset(request):
    return render(request, 'koleksi_aset.html')

def dekorasi(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try:
        Role = request.session['role']
    except:
        return redirect('/')
    cursor.execute("set search_path to hiday")
    cursor.execute(f"select email, a.nama, a.minimum_level, a.harga_beli, kama.jumlah from dekorasi d, koleksi_aset ka, aset a, koleksi_aset_memiliki_aset kama where d.id_aset = a.id and kama.id_koleksi_aset = ka.email and kama.id_aset = a.id")
    hasil = namedtuplefetchall(cursor)

    roleAdmin = False
    rolePengguna = False

    if Role == "Admin":
        roleAdmin = True
    elif Role == "Pengguna":
        rolePengguna = True
    
    data = {
        'list_koleksi_dekorasi' : hasil,
        'roleAdmin' : roleAdmin,
        'rolePengguna' : rolePengguna,
    }

    return render(request, "dekorasi.html", data) 

def bibit_tanaman(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try:
        Role = request.session['role']
    except:
        return redirect('/')
    cursor.execute("set search_path to hiday")
    cursor.execute(f"select email, a.nama, a.minimum_level, a.harga_beli, kama.jumlah from bibit_tanaman bt, koleksi_aset ka, aset a, koleksi_aset_memiliki_aset kama where bt.id_aset = a.id and kama.id_koleksi_aset = ka.email and kama.id_aset = a.id")
    hasil = namedtuplefetchall(cursor)

    roleAdmin = False
    rolePengguna = False

    if Role == "Admin":
        roleAdmin = True
    elif Role == "Pengguna":
        rolePengguna = True

    data = {
        'list_koleksi_bibit_tanaman' : hasil,
        'roleAdmin' : roleAdmin,
        'rolePengguna' : rolePengguna,
    }

    return render(request, "bibit_tanaman.html", data)

def kandang(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try:
        Role = request.session['role']
    except:
        return redirect('/')
    cursor.execute("set search_path to hiday")
    cursor.execute(f"select email, a.nama, a.minimum_level, a.harga_beli, kama.jumlah from kandang k, koleksi_aset ka, aset a, koleksi_aset_memiliki_aset kama where k.id_aset = a.id and kama.id_koleksi_aset = ka.email and kama.id_aset = a.id")
    hasil = namedtuplefetchall(cursor)

    roleAdmin = False
    rolePengguna = False

    if Role == "Admin":
        roleAdmin = True
    elif Role == "Pengguna":
        rolePengguna = True

    data = {
        'list_koleksi_kandang' : hasil,
        'roleAdmin' : roleAdmin,
        'rolePengguna' : rolePengguna,
    }

    return render(request, "kandang.html", data)

def hewan(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try:
        Role = request.session['role']
    except:
        return redirect('/')
    cursor.execute("set search_path to hiday")
    cursor.execute(f"select email, a.nama, a.minimum_level, a.harga_beli, kama.jumlah from hewan h, koleksi_aset ka, aset a, koleksi_aset_memiliki_aset kama where h.id_aset = a.id and kama.id_koleksi_aset = ka.email and kama.id_aset = a.id")
    hasil = namedtuplefetchall(cursor)

    roleAdmin = False
    rolePengguna = False

    if Role == "Admin":
        roleAdmin = True
    elif Role == "Pengguna":
        rolePengguna = True

    data = {
        'list_koleksi_hewan' : hasil,
        'roleAdmin' : roleAdmin,
        'rolePengguna' : rolePengguna,
    }

    return render(request, "hewan.html", data)

def alat_produksi(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try:
        Role = request.session['role']
    except:
        return redirect('/')
    cursor.execute("set search_path to hiday")
    cursor.execute(f"select email, a.nama, a.minimum_level, a.harga_beli, kama.jumlah from alat_produksi ap, koleksi_aset ka, aset a, koleksi_aset_memiliki_aset kama where ap.id_aset = a.id and kama.id_koleksi_aset = ka.email and kama.id_aset = a.id")
    hasil = namedtuplefetchall(cursor)

    roleAdmin = False
    rolePengguna = False

    if Role == "Admin":
        roleAdmin = True
    elif Role == "Pengguna":
        rolePengguna = True
    
    data = {
        'list_koleksi_alat_produksi' : hasil,
        'roleAdmin' : roleAdmin,
        'rolePengguna' : rolePengguna,
    }

    return render(request, "alat_produksi.html", data)

def petak_sawah(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try:
        Role = request.session['role']
    except:
        return redirect('/')
    cursor.execute("set search_path to hiday")
    cursor.execute(f"select email, a.nama, a.minimum_level, a.harga_beli, kama.jumlah from petak_sawah ps, koleksi_aset ka, aset a, koleksi_aset_memiliki_aset kama where ps.id_aset = a.id and kama.id_koleksi_aset = ka.email and kama.id_aset = a.id")
    hasil = namedtuplefetchall(cursor)

    roleAdmin = False
    rolePengguna = False

    if Role == "Admin":
        roleAdmin = True
    elif Role == "Pengguna":
        rolePengguna = True
    
    data = {
        'list_koleksi_petak_sawah' : hasil,
        'roleAdmin' : roleAdmin,
        'rolePengguna' : rolePengguna,
    }

    return render(request, "petak_sawah.html", data)