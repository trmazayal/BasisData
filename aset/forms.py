from django.forms import Form, formset_factory
from django import forms
from collections import namedtuple
from django.db import connection

# Create Form
class CreateDekorasiForm(forms.Form):
    id = forms.CharField(max_length=5, label='ID', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    nama = forms.CharField(max_length=50, label='Nama', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    minimum_level = forms.IntegerField(label='Minimum Level', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    harga_beli = forms.IntegerField(label='Harga Beli', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    harga_jual = forms.IntegerField(label='Harga Jual', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))

class CreateBibitTanamanForm(forms.Form):
    id = forms.CharField(max_length=5, label='ID', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    nama = forms.CharField(max_length=50, label='Nama', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    minimum_level = forms.IntegerField(label='Minimum Level', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    harga_beli = forms.IntegerField(label='Harga Beli', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    durasi_panen = forms.TimeField(label='Durasi Panen', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))

class CreateKandangForm(forms.Form):
    id = forms.CharField(max_length=5, label='ID', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    nama = forms.CharField(max_length=50, label='Nama', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    minimum_level = forms.IntegerField(label='Minimum Level', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    harga_beli = forms.IntegerField(label='Harga Beli', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    kapasitas_maks = forms.IntegerField(label='Kapasitas Maks', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    jenis_hewan = forms.CharField(max_length=50, label='Jenis Hewan', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))

class CreateHewanForm(forms.Form):
    id = forms.CharField(max_length=5, label='ID', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    nama = forms.CharField(max_length=50, label='Nama', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    minimum_level = forms.IntegerField(label='Minimum Level', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    harga_beli = forms.IntegerField(label='Harga Beli', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    durasi_produksi = forms.TimeField(label='Durasi Produksi', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))

class CreateAlatProduksiForm(forms.Form):
    id = forms.CharField(max_length=5, label='ID', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    nama = forms.CharField(max_length=50, label='Nama', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    minimum_level = forms.IntegerField(label='Minimum Level', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    harga_beli = forms.IntegerField(label='Harga Beli', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    kapasitas_maks = forms.IntegerField(label='Kapasitas Maks', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))

class CreatePetakSawahForm(forms.Form):
    id = forms.CharField(max_length=5, label='ID', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    nama = forms.CharField(max_length=50, label='Nama', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    minimum_level = forms.IntegerField(label='Minimum Level', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    harga_beli = forms.IntegerField(label='Harga Beli', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    jenis_tanaman = forms.CharField(max_length=50, label='Harga Jual', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))

# Update Form
class UpdateDekorasiForm(forms.Form):
    id = forms.CharField(max_length=5, label='ID', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    nama = forms.CharField(max_length=10, label='Nama', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    minimum_level = forms.IntegerField(label='Minimum Level', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    harga_beli = forms.IntegerField(label='Harga Beli', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    harga_jual = forms.IntegerField(label='Harga Jual', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))

class UpdateBibitTanamanForm(forms.Form):
    id = forms.CharField(max_length=5, label='ID', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    nama = forms.CharField(max_length=10, label='Nama', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    minimum_level = forms.IntegerField(label='Minimum Level', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    harga_beli = forms.IntegerField(label='Harga Beli', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    durasi_panen = forms.TimeField(label='Durasi Panen', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))

class UpdateKandangForm(forms.Form):
    id = forms.CharField(max_length=5, label='ID', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    nama = forms.CharField(max_length=10, label='Nama', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    minimum_level = forms.IntegerField(label='Minimum Level', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    harga_beli = forms.IntegerField(label='Harga Beli', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    kapasitas_maks = forms.IntegerField(label='Kapasitas Maks', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    jenis_hewan = forms.CharField(max_length=50, label='Jenis Hewan', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))

class UpdateHewanForm(forms.Form):
    id = forms.CharField(max_length=5, label='ID', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    nama = forms.CharField(max_length=10, label='Nama', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    minimum_level = forms.IntegerField(label='Minimum Level', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    harga_beli = forms.IntegerField(label='Harga Beli', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    durasi_produksi = forms.TimeField(label='Durasi Produksi', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    id_kandang = forms.CharField(max_length=5, label='ID Kandang', widget=forms.TextInput(attrs={'readonly':'readonly'}))

class UpdateAlatProduksiForm(forms.Form):
    id = forms.CharField(max_length=5, label='ID', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    nama = forms.CharField(max_length=10, label='Nama', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    minimum_level = forms.IntegerField(label='Minimum Level', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    harga_beli = forms.IntegerField(label='Harga Beli', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    kapasitas_maks = forms.IntegerField(label='Kapasitas Maks', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))

class UpdatePetakSawahForm(forms.Form):
    id = forms.CharField(max_length=5, label='ID', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    nama = forms.CharField(max_length=10, label='Nama', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    minimum_level = forms.IntegerField(label='Minimum Level', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    harga_beli = forms.IntegerField(label='Harga Beli', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    jenis_tanaman = forms.CharField(max_length=50, label='Harga Jual', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))