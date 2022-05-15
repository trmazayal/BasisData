from django.shortcuts import render, redirect
from collections import namedtuple
from django.db import connection
from .forms import UpdateProdukForm, CreateProdukForm

# Create your views here.
def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def max_index(id, relation):
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("select "+ id + " from " + relation + " order by " + id +"::int")
    result = namedtuplefetchall(cursor)
    idx = []
    for a in result:
        result_string = str(a).split('=')
        print(result_string)
        idx_string = result_string[1][1:-2]
        idx.append(int(idx_string))
    cursor.close()
    return idx[-1]

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
# def get_input_histori_pm(request):
#     input = request.POST
#     jum
#     return [nama,harga_jual,sifat_produk,jenis_produk]


# Create Produk
def createProduk(request):
    message =""
    # cursor.execute("select id_merk_obat from merk_obat order by cast(id_merk_obat as int)")
    # id_merk_obat_view = namedtuplefetchall(cursor)

    if request.method =='POST':
        input = get_input_produk(request)
        if input[3] == "Hasil Panen":
            prefixID =  "HP"
        elif input[3] == "Produk Makanan":
            prefixID =  "PM"
        elif input[3] == "Hasil Hewan":
            prefixID =  "PH"
        
        cursor = connection.cursor()
        cursor.execute("set search_path to hiday")
        cursor.execute("select id as c from produk where id like '"+ prefixID +"%' order by id asc")
        id_produk = namedtuplefetchall(cursor)
        id_produk = id_produk[-1].c
        
        id_produk = int(id_produk[2:])
        id_produk = int(id_produk) + 1
        idString2 = prefixID+str(id_produk)
        
        try :
            cursor.execute("insert into produk values ('"+idString2+"','"+input[0]+"','"+input[1]+"','"+input[2]+"')")
            cursor.close()
            return redirect('/read_produk/')
        except:
            message = "Data tidak berhasil dibuat"

    form = CreateProdukForm()
    
    jenis_produk = ['Hasil Panen', 'Produk Makanan', 'Hasil Hewan']
    
    args = {
        'jenis_produk': jenis_produk,
        'form': form,
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
                            when id like 'PH%' then 'Hasil Hewan'
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
    
    cursor.execute("update produk set nama = '" + nama + "',  harga_jual = '" +  harga_jual
    + "', sifat_produk = '"+  sifat_produk + "' where id = '"+ id +"'")

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
                        when id like 'PH%' then 'Hasil Hewan'
                    end as jenis_produk
                    from produk P
                    where id = '""" + id + "' order by jenis_produk, nama")
    hasil= namedtuplefetchall(cursor)
    nama = hasil[0].nama
    harga_jual = hasil[0].harga_jual
    sifat_produk = hasil[0].sifat_produk
    jenis_produk = hasil[0].jenis_produk
    
    formUpdate = UpdateProdukForm(initial={'id':id,'jenis_produk':jenis_produk ,'nama': nama, 'deskripsi_alat': harga_jual, 'harga_jual': harga_jual, 'sifat_produk': sifat_produk})

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
    cursor.execute("select id as id from produk where id ='"+ id + "'")
    id_produk = namedtuplefetchall(cursor)
    id_produk = id_produk[0].id
    cursor.execute("delete from produk where id ='"+ id + "'")
    cursor.execute("delete from produk where id ='"+ id_produk + "'")
    cursor.execute("select * from produk order by id asc")
    hasil = namedtuplefetchall(cursor)

    message = "Data berhasil dihapus"
    return viewsProduk(request, message)


# Create Produksi [Belum dihandle]
def createProduksi(request):
    message =""
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("select id_produk,nama from produk_makanan left join produk on produk_makanan.id_produk = produk.id order by nama")
    inama_produk = namedtuplefetchall(cursor)
    cursor.execute("select id_aset,nama from alat_produksi left join aset on alat_produksi.id_aset = aset.id order by nama")
    alat_produksi = namedtuplefetchall(cursor)
    
    cursor.execute("select nama from produk")
    daftar_produk = namedtuplefetchall(cursor)
    
    if request.method =='POST':
        input = get_input_produksi(request)
        nama_produk_makanan = input[0]
        nama_alat_produksi = input[1]
        durasi = int(input[2])
        jumlah_produk_hasil = input[3]
        

        cursor.execute("select id_aset from alat_produksi left join aset on alat_produksi.id_aset = aset.id where nama = '"+ nama_alat_produksi +"'")
        id_alat_produksi = namedtuplefetchall(cursor)
        id_alat_produksi = id_alat_produksi[0].id_aset
        
        cursor.execute("select id_produk from produk_makanan left join produk on produk_makanan.id_produk = produk.id where nama = '"+ nama_produk_makanan +"'")
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
        
        
        for i in range(lenBahan):
            for j in range(lenBahan):
                if (i!=j):
                    if(bahan[i]==bahan[j] and jumlah[i]==jumlah[j]):
                        cursor.close()
                        message = "Data tidak dapat diinputkan, karena ada data yang sama"
                        return render(request, 'produksi/createProduksi.html', {'message':message, 'nama_produk':nama_produk_makanan, 'alat_produksi':alat_produksi})
        
        id_produk = []
        for i in range(lenBahan):
            cursor.execute("select id from produk where nama = '"+ str(bahan[i]) +"'")
            hasil = namedtuplefetchall(cursor)
            if (hasil!=[]):
                id_produk.append(hasil[0].id)

        try :
            s = durasi*60
            format_durasi = '{:02}:{:02}:{:02}'.format(s//3600, s%3600//60, s%60)
            
            cursor.execute("insert into produksi (id_produk_makanan, id_alat_produksi, durasi, jumlah_unit_hasil) values ('"+str(id_produk_makanan)+"', '"+id_alat_produksi+"', '"+str(format_durasi)+"', '"+str(jumlah_produk_hasil)+"')")
            for i in range(lenBahan):
                cursor.execute("insert into produk_dibutuhkan_oleh_produk_makanan(id_produk_makanan, id_produk, jumlah) values ('"+str(id_produk_makanan)+"', '"+id_produk[i]+"', '"+jumlah[i]+"')")
            
            cursor.close()
            return redirect('/read_produksi/')
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
    print(produk_bahan)
    
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
# def updateProduk(request):
    

# Delete Produksi
def deleteProduksi(request, id):
    cursor = connection.cursor()
    id = str(id)
    cursor.execute("set search_path to hiday")
    cursor.execute("select id_produk_makanan as id from produksi p where p.id_produk_makanan ='"+ id + "'")
    id_produk = namedtuplefetchall(cursor)
    id_produk = id_produk[0].id
    cursor.execute("delete from produksi where id_produk_makanan ='"+ id + "'")
    cursor.execute("delete from produksi where id_produk_makanan ='"+ id_produk + "'")
    cursor.execute("select * from produksi order by id_produk_makanan")
    hasil = namedtuplefetchall(cursor)

    message = "Data berhasil dihapus"
    return viewsProduksi(request, message)

# Create History Produksi Makanan

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
                            where hpm.id_alat_produksi = alat.id_aset and hpm.id_produk_makanan = produk.id_produk"""+" and hpm.email = '"+email+"'")
        hasil = namedtuplefetchall(cursor)
    argument = {
        'hasil' : hasil,
        'roleAdmin' : roleAdmin,
        'rolePengguna' : rolePengguna,
        'message' : message
    }
    cursor.close()
    return render(request, 'produk/historiProduksiMakanan.html', argument)
