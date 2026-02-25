from django import forms
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field, Div, HTML
from .models import (Votante, Candidato, EventoElectoral, PartidoPolitico,
                     Departamento, Municipio, PuestoVotacion, MesaVotacion)


class VotanteForm(forms.ModelForm):
    class Meta:
        model = Votante
        fields = ['cedula', 'nombres', 'apellidos', 'email', 'telefono',
                  'fecha_nacimiento', 'departamento',
                  'direccion', 'barrio', 'latitud', 'longitud']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'departamento': forms.Select(attrs={'id': 'id_departamento'}),
            'latitud':  forms.HiddenInput(attrs={'id': 'id_latitud'}),
            'longitud': forms.HiddenInput(attrs={'id': 'id_longitud'}),
        }

    # Campos separados para municipio/puesto/mesa (manejados por JS en el template)
    municipio = forms.IntegerField(required=False, widget=forms.HiddenInput(attrs={'id': 'val_municipio'}))
    puesto    = forms.IntegerField(required=False, widget=forms.HiddenInput(attrs={'id': 'val_puesto'}))
    mesa      = forms.IntegerField(required=False, widget=forms.HiddenInput(attrs={'id': 'val_mesa'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-poblar valores ocultos al editar
        if self.instance.pk:
            self.initial['municipio'] = self.instance.municipio_id
            self.initial['puesto']    = self.instance.puesto_id
            self.initial['mesa']      = self.instance.mesa_id

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h5 class="text-primary mb-3"><i class="bi bi-person-badge"></i> Datos Personales</h5>'),
            Row(
                Column('cedula', css_class='col-md-4 mb-3'),
                Column('nombres', css_class='col-md-4 mb-3'),
                Column('apellidos', css_class='col-md-4 mb-3'),
            ),
            Row(
                Column('email', css_class='col-md-4 mb-3'),
                Column('telefono', css_class='col-md-4 mb-3'),
                Column('fecha_nacimiento', css_class='col-md-4 mb-3'),
            ),
            # Lugar de votación se renderiza manualmente en el template (ver bloque_lugar_votacion)
            HTML('''
            <hr>
            <h5 class="text-primary mb-3"><i class="bi bi-geo-alt"></i> Lugar de Votación</h5>
            <div id="bloque_lugar_votacion"></div>
            '''),
            Field('municipio'),
            Field('puesto'),
            Field('mesa'),
            HTML('''<hr><h5 class="text-success mb-3"><i class="bi bi-pin-map"></i> Dirección de Residencia</h5>'''),
            Row(
                Column('direccion', css_class='col-md-8 mb-3'),
                Column('barrio', css_class='col-md-4 mb-3'),
            ),
            HTML('''<div id="bloque-mapa" class="mb-4">
              <label class="form-label fw-semibold">
                <i class="bi bi-map text-success me-1"></i>
                Ubicación en el mapa <small class="text-muted fw-normal">(clic en el mapa o usa el GPS)</small>
              </label>
              <div class="d-flex gap-2 mb-2 flex-wrap">
                <button type="button" class="btn btn-outline-success btn-sm" onclick="usarMiUbicacion()">
                  <i class="bi bi-crosshair2 me-1"></i>Detectar mi ubicación
                </button>
                <button type="button" class="btn btn-outline-secondary btn-sm" onclick="buscarDireccion()">
                  <i class="bi bi-search me-1"></i>Buscar dirección en mapa
                </button>
                <span id="gps-status" class="text-muted small align-self-center"></span>
              </div>
              <div id="mapa-votante" style="height:340px;border-radius:12px;border:1px solid #dee2e6;"></div>
              <p class="text-muted mt-1 mb-0" style="font-size:.75rem;">
                <i class="bi bi-info-circle me-1"></i>Haz clic en el mapa para colocar el marcador en la dirección exacta del votante.
              </p>
            </div>'''),
            Field('latitud'),
            Field('longitud'),
            Div(
                Submit('submit', 'Guardar Votante', css_class='btn btn-primary btn-lg me-2'),
                HTML('<a href="{% url \'votante_lista\' %}" class="btn btn-secondary btn-lg">Cancelar</a>'),
                css_class='d-flex gap-2'
            )
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Asignar municipio/puesto/mesa desde los campos hidden
        mun_id    = self.cleaned_data.get('municipio')
        puesto_id = self.cleaned_data.get('puesto')
        mesa_id   = self.cleaned_data.get('mesa')
        instance.municipio_id = mun_id    if mun_id    else None
        instance.puesto_id    = puesto_id if puesto_id else None
        instance.mesa_id      = mesa_id   if mesa_id   else None
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
