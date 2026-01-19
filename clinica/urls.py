from django.urls import path
from clinica import views 
from django.contrib import admin


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('acerca_de/', views.acerca_de, name='acerca_de'),
    path('pacientes/', views.pacientes, name='pacientes'),
    path('pacientes/crear/', views.crear, name='crear'),
    path('pacientes/editar/', views.editar, name='editar'),
    path('eliminar/<int:folio_paciente>/', views.eliminar, name='eliminar'),
    #linea nueva para editar con folio
    path('pacientes/editar/<int:folio_paciente>/', views.editar, name='editar'),
    path('doctores/', views.doctores, name='doctores'),
    path('citas/', views.citas, name='citas'),
    path('doctores/crear/', views.crear_doctor, name='crear_doctor'),
    path('citas/crear/', views.crear_cita, name='crear_cita'),
    path('doctores/editar/', views.editar_doctor, name='editar_doctor'),
    path('citas/editar/', views.editar_cita, name='editar_cita'),
   # path("admin/", admin.site.urls),            # admin normal
    path("respaldos/", views.respaldos_view, name="respaldos"), #urls para respaldos
    path("hacer_respaldo/", views.hacer_respaldo, name="hacer_respaldo"),
    path('reporte_ingresos/', views.reporte_ingresos_doctor, name='reporte_ingresos'),
    path("horarios/", views.horarios_disponibles, name="horarios"),
]
