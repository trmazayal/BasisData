from email import message
from django.shortcuts import render, redirect
from django.db import connection
from collections import namedtuple

# jk_update = 0;

# def setUpdatePaketKoin(int):
#     jk_update = int

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

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

def paket_koin(request):
    try:
        email = request.session['email']
    except Exception as e:
        return redirect('/')
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    cursor.execute("select * from paket_koin")
    data_paket_koin = namedtuplefetchall(cursor)

    role = cekRole(email)
    roleAdmin = False
    rolePengguna = False
    if (role == 'Admin'):
        roleAdmin = True
    if (role == 'Pengguna'):
        rolePengguna = True

    argument = {
        'role' : role,
        'roleAdmin' : roleAdmin,
        'rolePengguna' : rolePengguna,
        'paket_koin' : data_paket_koin,
    }
    cursor.close()
    return render(request, "paket_koin.html", argument)


def transaksi_pembelian_koin(request):
    try:
        email = request.session['email']
    except Exception as e:
        return redirect('/')
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    role = cekRole(email)
    roleAdmin = False
    rolePengguna = False
    if (role == 'Admin'):
        roleAdmin = True
    if (role == 'Pengguna'):
        rolePengguna = True

    if (roleAdmin):
        cursor.execute("select * from transaksi_pembelian_koin")
        data_transaksi_pembelian_koin = namedtuplefetchall(cursor)

        argument = {
            'role' : role,
            'roleAdmin' : roleAdmin,
            'rolePengguna' : rolePengguna,
            'transaksi_pembelian_koin' : data_transaksi_pembelian_koin
        }
    elif (rolePengguna):
        cursor.execute("select * from transaksi_pembelian_koin where email='"+email+"'")
        data_transaksi_pembelian_koin = namedtuplefetchall(cursor)

        argument = {
            'role' : role,
            'roleAdmin' : roleAdmin,
            'rolePengguna' : rolePengguna,
            'transaksi_pembelian_koin' : data_transaksi_pembelian_koin
        }
    cursor.close()
    return render(request, "transaksi_pembelian_koin.html", argument)


def buat_paket_koin(request):
    try:
        email = request.session['email']
    except Exception as e:
        return redirect('/')

    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    role = cekRole(email)

    if (role == 'Pengguna'):
        # return redirect('/')
        ayam = ''

    argument = {
        # 'form' : buatPaketKoinForm,
    }
    cursor.close()
    return render(request, "buat_paket_koin.html", argument)

def ubah_paket_koin(request):
    try:
        email = request.session['email']
    except Exception as e:
        return redirect('/')

    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    role = cekRole(email)

    if (role == 'Pengguna'):
        ayam = ''
        # return redirect('/')

    argument = {
        # 'form' : ubahPaketKoinForm,
    }
    cursor.close()
    return render(request, "ubah_paket_koin.html", argument)


# dia bakal ambil dlu jumlh koin
# diset, trs diupdate

def pembelian_paket_koin(request):
    # admin gabisa beli
    try:
        email = request.session['email']
    except Exception as e:
        return redirect('/')

    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    role = cekRole(email)
    if (role == 'Admin'):
        ayam =''
        # return redirect('/')


    argument = {
        # 'form' : pembelianPaketKoinForm,
    }
    cursor.close()
    return render(request, "pembelian_paket_koin.html", argument)