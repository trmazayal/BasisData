from multiprocessing.sharedctypes import Value
from django import forms

class BuatPakerKoinForm(forms.Form):
    jumlah_koin = forms.IntegerField(label='Jumlah Koin', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required',
    'oninvalid' : "alert('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')"}))
    harga = forms.IntegerField(label='Harga', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required',
    'oninvalid' : "alert('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')"}))

class UpdatePaketKoinForm(forms.Form):
    jumlah_koin = forms.IntegerField(label='Jumlah Koin', required=True, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    harga = forms.IntegerField(label='Harga', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required',
    'oninvalid' : "alert('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')"}))


class BeliPaketKoinForm(forms.Form):
    paket_koin = forms.IntegerField(label='Paket Koin', required=True, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    harga = forms.IntegerField(label='Harga', required=True, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    jumlah = forms.IntegerField(label='Jumlah', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required',
    'oninvalid' : "alert('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')"}))
    cara_pembayaran = forms.CharField(max_length=50, label='Cara Pembayaran', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required', 
    'oninvalid' : "alert('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')"}))