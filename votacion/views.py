from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import (Votante, Candidato, EventoElectoral, PartidoPolitico,
                     Departamento, Municipio, PuestoVotacion, MesaVotacion, Encuesta)
from .forms import (VotanteForm, CandidatoForm, EventoElectoralForm,
                    PartidoForm, PuestoVotacionForm, MesaVotacionForm, VotanteBuscarForm)


# ─── DASHBOARD ───────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    context = {
        'total_votantes': Votante.objects.count(),
        'total_candidatos': Candidato.objects.filter(activo=True).count(),
        'total_eventos': EventoElectoral.objects.filter(activo=True).count(),
        'total_puestos': PuestoVotacion.objects.count(),
        'total_encuestas': Encuesta.objects.count(),
        'eventos_activos': EventoElectoral.objects.filter(activo=True).order_by('-fecha')[:5],
        'ultimos_votantes': Votante.objects.order_by('-creado_en')[:5],
    }
    return render(request, 'votacion/dashboard.html', context)


# ─── AJAX: Carga encadenada ───────────────────────────────────────────────────

def municipios_por_departamento(request):
    dep_id = request.GET.get('departamento_id')
    municipios = list(Municipio.objects.filter(departamento_id=dep_id).values('id', 'nombre').order_by('nombre'))
    return JsonResponse({'municipios': municipios})


def puestos_por_municipio(request):
    mun_id = request.GET.get('municipio_id')
    puestos = list(PuestoVotacion.objects.filter(municipio_id=mun_id).values('id', 'nombre', 'direccion').order_by('nombre'))
    return JsonResponse({'puestos': puestos})


def mesas_por_puesto(request):
    puesto_id = request.GET.get('puesto_id')
    mesas = list(MesaVotacion.objects.filter(puesto_id=puesto_id).values('id', 'numero', 'zona').order_by('numero'))
    return JsonResponse({'mesas': mesas})


# ─── VOTANTES ────────────────────────────────────────────────────────────────

@login_required
def votante_lista(request):
    form = VotanteBuscarForm(request.GET)
    votantes = Votante.objects.select_related('departamento', 'municipio', 'puesto', 'mesa').all()

    if form.is_valid():
        cedula = form.cleaned_data.get('cedula')
        nombre = form.cleaned_data.get('nombre')
        departamento = form.cleaned_data.get('departamento')
        municipio = form.cleaned_data.get('municipio')

        if cedula:
            votantes = votantes.filter(cedula__icontains=cedula)
        if nombre:
            votantes = votantes.filter(Q(nombres__icontains=nombre) | Q(apellidos__icontains=nombre))
        if departamento:
            votantes = votantes.filter(departamento=departamento)
        if municipio:
            votantes = votantes.filter(municipio=municipio)

    paginator = Paginator(votantes, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'votacion/votante_lista.html', {
        'page_obj': page_obj,
        'form': form,
        'total': votantes.count(),
    })


@login_required
def votante_crear(request):
    from_encuestador = request.GET.get('from') == 'encuestador'
    cedula_inicial = request.GET.get('cedula', '')

    if request.method == 'POST':
        form = VotanteForm(request.POST)
        if form.is_valid():
            votante = form.save(commit=False)
            votante.registrado_por = request.user
            votante.save()
            messages.success(request, f'✅ Votante {votante.nombre_completo} registrado exitosamente.')
            if from_encuestador or request.POST.get('from_encuestador'):
                # Volver al encuestador para continuar con la encuesta
                return redirect('encuestador_elegir_evento', pk=votante.pk)
            return redirect('votante_lista')
    else:
        initial = {}
        if cedula_inicial:
            initial['cedula'] = cedula_inicial
        form = VotanteForm(initial=initial)

    return render(request, 'votacion/votante_form.html', {
        'form': form,
        'titulo': 'Registrar Votante',
        'from_encuestador': from_encuestador,
    })


@login_required
def votante_editar(request, pk):
    votante = get_object_or_404(Votante, pk=pk)
    if request.method == 'POST':
        form = VotanteForm(request.POST, instance=votante)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Datos de {votante.nombre_completo} actualizados.')
            return redirect('votante_lista')
    else:
        form = VotanteForm(instance=votante)
    return render(request, 'votacion/votante_form.html', {'form': form, 'titulo': 'Editar Votante', 'votante': votante})


@login_required
def votante_detalle(request, pk):
    votante = get_object_or_404(Votante, pk=pk)
    return render(request, 'votacion/votante_detalle.html', {'votante': votante})


@login_required
def votante_eliminar(request, pk):
    votante = get_object_or_404(Votante, pk=pk)
    if request.method == 'POST':
        nombre = votante.nombre_completo
        votante.delete()
        messages.success(request, f'🗑️ Votante {nombre} eliminado.')
        return redirect('votante_lista')
    return render(request, 'votacion/confirmar_eliminar.html', {
        'objeto': votante,
        'tipo': 'votante',
        'url_cancelar': 'votante_lista',
    })


# ─── CANDIDATOS ──────────────────────────────────────────────────────────────

@login_required
def candidato_lista(request):
    evento_id = request.GET.get('evento')
    candidatos = Candidato.objects.select_related('evento', 'partido', 'departamento', 'municipio').all()

    eventos = EventoElectoral.objects.filter(activo=True)
    if evento_id:
        candidatos = candidatos.filter(evento_id=evento_id)

    paginator = Paginator(candidatos, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'votacion/candidato_lista.html', {
        'page_obj': page_obj,
        'eventos': eventos,
        'evento_seleccionado': evento_id,
    })


@login_required
def candidato_crear(request):
    if request.method == 'POST':
        form = CandidatoForm(request.POST, request.FILES)
        if form.is_valid():
            candidato = form.save()
            messages.success(request, f'✅ Candidato {candidato.nombre_completo} registrado.')
            return redirect('candidato_lista')
    else:
        form = CandidatoForm()
    return render(request, 'votacion/candidato_form.html', {'form': form, 'titulo': 'Registrar Candidato'})


@login_required
def candidato_editar(request, pk):
    candidato = get_object_or_404(Candidato, pk=pk)
    if request.method == 'POST':
        form = CandidatoForm(request.POST, request.FILES, instance=candidato)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Candidato actualizado.')
            return redirect('candidato_lista')
    else:
        form = CandidatoForm(instance=candidato)
    return render(request, 'votacion/candidato_form.html', {'form': form, 'titulo': 'Editar Candidato', 'candidato': candidato})


@login_required
def candidato_detalle(request, pk):
    candidato = get_object_or_404(Candidato, pk=pk)
    return render(request, 'votacion/candidato_detalle.html', {'candidato': candidato})


@login_required
def candidato_eliminar(request, pk):
    candidato = get_object_or_404(Candidato, pk=pk)
    if request.method == 'POST':
        nombre = candidato.nombre_completo
        candidato.delete()
        messages.success(request, f'🗑️ Candidato {nombre} eliminado.')
        return redirect('candidato_lista')
    return render(request, 'votacion/confirmar_eliminar.html', {
        'objeto': candidato,
        'tipo': 'candidato',
        'url_cancelar': 'candidato_lista',
    })


# ─── EVENTOS ELECTORALES ─────────────────────────────────────────────────────

@login_required
def evento_lista(request):
    eventos = EventoElectoral.objects.annotate(num_candidatos=Count('candidatos')).order_by('-fecha')
    return render(request, 'votacion/evento_lista.html', {'eventos': eventos})


@login_required
def evento_crear(request):
    if request.method == 'POST':
        form = EventoElectoralForm(request.POST)
        if form.is_valid():
            evento = form.save()
            messages.success(request, f'✅ Evento {evento.nombre} creado.')
            return redirect('evento_lista')
    else:
        form = EventoElectoralForm()
    return render(request, 'votacion/evento_form.html', {'form': form, 'titulo': 'Crear Evento Electoral'})


@login_required
def evento_editar(request, pk):
    evento = get_object_or_404(EventoElectoral, pk=pk)
    if request.method == 'POST':
        form = EventoElectoralForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Evento actualizado.')
            return redirect('evento_lista')
    else:
        form = EventoElectoralForm(instance=evento)
    return render(request, 'votacion/evento_form.html', {'form': form, 'titulo': 'Editar Evento', 'evento': evento})


@login_required
def evento_eliminar(request, pk):
    evento = get_object_or_404(EventoElectoral, pk=pk)
    if request.method == 'POST':
        nombre = evento.nombre
        evento.delete()
        messages.success(request, f'🗑️ Evento {nombre} eliminado.')
        return redirect('evento_lista')
    return render(request, 'votacion/confirmar_eliminar.html', {
        'objeto': evento,
        'tipo': 'evento electoral',
        'url_cancelar': 'evento_lista',
    })


# ─── PARTIDOS POLÍTICOS ───────────────────────────────────────────────────────

@login_required
def partido_lista(request):
    partidos = PartidoPolitico.objects.annotate(num_candidatos=Count('candidatos')).order_by('nombre')
    return render(request, 'votacion/partido_lista.html', {'partidos': partidos})


@login_required
def partido_crear(request):
    if request.method == 'POST':
        form = PartidoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Partido creado.')
            return redirect('partido_lista')
    else:
        form = PartidoForm()
    return render(request, 'votacion/partido_form.html', {'form': form, 'titulo': 'Crear Partido Político'})


@login_required
def partido_editar(request, pk):
    partido = get_object_or_404(PartidoPolitico, pk=pk)
    if request.method == 'POST':
        form = PartidoForm(request.POST, request.FILES, instance=partido)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Partido actualizado.')
            return redirect('partido_lista')
    else:
        form = PartidoForm(instance=partido)
    return render(request, 'votacion/partido_form.html', {'form': form, 'titulo': 'Editar Partido', 'partido': partido})


@login_required
def partido_eliminar(request, pk):
    partido = get_object_or_404(PartidoPolitico, pk=pk)
    if request.method == 'POST':
        partido.delete()
        messages.success(request, '🗑️ Partido eliminado.')
        return redirect('partido_lista')
    return render(request, 'votacion/confirmar_eliminar.html', {
        'objeto': partido,
        'tipo': 'partido político',
        'url_cancelar': 'partido_lista',
    })


# ─── PUESTOS DE VOTACIÓN ──────────────────────────────────────────────────────

@login_required
def puesto_lista(request):
    puestos = PuestoVotacion.objects.select_related('municipio__departamento').annotate(
        num_mesas=Count('mesas')).order_by('municipio__departamento__nombre', 'municipio__nombre', 'nombre')
    return render(request, 'votacion/puesto_lista.html', {'puestos': puestos})


@login_required
def puesto_crear(request):
    if request.method == 'POST':
        form = PuestoVotacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Puesto de votación creado.')
            return redirect('puesto_lista')
    else:
        form = PuestoVotacionForm()
    return render(request, 'votacion/puesto_form.html', {'form': form, 'titulo': 'Crear Puesto de Votación'})


@login_required
def puesto_editar(request, pk):
    puesto = get_object_or_404(PuestoVotacion, pk=pk)
    if request.method == 'POST':
        form = PuestoVotacionForm(request.POST, instance=puesto)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Puesto actualizado.')
            return redirect('puesto_lista')
    else:
        form = PuestoVotacionForm(instance=puesto)
    return render(request, 'votacion/puesto_form.html', {'form': form, 'titulo': 'Editar Puesto', 'puesto': puesto})


@login_required
def puesto_eliminar(request, pk):
    puesto = get_object_or_404(PuestoVotacion, pk=pk)
    if request.method == 'POST':
        puesto.delete()
        messages.success(request, '🗑️ Puesto eliminado.')
        return redirect('puesto_lista')
    return render(request, 'votacion/confirmar_eliminar.html', {
        'objeto': puesto,
        'tipo': 'puesto de votación',
        'url_cancelar': 'puesto_lista',
    })


# ─── MESAS ────────────────────────────────────────────────────────────────────

@login_required
def mesa_lista(request):
    mesas = MesaVotacion.objects.select_related('puesto__municipio__departamento').order_by(
        'puesto__municipio__nombre', 'puesto__nombre', 'numero')
    return render(request, 'votacion/mesa_lista.html', {'mesas': mesas})


@login_required
def mesa_crear(request):
    if request.method == 'POST':
        form = MesaVotacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Mesa creada.')
            return redirect('mesa_lista')
    else:
        form = MesaVotacionForm()
    return render(request, 'votacion/mesa_form.html', {'form': form, 'titulo': 'Crear Mesa de Votación'})


@login_required
def mesa_editar(request, pk):
    mesa = get_object_or_404(MesaVotacion, pk=pk)
    if request.method == 'POST':
        form = MesaVotacionForm(request.POST, instance=mesa)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Mesa actualizada.')
            return redirect('mesa_lista')
    else:
        form = MesaVotacionForm(instance=mesa)
    return render(request, 'votacion/mesa_form.html', {'form': form, 'titulo': 'Editar Mesa', 'mesa': mesa})


@login_required
def mesa_eliminar(request, pk):
    mesa = get_object_or_404(MesaVotacion, pk=pk)
    if request.method == 'POST':
        mesa.delete()
        messages.success(request, '🗑️ Mesa eliminada.')
        return redirect('mesa_lista')
    return render(request, 'votacion/confirmar_eliminar.html', {
        'objeto': mesa,
        'tipo': 'mesa de votación',
        'url_cancelar': 'mesa_lista',
    })


# ─── CONSULTA PÚBLICA ─────────────────────────────────────────────────────────

def consulta_publica(request):
    """Vista pública para que ciudadanos consulten su puesto de votación."""
    resultado = None
    error = None
    if request.method == 'POST':
        cedula = request.POST.get('cedula', '').strip()
        if cedula:
            try:
                resultado = Votante.objects.select_related(
                    'departamento', 'municipio', 'puesto', 'mesa'
                ).get(cedula=cedula)
            except Votante.DoesNotExist:
                error = f'No se encontró ningún registro con la cédula {cedula}.'
        else:
            error = 'Por favor ingrese su número de cédula.'
    return render(request, 'votacion/consulta_publica.html', {'resultado': resultado, 'error': error})


# ═══════════════════════════════════════════════════════════════
# MÓDULO ENCUESTADOR
# ═══════════════════════════════════════════════════════════════

@login_required
def encuestador_inicio(request):
    """Pantalla principal del encuestador: busca al votante por cédula."""
    error = None
    cedula = ''

    if request.method == 'POST':
        cedula = request.POST.get('cedula', '').strip()
        if not cedula:
            error = 'Por favor ingresa un número de cédula.'
        else:
            try:
                votante = Votante.objects.get(cedula=cedula)
                # Votante encontrado → elegir evento
                return redirect('encuestador_elegir_evento', pk=votante.pk)
            except Votante.DoesNotExist:
                # No existe → redirigir al registro con cédula pre-llenada
                return redirect(f'/votantes/nuevo/?cedula={cedula}&from=encuestador')

    # Estadística rápida para motivar al encuestador
    mis_encuestas_hoy = 0
    from django.utils import timezone
    hoy = timezone.now().date()
    mis_encuestas_hoy = Encuesta.objects.filter(
        encuestador=request.user,
        fecha__date=hoy
    ).count()

    return render(request, 'votacion/encuestador/inicio.html', {
        'error': error,
        'cedula': cedula,
        'mis_encuestas_hoy': mis_encuestas_hoy,
        'total_encuestas': Encuesta.objects.count(),
    })


@login_required
def encuestador_elegir_evento(request, pk):
    """Muestra los eventos activos para que el encuestador elija cuál encuestar."""
    votante = get_object_or_404(Votante, pk=pk)
    eventos_qs = EventoElectoral.objects.filter(activo=True).annotate(
        num_candidatos=Count('candidatos')
    ).filter(num_candidatos__gt=0)

    # Dict evento_id -> encuesta
    encuestas_dict = {
        e.evento_id: e
        for e in Encuesta.objects.filter(votante=votante).select_related('candidato')
    }

    # Enriquecer cada evento con flag ya_encuestado y encuesta previa
    eventos = []
    for ev in eventos_qs:
        ev.ya_encuestado = ev.pk in encuestas_dict
        ev.encuesta_previa = encuestas_dict.get(ev.pk)
        eventos.append(ev)

    return render(request, 'votacion/encuestador/elegir_evento.html', {
        'votante': votante,
        'eventos': eventos,
    })


@login_required
def encuestador_registrar_voto(request, votante_pk, evento_pk):
    """Muestra los candidatos del evento y registra/actualiza la intención de voto."""
    from .models import Encuesta
    votante = get_object_or_404(Votante, pk=votante_pk)
    evento = get_object_or_404(EventoElectoral, pk=evento_pk, activo=True)
    candidatos = Candidato.objects.filter(evento=evento, activo=True).select_related('partido').order_by('numero_lista', 'apellidos')

    # Verificar si ya respondió esta encuesta
    encuesta_existente = Encuesta.objects.filter(votante=votante, evento=evento).first()

    if request.method == 'POST':
        candidato_id = request.POST.get('candidato_id')
        observacion = request.POST.get('observacion', '').strip()

        if not candidato_id:
            messages.error(request, 'Debes seleccionar un candidato.')
        else:
            candidato = get_object_or_404(Candidato, pk=candidato_id, evento=evento)
            if encuesta_existente:
                # Actualizar respuesta existente
                encuesta_existente.candidato = candidato
                encuesta_existente.encuestador = request.user
                encuesta_existente.observacion = observacion
                encuesta_existente.save()
                messages.success(request, f'✅ Intención de voto de {votante.nombre_completo} actualizada a {candidato.nombre_completo}.')
            else:
                Encuesta.objects.create(
                    votante=votante,
                    evento=evento,
                    candidato=candidato,
                    encuestador=request.user,
                    observacion=observacion,
                )
                messages.success(request, f'✅ Encuesta registrada: {votante.nombre_completo} → {candidato.nombre_completo}.')
            return redirect('encuestador_inicio')

    return render(request, 'votacion/encuestador/registrar_voto.html', {
        'votante': votante,
        'evento': evento,
        'candidatos': candidatos,
        'encuesta_existente': encuesta_existente,
    })


@login_required
def encuestador_estadisticas(request):
    """Dashboard de resultados de encuestas por evento."""

    eventos = EventoElectoral.objects.filter(activo=True).annotate(
        total_encuestas=Count('encuestas')
    ).order_by('-fecha')

    evento_seleccionado = None
    resultados = []
    total_evento = 0

    # Determinar el evento a mostrar:
    # 1) el que viene en ?evento=
    # 2) si no, el único activo que exista
    # 3) si no, el primero de la lista
    evento_id = request.GET.get('evento')
    if evento_id:
        evento_seleccionado = get_object_or_404(EventoElectoral, pk=evento_id)
    elif eventos.exists():
        evento_seleccionado = eventos.first()

    if evento_seleccionado:
        total_evento = Encuesta.objects.filter(evento=evento_seleccionado).count()

        # ── Resultados agregados por candidato ──────────────────
        resultados_qs = list(
            Encuesta.objects
            .filter(evento=evento_seleccionado)
            .values(
                'candidato__id',
                'candidato__nombres',
                'candidato__apellidos',
                'candidato__foto',
                'candidato__partido__sigla',
                'candidato__partido__color',
                'candidato__numero_lista',
                'candidato__cargo_aspirado',
            )
            .annotate(votos=Count('id'))
            .order_by('-votos')
        )

        for r in resultados_qs:
            r['porcentaje'] = round((r['votos'] / total_evento * 100), 1) if total_evento > 0 else 0

        # ── Drill-down: detalle por municipio para cada candidato ─
        from collections import defaultdict

        encuestas_detalle = (
            Encuesta.objects
            .filter(evento=evento_seleccionado)
            .select_related(
                'votante', 'votante__municipio', 'votante__departamento',
                'votante__puesto', 'votante__mesa', 'candidato'
            )
            .order_by(
                'candidato__id',
                'votante__municipio__nombre',
                'votante__puesto__nombre',
                'votante__mesa__numero',
                'votante__apellidos'
            )
        )

        # drill[candidato_id] = lista de municipios con sus mesas y votantes
        # Usamos estructura: { cid: { mun_label: { mesa_label: [votantes] } } }
        raw = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for enc in encuestas_detalle:
            cid = enc.candidato_id
            v = enc.votante
            mun  = v.municipio.nombre if v.municipio else 'Sin municipio'
            dep  = v.departamento.nombre if v.departamento else ''
            mun_label  = f'{mun} ({dep})' if dep else mun
            puesto     = v.puesto.nombre if v.puesto else 'Sin puesto'
            mesa_num   = f'Mesa {v.mesa.numero}' if v.mesa else 'Sin mesa'
            mesa_label = f'{puesto} — {mesa_num}'
            raw[cid][mun_label][mesa_label].append({
                'nombre': v.nombre_completo,
                'cedula': v.cedula,
            })

        # Convertir a estructura serializable para el template
        # Lista de candidatos con su detalle, en el mismo orden que resultados_qs
        drill_list = []
        for r in resultados_qs:
            cid = r['candidato__id']
            municipios = []
            for mun_label, mesas in raw.get(cid, {}).items():
                mesas_list = []
                for mesa_label, votantes in mesas.items():
                    mesas_list.append({
                        'mesa': mesa_label,
                        'votantes': votantes,
                        'total': len(votantes),
                    })
                municipios.append({
                    'municipio': mun_label,
                    'mesas': mesas_list,
                    'total': sum(m['total'] for m in mesas_list),
                })
            drill_list.append(municipios)

        # Combinar resultados con su drill-down en el mismo índice
        resultados = []
        for r, drill in zip(resultados_qs, drill_list):
            r['drill'] = drill
            resultados.append(r)

    return render(request, 'votacion/encuestador/estadisticas.html', {
        'eventos': eventos,
        'evento_seleccionado': evento_seleccionado,
        'resultados': resultados,
        'total_evento': total_evento,
    })
