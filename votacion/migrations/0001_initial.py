# Generated migration for Colombia Vota

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('codigo', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'verbose_name': 'Departamento',
                'verbose_name_plural': 'Departamentos',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('codigo', models.CharField(max_length=10)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='municipios', to='votacion.departamento')),
            ],
            options={
                'verbose_name': 'Municipio',
                'verbose_name_plural': 'Municipios',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='EventoElectoral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('tipo', models.CharField(choices=[('PRESIDENCIA', 'Presidencia de la República'), ('CONGRESO_SENADO', 'Senado de la República'), ('CONGRESO_CAMARA', 'Cámara de Representantes'), ('GOBERNACION', 'Gobernación'), ('ALCALDIA', 'Alcaldía'), ('ASAMBLEA', 'Asamblea Departamental'), ('CONCEJO', 'Concejo Municipal'), ('JAL', 'Junta Administradora Local'), ('CONSULTA', 'Consulta Popular'), ('OTRO', 'Otro')], max_length=30)),
                ('fecha', models.DateField()),
                ('descripcion', models.TextField(blank=True)),
                ('activo', models.BooleanField(default=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Evento Electoral',
                'verbose_name_plural': 'Eventos Electorales',
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='PartidoPolitico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('sigla', models.CharField(max_length=20)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='partidos/')),
                ('color', models.CharField(default='#007bff', help_text='Color HEX del partido', max_length=7)),
            ],
            options={
                'verbose_name': 'Partido Político',
                'verbose_name_plural': 'Partidos Políticos',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='PuestoVotacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('direccion', models.CharField(max_length=300)),
                ('codigo', models.CharField(blank=True, max_length=20)),
                ('municipio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='puestos', to='votacion.municipio')),
            ],
            options={
                'verbose_name': 'Puesto de Votación',
                'verbose_name_plural': 'Puestos de Votación',
                'ordering': ['municipio', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='MesaVotacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.PositiveIntegerField()),
                ('zona', models.CharField(blank=True, help_text='Zona o salón de la mesa', max_length=50)),
                ('puesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mesas', to='votacion.puestovotacion')),
            ],
            options={
                'verbose_name': 'Mesa de Votación',
                'verbose_name_plural': 'Mesas de Votación',
                'ordering': ['puesto', 'numero'],
            },
        ),
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=200)),
                ('apellidos', models.CharField(max_length=200)),
                ('numero_lista', models.PositiveIntegerField(blank=True, help_text='Número en la tarjeta electoral', null=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='candidatos/')),
                ('cedula', models.CharField(blank=True, max_length=20)),
                ('cargo_aspirado', models.CharField(blank=True, max_length=200)),
                ('propuesta', models.TextField(blank=True, help_text='Propuesta o programa de gobierno')),
                ('activo', models.BooleanField(default=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('departamento', models.ForeignKey(blank=True, help_text='Departamento por el que aspira (si aplica)', null=True, on_delete=django.db.models.deletion.SET_NULL, to='votacion.departamento')),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidatos', to='votacion.eventoelectoral')),
                ('municipio', models.ForeignKey(blank=True, help_text='Municipio por el que aspira (si aplica)', null=True, on_delete=django.db.models.deletion.SET_NULL, to='votacion.municipio')),
                ('partido', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='candidatos', to='votacion.partidopolitico')),
            ],
            options={
                'verbose_name': 'Candidato',
                'verbose_name_plural': 'Candidatos',
                'ordering': ['evento', 'apellidos', 'nombres'],
            },
        ),
        migrations.CreateModel(
            name='Votante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=20, unique=True, verbose_name='Número de Cédula')),
                ('nombres', models.CharField(max_length=150, verbose_name='Nombres')),
                ('apellidos', models.CharField(max_length=150, verbose_name='Apellidos')),
                ('email', models.EmailField(blank=True, verbose_name='Correo Electrónico')),
                ('telefono', models.CharField(blank=True, max_length=20, verbose_name='Teléfono')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('departamento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='votacion.departamento', verbose_name='Departamento')),
                ('municipio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='votacion.municipio', verbose_name='Ciudad/Municipio')),
                ('puesto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='votacion.puestovotacion', verbose_name='Puesto de Votación')),
                ('mesa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='votacion.mesavotacion', verbose_name='Mesa')),
                ('registrado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Votante',
                'verbose_name_plural': 'Votantes',
                'ordering': ['apellidos', 'nombres'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='municipio',
            unique_together={('departamento', 'codigo')},
        ),
        migrations.AlterUniqueTogether(
            name='mesavotacion',
            unique_together={('puesto', 'numero')},
        ),
    ]
