"""beltexam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from beltexamapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("main", views.main),
    path("", views.index),
    path("travels", views.travels),
    path("register", views.register),
    path("login", views.login),
    path("logout", views.logout),
    path("travels/destination/<id>", views.destination),
    path("travels/add",views.add_dest_page),
    path("adddest", views.adddest),
    path("join/<id>",views.join),
    path("destination/<id>", views.destination)
]
