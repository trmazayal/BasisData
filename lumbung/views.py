from ast import arguments
import datetime
import email
from email import message
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
    message =""
    email = request.session['email']
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("select * from lumbung where email ='"+ email+ "'")
    hasil= namedtuplefetchall(cursor)
    level = hasil[0].level
    level_up = level + 1
    kapasitas_maksimal = hasil[0].kapasitas_maksimal
    kapasitas_up = kapasitas_maksimal + 50
    biaya_upgrade = "200"
    total = hasil[0].total
    cursor.execute("select * from pengguna where email ='"+ email+ "'")
    hasil= namedtuplefetchall(cursor)
    koin = hasil[0].koin
    ct = datetime.datetime.now()
    date_time = ct.strftime("%Y-%m-%d %H:%M:%S")

    
    form = upgradeLumbungForm(initial={'level_lumbung': str(level) + " ⇨ " + str(level_up), 'kapasitas_lumbung': str(kapasitas_maksimal) + " ⇨ " + str(kapasitas_up), 'biaya_upgrade': biaya_upgrade})

    if request.method =='POST':
        
        if koin>=200:
            cursor.execute("update lumbung set email = '"+ email +"', level = '"+ str(level_up) +"', kapasitas_maksimal = '"+ str(kapasitas_up) +"', total = '"+ str(total) +"' where email = '"+ email +"'")
            cursor.execute("insert into transaksi_upgrade_lumbung values ('"+ email +"','"+ date_time +"')")
            cursor.close()
            return redirect('/lumbung/transaksi-upgrade-lumbung/')
        else:
            message = "Koin anda tidak cukup, silahkan cari Koin terlebih dahulu"
        
    
    argument = {
        'form': form,
        'message' : message
        }
    return render(request, "upgrade_lumbung.html", argument)

def produksi_tanaman(request):
    email = request.session['email']
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("select a.nama from aset a, koleksi_aset_memiliki_aset km where a.id = km.id_aset and a.id like 'BT%' and km.id_koleksi_aset = '"+ email +"'")
    bibit_choices = namedtuplefetchall(cursor)

    
    message = ""
    if request.method =='POST':

        in_bibit_tanaman = request.POST['bibit_tanaman']
        jumlah = request.POST['in-jumlah']
        xp = request.POST['in-xp']
        ct = datetime.datetime.now()
        date_time = ct.strftime("%Y-%m-%d %H:%M:%S")


        cursor.execute("select km.jumlah from aset a, koleksi_aset_memiliki_aset km where a.id = km.id_aset and a.nama = '"+ in_bibit_tanaman +"' and km.id_koleksi_aset = '"+ email +"'")
        jumlah_bibit_asli = namedtuplefetchall(cursor)[0].jumlah
        cursor.execute("select id from aset where nama = '"+ in_bibit_tanaman +"'")
        id_bibit = namedtuplefetchall(cursor)[0].id
        if int(jumlah_bibit_asli) >= int(jumlah):
            cursor.execute("insert into histori_produksi values ('"+ email +"','"+ date_time +"','"+ date_time +"','"+ jumlah +"','"+ xp +"')")
            cursor.execute("insert into histori_tanaman values ('"+ email +"','"+ date_time +"','"+ id_bibit +"')")
            cursor.close()
            return redirect('/lumbung/histori-produksi-tanaman/')
        else :
            message = "Anda tidak memiliki bibit yang cukup, silahkan membeli bibit terlebih dahulu"
    
    form = produksiTanamanForm()

    argument = {
        'bibit_tanaman' : bibit_choices,
        'form' : form,
        'message' : message
    }

    return render(request, "produksi_tanaman.html", argument)