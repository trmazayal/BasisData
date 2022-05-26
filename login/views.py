from django.shortcuts import render, redirect
from .forms import LoginForm, ChoiceRoleForm, AdminRoleForm, PenggunaRoleForm
from django.db import connection
from collections import namedtuple


def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def index(request, validasi = None):
    try:
        return login(request)
    except KeyError:
        formulir = LoginForm()
        message = ""
        if(validasi==False):
            message = "Invalid email or password"
        argument = { 
            'formlogin' : formulir,
            'message' : message
        }
        return render(request, 'login.html', argument)
    
def login(request):
    try:
        email = request.session['email']
        password = request.session['password']
    except:
        email = request.POST['email']
        password = request.POST['password']

    email = str(email)
    password = str(password)
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("""select result.email, result.password
                        from akun, (
                        select email, password
                        from pengguna
                        union
                        select email, password
                        from admin
                        ) as result
                        where akun.email = result.email and  result.email='"""+email+"' and result.password='"+password+"'")
     
    hasil = namedtuplefetchall(cursor)
    role = cekRole(email)
    roleAdmin = False
    rolePengguna = False
    if (role == 'Admin'):
        roleAdmin = True
    if (role == 'Pengguna'):
        rolePengguna = True

    cursor.execute("set search_path to public")
    if (hasil == []):
        cursor.close()
        return index(request, False)
    else:
        request.session['email'] = hasil[0].email
        request.session['password'] = hasil[0].password
        request.session.set_expiry(86400)
        request.session['role'] = role
        argument = {
            'nama_akun' : email.split("@", 1)[0],
            'email' : email,
            'roleAdmin' : roleAdmin,
            'rolePengguna' : rolePengguna
        }
        cursor.close()
        return render(request, "home.html", argument)

def logout(request):
    request.session.flush()
    request.session.clear_expired()
    return index(request)

def profil(request):
    try:
        email = request.session['email']
    except Exception as e:
        return redirect('/')
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("select * from akun where email='"+email+"'")
    pengguna = namedtuplefetchall(cursor)

    role = cekRole(email)
    roleAdmin = False
    rolePengguna = False
    if (role == 'Admin'):
        roleAdmin = True
    if (role == 'Pengguna'):
        rolePengguna = True
        
    if (roleAdmin):
        cursor.execute("select * from admin where email='"+email+"'")
        admin = namedtuplefetchall(cursor)
        email = admin[0].email

        argument = {
            'nama_akun' : email.split("@", 1)[0],
            'email' : email,
            'role' : role,
            'roleAdmin' : roleAdmin,
            'rolePengguna' : rolePengguna
        }
    elif (rolePengguna):
        cursor.execute("select * from pengguna where email='"+email+"'")
        pengguna = namedtuplefetchall(cursor)
        email = pengguna[0].email
        nama_area_pertanian = pengguna[0].nama_area_pertanian
        xp = pengguna[0].xp
        koin = pengguna[0].koin
        level = pengguna[0].level
        
        argument = {
            'nama_akun' : email.split("@", 1)[0],
            'email' : email,
            'role' : role,
            'roleAdmin' : roleAdmin,
            'rolePengguna' : rolePengguna,
            'nama_area_pertanian' : nama_area_pertanian,
            'xp' : xp,
            'koin' : koin,
            'level' : level
        }
    cursor.close()
    return render(request, "profil.html", argument)

    
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


def register(request):
    formulir = ChoiceRoleForm()
    argument = { 
        'form' : formulir,
        'formrole' : True,
        'roleAdmin' : False,
        'rolePengguna' : False
    }
    return render(request, 'registerPengguna.html', argument)

def registerPenggunaRole(request, message="", role=None):
    try:
        Role = str(request.POST['Role'])
    except:
        Role = role
        
    roleAdmin = False
    rolePengguna = False
    if(Role == "Admin"):
        formulir = AdminRoleForm()
        roleAdmin = True
    elif(Role == "Pengguna"):
        formulir = PenggunaRoleForm()
        rolePengguna = True

    argument = { 
        'form' : formulir,
        'role' : Role,
        'roleAdmin' : roleAdmin,
        'rolePengguna' : rolePengguna,
        'message': message
    }
    return render(request, 'registerPengguna.html', argument)


def insertAdmin(request):
    email = str(request.POST['email'])
    password = str(request.POST['password'])

    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("select * from akun where email='"+email+"'")
    hasil = namedtuplefetchall(cursor)
    if (hasil == []):
        cursor.execute("insert into akun values ('"+email+"')")
        cursor.execute("insert into admin values ('"+email+"','"+password+"')")
        
    else:
        cursor.close()
        return registerPenggunaRole(request, "Email sudah digunakan", 'Admin')
            
                
    cursor.execute("select * from admin where email='"+email+"' and password='"+password+"'")
    hasil = namedtuplefetchall(cursor)

    if (hasil == []):
        cursor.close()
        return index(request, False)
    else:
        cursor.execute("set search_path to public")
        request.session['email'] = hasil[0].email
        request.session['password'] = hasil[0].password
        request.session.set_expiry(1800)
        request.session['role'] = 'Admin'
        argument = {
            'nama_akun' : email.split("@", 1)[0],
            'hasil' : hasil,
            'roleAdmin' : True,
            'rolePengguna' : False,
        }
        cursor.close()
        return render(request, "home.html", argument)


def insertPengguna(request):
    email = str(request.POST['email'])
    password = str(request.POST['password'])
    nama_area_pertanian = str(request.POST['nama_area_pertanian'])
    xp = str(0)
    koin = str(0)
    level = str(1)

    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")

    cursor.execute("select * from akun where email='"+email+"'")
    hasil = namedtuplefetchall(cursor)
    if (hasil != []):
        cursor.close()
        return registerPenggunaRole(request, "Email sudah digunakan", "Pengguna")
    
    cursor.execute("insert into akun values ('"+email+"')")
    cursor.execute("insert into pengguna values ('"+email+"','"+password+"','"+nama_area_pertanian+"','"+xp+"','"+koin+"','"+level+"')")
                
    cursor.execute("select * from pengguna where email='"+email+"' and password='"+password+"'")
    hasil = namedtuplefetchall(cursor)

    if (hasil == []):
        cursor.close()
        return index(request, False)
    else:
        cursor.execute("set search_path to public")
        request.session['email'] = hasil[0].email
        request.session['password'] = hasil[0].password
        request.session['nama_area_pertanian'] = hasil[0].nama_area_pertanian
        request.session['xp'] = 0
        request.session['koin'] = 0
        request.session['level'] = 1
        request.session.set_expiry(1800)
        request.session['role'] = 'Pengguna'
        argument = {
            'nama_akun' : email.split("@", 1)[0],
            'hasil' : hasil,
            'roleAdmin' : False,
            'rolePengguna' : True,
        }
        cursor.close()
        return render(request, "home.html", argument)
    
def lihatIsiLumbung(request):
    try:
        email = request.session['email']
    except Exception as e:
        return redirect('/')
    cursor = connection.cursor()
    cursor.execute("set search_path to hiday")
    cursor.execute("select * from akun where email='"+email+"'")
    pengguna = namedtuplefetchall(cursor)

    role = cekRole(email)
    roleAdmin = False
    rolePengguna = False
    if (role == 'Admin'):
        roleAdmin = True
    if (role == 'Pengguna'):
        rolePengguna = True
        
    if (roleAdmin):
        cursor.execute("select * from admin where email='"+email+"'")
        admin = namedtuplefetchall(cursor)
        email = admin[0].email

        cursor.execute("""select l.email,id_produk, p.nama, p.harga_jual, p.sifat_produk, lmp.jumlah
                from lumbung l, lumbung_memiliki_produk lmp, produk p
                where l.email = lmp.id_lumbung
                and lmp.id_produk = p.id
                and id_produk like 'HP%' order by id_produk,l.email""")
        hasil_panen = namedtuplefetchall(cursor)
        
        cursor.execute("""select l.email,id_produk, p.nama, p.harga_jual, p.sifat_produk, lmp.jumlah
                from lumbung l, lumbung_memiliki_produk lmp, produk p
                where l.email = lmp.id_lumbung
                and lmp.id_produk = p.id
                and id_produk like 'PH%' order by id_produk,l.email""")
        produk_hewan = namedtuplefetchall(cursor)
        
        cursor.execute("""select l.email,id_produk, p.nama, p.harga_jual, p.sifat_produk, lmp.jumlah
                from lumbung l, lumbung_memiliki_produk lmp, produk p
                where l.email = lmp.id_lumbung
                and lmp.id_produk = p.id
                and id_produk like 'PM%' order by id_produk,l.email""")
        produk_makanan = namedtuplefetchall(cursor)


        argument = {
            'hasil_panen' : hasil_panen,
            'produk_hewan' : produk_hewan,
            'produk_makanan' : produk_makanan,
            'role' : role,
            'roleAdmin' : roleAdmin,
            'rolePengguna' : rolePengguna,
        }
    
    elif (rolePengguna):
        cursor.execute("select * from pengguna where email='"+email+"'")
        pengguna = namedtuplefetchall(cursor)
        email = pengguna[0].email
        
        cursor.execute("""select level, total , kapasitas_maksimal 
                       from lumbung where email='"""
                       +email+"'")
        lumbung = namedtuplefetchall(cursor)
        level = lumbung[0].level
        total = lumbung[0].total
        kapasitas_maksimal = lumbung[0].kapasitas_maksimal
        
        cursor.execute("""select id_produk, p.nama, p.harga_jual, p.sifat_produk, lmp.jumlah
                from lumbung l, lumbung_memiliki_produk lmp, produk p
                where l.email = lmp.id_lumbung 
                and lmp.id_produk = p.id 
                and id_produk like 'HP%' 
                and lmp.id_lumbung = '"""+email+"' order by id_produk""")
        hasil_panen = namedtuplefetchall(cursor)
        
        cursor.execute("""select id_produk, p.nama, p.harga_jual, p.sifat_produk, lmp.jumlah
                from lumbung l, lumbung_memiliki_produk lmp, produk p
                where l.email = lmp.id_lumbung 
                and lmp.id_produk = p.id 
                and id_produk like 'PH%' 
                and lmp.id_lumbung = '"""+email+"' order by id_produk""")
        produk_hewan = namedtuplefetchall(cursor)
        
        cursor.execute("""select id_produk, p.nama, p.harga_jual, p.sifat_produk, lmp.jumlah
                from lumbung l, lumbung_memiliki_produk lmp, produk p
                where l.email = lmp.id_lumbung 
                and lmp.id_produk = p.id 
                and id_produk like 'PM%' 
                and lmp.id_lumbung = '"""+email+"' order by id_produk""")
        produk_makanan = namedtuplefetchall(cursor)
        
        argument = {
            'hasil_panen' : hasil_panen,
            'produk_hewan' : produk_hewan,
            'produk_makanan' : produk_makanan,
            'role' : role,
            'roleAdmin' : roleAdmin,
            'rolePengguna' : rolePengguna,
            'level' : level,
            'total' : total,
            'kapasitas_maksimal' : kapasitas_maksimal,
        }
    cursor.close()
    return render(request, "lumbung.html", argument)