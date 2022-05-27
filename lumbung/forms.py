from django import forms

BIBIT_CHOICES = [
    ('padi', 'Padi'),
    ('jagung', 'Jagung'),
    ('tebu', 'Tebu'),
    ('wortel', 'Wortel'),
    ('stroberi', 'Stroberi'),
]

class upgradeLumbungForm(forms.Form):
    level_lumbung = forms.IntegerField(label = 'Level Lumbung')
    kapasitas_lumbung = forms.IntegerField(label='Kapasitas Lumbung')
    biaya_upgrade = forms.CharField(
    required=False,
    widget=forms.TextInput(attrs={'readonly': True, 'value': '200'}),)

class produksiTanamanForm(forms.Form):
    bibit_tanaman = forms.CharField(label='Bibit Tanaman', 
    widget=forms.Select(choices=BIBIT_CHOICES))
    # Role = forms.ChoiceField(choices=BIBIT_CHOICES, widget=forms.RadioSelect)
    jumlah = forms.IntegerField(label = 'Jumlah')
    xp = forms.CharField(
    required=False,
    widget=forms.TextInput(attrs={'readonly': True, 'value': '5'}),)
