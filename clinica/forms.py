from django import forms
from clinica.models import Paciente, Cita

class PacienteForm(forms.ModelForm):   
    class Meta:
        model = Paciente   
        fields = '__all__'  # Esto incluirá todos los campos del modelo Paciente

class CitaAdminForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get("cedula_doctor")
        fecha = cleaned_data.get("fecha")
        hora = cleaned_data.get("hora")

        if doctor and fecha and hora:
            existe = Cita.objects.filter(
                cedula_doctor=doctor,
                fecha=fecha,
                hora=hora
            ).exclude(pk=self.instance.pk).exists()

            if existe:
                raise forms.ValidationError(
                    "El doctor ya tiene una cita registrada en ese horario."
                )
        return cleaned_data
