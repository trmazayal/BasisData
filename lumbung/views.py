from django.shortcuts import render, redirect
from django.db import connection
from collections import namedtuple

from lumbung.forms import produksiTanamanForm, upgradeLumbungForm

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

def transaksi_upgrade_lumbung(request):
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
        cursor.execute("select * from transaksi_upgrade_lumbung")
        data_transaksi_upgrade_lumbung = namedtuplefetchall(cursor)

        argument = {
            'role' : role,
            'roleAdmin' : roleAdmin,
            'rolePengguna' : rolePengguna,
            'transaksi_upgrade_lumbung' : data_transaksi_upgrade_lumbung
        }
    elif (rolePengguna):
        cursor.execute("select * from transaksi_upgrade_lumbung where email='"+email+"'")
        data_transaksi_upgrade_lumbung = namedtuplefetchall(cursor)

        argument = {
            'role' : role,
            'roleAdmin' : roleAdmin,
            'rolePengguna' : rolePengguna,
            'transaksi_upgrade_lumbung' : data_transaksi_upgrade_lumbung
        }
    cursor.close()
    return render(request, "transaksi_upgrade_lumbung.html", argument)

def histori_produksi_tanaman(request):
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
        cursor.execute("select distinct * from histori_produksi hp natural join histori_tanaman ht natural join aset a where hp.email = ht.email and hp.waktu_awal = ht.waktu_awal and ht.id_bibit_tanaman = a.id")
        data_transaksi_upgrade_lumbung = namedtuplefetchall(cursor)

        argument = {
            'role' : role,
            'roleAdmin' : roleAdmin,
            'rolePengguna' : rolePengguna,
            'transaksi_upgrade_lumbung' : data_transaksi_upgrade_lumbung
        }
    elif (rolePengguna):
        cursor.execute("select distinct * from histori_produksi hp natural join histori_tanaman ht natural join aset a where hp.email='"+email+"' and hp.email = ht.email and hp.waktu_awal = ht.waktu_awal and ht.id_bibit_tanaman = a.id")
        data_transaksi_upgrade_lumbung = namedtuplefetchall(cursor)

        argument = {
            'role' : role,
            'roleAdmin' : roleAdmin,
            'rolePengguna' : rolePengguna,
            'transaksi_upgrade_lumbung' : data_transaksi_upgrade_lumbung
        }
    cursor.close()
    return render(request, "histori_produksi_tanaman.html", argument)

def upgrade_lumbung(request):
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

    message = "Koin anda tidak cukup, silahkan cari Koin terlebih dahulu"

    if (roleAdmin):

        argument = {
            'role' : role,
            'roleAdmin' : roleAdmin,
            'rolePengguna' : rolePengguna,
            'form' : upgradeLumbungForm,
            'message' : message
        }
    elif (rolePengguna):

        argument = {
            'role' : role,
            'roleAdmin' : roleAdmin,
            'rolePengguna' : rolePengguna,
            'form' : upgradeLumbungForm,
            'message' : message
        }
    cursor.close()
    return render(request, "upgrade_lumbung.html", argument)

def produksi_tanaman(request):
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

    message = "Anda tidak memiliki bibit yang cukup, silahkan membeli bibit terlebih dahulu"

    if (roleAdmin):

        argument = {
            'role' : role,
            'roleAdmin' : roleAdmin,
            'rolePengguna' : rolePengguna,
            'form' : produksiTanamanForm,
            'message' : message
        }
    elif (rolePengguna):

        argument = {
            'role' : role,
            'roleAdmin' : roleAdmin,
            'rolePengguna' : rolePengguna,
            'form' : produksiTanamanForm,
            'message' : message
        }
    cursor.close()
    return render(request, "produksi_tanaman.html", argument)