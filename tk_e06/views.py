import email
from urllib import request, response
from django.shortcuts import render
from django.db import connection
from collections import namedtuple

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def create_histori_hewan(request):
    email = str(request.session['email'])
    role = cekRole(email)
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    data = []
    html = ""

    if (role == "Pengguna"):
        cursor.execute("select a.nama from histori_hewan as hw, hewan as h, aset as a where hw.email = '"+email+"' AND hw.id_hewan = h.id_aset AND h.id_aset=a.id")
        data = namedtuplefetchall(cursor)
        html = "formCreate_histori_hewan.html"

    arguments = {
        'result': data
    }

    cursor.execute("set search_path to public")
    cursor.close()
    return render(request, html, arguments)


def list_histori_hewan(request):
    email = str(request.session['email'])
    role = cekRole(email)
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    data = []
    html = ""

    if (role == "Pengguna"):
        cursor.execute("select hw.waktu_awal, hp.waktu_selesai, hp.jumlah, hp.xp, a.nama from histori_hewan as hw, histori_produksi as hp, aset as a where hw.email = '"+email+"' AND hw.id_hewan = a.id AND hw.email = hp.email AND hw.waktu_awal = hp.waktu_awal")
        data = namedtuplefetchall(cursor)
        html = "pengguna_listhistorihewan.html"

    else:
        cursor.execute("select hw.email, hw.waktu_awal, hp.waktu_selesai, hp.jumlah, hp.xp, a.nama from histori_hewan as hw, histori_produksi as hp, aset as a where hw.email = hp.email AND hw.id_hewan = a.id AND hp.waktu_awal = hw.waktu_awal")
        data = namedtuplefetchall(cursor)
        html = "admin_listhistorihewan.html"

    arguments = {
        'result': data
    }

    cursor.execute("set search_path to public")
    cursor.close()

    return render(request, html, arguments)

def create_histori_hewan(request):
    email = str(request.session['email'])
    role = cekRole(email)
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    data = []
    html = ""

    if (role == "Pengguna"):
        cursor.execute("select a.nama from histori_hewan as hw, hewan as h, aset as a where hw.email = '"+email+"' AND hw.id_hewan = h.id_aset AND h.id_aset=a.id")
        data = namedtuplefetchall(cursor)
        html = "formCreate_histori_hewan.html"

    arguments = {
        'result': data
    }

    cursor.execute("set search_path to public")
    cursor.close()
    return render(request, html, arguments)

def list_histori_penjualan(request):
    email = str(request.session['email'])
    role = cekRole(email)
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    data = []
    html = ""

    if (role == "Pengguna"):
        cursor.execute("select * from histori_penjualan where email = '"+email+"'")
        data = namedtuplefetchall(cursor)
        html = "pengguna_listhistoripenjualan.html"

    else:
        cursor.execute("select * from histori_penjualan")
        data = namedtuplefetchall(cursor)
        html = "admin_listhistoripenjualan.html"

    arguments = {
        'result': data
    }

    cursor.execute("set search_path to public")
    cursor.close()

    return render(request, html, arguments)

def detail_histori_penjualan(request, id_pesanan):
    email = str(request.session['email'])
    role = cekRole(email)
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    data = []
    html = ""

    if (role == "Pengguna"):
        cursor.execute("select hp.waktu_penjualan, p.nama as pnama, hp.koin, hp.xp, hp.id_pesanan, dp.subtotal, dp.jumlah, pr.nama as prnama, p.jenis, p.status, p.total from pesanan as p, detail_pesanan as dp, produk as pr, histori_penjualan as hp where dp.id_pesanan = p.id AND dp.id_produk = pr.id AND dp.id_pesanan = '"+id_pesanan+"' AND hp.email = '"+email+"' AND dp.id_produk = pr.id")
        data = namedtuplefetchall(cursor)
        html = "pengguna_detailhistoripenjualan.html"

    else:
        cursor.execute("select hp.email, hp.waktu_penjualan, p.nama as pnama, hp.koin, hp.xp, hp.id_pesanan, dp.subtotal, dp.jumlah, pr.nama as prnama, p.jenis, p.status, p.total from pesanan as p, detail_pesanan as dp, produk as pr, histori_penjualan as hp where dp.id_pesanan = p.id AND dp.id_pesanan = '"+id_pesanan+"' AND dp.id_produk = pr.id")
        data = namedtuplefetchall(cursor)
        html = "admin_detailhistoripenjualan.html"

    print(data)
    arguments = {
        'result': data
    }

    cursor.execute("set search_path to public")
    cursor.close()

    return render(request, html, arguments)

def create_histori_penjualan(request): #belum diimplementasikan secara maksimal
    email = str(request.session['email'])
    role = cekRole(email)
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    data = []
    html = ""

    if (role == "Pengguna"):
        cursor.execute("select a.nama from histori_hewan as hw, hewan as h, aset as a where hw.email = '"+email+"' AND hw.id_hewan = h.id_aset AND h.id_aset=a.id")
        data = namedtuplefetchall(cursor)
        html = "formCreate_histori_penjualan.html"

    arguments = {
        'result': data
    }

    cursor.execute("set search_path to public")
    cursor.close()
    return render(request, html, arguments)

def list_pesanan(request):
    email = str(request.session['email'])
    role = cekRole(email)
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    data = []
    html = ""

    if (role == "Pengguna"):
        cursor.execute("select p.id, p.status, p.jenis, p.nama, p.total from pesanan as p, histori_penjualan as hp where p.id = hp.id_pesanan AND hp.email = '"+email+"'")
        data = namedtuplefetchall(cursor)
        html = "pengguna_listpesanan.html"

    else:
        cursor.execute("select * from pesanan")
        data = namedtuplefetchall(cursor)
        html = "admin_listpesanan.html"

    arguments = {
        'result': data
    }

    cursor.execute("set search_path to public")
    cursor.close()

    return render(request, html, arguments)

def detail_pesanan(request, id_pesanan):
    email = str(request.session['email'])
    role = cekRole(email)
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    data = []
    html = ""

    if (role == "Pengguna"):
        cursor.execute("select hp.waktu_penjualan, p.id, p.nama as pnama, p.jenis, p.status, pr.nama as prnama, dp.jumlah, dp.subtotal, p.total from pesanan as p, detail_pesanan as dp, produk as pr, histori_penjualan as hp where dp.id_pesanan = p.id AND dp.id_produk = pr.id AND dp.id_pesanan = '"+id_pesanan+"' AND hp.email = '"+email+"' AND dp.id_produk = pr.id")
        data = namedtuplefetchall(cursor)
        html = "pengguna_detailpesanan.html"

    else:
        cursor.execute("select hp.email, hp.waktu_penjualan, p.id, p.nama as pnama, p.jenis, p.status, pr.nama as prnama, dp.jumlah, dp.subtotal, p.total from pesanan as p, detail_pesanan as dp, produk as pr, histori_penjualan as hp where dp.id_pesanan = p.id AND dp.id_pesanan = '"+id_pesanan+"' AND dp.id_produk = pr.id")
        data = namedtuplefetchall(cursor)
        html = "admin_detailpesanan.html"

    arguments = {
        'result': data
    }

    cursor.execute("set search_path to public")
    cursor.close()

    return render(request, html, arguments)

def create_pesanan(request): #belum diimplementasikan secara maksimal
    email = str(request.session['email'])
    role = cekRole(email)
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    data = []
    html = ""

    if (role == "Admin"):
        cursor.execute("select p.*, dp.*, pr.nama as pnama from pesanan as p, detail pesanan as dp, produk as pr")
        data = namedtuplefetchall(cursor)
        html = "formCreate_pesanan.html"

    arguments = {
        'result': data
    }

    cursor.execute("set search_path to public")
    cursor.close()
    return render(request, html, arguments)

def update_pesanan(request): #belum diimplementasikan secara maksimal
    email = str(request.session['email'])
    role = cekRole(email)
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    data = []
    html = ""

    if (role == "Admin"):
        cursor.execute("select p.*, dp.*, pr.nama as pnama from pesanan as p, detail pesanan as dp, produk as pr")
        data = namedtuplefetchall(cursor)
        html = "formUpdate_histori_penjualan.html"

    arguments = {
        'result': data
    }

    cursor.execute("set search_path to public")
    cursor.close()
    return render(request, html, arguments)

def cekRole(email):
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("select * from admin where email='"+email+"'")
    admin = namedtuplefetchall(cursor)
    if (admin != []):
        cursor.close()
        return "Admin"
    else:
        cursor.execute("select * from pengguna where email='"+email+"'")
        pengguna = namedtuplefetchall(cursor)
        if (pengguna != []):
            cursor.close()
            return "Pengguna"