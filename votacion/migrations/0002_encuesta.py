from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('votacion', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('observacion', models.CharField(blank=True, help_text='Nota opcional del encuestador', max_length=300)),
                ('candidato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='encuestas', to='votacion.candidato')),
                ('encuestador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='encuestas_realizadas', to=settings.AUTH_USER_MODEL)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='encuestas', to='votacion.eventoelectoral')),
                ('votante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='encuestas', to='votacion.votante')),
            ],
            options={
                'verbose_name': 'Encuesta',
                'verbose_name_plural': 'Encuestas',
                'ordering': ['-fecha'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='encuesta',
            unique_together={('votante', 'evento')},
        ),
    ]
