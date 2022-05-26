from django import forms

class UpdateProdukForm(forms.Form):
    id = forms.CharField(max_length=10, label='ID', widget=forms.TextInput(attrs={'readonly':'readonly', 'style':'color:#c9c9c9;'}))
    jenis_produk =  forms.CharField(max_length=10, label='Jenis', widget=forms.TextInput(attrs={'readonly':'readonly', 'style':'color:#c9c9c9;'}))
    nama = forms.CharField(max_length=10, label='Nama', widget=forms.TextInput(attrs={'readonly':'readonly', 'style':'color:#c9c9c9;'}))
    harga_jual = forms.CharField(label='Harga Jual', required=True, 
                                 widget=forms.TextInput(
                                    attrs={
                                        'placeholder':'*Required', 
                                        'oninvalid' : "this.setCustomValidity('Harga jual harus diisi!')",
                                        'oninput' : "validity.valid||(value='');"}))
    sifat_produk = forms.CharField(max_length=20, label='Sifat', required=True, 
                                   widget=forms.TextInput(
                                    attrs={
                                        'placeholder':'*Required', 
                                        'oninvalid' : "this.setCustomValidity('Sifat produk harus diisi!')",
                                        'oninput' : "validity.valid||(value='');"}))
    
class UpdateProduksiForm(forms.Form):
    nama_produk_makanan = forms.CharField(max_length=10, label='Nama Produk Makanan', widget=forms.TextInput(attrs={'readonly':'readonly', 'style':'color:#c9c9c9;'}))
    alat_produksi = forms.CharField(max_length=10, label='Alat Produksi', widget=forms.TextInput(attrs={'readonly':'readonly', 'style':'color:#c9c9c9;'}))
    durasi = forms.IntegerField(label='Durasi Produksi (dalam menit)', required=True, 
                                widget=forms.TextInput(
                                    attrs={
                                        'placeholder':'*Required', 
                                        'oninvalid' : "this.setCustomValidity('Durasi produksi harus diisi!')",
                                        'oninput' : "validity.valid||(value='');"}))
    jumlah_produk_hasil = forms.IntegerField(label='Jumlah Produk yang Dihasilkan', required=True, 
                                             widget=forms.TextInput(
                                                attrs={
                                                    'placeholder':'*Required', 
                                                    'oninvalid' : "this.setCustomValidity('Jumlah produksi yang dihasilkan harus diisi!')",
                                                    'oninput' : "validity.valid||(value='');"}))
