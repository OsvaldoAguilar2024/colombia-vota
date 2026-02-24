from django.db import models
from django.contrib.auth.models import User


# ──────────────────────────────────────────────
# GEOGRAFÍA COLOMBIA
# ──────────────────────────────────────────────

class Departamento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=10, unique=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return self.nombre


class Municipio(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='municipios')
    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=10)

    class Meta:
        ordering = ['nombre']
        unique_together = ('departamento', 'codigo')
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'

    def __str__(self):
        return f'{self.nombre} ({self.departamento.nombre})'


# ──────────────────────────────────────────────
# PUESTOS Y MESAS DE VOTACIÓN
# ──────────────────────────────────────────────

class PuestoVotacion(models.Model):
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='puestos')
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=300)
    codigo = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['municipio', 'nombre']
        verbose_name = 'Puesto de Votación'
        verbose_name_plural = 'Puestos de Votación'

    def __str__(self):
        return f'{self.nombre} - {self.municipio.nombre}'


class MesaVotacion(models.Model):
    puesto = models.ForeignKey(PuestoVotacion, on_delete=models.CASCADE, related_name='mesas')
    numero = models.PositiveIntegerField()
    zona = models.CharField(max_length=50, blank=True, help_text='Zona o salón de la mesa')

    class Meta:
        ordering = ['puesto', 'numero']
        unique_together = ('puesto', 'numero')
        verbose_name = 'Mesa de Votación'
        verbose_name_plural = 'Mesas de Votación'

    def __str__(self):
        return f'Mesa {self.numero} - {self.puesto.nombre}'


# ──────────────────────────────────────────────
# EVENTOS ELECTORALES
# ──────────────────────────────────────────────

TIPO_ELECCION_CHOICES = [
    ('PRESIDENCIA', 'Presidencia de la República'),
    ('CONGRESO_SENADO', 'Senado de la República'),
    ('CONGRESO_CAMARA', 'Cámara de Representantes'),
    ('GOBERNACION', 'Gobernación'),
    ('ALCALDIA', 'Alcaldía'),
    ('ASAMBLEA', 'Asamblea Departamental'),
    ('CONCEJO', 'Concejo Municipal'),
    ('JAL', 'Junta Administradora Local'),
    ('CONSULTA', 'Consulta Popular'),
    ('OTRO', 'Otro'),
]


class EventoElectoral(models.Model):
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=30, choices=TIPO_ELECCION_CHOICES)
    fecha = models.DateField()
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Evento Electoral'
        verbose_name_plural = 'Eventos Electorales'

    def __str__(self):
        return f'{self.nombre} ({self.fecha})'


# ──────────────────────────────────────────────
# PARTIDOS POLÍTICOS
# ──────────────────────────────────────────────

class PartidoPolitico(models.Model):
    nombre = models.CharField(max_length=200)
    sigla = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='partidos/', blank=True, null=True)
    color = models.CharField(max_length=7, default='#007bff', help_text='Color HEX del partido')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Partido Político'
        verbose_name_plural = 'Partidos Políticos'

    def __str__(self):
        return f'{self.sigla} - {self.nombre}'


# ──────────────────────────────────────────────
# CANDIDATOS
# ──────────────────────────────────────────────

class Candidato(models.Model):
    evento = models.ForeignKey(EventoElectoral, on_delete=models.CASCADE, related_name='candidatos')
    partido = models.ForeignKey(PartidoPolitico, on_delete=models.SET_NULL, null=True, blank=True, related_name='candidatos')
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    numero_lista = models.PositiveIntegerField(blank=True, null=True, help_text='Número en la tarjeta electoral')
    foto = models.ImageField(upload_to='candidatos/', blank=True, null=True)
    cedula = models.CharField(max_length=20, blank=True)
    cargo_aspirado = models.CharField(max_length=200, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True,
                                     help_text='Departamento por el que aspira (si aplica)')
    municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True,
                                  help_text='Municipio por el que aspira (si aplica)')
    propuesta = models.TextField(blank=True, help_text='Propuesta o programa de gobierno')
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['evento', 'apellidos', 'nombres']
        verbose_name = 'Candidato'
        verbose_name_plural = 'Candidatos'

    def __str__(self):
        return f'{self.apellidos} {self.nombres} - {self.evento.nombre}'

    @property
    def nombre_completo(self):
        return f'{self.nombres} {self.apellidos}'


# ──────────────────────────────────────────────
# VOTANTES
# ──────────────────────────────────────────────

class Votante(models.Model):
    cedula = models.CharField(max_length=20, unique=True, verbose_name='Número de Cédula')
    nombres = models.CharField(max_length=150, verbose_name='Nombres')
    apellidos = models.CharField(max_length=150, verbose_name='Apellidos')
    email = models.EmailField(blank=True, verbose_name='Correo Electrónico')
    telefono = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name='Fecha de Nacimiento')

    # Puesto de votación asignado
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, verbose_name='Departamento')
    municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, verbose_name='Ciudad/Municipio')
    puesto = models.ForeignKey(PuestoVotacion, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Puesto de Votación')
    mesa = models.ForeignKey(MesaVotacion, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Mesa')

    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['apellidos', 'nombres']
        verbose_name = 'Votante'
        verbose_name_plural = 'Votantes'

    def __str__(self):
        return f'{self.apellidos} {self.nombres} (CC: {self.cedula})'

    @property
    def nombre_completo(self):
        return f'{self.nombres} {self.apellidos}'

# ──────────────────────────────────────────────
# ENCUESTA DE INTENCIÓN DE VOTO
# ──────────────────────────────────────────────

class Encuesta(models.Model):
    """
    Registra la intención de voto de un votante para un evento electoral.
    Un votante solo puede tener UNA encuesta por evento (unique_together).
    """
    votante = models.ForeignKey(Votante, on_delete=models.CASCADE, related_name='encuestas')
    evento = models.ForeignKey(EventoElectoral, on_delete=models.CASCADE, related_name='encuestas')
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, related_name='encuestas')
    encuestador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='encuestas_realizadas')
    fecha = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    observacion = models.CharField(max_length=300, blank=True,
                                   help_text='Nota opcional del encuestador')

    class Meta:
        unique_together = ('votante', 'evento')
        ordering = ['-fecha']
        verbose_name = 'Encuesta'
        verbose_name_plural = 'Encuestas'

    def __str__(self):
        return f'{self.votante.nombre_completo} → {self.candidato.nombre_completo} ({self.evento.nombre})'
