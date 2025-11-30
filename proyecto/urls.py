"""
URL configuration for proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

# Importamos directamente las urlpatterns de la app 'clinica' y las anexamos
try:
    # import local module; si falla se lanzará ImportError
    from clinica import urls as clinica_urls
except Exception:
    clinica_urls = None

urlpatterns = [
    path('admin/', admin.site.urls), 
]

if clinica_urls is not None and hasattr(clinica_urls, 'urlpatterns'):
    # Añadimos las rutas de la app al root (equivalente a include('clinica.urls') para la raíz)
    urlpatterns += clinica_urls.urlpatterns
