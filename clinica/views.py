from django.shortcuts import redirect, render
from django.http import HttpResponse
from clinica.models import Doctor, Paciente, Cita
from clinica.forms import PacienteForm
from django.db import transaction
from django.contrib import messages
import subprocess, datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db import connection

def inicio(request):
    return render(request, 'paginas/inicio.html')

def acerca_de(request):
    return render(request, 'paginas/acerca_de.html')

def pacientes(request):
    pacientes = Paciente.objects.all()
    #print(pacientes) Esto imprimirá la lista de pacientes en la consola del servidor
    return render(request, 'pacientes/index.html', {'pacientes': pacientes})

def crear(request):
    formulario = PacienteForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('pacientes')
    return render(request, 'pacientes/crear.html', {'formulario': formulario})

def editar(request, folio_paciente):
    pacientes = Paciente.objects.get(folio_paciente=folio_paciente) #nuevo
    formulario = PacienteForm(request.POST or None, instance=pacientes) #nuevo 
    if formulario.is_valid() and request.method == 'POST': #modificado
        formulario.save()
        return redirect('pacientes')
    return render(request, 'pacientes/editar.html', {'formulario': formulario}) #nuev

def eliminar(request, folio_paciente):
    Paciente.objects.get(folio_paciente=folio_paciente).delete()
    #print(pacientes)
    return redirect('pacientes')

def doctores(request):
    doctores = Doctor.objects.all()
    print(doctores)
    return render(request, 'doctores/index.html', {'doctores': doctores})

def citas(request):
    citas = Cita.objects.all()
    print(citas)
    return render(request, 'citas/index.html', {'citas': citas})

def crear_doctor(request):
    return render(request, 'doctores/crear.html')

@transaction.atomic #transaccion para citas
def crear_cita(request):
    if request.method == "POST":

        doctor = request.POST.get("doctor")
        paciente = request.POST.get("paciente")
        fecha = request.POST.get("fecha")
        hora = request.POST.get("hora")
        costo = request.POST.get("costo", 0)

        existe = Cita.objects.filter(
            cedula_doctor_id=doctor,
            fecha=fecha,
            hora=hora
        ).exists()

        if existe:
            messages.error(request, "El doctor ya tiene una cita en ese horario")
            return redirect("citas")   #agregr la url de citas

        #crear la cita si no existe
        Cita.objects.create(
            cedula_doctor_id=doctor,
            folio_paciente_id=paciente,
            fecha=fecha,
            hora=hora,
            costo=costo
        )

        messages.success(request, "Cita creada exitosamente.")
        return redirect("citas")
    return render(request, "citas/crear.html")


def editar_doctor(request):
    return render(request, 'doctores/editar.html')

def editar_cita(request):
    return render(request, 'citas/editar.html')

@staff_member_required
def respaldos_view(request):
    return render(request, "admin/respaldos.html")

#respaldos
@staff_member_required
def hacer_respaldo(request):
    fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo = f"respaldo_{fecha}.sql"

    cmd = [
        "mysqldump",
        "-u", "root",
        "-p23290796",
        "clinica_db"
    ]

    with open(archivo, "w") as f:
        subprocess.run(cmd, stdout=f)

    return HttpResponse(f"Respaldo generado: {archivo}")


def reporte_ingresos_doctor(request):
    datos = None

    with connection.cursor() as cursor:
        cursor.callproc("ingresos_mes_actual")
        resultados = cursor.fetchall()

    datos = []
    for fila in resultados:
        datos.append({
            "cedula": fila[0],
            "doctor": fila[1],
            "ingresos": fila[2],
            "total_citas": fila[3],
        })

    return render(request, "admin/reportes_doctor.html", {"datos": datos})

#vista para mostras horarios disponibles
def horarios_disponibles(request):
    datos = None
    doctores = None
    # Obtener la lista de doctores
    with connection.cursor() as cursor:
        cursor.execute("SELECT cedula_doctor, nombre_doc FROM clinica_doctor")
        doctores = cursor.fetchall()

    if request.method == "POST":
        cedula = request.POST.get("doctor")

        with connection.cursor() as cursor:
            cursor.callproc("horas_disponibles_doctor", [cedula])
            resultados = cursor.fetchall()

        datos = []
        for fila in resultados:
            datos.append({
                "hora": fila[0],
            })

    return render(request, "admin/horarios.html", {
        "doctores": doctores,
        "datos": datos,
    })