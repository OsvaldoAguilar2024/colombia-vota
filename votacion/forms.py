from django import forms
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field, Div, HTML
from .models import (Votante, Candidato, EventoElectoral, PartidoPolitico,
                     Departamento, Municipio, PuestoVotacion, MesaVotacion)


class VotanteForm(forms.ModelForm):
    """Formulario de votante — layout gestionado 100% en el template HTML."""
    class Meta:
        model = Votante
        fields = ['cedula', 'nombres', 'apellidos', 'email', 'telefono',
                  'fecha_nacimiento', 'direccion', 'barrio', 'latitud', 'longitud']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cedula':     forms.TextInput(attrs={'class': 'form-control'}),
            'nombres':    forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos':  forms.TextInput(attrs={'class': 'form-control'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono':   forms.TextInput(attrs={'class': 'form-control'}),
            'direccion':  forms.TextInput(attrs={'class': 'form-control'}),
            'barrio':     forms.TextInput(attrs={'class': 'form-control'}),
            'latitud':    forms.HiddenInput(),
            'longitud':   forms.HiddenInput(),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        # municipio/puesto/mesa vienen como campos POST directos
        from .models import Municipio, PuestoVotacion, MesaVotacion
        data = self.data
        try:
            instance.municipio_id = int(data.get('municipio') or 0) or None
        except (ValueError, TypeError):
            instance.municipio_id = None
        try:
            instance.puesto_id = int(data.get('puesto') or 0) or None
        except (ValueError, TypeError):
            instance.puesto_id = None
        try:
            instance.mesa_id = int(data.get('mesa') or 0) or None
        except (ValueError, TypeError):
            instance.mesa_id = None
        # departamento también viene del POST
        try:
            instance.departamento_id = int(data.get('departamento') or 0) or None
        except (ValueError, TypeError):
            instance.departamento_id = None
        if commit:
            instance.save()
        return instance


class CandidatoForm(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = ['evento', 'partido', 'nombres', 'apellidos', 'numero_lista',
                  'cedula', 'cargo_aspirado', 'departamento', 'municipio', 'foto', 'propuesta', 'activo']
        widgets = {
            'propuesta': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h5 class="text-primary mb-3"><i class="bi bi-person-check"></i> Información del Candidato</h5>'),
            Row(
                Column('evento', css_class='col-md-6 mb-3'),
                Column('partido', css_class='col-md-6 mb-3'),
            ),
            Row(
                Column('nombres', css_class='col-md-4 mb-3'),
                Column('apellidos', css_class='col-md-4 mb-3'),
                Column('cedula', css_class='col-md-4 mb-3'),
            ),
            Row(
                Column('numero_lista', css_class='col-md-4 mb-3'),
                Column('cargo_aspirado', css_class='col-md-4 mb-3'),
                Column('foto', css_class='col-md-4 mb-3'),
            ),
            Row(
                Column('departamento', css_class='col-md-6 mb-3'),
                Column('municipio', css_class='col-md-6 mb-3'),
            ),
            Field('propuesta'),
            Field('activo'),
            Div(
                Submit('submit', 'Guardar Candidato', css_class='btn btn-primary btn-lg me-2'),
                HTML('<a href="{% url \'candidato_lista\' %}" class="btn btn-secondary btn-lg">Cancelar</a>'),
                css_class='d-flex gap-2 mt-3'
            )
        )


class EventoElectoralForm(forms.ModelForm):
    class Meta:
        model = EventoElectoral
        fields = ['nombre', 'tipo', 'fecha', 'descripcion', 'activo']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='col-md-8 mb-3'),
                Column('fecha', css_class='col-md-4 mb-3'),
            ),
            Row(
                Column('tipo', css_class='col-md-6 mb-3'),
                Column('activo', css_class='col-md-6 mb-3 pt-4'),
            ),
            Field('descripcion'),
            Div(
                Submit('submit', 'Guardar Evento', css_class='btn btn-primary btn-lg me-2'),
                HTML('<a href="{% url \'evento_lista\' %}" class="btn btn-secondary btn-lg">Cancelar</a>'),
                css_class='d-flex gap-2 mt-3'
            )
        )


class PartidoForm(forms.ModelForm):
    class Meta:
        model = PartidoPolitico
        fields = ['nombre', 'sigla', 'logo', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='col-md-6 mb-3'),
                Column('sigla', css_class='col-md-3 mb-3'),
                Column('color', css_class='col-md-3 mb-3'),
            ),
            Field('logo'),
            Div(
                Submit('submit', 'Guardar Partido', css_class='btn btn-primary btn-lg me-2'),
                HTML('<a href="{% url \'partido_lista\' %}" class="btn btn-secondary btn-lg">Cancelar</a>'),
                css_class='d-flex gap-2 mt-3'
            )
        )


class PuestoVotacionForm(forms.ModelForm):
    class Meta:
        model = PuestoVotacion
        fields = ['municipio', 'nombre', 'direccion', 'codigo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('municipio', css_class='col-md-6 mb-3'),
                Column('codigo', css_class='col-md-6 mb-3'),
            ),
            Row(
                Column('nombre', css_class='col-md-6 mb-3'),
                Column('direccion', css_class='col-md-6 mb-3'),
            ),
            Div(
                Submit('submit', 'Guardar Puesto', css_class='btn btn-primary btn-lg me-2'),
                HTML('<a href="{% url \'puesto_lista\' %}" class="btn btn-secondary btn-lg">Cancelar</a>'),
                css_class='d-flex gap-2 mt-3'
            )
        )


class MesaVotacionForm(forms.ModelForm):
    class Meta:
        model = MesaVotacion
        fields = ['puesto', 'numero', 'zona']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('puesto', css_class='col-md-6 mb-3'),
                Column('numero', css_class='col-md-3 mb-3'),
                Column('zona', css_class='col-md-3 mb-3'),
            ),
            Div(
                Submit('submit', 'Guardar Mesa', css_class='btn btn-primary btn-lg me-2'),
                HTML('<a href="{% url \'mesa_lista\' %}" class="btn btn-secondary btn-lg">Cancelar</a>'),
                css_class='d-flex gap-2 mt-3'
            )
        )


class VotanteBuscarForm(forms.Form):
    cedula = forms.CharField(max_length=20, label='Número de Cédula', required=False)
    nombre = forms.CharField(max_length=200, label='Nombre o Apellido', required=False)
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(), required=False, empty_label='Todos')
    municipio = forms.ModelChoiceField(queryset=Municipio.objects.all(), required=False, empty_label='Todos')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.method = 'GET'
        self.helper.layout = Layout(
            Row(
                Column('cedula', css_class='col-md-3 mb-3'),
                Column('nombre', css_class='col-md-3 mb-3'),
                Column('departamento', css_class='col-md-3 mb-3'),
                Column('municipio', css_class='col-md-3 mb-3'),
            ),
            Submit('buscar', 'Buscar', css_class='btn btn-primary')
        )
