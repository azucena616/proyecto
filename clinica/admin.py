from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import transaction
import datetime
import subprocess
from django.urls import path
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import CitaAdminForm
from clinica.models import Doctor, Paciente, Cita, HistorialCitas

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
    form = CitaAdminForm 
    list_display=["num_cita","cedula_doctor","folio_paciente","costo","fecha","hora"]
    search_fields = ["num_cita", "folio_paciente__nombre_paciente"]
    list_filter = ["cedula_doctor", "fecha"]
    #se añadio una transaccion para evitar citas duplicadas
    @transaction.atomic
    def save_model(self, request, obj, form, change):
        # Guarda la cita dentro de la transacción
        super().save_model(request, obj, form, change)
        messages.success(request, "Cita registrada correctamente.") 
admin.site.register(Cita, CitasClinica)


class HistorialCitasAdmin(admin.ModelAdmin):
    list_display = ["id", "cedula_doctor", "folio_paciente", "fecha", "hora", "accion", "created_at"]
    list_filter = ["cedula_doctor", "fecha", "accion"]
    search_fields = ["cedula_doctor__nombre_doc", "folio_paciente__nombre_paciente", "accion"]
    readonly_fields = ["id", "created_at"]  # No editable, ya que se llenan automáticamente
admin.site.register(HistorialCitas, HistorialCitasAdmin)





