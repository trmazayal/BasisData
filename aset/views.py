from django.shortcuts import render, redirect, HttpResponse
from django.db import connection
from collections import namedtuple
from login.views import namedtuplefetchall, cekRole
from .forms import CreateDekorasiForm, CreateBibitTanamanForm, CreateKandangForm, CreateHewanForm, CreateAlatProduksiForm, CreatePetakSawahForm, UpdateDekorasiForm, UpdateBibitTanamanForm, UpdateKandangForm, UpdateHewanForm, UpdateAlatProduksiForm, UpdatePetakSawahForm

def read_aset(request):
    return render(request, 'read_aset.html')

def read_dekorasi(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try:
        Role = request.session['role']
    except:
        return redirect('/')
    cursor.execute("set search_path to hiday")
    cursor.execute(f"""select *,
                    case
	                    when not exists(select * from koleksi_aset_memiliki_aset kama where kama.id_aset = dekorasi.id_aset) and
                        not exists(select * from dekorasi_memiliki_histori_penjualan dmhp where dmhp.id_dekorasi = dekorasi.id_aset)
                    then 1 else 0 end as can_delete
                    from aset left join dekorasi on dekorasi.id_aset = aset.id
                    """)
    hasil = namedtuplefetchall(cursor)

    data = {
            'list_dekorasi' : hasil,
    }

    roleAdmin = False
    rolePengguna = False

    if Role == "Admin":
        roleAdmin = True
    elif Role == "Pengguna":
        rolePengguna = True

    data = {
        'list_dekorasi' : hasil,
        'roleAdmin' : roleAdmin,
        'rolePengguna' : rolePengguna,
    }

    return render(request, "read_dekorasi.html", data) 

def read_bibit_tanaman(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try:
        Role = request.session['role']
    except:
        return redirect('/')
    cursor.execute("set search_path to hiday")
    cursor.execute(f"""select id_aset, nama, minimum_level, harga_beli, CAST(extract(epoch from durasi_panen::interval) / 60 AS int) durasi_panen,
                    case
                        when not exists(select * from koleksi_aset_memiliki_aset kama where kama.id_aset = bibit_tanaman.id_aset) and 
                        not exists(select * from bibit_tanaman_menghasilkan_hasil_panen btmhp where btmhp.id_bibit_tanaman = bibit_tanaman.id_aset) and 
                        not exists(select * from histori_tanaman ht where ht.id_bibit_tanaman = bibit_tanaman.id_aset) 
                    then 1 else 0 end as can_delete
                    from aset left join bibit_tanaman on bibit_tanaman.id_aset = aset.id""")
    hasil = namedtuplefetchall(cursor)

    roleAdmin = False
    rolePengguna = False

    if Role == "Admin":
        roleAdmin = True
    elif Role == "Pengguna":
        rolePengguna = True

    data = {
        'list_bibit_tanaman' : hasil,
        'roleAdmin' : roleAdmin,
        'rolePengguna' : rolePengguna,
    }

    return render(request, "read_bibit_tanaman.html", data)

def read_kandang(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try:
        Role = request.session['role']
    except:
        return redirect('/')
    cursor.execute("set search_path to hiday")
    cursor.execute(f"""select *,
                    case
	                    when not exists(select * from koleksi_aset_memiliki_aset kama where kama.id_aset = kandang.id_aset)
                    then 1 else 0 end as can_delete
                    from aset left join kandang on kandang.id_aset = aset.id""")
    hasil = namedtuplefetchall(cursor)

    roleAdmin = False
    rolePengguna = False

    if Role == "Admin":
        roleAdmin = True
    elif Role == "Pengguna":
        rolePengguna = True
    
    data = {
        'list_kandang' : hasil,
        'roleAdmin' : roleAdmin,
        'rolePengguna' : rolePengguna,
    }

    return render(request, "read_kandang.html", data)

def read_hewan(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try:
        Role = request.session['role']
    except:
        return redirect('/')
    cursor.execute("set search_path to hiday")
    cursor.execute(f"""select id_aset, nama, minimum_level, harga_beli, CAST(extract(epoch from durasi_produksi::interval) / 60 AS int) durasi_produksi, id_kandang,
                    case
	                    when not exists(select * from koleksi_aset_memiliki_aset kama where kama.id_aset = hewan.id_aset) and 
                        not exists(select * from hewan_menghasilkan_produk_hewan hmph where hmph.id_hewan = hewan.id_aset) and 
                        not exists(select * from histori_hewan hh where hh.id_hewan = hewan.id_aset)
                    then 1 else 0 end as can_delete
                    from aset left join hewan on hewan.id_aset = aset.id""")
    hasil = namedtuplefetchall(cursor)

    roleAdmin = False
    rolePengguna = False

    if Role == "Admin":
        roleAdmin = True
    elif Role == "Pengguna":
        rolePengguna = True

    data = {
        'list_hewan' : hasil,
        'roleAdmin' : roleAdmin,
        'rolePengguna' : rolePengguna,
    }

    return render(request, "read_hewan.html", data)

def read_alat_produksi(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try:
        Role = request.session['role']
    except:
        return redirect('/')
    cursor.execute("set search_path to hiday")
    cursor.execute(f"""select *,
                    case
	                    when not exists(select * from koleksi_aset_memiliki_aset kama where kama.id_aset = alat_produksi.id_aset) and 
                        not exists(select * from produksi p where p.id_alat_produksi = alat_produksi.id_aset)
                    then 1 else 0 end as can_delete
                    from aset left join alat_produksi on alat_produksi.id_aset = aset.id""")
    hasil = namedtuplefetchall(cursor)

    roleAdmin = False
    rolePengguna = False

    if Role == "Admin":
        roleAdmin = True
    elif Role == "Pengguna":
        rolePengguna = True
    
    data = {
        'list_alat_produksi' : hasil,
        'roleAdmin' : roleAdmin,
        'rolePengguna' : rolePengguna,
    }

    return render(request, "read_alat_produksi.html", data)

def read_petak_sawah(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try:
        Role = request.session['role']
    except:
        return redirect('/')
    cursor.execute("set search_path to hiday")
    cursor.execute(f"""select *,
                    case
	                    when not exists(select * from koleksi_aset_memiliki_aset kama where kama.id_aset = petak_sawah.id_aset)
                    then 1 else 0 end as can_delete
                    from aset left join petak_sawah on petak_sawah.id_aset = aset.id""")
    hasil = namedtuplefetchall(cursor)

    roleAdmin = False
    rolePengguna = False

    if Role == "Admin":
        roleAdmin = True
    elif Role == "Pengguna":
        rolePengguna = True
    
    data = {
        'list_petak_sawah' : hasil,
        'roleAdmin' : roleAdmin,
        'rolePengguna' : rolePengguna,
    }

    return render(request, "read_petak_sawah.html", data)

def create_aset(request):
    return render(request, 'create_aset.html')

def get_input_dekorasi(request):
    input = request.POST
    nama = input['nama']
    minimum_level = input['minimum_level']
    harga_beli = input['harga_beli']
    harga_jual = input['harga_jual']
    return [nama, minimum_level, harga_beli, harga_jual]

def create_dekorasi(request):
    message =""
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("select id as c from aset where id like 'DK%' order by id asc")
    id_aset = namedtuplefetchall(cursor)
    print(id_aset)
    id_aset = id_aset[-1].c
    
    id_aset = int(id_aset[2:])
    id_aset = int(id_aset) + 1
    id_dekorasi = "DK"+f"{id_aset:03d}"
    
    if request.method == 'POST':
        input = get_input_dekorasi(request)
        try:
            cursor.execute("insert into aset values ('"+id_dekorasi+"','"+input[0]+"','"+input[1]+"','"+input[2]+"')")
            cursor.execute("insert into dekorasi values ('"+id_dekorasi+"','"+input[3]+"')")
            cursor.close()
            return redirect('/aset/read/dekorasi/')
        except:
           message = "Data tidak berhasil dibuat"


    form = CreateDekorasiForm(initial={'id':id_dekorasi})
    
    data = {
        'form': form,
        'message' : message
    }

    return render(request, "create_dekorasi.html", data)

def get_input_bibit_tanaman(request):
    input = request.POST
    nama = input['nama']
    minimum_level = input['minimum_level']
    harga_beli = input['harga_beli']
    durasi_panen = input['durasi_panen']
    return [nama, minimum_level, harga_beli, durasi_panen]

def create_bibit_tanaman(request):
    message =""
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("select id as c from aset where id like 'BT%' order by id asc")
    id_aset = namedtuplefetchall(cursor)
    id_aset = id_aset[-1].c
    
    id_aset = int(id_aset[2:])
    id_aset = int(id_aset) + 1
    id_bibit_tanaman= "BT"+f"{id_aset:03d}"
        
    if request.method == 'POST':
        input = get_input_bibit_tanaman(request)
        durasi = int(input[3])
        s = durasi*60
        format_durasi = '{:02}:{:02}:{:02}'.format(s//3600, s%3600//60, s%60)
        try:
            cursor.execute("insert into aset values ('"+id_bibit_tanaman+"','"+input[0]+"','"+input[1]+"','"+input[2]+"')")
            cursor.execute("insert into bibit_tanaman values ('"+id_bibit_tanaman+"','"+str(format_durasi)+"')")
            cursor.close()
            return redirect('/aset/read/bibit-tanaman/')
        except:
            message = "Data tidak berhasil dibuat"

    form = CreateBibitTanamanForm(initial={'id':id_bibit_tanaman})
    
    data = {
        'form': form,
        'message' : message
    }

    return render(request, "create_bibit_tanaman.html", data)

def get_input_kandang(request):
    input = request.POST
    nama = input['nama']
    minimum_level = input['minimum_level']
    harga_beli = input['harga_beli']
    kapasitas_maks = input['kapasitas_maks']
    jenis_hewan = input['jenis_hewan']
    return [nama, minimum_level, harga_beli, kapasitas_maks, jenis_hewan]

def create_kandang(request):
    message =""
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("select id as c from aset where id like 'KD%' order by id asc")
    id_aset = namedtuplefetchall(cursor)
    id_aset = id_aset[-1].c
    
    id_aset = int(id_aset[2:])
    id_aset = int(id_aset) + 1
    id_kandang = "KD"+f"{id_aset:03d}"

    if request.method == 'POST':
        input = get_input_kandang(request)
        try :
            cursor.execute("insert into aset values ('"+id_kandang+"','"+input[0]+"','"+input[1]+"', '"+input[2]+"')")
            cursor.execute("insert into kandang values ('"+id_kandang+"','"+input[3]+"', '"+input[4]+"')")
            cursor.close()
            return redirect('/aset/read/kandang/')
        except Exception as e:
            message = "Data tidak berhasil dibuat"

    form = CreateKandangForm(initial={'id':id_kandang})
    
    data = {
        'form': form,
        'message' : message
    }

    return render(request, "create_kandang.html", data)

def get_input_hewan(request):
    input = request.POST
    nama = input['nama']
    minimum_level = input['minimum_level']
    harga_beli = input['harga_beli']
    durasi_produksi = input['durasi_produksi']
    return [nama, minimum_level, harga_beli, durasi_produksi]

def create_hewan(request):
    message =""
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("select id as c from aset where id like 'HW%' order by id asc")
    id_aset = namedtuplefetchall(cursor)
    id_aset = id_aset[-1].c
    
    id_aset = int(id_aset[2:])
    id_aset = int(id_aset) + 1
    id_hewan = "HW"+f"{id_aset:03d}"

    if request.method == 'POST':
        input = get_input_hewan(request)
        durasi = int(input[3])
        s = durasi*60
        format_durasi = '{:02}:{:02}:{:02}'.format(s//3600, s%3600//60, s%60)
        try:
            cursor.execute("select id_aset from hiday.kandang where kandang.jenis_hewan ='"+ input[0]+"'" )
            id_kandang = namedtuplefetchall(cursor)
            id_kandang = id_kandang[0][0]
            cursor.execute("insert into aset values ('"+id_hewan+"','"+input[0]+"','"+input[1]+"', '"+input[2]+"')")
            cursor.execute("insert into hewan values ('"+id_hewan+"','" +str(format_durasi)+"', '"+id_kandang+"')")
            cursor.close()
            return redirect('/aset/read/hewan/')
        except IndexError as e:
            message = "Data untuk kandang hewan tersebut belum ada, silahkan membuat kandang terlebih dahulu."
        except Exception as e:
            print(e)
            message = "Data tidak berhasil dibuat"


    form = CreateHewanForm(initial={'id':id_hewan})
    
    data = {
        'form': form,
        'message' : message
    }

    return render(request, "create_hewan.html", data)

def get_input_alat_produksi(request):
    input = request.POST
    nama = input['nama']
    minimum_level = input['minimum_level']
    harga_beli = input['harga_beli']
    kapasitas_maks = input['kapasitas_maks']
    return [nama, minimum_level, harga_beli, kapasitas_maks]

def create_alat_produksi(request):
    message =""
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("select id as c from aset where id like 'AP%' order by id asc")
    id_aset = namedtuplefetchall(cursor)
    id_aset = id_aset[-1].c
    
    id_aset = int(id_aset[2:])
    id_aset = int(id_aset) + 1
    id_alat_produksi = "AP"+f"{id_aset:03d}"

    if request.method == 'POST':
        input = get_input_alat_produksi(request)
        try:
            cursor.execute("insert into aset values ('"+id_alat_produksi+"','"+input[0]+"','"+input[1]+"', '"+input[2]+"')")
            cursor.execute("insert into alat_produksi values ('"+id_alat_produksi+"','"+input[3]+"')")
            cursor.close()
            return redirect('/aset/read/alat-produksi/')
        except:
            message = "Data tidak berhasil dibuat"

    form = CreateAlatProduksiForm(initial={'id':id_alat_produksi})
    
    data = {
        'form': form,
        'message' : message
    }

    return render(request, "create_alat_produksi.html", data)

def get_input_petak_sawah(request):
    input = request.POST
    nama = input['nama']
    minimum_level = input['minimum_level']
    harga_beli = input['harga_beli']
    return [nama, minimum_level, harga_beli]

def create_petak_sawah(request):
    message =""
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("select id as c from aset where id like 'PS%' order by id asc")
    id_aset = namedtuplefetchall(cursor)
    cursor.execute("set search_path to hiday")
    cursor.execute("select a.nama from bibit_tanaman bt, aset a where bt.id_aset = a.id")
    result = namedtuplefetchall(cursor)
    id_aset = id_aset[-1].c
    
    id_aset = int(id_aset[2:])
    id_aset = int(id_aset) + 1
    id_petak_sawah = "PS"+f"{id_aset:03d}"
    print(id_petak_sawah)
    if request.method == 'POST':
        input = get_input_petak_sawah(request)
        bibit_tanaman = request.POST.get("tanaman")
        try:
            cursor.execute("insert into aset values ('"+id_petak_sawah+"','"+input[0]+"',"+input[1]+", "+input[2]+")")
            cursor.execute("insert into petak_sawah values ('"+id_petak_sawah+"','"+bibit_tanaman+"')")
            cursor.close()
            return redirect('/aset/read/petak-sawah/')
        except Exception as e:
            print(e)
            message = "Data tidak berhasil dibuat"
    
    data = {
        'message' : message,
        'tanaman': result,
        'id': id_petak_sawah,
    }

    return render(request, "create_petak_sawah.html", data)

def updateDekorasi(request):
    id = request.POST['id']
    nama = request.POST['nama']
    minimum_level = request.POST['minimum_level']
    harga_beli = request.POST['harga_beli']
    harga_jual = request.POST['harga_jual']

    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("update aset set minimum_level = '" + minimum_level + "',  harga_beli = '" + harga_beli 
    + "' where id = '"+ id +"'")
    cursor.execute("update dekorasi set harga_jual = '" + harga_jual + "' where id_aset = '"+ id +"'")

    return read_dekorasi(request)

def formUpdateDekorasi(request, id):
    cursor = connection.cursor()
    id = str(id)
    cursor.execute("set search_path to hiday")
    cursor.execute("""select a.id, a.nama, a.minimum_level, a.harga_beli, d.harga_jual
                    from aset a, dekorasi d
                    where a.id = '""" + id + "' and d.id_aset = a.id order by id")
    hasil = namedtuplefetchall(cursor)
    nama = hasil[0].nama
    minimum_level = hasil[0].minimum_level
    harga_beli = hasil[0].harga_beli
    harga_jual = hasil[0].harga_jual
    
    formUpdate = UpdateDekorasiForm(initial={'id':id, 'nama': nama, 'minimum_level': minimum_level, 'harga_beli': harga_beli, 'harga_jual': harga_jual})

    data = {
        'form' : formUpdate,
    }
    cursor.close()

    return render(request, 'update_dekorasi.html', data)

def updateBibitTanaman(request):
    id = request.POST['id']
    nama = request.POST['nama']
    minimum_level = request.POST['minimum_level']
    harga_beli = request.POST['harga_beli']
    durasi_panen = request.POST['durasi_panen']

    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("update aset set minimum_level = '" + minimum_level + "',  harga_beli = '" + harga_beli 
    + "' where id = '"+ id +"'")
    cursor.execute("update bibit_tanaman set durasi_panen = '" + durasi_panen + "' where id_aset = '"+ id +"'")

    return read_bibit_tanaman(request)

def formUpdateBibitTanaman(request, id):
    cursor = connection.cursor()
    id = str(id)
    cursor.execute("set search_path to hiday")
    cursor.execute("""select a.id, a.nama, a.minimum_level, a.harga_beli, bt.durasi_panen
                    from aset a, bibit_tanaman bt
                    where a.id = '""" + id + "' and bt.id_aset = a.id order by id")
    hasil = namedtuplefetchall(cursor)
    nama = hasil[0].nama
    minimum_level = hasil[0].minimum_level
    harga_beli = hasil[0].harga_beli
    durasi_panen = hasil[0].durasi_panen
    print(hasil)
    
    formUpdate = UpdateBibitTanamanForm(initial={'id':id, 'nama': nama, 'minimum_level': minimum_level, 'harga_beli': harga_beli, 'durasi_panen': durasi_panen})

    data = {
        'form' : formUpdate,
    }
    cursor.close()

    return render(request, 'update_bibit_tanaman.html', data)

def updateKandang(request):
    id = request.POST['id']
    nama = request.POST['nama']
    minimum_level = request.POST['minimum_level']
    harga_beli = request.POST['harga_beli']
    kapasitas_maks = request.POST['kapasitas_maks']
    jenis_hewan = request.POST['jenis_hewan']

    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("update aset set minimum_level = '" + minimum_level + "',  harga_beli = '" + harga_beli 
    + "' where id = '"+ id +"'")
    cursor.execute("update kandang set kapasitas_maks = '" + kapasitas_maks + "', jenis_hewan = '" + jenis_hewan + "' where id_aset = '"+ id +"'")

    return read_kandang(request)

def formUpdateKandang(request, id):
    cursor = connection.cursor()
    id = str(id)
    cursor.execute("set search_path to hiday")
    cursor.execute("""select a.id, a.nama, a.minimum_level, a.harga_beli, k.kapasitas_maks, k.jenis_hewan
                    from aset a, kandang k
                    where a.id = '""" + id + "' and k.id_aset = a.id order by id")
    hasil = namedtuplefetchall(cursor)
    nama = hasil[0].nama
    minimum_level = hasil[0].minimum_level
    harga_beli = hasil[0].harga_beli
    kapasitas_maks = hasil[0].kapasitas_maks
    jenis_hewan = hasil[0].jenis_hewan
    
    formUpdate = UpdateKandangForm(initial={'id':id, 'nama': nama, 'minimum_level': minimum_level, 'harga_beli': harga_beli, 'kapasitas_maks': kapasitas_maks, 'jenis_hewan': jenis_hewan})

    data = {
        'form' : formUpdate,
    }
    cursor.close()

    return render(request, 'update_kandang.html', data)

def updateHewan(request):
    id = request.POST['id']
    nama = request.POST['nama']
    minimum_level = request.POST['minimum_level']
    harga_beli = request.POST['harga_beli']
    durasi_produksi = request.POST['durasi_produksi']
    id_kandang = request.POST['id_kandang']

    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("update aset set minimum_level = '" + minimum_level + "',  harga_beli = '" + harga_beli 
    + "' where id = '"+ id +"'")
    cursor.execute("update hewan set durasi_produksi = '" + durasi_produksi + "' where id_aset = '"+ id +"'")

    return read_hewan(request)

def formUpdateHewan(request, id):
    cursor = connection.cursor()
    id = str(id)
    cursor.execute("set search_path to hiday")
    cursor.execute("""select a.id, a.nama, a.minimum_level, a.harga_beli, h.durasi_produksi, h.id_kandang
                    from aset a, hewan h
                    where a.id = '""" + id + "' and h.id_aset = a.id order by id")
    hasil = namedtuplefetchall(cursor)
    nama = hasil[0].nama
    minimum_level = hasil[0].minimum_level
    harga_beli = hasil[0].harga_beli
    durasi_produksi = hasil[0].durasi_produksi
    id_kandang = hasil[0].id_kandang
    
    formUpdate = UpdateHewanForm(initial={'id':id, 'nama': nama, 'minimum_level': minimum_level, 'harga_beli': harga_beli, 'durasi_produksi': durasi_produksi, 'id_kandang': id_kandang})

    data = {
        'form' : formUpdate,
    }
    cursor.close()

    return render(request, 'update_hewan.html', data)

def updateAlatProduksi(request):
    id = request.POST['id']
    nama = request.POST['nama']
    minimum_level = request.POST['minimum_level']
    harga_beli = request.POST['harga_beli']
    kapasitas_maks = request.POST['kapasitas_maks']

    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("update aset set minimum_level = '" + minimum_level + "',  harga_beli = '" + harga_beli 
    + "' where id = '"+ id +"'")
    cursor.execute("update alat_produksi set kapasitas_maks = '" + kapasitas_maks + "' where id_aset = '"+ id +"'")

    return read_alat_produksi(request)

def formUpdateAlatProduksi(request, id):
    cursor = connection.cursor()
    id = str(id)
    cursor.execute("set search_path to hiday")
    cursor.execute("""select a.id, a.nama, a.minimum_level, a.harga_beli, ap.kapasitas_maks
                    from aset a, alat_produksi ap
                    where a.id = '""" + id + "' and ap.id_aset = a.id order by id")
    hasil = namedtuplefetchall(cursor)
    nama = hasil[0].nama
    minimum_level = hasil[0].minimum_level
    harga_beli = hasil[0].harga_beli
    kapasitas_maks = hasil[0].kapasitas_maks
    
    formUpdate = UpdateAlatProduksiForm(initial={'id':id, 'nama': nama, 'minimum_level': minimum_level, 'harga_beli': harga_beli, 'kapasitas_maks': kapasitas_maks})

    data = {
        'form' : formUpdate,
    }
    cursor.close()

    return render(request, 'update_alat_produksi.html', data)

def formUpdatePetakSawah(request, id):
    cursor = connection.cursor()
    id = str(id)
    cursor.execute("set search_path to hiday")
    cursor.execute("""select a.id, a.nama, a.minimum_level, a.harga_beli, ps.jenis_tanaman
                    from aset a, petak_sawah ps
                    where a.id = '""" + id + "' and ps.id_aset = a.id order by id")
    hasil = namedtuplefetchall(cursor)
    nama = hasil[0].nama
    minimum_level = hasil[0].minimum_level
    harga_beli = hasil[0].harga_beli
    cursor.execute("select a.nama from bibit_tanaman bt, aset a where bt.id_aset = a.id")
    result = namedtuplefetchall(cursor)
    
    if request.method == 'POST':
        minimum_level = request.POST.get("minimum_level")
        harga_beli = request.POST.get("harga_beli")
        tanaman = request.POST.get("tanaman")

        cursor.execute("update aset set minimum_level = '" + minimum_level + "',  harga_beli = '" + harga_beli + "' where id = '"+ id +"'")
        cursor.execute("update petak_sawah set jenis_tanaman = '" + tanaman + "' where id_aset = '"+ id +"'")

        return redirect('/aset/read/petak-sawah/')

    data = {
       'id': id,
       'nama': nama,
       'minimum_level': minimum_level,
       'harga_beli':harga_beli,
       'tanaman': result

    }
    cursor.close()

    return render(request, 'update_petak_sawah.html', data)

def deleteDekorasi(request, id):
    cursor = connection.cursor()
    id = str(id)
    cursor.execute("set search_path to hiday")
    cursor.execute("select id_aset as id from dekorasi d where d.id_aset ='"+ id + "'")
    id_aset = namedtuplefetchall(cursor)
    id_aset = id_aset[0].id
    cursor.execute("delete from aset where id ='"+ id + "'")
    cursor.execute("delete from dekorasi where id_aset ='"+ id_aset + "'")
    cursor.execute("select * from aset left join dekorasi on dekorasi.id_aset = aset.id")
    hasil = namedtuplefetchall(cursor)

    return read_dekorasi(request)

def deleteBibitTanaman(request, id):
    cursor = connection.cursor()
    id = str(id)
    cursor.execute("set search_path to hiday")
    cursor.execute("select id_aset as id from bibit_tanaman bt where bt.id_aset ='"+ id + "'")
    id_aset = namedtuplefetchall(cursor)
    id_aset = id_aset[0].id
    cursor.execute("delete from aset where id ='"+ id + "'")
    cursor.execute("delete from bibit_tanaman where id_aset ='"+ id_aset + "'")
    cursor.execute("select * from aset left join bibit_tanaman on bibit_tanaman.id_aset = aset.id")
    hasil = namedtuplefetchall(cursor)

    return read_bibit_tanaman(request)

def deleteKandang(request, id):
    cursor = connection.cursor()
    id = str(id)
    cursor.execute("set search_path to hiday")
    cursor.execute("select id_aset as id from kandang k where k.id_aset ='"+ id + "'")
    id_aset = namedtuplefetchall(cursor)
    id_aset = id_aset[0].id
    cursor.execute("delete from aset where id ='"+ id + "'")
    cursor.execute("delete from kandang where id_aset ='"+ id_aset + "'")
    cursor.execute("select * from aset left join kandang on kandang.id_aset = aset.id")
    hasil = namedtuplefetchall(cursor)

    return read_kandang(request)

def deleteHewan(request, id):
    cursor = connection.cursor()
    id = str(id)
    cursor.execute("set search_path to hiday")
    cursor.execute("select id_aset as id from hewan h where h.id_aset ='"+ id + "'")
    id_aset = namedtuplefetchall(cursor)
    id_aset = id_aset[0].id
    cursor.execute("delete from aset where id ='"+ id + "'")
    cursor.execute("delete from hewan where id_aset ='"+ id_aset + "'")
    cursor.execute("select * from aset left join hewan on hewan.id_aset = aset.id")
    hasil = namedtuplefetchall(cursor)

    return read_hewan(request)

def deleteAlatProduksi(request, id):
    cursor = connection.cursor()
    id = str(id)
    cursor.execute("set search_path to hiday")
    cursor.execute("select id_aset as id from alat_produksi ap where ap.id_aset ='"+ id + "'")
    id_aset = namedtuplefetchall(cursor)
    id_aset = id_aset[0].id
    cursor.execute("delete from aset where id ='"+ id + "'")
    cursor.execute("delete from alat_produksi where id_aset ='"+ id_aset + "'")
    cursor.execute("select * from aset left join alat_produksi on alat_produksi.id_aset = aset.id")
    hasil = namedtuplefetchall(cursor)

    return read_alat_produksi(request)

def deletePetakSawah(request, id):
    cursor = connection.cursor()
    id = str(id)
    cursor.execute("set search_path to hiday")
    cursor.execute("select id_aset as id from petak_sawah ps where ps.id_aset ='"+ id + "'")
    id_aset = namedtuplefetchall(cursor)
    print(id_aset)
    id_aset = id_aset[0].id
    cursor.execute("delete from aset where id ='"+ id + "'")
    cursor.execute("delete from petak_sawah where id_aset ='"+ id_aset + "'")
    cursor.execute("select * from aset left join petak_sawah on petak_sawah.id_aset = aset.id")
    hasil = namedtuplefetchall(cursor)

    return read_petak_sawah(request)