from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (Departamento, Municipio, PuestoVotacion, MesaVotacion,
                     EventoElectoral, PartidoPolitico, Candidato, Votante, Encuesta)


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo']
    search_fields = ['nombre', 'codigo']


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'departamento', 'codigo']
    list_filter = ['departamento']
    search_fields = ['nombre', 'codigo']


@admin.register(PuestoVotacion)
class PuestoVotacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'municipio', 'direccion', 'codigo']
    list_filter = ['municipio__departamento', 'municipio']
    search_fields = ['nombre', 'codigo', 'direccion']


@admin.register(MesaVotacion)
class MesaVotacionAdmin(admin.ModelAdmin):
    list_display = ['numero', 'puesto', 'zona']
    list_filter = ['puesto__municipio__departamento']
    search_fields = ['puesto__nombre']


@admin.register(EventoElectoral)
class EventoElectoralAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'fecha', 'activo']
    list_filter = ['tipo', 'activo']
    search_fields = ['nombre']


@admin.register(PartidoPolitico)
class PartidoPoliticoAdmin(admin.ModelAdmin):
    list_display = ['sigla', 'nombre', 'color']
    search_fields = ['nombre', 'sigla']


@admin.register(Candidato)
class CandidatoAdmin(ImportExportModelAdmin):
    list_display = ['apellidos', 'nombres', 'evento', 'partido', 'cargo_aspirado', 'activo']
    list_filter = ['evento', 'partido', 'activo', 'departamento']
    search_fields = ['nombres', 'apellidos', 'cedula']


@admin.register(Votante)
class VotanteAdmin(ImportExportModelAdmin):
    list_display = ['cedula', 'apellidos', 'nombres', 'departamento', 'municipio', 'puesto', 'mesa']
    list_filter = ['departamento', 'municipio']
    search_fields = ['cedula', 'nombres', 'apellidos']
    readonly_fields = ['creado_en', 'actualizado_en']


@admin.register(Encuesta)
class EncuestaAdmin(admin.ModelAdmin):
    list_display = ['votante', 'evento', 'candidato', 'encuestador', 'fecha']
    list_filter = ['evento', 'candidato__partido', 'encuestador']
    search_fields = ['votante__cedula', 'votante__nombres', 'votante__apellidos']
    readonly_fields = ['fecha', 'actualizado_en']
