from django.shortcuts import render, redirect, HttpResponse
from django.db import connection
from collections import namedtuple
from login.views import namedtuplefetchall, cekRole

def transaksi_pembelian(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    cursor.execute(f"select * from transaksi_pembelian")
    hasil = namedtuplefetchall(cursor)

    data = {
            'list_transaksi_pembelian' : hasil,
    }

    role = cekRole(email)
    roleAdmin = False
    rolePengguna = False
    if (role == 'Admin'):
        roleAdmin = True
    if (role == 'Pengguna'):
        rolePengguna = True

    return render(request, "readTransaksiPembelian.html", data)