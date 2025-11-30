from django import forms
from clinica.models import Paciente

class PacienteForm(forms.ModelForm):   
    class Meta:
        model = Paciente   
        fields = '__all__'  # Esto incluirá todos los campos del modelo Paciente

