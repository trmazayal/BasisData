from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label = 'Email', max_length=50)
    password = forms.CharField(label = 'Password',  widget=forms.PasswordInput, max_length=128)

class ChoiceRoleForm(forms.Form):
    CHOICES=[
        ('Admin','Admin'),
        ('Pengguna','Pengguna')]
    Role = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

class AdminRoleForm(forms.Form):
    email = forms.CharField(label = 'Email' , max_length=50)
    password = forms.CharField(label = 'Password',  widget=forms.PasswordInput, max_length=128)

class PenggunaRoleForm(forms.Form):
    email = forms.CharField(label = 'Email', max_length=50)
    password = forms.CharField(label = 'Password',  widget=forms.PasswordInput, max_length=128)
    nama_area_pertanian = forms.CharField(label = 'nama_area_pertanian', max_length=50)
