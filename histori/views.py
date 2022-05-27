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
        cursor.execute("select hw.email, hw.waktu_awal, hp.waktu_selesai, hp.jumlah, hp.xp, a.nama from histori_hewan as hw, histori_produksi as hp, aset as a where hw.email = hp.email AND hp.waktu_awal = hw.waktu_awal AND hw.id_hewan = a.id")
        data = namedtuplefetchall(cursor)
        html = "admin_listhistorihewan.html"

    print(data)
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
        cursor.execute("select dp.subtotal from histori_penjualan as hp, pesanan as p, detail_pesanan as dp where hp.id_pesanan = p.id AND p.id = dp.id_pesanan")
        totalKoin = namedtuplefetchall(cursor)
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
        cursor.execute("select hp.email, hp.waktu_penjualan, p.nama as pnama, hp.koin, hp.xp, hp.id_pesanan, p.jenis, p.status, p.total from pesanan as p, histori_penjualan as hp where p.id = '"+id_pesanan+"' AND hp.email='"+email+"'")
        data1 = namedtuplefetchall(cursor)
        cursor.execute("select dp.subtotal, dp.jumlah, pr.nama as prnama from produk as pr, detail_pesanan as dp, pesanan as p, histori_penjualan as hp where p.id = dp.id_pesanan AND dp.id_produk = pr.id AND dp.id_pesanan = '"+id_pesanan+"' AND hp.email='"+email+"'")
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

    body = request.POST
    id_pesanan = str(body.get('id'))

    cursor.execute(
        """
        INSERT INTO HISTORI_PENJUALAN VALUES(
            %s, %s, %s, %s, %s 
        )
        """, [email, waktu_penjualan, koin, xp, id_pesanan]
    )

    return redirect ('/ListHistoriPenjualan')

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
        cursor.execute("select distinct pr.nama as prnama, dp.jumlah, dp.subtotal from pesanan as p, detail_pesanan as dp, produk as pr, histori_penjualan as hp where dp.id_pesanan = p.id AND dp.id_produk = pr.id AND dp.id_pesanan = '"+id_pesanan+"'")
        data2 = namedtuplefetchall(cursor)
        html = "admin_detailpesanan.html"

    print(data1)
    print(data2)
    total = 0
    for q in range(len(data2)):
        print(data2[q].subtotal)
        total += int(data2[q].subtotal)

    print(total)
    arguments = {
        'result1': data1,
        'result2' : data2
    }
    arguments['total_koin'] = total

    cursor.execute("set search_path to public")
    cursor.close()

    return render(request, html, arguments)

def create_pesanan_view(request): #belum diimplementasikan secara maksimal
    email = str(request.session['email'])
    role = cekRole(email)
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    print(role)

    data = []
    html = ""

    if (role == "Admin"):
        cursor.execute("select id from pesanan order by id desc limit 1")
        id_pesanan = namedtuplefetchall(cursor)
        cursor.execute("select nama from produk")
        nama_produk = namedtuplefetchall(cursor)
        html = "formCreate_pesanan.html"

    print(id_pesanan)
    id_str = id_pesanan[0].id
    id_int = int(id_str[2:5])
    print(id_int)
    id_int = id_int+1
    if (id_int < 10):
        str_id = "PS00" + str(id_int)
    elif (id_int < 100):
        str_id = "PS0" + str(id_int)
    else:
        str_id = "PS" + str(id_int)

    arguments = {
        'id': str_id,
        'nama_produk': nama_produk
    }

    cursor.execute("set search_path to public")
    cursor.close()

    return render(request, html, arguments)

def create_pesanan(request): #belum diimplementasikan maksimal
    email = str(request.session['email'])
    role = cekRole(email)
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    if (role == "Pengguna"):
        return HttpResponse("You are not authorized")

    if request.method != "POST":
        return create_pesanan_view(request)

    body = request.POST

    id_pesanan = str(body.get('input_idpesanan'))
    nama = str(body.get('input_namapesanan'))
    jenis = str(body.get('input_jenispesanan'))
    jumlah = str(body.get('input_jumlahpesanan'))

    cursor.execute(
        """
        INSERT INTO PESANAN VALUES (
            %s, "Baru Dipesan", %s, %s, %s
        )
        """, [id_pesanan, jenis, nama, subtotal]
        )

    cursor.execute(
        """
        SELECT no_urut FROM DETAIL_PESANAN
        order by no_urut desc limit 1
        """
    )
    noUrut = namedtuplefetchall(cursor)

    print(noUrut)
    noUrut_str = noUrut[0].nomor_urut
    noUrut_int = int(noUrut_str[2:5])
    print(noUrut_int)
    noUrut_int = noUrut_int+1
    if (noUrut_int < 10):
        str_noUrut = "NO00" + str(noUrut_int)
    elif (noUrut_int < 100):
        str_noUrut = "NO0" + str(noUrut_int)
    else:
        str_noUrut = "NO" + str(noUrut_int)

    cursor.execute(
        """
        INSERT INTO DETAIL_PESANAN VALUES (
            %s, %s, %s, %s, %s)
        """, [id_pesanan, str_noUrut, subtotal, jumlah, id_produk]
    )

    cursor.execute("set search_path to public")
    cursor.close()

    return redirect('/ListPesanan/')

def update_pesanan_view(request, id_pesanan):
    email = str(request.session['email'])
    role = cekRole(email)
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    data = []
    html = ""

    if (role == "Admin"):
        cursor.execute("select p.id, p.nama, p.jenis, p.status from pesanan as p where p.id='"+id_pesanan+"'")
        data1 = namedtuplefetchall(cursor)
        cursor.execute("select dp.subtotal, dp.jumlah, pr.nama as prnama from produk as pr, detail_pesanan as dp, pesanan as p where p.id = dp.id_pesanan AND dp.id_produk = pr.id AND dp.id_pesanan = '"+id_pesanan+"'")
        data2 = namedtuplefetchall(cursor)
        html = "formUpdate_pesanan.html"

    print(data1)
    print(data2)
    total = 0
    for q in range(len(data2)):
        print(data2[q].subtotal)
        total += int(data2[q].subtotal)

    print(total)
    arguments = {
        'result1': data1,
        'result2' : data2,
        'total_koin' : total
    }

    cursor.execute("set search_path to public")
    cursor.close()

    return render(request, html, arguments)

def update_pesanan(request, id_pesanan): #belum diimplementasikan secara maksimal
    email = str(request.session['email'])
    role = cekRole(email)
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    if (role == "Pengguna"):
        return HttpResponse("You are not authorized")

    if (request != "POST"):
        return update_pesanan_view(request, id_pesanan)

    body = request.POST
    nama = str(body.get('input_namapesanan'))
    jenis = str(body.get('input_jenispesanan'))
    status = str(body.get('input_statuspesanan'))
    
    cursor.execute("select p.id, p.nama, p.jenis, p.status from pesanan as p where p.id='"+id_pesanan+"'")
    data1 = namedtuplefetchall(cursor)

    nama_sebelum = data1[0].nama
    jenis_sebelum = data1[0].jenis
    status_sebelum = data1[0].status

    if (nama=="" or jenis=="" or status==""):
        nama = nama_sebelum
        jenis = jenis_sebelum
        status = status_sebelum

    cursor.execute("update pesanan set nama = %s,  jenis = %s, status = %s where id = %s", 
                    [nama, jenis, status, id_pesanan])

    cursor.execute("set search_path to public")

    return list_pesanan(request)

def delete_pesanan(request, pesananID):
    cursor = connection.cursor()
    id_pesanan = str(pesananID)
    cursor.execute("set search_path to hiday")
    cursor.execute("delete from pesanan where id = %s", [id_pesanan])
    cursor.execute("set search_path to public")
    message = "Data berhasil dihapus"
    return list_pesanan(request)

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