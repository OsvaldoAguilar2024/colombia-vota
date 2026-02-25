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
                  'fecha_nacimiento', 'departamento', 'municipio', 'puesto', 'mesa',
                  'direccion', 'barrio', 'latitud', 'longitud']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'departamento': forms.Select(attrs={'id': 'id_departamento', 'onchange': 'cargarMunicipios(this.value)'}),
            'municipio': forms.Select(attrs={'id': 'id_municipio', 'onchange': 'cargarPuestos(this.value)'}),
            'puesto': forms.Select(attrs={'id': 'id_puesto', 'onchange': 'cargarMesas(this.value)'}),
            'mesa': forms.Select(attrs={'id': 'id_mesa'}),
            'latitud':  forms.HiddenInput(attrs={'id': 'id_latitud'}),
            'longitud': forms.HiddenInput(attrs={'id': 'id_longitud'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Al CREAR (GET sin datos): selects vacíos, el AJAX los llena
        # Al GUARDAR (POST): se llenan con el valor enviado para pasar validación
        # Al EDITAR: se llenan con los datos del objeto existente

        # ── Municipio ──────────────────────────────────────────────
        if 'municipio' in self.data and self.data.get('municipio'):
            try:
                mun_id = int(self.data['municipio'])
                self.fields['municipio'].queryset = Municipio.objects.filter(pk=mun_id)
            except (ValueError, TypeError):
                self.fields['municipio'].queryset = Municipio.objects.none()
        elif self.instance.pk and self.instance.municipio:
            self.fields['municipio'].queryset = Municipio.objects.filter(pk=self.instance.municipio.pk)
        else:
            self.fields['municipio'].queryset = Municipio.objects.none()

        # ── Puesto ─────────────────────────────────────────────────
        if 'puesto' in self.data and self.data.get('puesto'):
            try:
                puesto_id = int(self.data['puesto'])
                self.fields['puesto'].queryset = PuestoVotacion.objects.filter(pk=puesto_id)
            except (ValueError, TypeError):
                self.fields['puesto'].queryset = PuestoVotacion.objects.none()
        elif self.instance.pk and self.instance.puesto:
            self.fields['puesto'].queryset = PuestoVotacion.objects.filter(pk=self.instance.puesto.pk)
        else:
            self.fields['puesto'].queryset = PuestoVotacion.objects.none()

        # ── Mesa ───────────────────────────────────────────────────
        if 'mesa' in self.data and self.data.get('mesa'):
            try:
                mesa_id = int(self.data['mesa'])
                self.fields['mesa'].queryset = MesaVotacion.objects.filter(pk=mesa_id)
            except (ValueError, TypeError):
                self.fields['mesa'].queryset = MesaVotacion.objects.none()
        elif self.instance.pk and self.instance.mesa:
            self.fields['mesa'].queryset = MesaVotacion.objects.filter(pk=self.instance.mesa.pk)
        else:
            self.fields['mesa'].queryset = MesaVotacion.objects.none()

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
            HTML('<hr><h5 class="text-primary mb-3"><i class="bi bi-geo-alt"></i> Lugar de Votación</h5>'),
            Row(
                Column('departamento', css_class='col-md-6 mb-3'),
                Column('municipio', css_class='col-md-6 mb-3'),
            ),
            Row(
                Column('puesto', css_class='col-md-6 mb-3'),
                Column('mesa', css_class='col-md-6 mb-3'),
            ),
            HTML('<hr><h5 class="text-success mb-3"><i class="bi bi-pin-map"></i> Dirección de Residencia</h5>'),
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
