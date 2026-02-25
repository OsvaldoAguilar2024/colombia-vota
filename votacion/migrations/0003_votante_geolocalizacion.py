from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votacion', '0002_encuesta'),
    ]

    operations = [
        migrations.AddField(
            model_name='votante',
            name='direccion',
            field=models.CharField(blank=True, max_length=300, verbose_name='Dirección de residencia'),
        ),
        migrations.AddField(
            model_name='votante',
            name='barrio',
            field=models.CharField(blank=True, max_length=150, verbose_name='Barrio'),
        ),
        migrations.AddField(
            model_name='votante',
            name='latitud',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True, verbose_name='Latitud'),
        ),
        migrations.AddField(
            model_name='votante',
            name='longitud',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True, verbose_name='Longitud'),
        ),
    ]
