from django.shortcuts import render, redirect, HttpResponse
from django.db import connection
from collections import namedtuple
from login.views import namedtuplefetchall, cekRole
from .forms import CreateTransaksiPembelianAsetForm
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def read_transaksi_pembelian_aset(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try:
        Role = request.session['role']
    except:
        return redirect('/')
    cursor.execute("set search_path to hiday")

    cursor.execute("""select tp.email, tp.waktu, a.nama, tp.jumlah, a.harga_beli * tp.jumlah as total_harga,
                    case
                        when tp.id_aset like 'DK%' then 'Dekorasi'
                        when tp.id_aset like 'BT%' then 'Bibit Tanaman'
                        when tp.id_aset like 'KD%' then 'Kandang'
                        when tp.id_aset like 'HW%' then 'Hewan'
                        when tp.id_aset like 'AP%' then 'Alat Produksi'
                        when tp.id_aset like 'PS%' then 'Petak Sawah'
                    end as jenis_aset
                    from transaksi_pembelian tp, aset a
                    where tp.id_aset = a.id""")
    hasil = namedtuplefetchall(cursor)

    roleAdmin = False
    rolePengguna = False

    if Role == "Admin":
        roleAdmin = True
    elif Role == "Pengguna":
        rolePengguna = True

    data = {
        'list_transaksi_pembelian' : hasil,
        'roleAdmin' : roleAdmin,
        'rolePengguna' : rolePengguna,
    }

    return render(request, "read_transaksi_pembelian_aset.html", data)

@csrf_exempt
def get_input_transaksi_pembelian_aset(request):
    input = request.POST
    jumlah = input['jumlah']
    return [jumlah]

@csrf_exempt
def create_transaksi_pembelian_aset(request):
    message =""
    cursor = connection.cursor()
    cursor.execute("select nama from hiday.aset")
    result = namedtuplefetchall(cursor)
    if request.method == 'POST':
        input = get_input_transaksi_pembelian_aset(request)
        aset = request.POST.get("aset")
        email = str(request.session['email'])
        cursor = connection.cursor()
        cursor.execute("set search_path to hiday")
        cursor.execute("select id as c from aset where nama = '" + aset +"'")
        id_aset_result = namedtuplefetchall(cursor)
        id_aset = id_aset_result[0][0]
        cursor.close()

        try:
            time = str(datetime.now())
            cursor = connection.cursor()
            cursor.execute("insert into transaksi_pembelian values ('"+email+"', '"+time+"', '"+input[0]+"', '"+id_aset+"')")
            cursor.close()
            return redirect('/transaksi-pembelian/read/')
        except Exception as e:
            print(e)
            message = "Data tidak berhasil dibuat"

    form = CreateTransaksiPembelianAsetForm()

    data = {
        'form' : form,
        'message' : message,
        'aset' : result
    }



    return render(request, "create_transaksi_pembelian_aset.html", data)