from django.forms import Form, formset_factory
from django import forms
from collections import namedtuple
from django.db import connection

class CreateTransaksiPembelianAsetForm(forms.Form):
    jumlah = forms.IntegerField(label='Jumlah', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))