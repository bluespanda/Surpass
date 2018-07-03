"""Surpass URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'db'

urlpatterns = [
    path('', views.index, name="index"),
    path('host/list', views.host_list, name="host_list"),
    url('^host/getdetail/(?P<host_id>[0-9]+)$', views.host_detail, name="host_detail"),
    url('^host/edit/(?P<host_id>[0-9]+)$', views.host_edit_page, name="host_edit_page"),
    url('^host/delete/(?P<host_id>[0-9]+)$', views.host_delete, name="host_delete"),
    path('host/action/', views.host_edit_action, name="host_edit_action"),

    path('database/list', views.database_list, name="database_list"),
    url('^databases', views.databases),
    url('^database/edit/(?P<database_id>[0-9]+)$', views.database_edit_page, name="database_edit_page"),
    url('^database/delete/(?P<database_id>[0-9]+)$', views.database_delete_page, name="database_delete_page"),
    path('database/action/', views.database_edit_action, name="database_edit_action"),















]
