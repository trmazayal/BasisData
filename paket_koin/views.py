from django.shortcuts import render, redirect
from django.db import connection
from collections import namedtuple
import datetime

from paket_koin.forms import BeliPaketKoinForm, BuatPakerKoinForm, UpdatePaketKoinForm


def get_input_paket_koin(request):
    input = request.POST
    jumlah_koin = input['jumlah_koin']
    harga = input['harga']
    return [jumlah_koin, harga]

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
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try:
        email = request.session['email']
    except Exception as e:
        return redirect('/')

    cursor.execute("set search_path to hiday")
    cursor.execute("""select jumlah_koin, harga,
                        case
                            when not exists(select distinct pk.jumlah_koin from transaksi_pembelian_koin tpk where tpk.paket_koin = jumlah_koin)
                            then 1 else 0 
                            end as bisa_delete
                        from paket_koin pk
                        order by jumlah_koin asc""")
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
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try:
        email = request.session['email']
    except Exception as e:
        return redirect('/')
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

def form_buat_paket_koin(request):
    if request.method =='POST':
        cursor = connection.cursor()
        cursor.execute("set search_path to hiday")
        input = get_input_paket_koin(request)
        
        try :
            cursor.execute("insert into paket_koin values ('"+input[0]+"','"+input[1]+"')")
            cursor.close()
            return redirect('/paket-koin/')
        except:
            return redirect('/paket-koin/')

    return redirect('/paket-koin/')

def buat_paket_koin(request):
    argument = {
        'form': BuatPakerKoinForm(),
        }
    return render(request, "buat_paket_koin.html", argument)

def delete_paket_koin(request, jumlah_koin):
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("delete from paket_koin where jumlah_koin ='"+ jumlah_koin + "'")
    cursor.execute("select * from paket_koin order by jumlah_koin asc")
    hasil = namedtuplefetchall(cursor)
    cursor.close()
    return redirect('/paket-koin/')

def update_paket_koin(request): #form
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    jumlah_koin = request.POST['jumlah_koin']
    harga = request.POST['harga']

    
    cursor.execute("update paket_koin set jumlah_koin = '" + jumlah_koin + "',  harga = '" +  harga + "' where jumlah_koin = '"+ jumlah_koin +"'")

    return redirect('/paket-koin/')

def ubah_paket_koin(request, jumlah_koin):
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("select * from paket_koin where jumlah_koin ='"+ jumlah_koin + "'")
    hasil= namedtuplefetchall(cursor)
    jumlah_koin_u = hasil[0].jumlah_koin
    harga = hasil[0].harga
    
    form = UpdatePaketKoinForm(initial={'jumlah_koin': jumlah_koin_u, 'harga': harga})

    argument = {
        'form' : form,
    }
    cursor.close()
    return render(request, "ubah_paket_koin.html", argument)

def form_beli_paket_koin(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    email = request.session['email']
    cursor.execute("set search_path to hiday")

    if request.method =='POST':
        paket_koin_f = request.POST['paket_koin']
        jumlah = request.POST['jumlah']
        cara_pembayaran = request.POST['cara_pembayaran']
        ct = datetime.datetime.now()
        date_time = ct.strftime("%Y-%m-%d %H:%M:%S")
        total = "0"

        cursor = connection.cursor()
        cursor.execute("set search_path to hiday")
        try:
            cursor.execute("insert into transaksi_pembelian_koin values ('"+ email +"','"+ date_time +"','"+ str(jumlah) +"','"+ str(cara_pembayaran) +"','"+ paket_koin_f +"','" + total + "')")
            cursor.close()
        except:
            return redirect('/paket-koin/transaksi-pembelian-koin')

    return redirect('/paket-koin/transaksi-pembelian-koin/')

def pembelian_paket_koin(request, jumlah_koin):
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    cursor.execute("select * from paket_koin where jumlah_koin ='"+ jumlah_koin + "'")
    hasil= namedtuplefetchall(cursor)
    jumlah_koin = hasil[0].jumlah_koin
    harga = hasil[0].harga
    
    form = BeliPaketKoinForm(initial={'paket_koin': jumlah_koin, 'harga': harga})
    argument = {
        'form': form,
        }
    return render(request, "pembelian_paket_koin.html", argument)
