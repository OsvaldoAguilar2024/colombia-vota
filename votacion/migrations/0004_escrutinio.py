from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('votacion', '0003_votante_geolocalizacion'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SesionEscrutinio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('BORRADOR', 'Borrador'), ('CERRADA', 'Cerrada')], default='BORRADOR', max_length=10)),
                ('total_votos_mesa', models.IntegerField(default=0, help_text='Total de votos válidos escrutados en la mesa')),
                ('votos_blancos', models.IntegerField(default=0)),
                ('votos_nulos', models.IntegerField(default=0)),
                ('foto_e14', models.ImageField(blank=True, null=True, upload_to='e14/', verbose_name='Foto del E-14')),
                ('observacion', models.TextField(blank=True)),
                ('fecha_apertura', models.DateTimeField(auto_now_add=True)),
                ('fecha_cierre', models.DateTimeField(blank=True, null=True)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sesiones_escrutinio', to='votacion.eventoelectoral')),
                ('mesa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sesiones_escrutinio', to='votacion.mesavotacion')),
                ('testigo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sesiones_testigo', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sesión de Escrutinio',
                'verbose_name_plural': 'Sesiones de Escrutinio',
                'ordering': ['-fecha_apertura'],
                'unique_together': {('mesa', 'evento')},
            },
        ),
        migrations.CreateModel(
            name='ResultadoMesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votos_reales', models.IntegerField(default=0)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('candidato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultados_mesa', to='votacion.candidato')),
                ('registrado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('sesion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultados', to='votacion.sesionescrutinio')),
            ],
            options={
                'verbose_name': 'Resultado por Mesa',
                'verbose_name_plural': 'Resultados por Mesa',
                'ordering': ['-votos_reales'],
                'unique_together': {('sesion', 'candidato')},
            },
        ),
    ]
