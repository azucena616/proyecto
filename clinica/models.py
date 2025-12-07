from django.db import models
from django.core.validators import RegexValidator, EmailValidator

class Doctor(models.Model):
    cedula_doctor = models.CharField("Cédula",
        max_length=10,
        primary_key=True,
        validators=[RegexValidator(regex='^[0-9]+$', message='La cédula debe contener solo números')]
    )
    nombre_doc = models.CharField("Doctor",
        max_length=40,
        validators=[RegexValidator(regex='^[^0-9]+$', message='El nombre no debe contener números')],
        blank=False,
        null=False
    )
    especialidad = models.CharField( max_length=20, blank=True, null=True)

    turno = models.CharField(
        max_length=1,
        choices=[('M', 'Matutino'), ('V', 'Vespertino'), ('m', 'Matutino'), ('v', 'Vespertino')],
        blank=False,
        null=False
    )
    telefono_doc = models.CharField("Teléfono",
        max_length=10,
        validators=[RegexValidator(regex='^[0-9]{10}$', message='El teléfono debe tener exactamente 10 dígitos numéricos')],
        blank=False,
        null=False
    )
    correo_doc = models.CharField("Correo",
        max_length=30,
        validators=[EmailValidator(message='Ingresa un correo válido')],
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctores"


    def __str__(self):
        #return f"{self.nombre_doc}"
        return f"{self.cedula_doctor} - {self.nombre_doc}"

class Paciente(models.Model):
    folio_paciente = models.AutoField("Fólio", primary_key=True)

    nombre_paciente = models.CharField("Nombre del paciente",
        max_length=40,
        validators=[RegexValidator(regex='^[^0-9]+$', message='El nombre no debe contener números')],
        blank=False,  
        null=False    
    )

    telefono_paciente = models.CharField("Teléfono",
        max_length=10,
        validators=[RegexValidator(regex='^[0-9]{10}$', message='El teléfono debe tener exactamente 10 dígitos numéricos')],
        blank=False,
        null=False
    )

    correo_paciente = models.CharField("Correo",
        max_length=30,
        validators=[EmailValidator(message='Ingresa un correo válido')],
        blank=True,
        null=True
    )

    adeudo = models.DecimalField( 
        max_digits=8,
        decimal_places=2,
        default=0.00,
        blank=True,      
        null=True
    )

    def __str__(self):
         return f"{self.folio_paciente} - {self.nombre_paciente}"
    
class Cita(models.Model):
    num_cita = models.AutoField(primary_key=True)
    cedula_doctor = models.ForeignKey(Doctor,
     on_delete=models.CASCADE,
     verbose_name="Doctor")
    folio_paciente = models.ForeignKey(Paciente, 
    on_delete=models.CASCADE,
    verbose_name="Paciente")
    costo = models.DecimalField( 
        max_digits=8,
        decimal_places=2,
        default=0.00,
        blank=True,      
        null=True
    )

    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"Cita {self.num_cita} - Doctor: {self.cedula_doctor.nombre_doc} - Paciente: {self.folio_paciente.nombre_paciente}"

class HistorialCitas(models.Model):
    id = models.AutoField(primary_key=True)
    cedula_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Doctor")
    folio_paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, verbose_name="Paciente")
    fecha = models.DateField()
    hora = models.TimeField()
    accion = models.CharField(max_length=50)  # Ejemplo: "Cita creada", "Cita modificada", "Cita cancelada"
    created_at = models.DateTimeField(auto_now_add=True)  # Guarda automáticamente cuándo se registró

    class Meta:
        verbose_name = "Historial de cita"
        verbose_name_plural = "Historial de citas"

    def __str__(self):
        return f"{self.accion} - Doctor: {self.cedula_doctor.nombre_doc} - Paciente: {self.folio_paciente.nombre_paciente} - {self.fecha} {self.hora}"

