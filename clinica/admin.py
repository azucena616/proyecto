from django.contrib import admin
from django.http import HttpResponse
import datetime
import subprocess
from django.urls import path
from clinica.models import Doctor, Paciente, Cita

#admin.site.register(Cita)

admin.site.site_header="Clinica Admin"
admin.site.site_title="Clinica Admin Portal"
admin.site.index_title="Bienvenido a la Clinica"

class DoctoresClinica(admin.ModelAdmin): 
    list_display=["cedula_doctor","nombre_doc","especialidad","telefono_doc", "turno", "correo_doc"]
    search_fields = ["cedula_doctor", "nombre_doc"]
    list_filter = ["especialidad"]
admin.site.register(Doctor, DoctoresClinica)
 
class PacientesClinica(admin.ModelAdmin): 
    list_display=["folio_paciente","nombre_paciente","telefono_paciente", "correo_paciente","adeudo"]
    search_fields = ["folio_paciente", "nombre_paciente"]
    list_filter = ["adeudo"]
admin.site.register(Paciente, PacientesClinica)

class CitasClinica(admin.ModelAdmin): 
    list_display=["num_cita","cedula_doctor","folio_paciente","costo","fecha","hora"]
    search_fields = ["num_cita", "folio_paciente__nombre_paciente"]
    list_filter = ["cedula_doctor", "fecha"]
admin.site.register(Cita, CitasClinica)


