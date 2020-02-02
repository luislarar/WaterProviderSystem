"""waterprovidersystem URL Configuration

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
from django.urls import re_path, path
from django.conf.urls import url, include
from django.contrib import admin

import coreapp.template_views as templates

import coreapp.urls as urls_core

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rest/', include(urls_core)),
    url(r'^$', templates.Index.as_view(), name='dashboard'),
    path('clientes/', templates.ClienteList.as_view(), name='clientes'),
    path('clientes/new', templates.ClienteCreate.as_view(), name='crear cliente'),
    re_path(r'^clientes/(?P<id>[\d]+)$',templates.ClienteEdit.as_view(), name='editar cliente'),
    path('pagos/', templates.PagoList, name='pagos'),
    #re_path(r'^pagos/(?P<id>[\d]+)$',templates.ClientList, name='detalle pago'),
]

#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#urlpatterns += staticfiles_urlpatterns()

