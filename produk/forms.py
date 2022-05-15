from django.forms import Form, formset_factory
from django import forms
from collections import namedtuple
from django.db import connection


class UpdateProdukForm(forms.Form):
    id = forms.CharField(max_length=10, label='ID', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    jenis_produk =  forms.CharField(max_length=10, label='Jenis', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    nama = forms.CharField(max_length=10, label='Nama', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    harga_jual = forms.CharField(label='Harga Jual', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    sifat_produk = forms.CharField(max_length=20, label='Sifat', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    
class CreateProdukForm(forms.Form):
    nama = forms.CharField(max_length=50, label='Nama', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    harga_jual = forms.CharField(label='Harga Jual', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    sifat_produk = forms.CharField(max_length=20, label='Sifat', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    
# class CreateProduksiForm(forms.Form):
#     durasi = forms.CharField(max_length=10, label='Durasi', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
#     jumlah_produk_hasil = forms.CharField(max_length=10, label='Jumlah Produk Hasil', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    