from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Consulta pública (sin login)
    path('consulta/', views.consulta_publica, name='consulta_publica'),

    # AJAX endpoints
    path('api/municipios/', views.municipios_por_departamento, name='api_municipios'),
    path('api/puestos/', views.puestos_por_municipio, name='api_puestos'),
    path('api/mesas/', views.mesas_por_puesto, name='api_mesas'),

    # Votantes
    path('votantes/', views.votante_lista, name='votante_lista'),
    path('votantes/nuevo/', views.votante_crear, name='votante_crear'),
    path('votantes/<int:pk>/', views.votante_detalle, name='votante_detalle'),
    path('votantes/<int:pk>/editar/', views.votante_editar, name='votante_editar'),
    path('votantes/<int:pk>/eliminar/', views.votante_eliminar, name='votante_eliminar'),

    # Candidatos
    path('candidatos/', views.candidato_lista, name='candidato_lista'),
    path('candidatos/nuevo/', views.candidato_crear, name='candidato_crear'),
    path('candidatos/<int:pk>/', views.candidato_detalle, name='candidato_detalle'),
    path('candidatos/<int:pk>/editar/', views.candidato_editar, name='candidato_editar'),
    path('candidatos/<int:pk>/eliminar/', views.candidato_eliminar, name='candidato_eliminar'),

    # Eventos electorales
    path('eventos/', views.evento_lista, name='evento_lista'),
    path('eventos/nuevo/', views.evento_crear, name='evento_crear'),
    path('eventos/<int:pk>/editar/', views.evento_editar, name='evento_editar'),
    path('eventos/<int:pk>/eliminar/', views.evento_eliminar, name='evento_eliminar'),

    # Partidos políticos
    path('partidos/', views.partido_lista, name='partido_lista'),
    path('partidos/nuevo/', views.partido_crear, name='partido_crear'),
    path('partidos/<int:pk>/editar/', views.partido_editar, name='partido_editar'),
    path('partidos/<int:pk>/eliminar/', views.partido_eliminar, name='partido_eliminar'),

    # Puestos de votación
    path('puestos/', views.puesto_lista, name='puesto_lista'),
    path('puestos/nuevo/', views.puesto_crear, name='puesto_crear'),
    path('puestos/<int:pk>/editar/', views.puesto_editar, name='puesto_editar'),
    path('puestos/<int:pk>/eliminar/', views.puesto_eliminar, name='puesto_eliminar'),

    # Mesas de votación
    path('mesas/', views.mesa_lista, name='mesa_lista'),
    path('mesas/nueva/', views.mesa_crear, name='mesa_crear'),
    path('mesas/<int:pk>/editar/', views.mesa_editar, name='mesa_editar'),
    path('mesas/<int:pk>/eliminar/', views.mesa_eliminar, name='mesa_eliminar'),

    # ── MÓDULO ENCUESTADOR ──────────────────────────────────────
    path('encuestador/', views.encuestador_inicio, name='encuestador_inicio'),
    path('encuestador/votante/<int:pk>/eventos/', views.encuestador_elegir_evento, name='encuestador_elegir_evento'),
    path('encuestador/votante/<int:votante_pk>/evento/<int:evento_pk>/votar/', views.encuestador_registrar_voto, name='encuestador_registrar_voto'),
    path('encuestador/estadisticas/', views.encuestador_estadisticas, name='encuestador_estadisticas'),
]
