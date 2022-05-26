from pyexpat.errors import messages
from unittest import result
from urllib import request, response
from django.shortcuts import render, redirect, HttpResponse
from django.db import connection
from collections import namedtuple

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def create_histori_hewan_view(request):
    email = str(request.session['email'])
    role = cekRole(email)
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    data = []
    html = ""

    if (role == "Pengguna"):
        cursor.execute("select hw.id_hewan from histori_hewan as hw, hewan as h where hw.email = '"+email+"' AND hw.id_hewan = h.id_aset")
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

    if (role == "Admin"):
        return HttpResponse("You are not authorized")

    if request.method != "POST":
        return create_histori_hewan_view(request)

    body = request.POST

    id_hewan = str(body.get('id_hewan_input'))
    jumlah = str(body.get('jumlah_input'))
    xp = 5 * int(jumlah)

    cursor.execute("SELECT HP.jumlah FROM HISTORI_HEWAN as HH, HISTORI_PRODUKSI as HP WHERE HH.email=HP.email and HH.email='"+email+"' AND HH.waktu_awal=HP.waktu_awal")
    jumlah_dimiliki_tuple = namedtuplefetchall(cursor)
    jumlah_dimiliki = int(jumlah_dimiliki_tuple[0].jumlah)

    if (int(jumlah)>jumlah_dimiliki):
        messages.info(request, "Anda tidak memiliki hewan yang cukup, silahkan membeli hewan terlebih dahulu")
        return redirect('/CreateHistoriHewan/')

    cursor.execute(
        """
        INSERT INTO HISTORI_PRODUKSI VALUES (
            %s, current_timestamp, current_timestamp, %s, %s
        )
        """, [email, jumlah, xp]
        )
    cursor.execute(
        """
        SELECT HP.waktu_awal FROM HISTORI_PRODUKSI as HP WHERE HP.email = %s AND jumlah = %s AND xp = %s
        """, [email, jumlah, xp]
    )
    waktu_tuple = namedtuplefetchall(cursor)
    print(waktu_tuple)
    waktu = waktu_tuple[0].waktu_awal
    print(waktu)
    cursor.execute(
        """
        INSERT INTO HISTORI_HEWAN VALUES (
            %s, %s, %s)
        """, [email, waktu, id_hewan]
    )

    cursor.execute("set search_path to public")
    cursor.close()

    return redirect('/ListHistoriHewan/')


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
        cursor.execute("select dp.subtotal from histori_penjualan as hp, pesanan as p, detail_pesanan as dp where hp.email= '"+email+"' AND hp.id_pesanan = p.id AND p.id = dp.id_pesanan")
        totalKoin = namedtuplefetchall(cursor)
        html = "pengguna_listhistoripenjualan.html"

    else:
        cursor.execute("select * from histori_penjualan")
        data = namedtuplefetchall(cursor)
        html = "admin_listhistoripenjualan.html"

    print(data)
    print(totalKoin)
    total = 0
    for q in range(len(totalKoin)):
        print(totalKoin[q].subtotal)
        total += int(totalKoin[q].subtotal)

    print(total)

    arguments = {
        'result': data
    }
    arguments['total_koin'] = total

    cursor.execute("set search_path to public")
    cursor.close()

    return render(request, html, arguments)

def create_histori_penjualan_view(request):
    email = str(request.session['email'])
    role = cekRole(email)
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    data = []
    html = ""

    if (role == "Pengguna"):
        cursor.execute("")
        data = namedtuplefetchall(cursor)
        html = "formCreate_histori_penjualan.html"

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
        cursor.execute("select hp.waktu_penjualan, p.nama as pnama, hp.koin, hp.xp, hp.id_pesanan, p.jenis, p.status, p.total from pesanan as p, histori_penjualan as hp where p.id = '"+id_pesanan+"' AND hp.email = '"+email+"' and p.id = hp.id_pesanan")
        data1 = namedtuplefetchall(cursor)
        cursor.execute("select dp.subtotal, dp.jumlah, pr.nama as prnama from produk as pr, detail_pesanan as dp, pesanan as p, histori_penjualan as hp where p.id = dp.id_pesanan AND dp.id_produk = pr.id AND hp.email = '"+email+"' AND dp.id_pesanan = '"+id_pesanan+"'")
        data2 = namedtuplefetchall(cursor)
        html = "pengguna_detailhistoripenjualan.html"

    else:
        cursor.execute("select hp.waktu_penjualan, p.nama as pnama, hp.koin, hp.xp, hp.id_pesanan, p.jenis, p.status, p.total from pesanan as p, histori_penjualan as hp where p.id = '"+id_pesanan+"'")
        data1 = namedtuplefetchall(cursor)
        cursor.execute("select dp.subtotal, dp.jumlah, pr.nama as prnama from produk as pr, detail_pesanan as dp, pesanan as p, histori_penjualan as hp where p.id = dp.id_pesanan AND dp.id_produk = pr.id AND dp.id_pesanan = '"+id_pesanan+"'")
        data2 = namedtuplefetchall(cursor)
        html = "admin_detailhistoripenjualan.html"

    print(data1)
    print(data2)
    total = 0
    for q in range(len(data2)):
        print(data2[q].subtotal)
        total += int(data2[q].subtotal)

    print(total)

    arguments = {
        'result1': data1,
        'result2': data2
    }
    arguments['total_koin'] = total

    cursor.execute("set search_path to public")
    cursor.close()

    return render(request, html, arguments)

def create_histori_penjualan(request): #belum diimplementasikan secara maksimal
    email = str(request.session['email'])
    role = cekRole(email)
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    if (role == "Admin"):
        return HttpResponse("You are not authorized")

    # if request.method != "POST":
    #     return create_histori_penjualan_view(request)

    body = request.POST


    return redirect ()

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
        cursor.execute("select p.nama as pnama, hp.koin, hp.xp, p.id, p.jenis, p.status, p.total from pesanan as p, histori_penjualan as hp where p.id = '"+id_pesanan+"' AND hp.email = '"+email+"' AND hp.id_pesanan = p.id")
        data1 = namedtuplefetchall(cursor)
        cursor.execute("select pr.nama as prnama, dp.jumlah, dp.subtotal from pesanan as p, detail_pesanan as dp, produk as pr, histori_penjualan as hp where dp.id_pesanan = p.id AND dp.id_produk = pr.id AND dp.id_pesanan = '"+id_pesanan+"' AND hp.email = '"+email+"'")
        data2 = namedtuplefetchall(cursor)
        html = "pengguna_detailpesanan.html"

    else:
        cursor.execute("select p.nama as pnama, hp.koin, hp.xp, p.id, p.jenis, p.status, p.total from pesanan as p, histori_penjualan as hp where p.id = '"+id_pesanan+"' AND hp.id_pesanan = p.id")
        data1 = namedtuplefetchall(cursor)
        cursor.execute("select pr.nama as prnama, dp.jumlah, dp.subtotal from pesanan as p, detail_pesanan as dp, produk as pr, histori_penjualan as hp where dp.id_pesanan = p.id AND dp.id_produk = pr.id AND dp.id_pesanan = '"+id_pesanan+"'")
        data2 = namedtuplefetchall(cursor)
        html = "admin_detailpesanan.html"

    print(data1)
    print(data2)
    arguments = {
        'result1': data1,
        'result2' : data2
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