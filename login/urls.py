"""TK4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import index, lihatIsiLumbung, login, register, registerPenggunaRole, insertAdmin, profil, logout, insertPengguna

app_name = 'authentication'

urlpatterns = [
    path('', index, name='login'),
    path('Profil/', profil, name='profil'),
    path('LihatIsiLumbung/', lihatIsiLumbung, name='lihatIsiLumbung'),
    path('Logout/', logout,  name='logout'),
    path('Home/', login),
    path('Register/', register),
    path('RegisterRole/', registerPenggunaRole),
    path('insertAdmin/', insertAdmin),
    path('insertPengguna/', insertPengguna),
]