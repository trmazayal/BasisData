from django import forms

class upgradeLumbungForm(forms.Form):
    level_lumbung = forms.CharField(label='Level Lumbung', required=True, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    kapasitas_lumbung = forms.CharField(label='Kapasitas Lumbung', required=True, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    biaya_upgrade  = forms.CharField(label='Biaya Upgrade ', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))

class produksiTanamanForm(forms.Form):
    jumlah = forms.CharField(label='Jumlah', required=True, widget=forms.TextInput(attrs={'placeholder':'*Required'}))
    xp = forms.CharField(label='XP', required=True, widget=forms.TextInput(attrs={'readonly':'readonly'}))