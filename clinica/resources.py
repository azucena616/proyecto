from import_export import resources
from .models import Paciente, Doctor, Cita

class PacienteResource(resources.ModelResource):
    class Meta:
        model = Paciente
        fields = (
            'folio_paciente',
            'nombre_paciente',
            'telefono_paciente',
            'correo_paciente',
            'adeudo',
        )
        export_order = fields
        import_id_fields = ['folio_paciente']

class DoctorResource(resources.ModelResource):
    class Meta:
        model = Doctor
        fields = (
            'cedula_doctor',
            'nombre_doc',
            'especialidad',
            'turno',
            'telefono_doc',
            'correo_doc',
        )
        export_order = fields
        import_id_fields = ['cedula_doctor']

class CitaResource(resources.ModelResource):
    class Meta:
        model = Cita
        fields = (
            'num_cita',
            'cedula_doctor_id',
            'folio_paciente_id',
            'costo',
            'fecha',
            'hora',
        )
        export_order = fields
        import_id_fields = ['num_cita']
        

