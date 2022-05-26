from datetime import datetime
from django.shortcuts import render, redirect
from collections import namedtuple
from django.db import connection
from .forms import UpdateProdukForm, UpdateProduksiForm

# Create your views here.
def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

# Input Produk
def get_input_produk(request):
    input = request.POST
    nama = input['nama']
    harga_jual = input['harga_jual']
    sifat_produk = input['sifat_produk']
    jenis_produk = input['jenis_produk']
    return [nama,harga_jual,sifat_produk,jenis_produk]

# Input Produksi
def get_input_produksi(request):
    input = request.POST
    nama_produk = input['nama_produk']
    alat_produksi = input['alat_produksi']
    durasi = input['durasi']
    jumlah_produk_hasil = input['jumlah_produk_hasil']
    return [nama_produk, alat_produksi, durasi, jumlah_produk_hasil]

# Input Histori Produksi Makanan
def get_input_histori_pm(request):
    input = request.POST
    nama_produk = input['nama_produk']
    jumlah_produksi = input['jumlah_produksi']
    xp = input['xp']
    return [nama_produk, jumlah_produksi,xp]

# Create Produk
def createProduk(request):
    message =""
    if request.method =='POST':
        input = get_input_produk(request)
        if input[3] == "Hasil Panen":
            prefixID =  "HP"
        elif input[3] == "Produk Makanan":
            prefixID =  "PM"
        elif input[3] == "Produk Hewan":
            prefixID =  "PH"
        
        cursor = connection.cursor()
        cursor.execute("set search_path to hiday")
        cursor.execute("select id as c from produk where id like %s order by id asc", [prefixID + "%"])
        id_produk = namedtuplefetchall(cursor)
        id_produk = id_produk[-1].c
        
        id_produk = int(id_produk[2:])
        id_produk = int(id_produk) + 1
        idProduk = prefixID+(str(id_produk).zfill(3))
        
        try :
            cursor.execute("insert into produk values (%s,%s,%s,%s)", [idProduk, input[0], input[1], input[2]])
            if(input[3] == "Hasil Panen"):
                cursor.execute("insert into hasil_panen values (%s)", [idProduk])
            elif(input[3] == "Produk Makanan"):
                cursor.execute("insert into produk_makanan values (%s)", [idProduk])
            elif(input[3] == "Produk Hewan"):
                cursor.execute("insert into produk_hewan values (%s)", [idProduk])
            cursor.close()
            return redirect('/produk/read_produk/')
        except:
            message = "Data tidak berhasil dibuat"
    
    jenis_produk = ['Hasil Panen', 'Produk Makanan', 'Produk Hewan']
    
    args = {
        'jenis_produk': jenis_produk,
        'message' : message
        }
    return render(request, "produk/createProduk.html", args)

# Read Produk
def viewsProduk(request, message=""):
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try:
        Role = request.session['role']
    except:
        return redirect('/')
    cursor.execute("set search_path to hiday")
    cursor.execute("select * from produk order by id asc")
    cursor.execute("""select id, nama, harga_jual, sifat_produk,
                        case
                            when id like 'HP%' then 'Hasil Panen'
                            when id like 'PM%' then 'Produk Makanan'
                            when id like 'PH%' then 'Produk Hewan'
                        end as jenis_produk,
                        case
                            when not exists(select * from detail_pesanan dp where dp.id_produk = id) and
                                not exists(select * from lumbung_memiliki_produk lmp where lmp.id_produk = id) and
                                not exists(select * from produk_dibutuhkan_oleh_produk_makanan pdpm where pdpm.id_produk = id) and
                                not exists(select * from produksi p where p.id_produk_makanan = id) and
                                not exists(select * from hewan_menghasilkan_produk_hewan hmp where hmp.id_produk_hewan = id) and
                                not exists(select * from bibit_tanaman_menghasilkan_hasil_panen bt where bt.id_hasil_panen = id)
                                then 1 else 0 end as can_delete
                        from produk P
                        order by jenis_produk, nama""")
    hasil = namedtuplefetchall(cursor)
    
    roleAdmin = False
    rolePengguna = False

    if Role == "Admin":
        roleAdmin = True
    elif Role == "Pengguna":
        rolePengguna = True

    argument = {
        'hasil' : hasil,
        'roleAdmin' : roleAdmin,
        'rolePengguna' : rolePengguna,
        'message' : message
    }
    cursor.close()
    return render(request, 'produk/produk.html', argument)

# Update Produk
def updateProduk(request):
    id = request.POST['id']
    nama = request.POST['nama']
    harga_jual = request.POST['harga_jual']
    sifat_produk = request.POST['sifat_produk']

    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    
    cursor.execute("update produk set nama = %s,  harga_jual = %s, sifat_produk = %s where id = %s", 
                   [nama, harga_jual, sifat_produk, id])

    message = "Data berhasil di update"
    return viewsProduk(request, message)

def formUpdateProduk(request, id):
    cursor = connection.cursor()
    id = str(id)
    cursor.execute("set search_path to hiday")
    cursor.execute("""select id, nama, harga_jual, sifat_produk,
                    case
                        when id like 'HP%' then 'Hasil Panen'
                        when id like 'PM%' then 'Produk Makanan'
                        when id like 'PH%' then 'Produk Hewan'
                    end as jenis_produk
                    from produk P
                    where id = '""" + id + "'")
    hasil= namedtuplefetchall(cursor)
    nama = hasil[0].nama
    harga_jual = hasil[0].harga_jual
    sifat_produk = hasil[0].sifat_produk
    jenis_produk = hasil[0].jenis_produk
    
    formUpdate = UpdateProdukForm(initial={
        'id':id,
        'jenis_produk':jenis_produk ,
        'nama': nama, 
        'harga_jual': harga_jual, 
        'sifat_produk': sifat_produk})

    argument = {
        'form' : formUpdate,
    }
    cursor.close()
    return render(request, 'produk/updateProduk.html', argument)

# Delete Produk
def deleteProduk(request, id):
    cursor = connection.cursor()
    id = str(id)
    cursor.execute("set search_path to hiday")
    cursor.execute("delete from produk where id = %s", [id])
    message = "Data berhasil dihapus"
    return viewsProduk(request, message)


# Create Produksi
def createProduksi(request):
    message =""
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("select id_produk,nama from produk_makanan left join produk on produk_makanan.id_produk = produk.id order by nama")
    inama_produk = namedtuplefetchall(cursor)
    cursor.execute("select id_aset,nama from alat_produksi left join aset on alat_produksi.id_aset = aset.id order by nama")
    alat_produksi = namedtuplefetchall(cursor)
    
    cursor.execute("select nama from produk order by nama")
    daftar_produk = namedtuplefetchall(cursor)
    
    if request.method =='POST':
        input = get_input_produksi(request)
        nama_produk_makanan = input[0]
        nama_alat_produksi = input[1]
        durasi = int(input[2])
        jumlah_produk_hasil = input[3]
        
        cursor.execute("select id_aset from alat_produksi left join aset on alat_produksi.id_aset = aset.id where nama = %s", [nama_alat_produksi])
        id_alat_produksi = namedtuplefetchall(cursor)
        id_alat_produksi = id_alat_produksi[0].id_aset
        
        cursor.execute("select id_produk from produk_makanan left join produk on produk_makanan.id_produk = produk.id where nama = %s", [nama_produk_makanan])
        id_produk_makanan = namedtuplefetchall(cursor)
        id_produk_makanan = id_produk_makanan[0].id_produk
          
        bahan = []
        jumlah = []
        count_id = 0

        while True:
            try:
                count_id = count_id + 1
                
                id_bahan = "bahan"+ str(count_id)
                hasil1 = str(request.POST[id_bahan])
                bahan.append(hasil1)
                
                id_jumlah = "jumlah"+ str(count_id)
                hasil2 = str(request.POST[id_jumlah])
                jumlah.append(hasil2)
            except Exception as e:
                break
        lenBahan = len(bahan)
        
        setBahan = set(bahan)
        if len(setBahan) != lenBahan:
            message = "Data tidak berhasil dibuat, karena terdapat bahan yang sama"
            args = {
                'nama_produk': inama_produk,
                'alat_produksi': alat_produksi,
                'daftar_produk': daftar_produk,
                'message' : message
            }
            return render(request, 'produk/createProduksi.html', args)
            
        id_produk = []
        for i in range(lenBahan):
            cursor.execute("select id from produk where nama = %s", [bahan[i]])
            hasil = namedtuplefetchall(cursor)
            if (hasil!=[]):
                id_produk.append(hasil[0].id)

        try :
            format_durasi = get_format_time(durasi)
            
            cursor.execute("insert into produksi values (%s, %s, %s, %s)", [id_alat_produksi,id_produk_makanan, format_durasi, jumlah_produk_hasil])
            for i in range(lenBahan):
                cursor.execute("insert into produk_dibutuhkan_oleh_produk_makanan values (%s, %s, %s)", [id_produk_makanan, id_produk[i], jumlah[i]])
            cursor.close()
            return redirect('/produk/read_produksi')
        except:
            message = "Data tidak berhasil dibuat"      
        
    args = {
        'nama_produk': inama_produk,
        'alat_produksi': alat_produksi,
        'daftar_produk': daftar_produk,
        'message' : message
        }
    return render(request, "produk/createProduksi.html", args)

# Read Produksi
def viewsProduksi(request, message=""):
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try:
        Role = request.session['role']
    except:
        return redirect('/')
    cursor.execute("set search_path to hiday")
    cursor.execute("select * from produk order by id asc")
    cursor.execute("""select p.id_produk_makanan, produk.nama as produk_makanan,alat.nama as alat_produksi,CAST(extract(epoch from durasi::interval) / 60 AS int) durasi, jumlah_unit_hasil,
                        case
                            when not exists(select * from histori_produksi_makanan hpm where hpm.id_produk_makanan = produk.id_produk)
                        then 1 else 0 end as can_delete
                        from produksi p,
                             (select id_aset,nama
                            from alat_produksi left join aset on alat_produksi.id_aset = aset.id) as alat,
                            (select id_produk, nama
                            from produk_makanan left join produk on produk_makanan.id_produk = produk.id) as produk
                            where p.id_alat_produksi = alat.id_aset and p.id_produk_makanan = produk.id_produk
                        order by p.id_produk_makanan""")
    hasil = namedtuplefetchall(cursor)
    
    cursor.execute("""select   id_produk_makanan ,id_produk, nama, jumlah
                        from produk p, produk_dibutuhkan_oleh_produk_makanan pdm
                        where p.id = pdm.id_produk""")
    produk_bahan = namedtuplefetchall(cursor)
    
    roleAdmin = False
    rolePengguna = False

    if Role == "Admin":
        roleAdmin = True
    elif Role == "Pengguna":
        rolePengguna = True

    argument = {
        'hasil' : hasil,
        'produk_bahan' : produk_bahan,
        'roleAdmin' : roleAdmin,
        'rolePengguna' : rolePengguna,
        'message' : message
    }
    cursor.close()
    return render(request, 'produk/produksi.html', argument)


# Update Produksi
def updateProduksi(request):
    nama_produk_makanan = request.POST['nama_produk_makanan']
    durasi = request.POST['durasi']
    jumlah_produk_hasil = request.POST['jumlah_produk_hasil']
    
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    
    cursor.execute("""select id_produk
                        from produk_makanan left join produk on produk_makanan.id_produk = produk.id
                        where nama = %s""", [nama_produk_makanan])
    hasil = namedtuplefetchall(cursor)
    id_produk_makanan = hasil[0].id_produk
    
    durasi = get_format_time(durasi)
    
    cursor.execute("update produksi set durasi = %s, jumlah_unit_hasil = %s where id_produk_makanan = %s", [durasi, jumlah_produk_hasil, id_produk_makanan])

    message = "Data berhasil di update"
    return viewsProduksi(request, message)
    
def formUpdateProduksi(request, id):
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    
    cursor.execute("""select id_alat_produksi,durasi,jumlah_unit_hasil
                    from produksi
                    where id_produk_makanan = %s""", [id])
    hasil = namedtuplefetchall(cursor)
    id_alat_produksi = hasil[0].id_alat_produksi
    durasi = get_minutes(str(hasil[0].durasi))
    jumlah_unit_hasil = hasil[0].jumlah_unit_hasil
    
    cursor.execute("""select nama
            from produk_makanan pm left join produk p on pm.id_produk = p.id
            where id_produk = %s""", [id])
    nama_produksi_makanan = namedtuplefetchall(cursor)
    
    cursor.execute("""select nama
                        from alat_produksi left join aset on alat_produksi.id_aset = aset.id
                        where id_aset = %s""", [id_alat_produksi])
    nama_alat_produksi = namedtuplefetchall(cursor)
    
    cursor.execute("""select id_produk, nama, jumlah
        from produk p, produk_dibutuhkan_oleh_produk_makanan pdm
        where p.id = pdm.id_produk and pdm.id_produk_makanan = %s""", [id])
    daftar_bahan = namedtuplefetchall(cursor)
    
    cursor.close()
    
    formUpdate = UpdateProduksiForm(initial={
        'id_produk_makanan': id,
        'nama_produk_makanan': nama_produksi_makanan[0].nama,
        'alat_produksi': nama_alat_produksi[0].nama,
        'durasi': durasi,
        'jumlah_produk_hasil': jumlah_unit_hasil
    })
    
    arguments = {
        'form': formUpdate,
        'daftar_bahan': daftar_bahan
    }
    cursor.close()
    return render(request, 'produk/updateProduksi.html', arguments)

    
# Delete Produksi
def deleteProduksi(request, id):
    cursor = connection.cursor()
    id = str(id)
    cursor.execute("set search_path to hiday")
    cursor.execute("select id_produk_makanan as id from produksi p where p.id_produk_makanan = %s", [id])
    id_produk = namedtuplefetchall(cursor)
    id_produk = id_produk[0].id
    cursor.execute("delete from produksi where id_produk_makanan = %s", [id])
    cursor.execute("delete from produk_dibutuhkan_oleh_produk_makanan where id_produk_makanan = %s", [id_produk])
    cursor.close()

    message = "Data berhasil dihapus"
    return viewsProduksi(request, message)

# Create History Produksi Makanan
def createHistoriProduksiMakanan(request):
    message =""
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("select id, nama from produk_makanan pm left join produk p on pm.id_produk = p.id order by nama")
    nama_produk = namedtuplefetchall(cursor)
    
    if request.method =='POST':
        input = get_input_histori_pm(request)
        id_nama_produk = str(input[0])
        jumlah_produksi = str(input[1])
        xp = str(input[2])
        cursor.execute("set search_path to public")
        email = str(request.session['email'])
        date_time = get_time_now()
        
        cursor.execute("set search_path to hiday")
        
        try:
            cursor.execute("select id_alat_produksi from produksi where id_produk_makanan = %s", [id_nama_produk])
            hasil = namedtuplefetchall(cursor)
            id_alat_produksi = hasil[0].id_alat_produksi
            
            cursor.execute("insert into histori_produksi values (%s, %s, %s, %s, %s)", [email, date_time, date_time, jumlah_produksi, xp])
            
            cursor.execute("insert into histori_produksi_makanan values (%s, %s, %s, %s)", [email, date_time, id_alat_produksi, id_nama_produk])
            return viewsHistoriProduksiMakanan(request, message)
        except Exception as e:
            cursor.execute("delete from histori_produksi hp where hp.email = %s and hp.waktu_awal = %s", [email, date_time])
            temp = str(e)
            message = temp[:temp.find("CONTEXT:")] 
        
    args = {
        'nama_produk': nama_produk,
        'message' : message
        }
    return render(request, "produk/createHistoriProduksiMakanan.html", args)

# Read Histori Produksi Makanan
def viewsHistoriProduksiMakanan(request, message=""):
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try:
        Role = request.session['role']
    except:
        return redirect('/')
    roleAdmin = False
    rolePengguna = False

    if Role == "Admin":
        roleAdmin = True
    elif Role == "Pengguna":
        rolePengguna = True
    
    if (roleAdmin):
        cursor.execute("set search_path to hiday")
        cursor.execute("""select hpm.email,  to_char(hp.waktu_awal, 'HH:MI:SS') as waktu_awal, to_char(hp.waktu_selesai, 'HH:MI:SS') as waktu_selesai, hp.jumlah, hp.xp,produk.nama as produk, alat.nama as alat
                            from histori_produksi_makanan hpm left join histori_produksi hp on hpm.email = hp.email and hpm.waktu_awal = hp.waktu_awal,
                                    (select id_aset,nama
                                from alat_produksi left join aset on alat_produksi.id_aset = aset.id) as alat,
                                (select id_produk, nama
                                from produk_makanan left join produk on produk_makanan.id_produk = produk.id) as produk
                            where hpm.id_alat_produksi = alat.id_aset and hpm.id_produk_makanan = produk.id_produk
                            order by hpm.email""")
        hasil = namedtuplefetchall(cursor)
    elif (rolePengguna):
        cursor.execute("set search_path to hiday")
        email = request.session['email']
        cursor.execute("""select hpm.email,  to_char(hp.waktu_awal, 'HH:MI:SS') as waktu_awal, to_char(hp.waktu_selesai, 'HH:MI:SS') as waktu_selesai, hp.jumlah, hp.xp,produk.nama as produk, alat.nama as alat
                    from histori_produksi_makanan hpm left join histori_produksi hp on hpm.email = hp.email and hpm.waktu_awal = hp.waktu_awal,
                            (select id_aset,nama
                        from alat_produksi left join aset on alat_produksi.id_aset = aset.id) as alat,
                        (select id_produk, nama
                        from produk_makanan left join produk on produk_makanan.id_produk = produk.id) as produk
                    where hpm.id_alat_produksi = alat.id_aset and hpm.id_produk_makanan = produk.id_produk and hpm.email = %s""", [email])
        hasil = namedtuplefetchall(cursor)
    argument = {
        'hasil' : hasil,
        'roleAdmin' : roleAdmin,
        'rolePengguna' : rolePengguna,
        'message' : message
    }
    cursor.close()
    return render(request, 'produk/historiProduksiMakanan.html', argument)


def get_minutes(time_str):
    hh, mm, ss = time_str.split(':')
    return int(hh) * 60 + int(mm) 

def get_format_time(time_str):
    s = int(time_str)*60
    return '{:02}:{:02}:{:02}'.format(s//3600, s%3600//60, s%60)

def get_time_now():
    date_time = datetime.now()
    return date_time.strftime("%Y-%m-%d %H:%M:%S")
