# from multiprocessing.sharedctypes import Value
# from django import forms


# class buatPaketKoinForm(forms.Form):
#     jumlah_koin = forms.IntegerField(label = 'Jumlah Koin')
#     harga = forms.IntegerField(label='Harga')

# class ubahPaketKoinForm(forms.Form):
#     jumlah_koin = forms.CharField(
#     required=False,
#     widget=forms.TextInput(attrs={'readonly': True, 'value': '100'}),
#     )
#     harga = forms.IntegerField(label='Harga')

# class pembelianPaketKoinForm(forms.Form):
#     paket_koin = forms.CharField(
#     required=False,
#     widget=forms.TextInput(attrs={'readonly': True, 'value': '100'}),
#     )
#     harga= forms.CharField(
#     required=False,
#     widget=forms.TextInput(attrs={'readonly': True, 'value': '15000'}),
#     )
#     jumlah = forms.IntegerField(label='Jumlah')
#     bayar = forms.CharField(label='Cara Pembayaran')