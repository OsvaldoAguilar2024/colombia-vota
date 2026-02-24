"""
Management command to load initial Colombia departamentos and municipios data.
Usage: python manage.py cargar_datos_colombia
"""
from django.core.management.base import BaseCommand
from votacion.models import Departamento, Municipio


DEPARTAMENTOS_MUNICIPIOS = {
    "Amazonas": {"codigo": "91", "municipios": [("Leticia", "91001"), ("Puerto Nariño", "91540")]},
    "Antioquia": {"codigo": "05", "municipios": [
        ("Medellín", "05001"), ("Bello", "05088"), ("Itagüí", "05360"),
        ("Envigado", "05266"), ("Apartadó", "05045"),
        ("Turbo", "05837"), ("Caucasia", "05154"), ("Rionegro", "05615"),
    ]},
    "Arauca": {"codigo": "81", "municipios": [("Arauca", "81001"), ("Saravena", "81736"), ("Tame", "81794")]},
    "Atlántico": {"codigo": "08", "municipios": [
        ("Barranquilla", "08001"), ("Soledad", "08758"), ("Malambo", "08433"),
        ("Sabanalarga", "08638"), ("Baranoa", "08078"),
    ]},
    "Bogotá D.C.": {"codigo": "11", "municipios": [("Bogotá D.C.", "11001")]},
    "Bolívar": {"codigo": "13", "municipios": [
        ("Cartagena de Indias", "13001"), ("Magangué", "13430"), ("Mompós", "13468"),
    ]},
    "Boyacá": {"codigo": "15", "municipios": [
        ("Tunja", "15001"), ("Duitama", "15238"), ("Sogamoso", "15762"), ("Chiquinquirá", "15176"),
    ]},
    "Caldas": {"codigo": "17", "municipios": [
        ("Manizales", "17001"), ("La Dorada", "17380"), ("Chinchiná", "17174"),
    ]},
    "Caquetá": {"codigo": "18", "municipios": [("Florencia", "18001"), ("San Vicente del Caguán", "18610")]},
    "Casanare": {"codigo": "85", "municipios": [("Yopal", "85001"), ("Aguazul", "85010")]},
    "Cauca": {"codigo": "19", "municipios": [("Popayán", "19001"), ("Santander de Quilichao", "19698")]},
    "Cesar": {"codigo": "20", "municipios": [("Valledupar", "20001"), ("Aguachica", "20011")]},
    "Chocó": {"codigo": "27", "municipios": [("Quibdó", "27001"), ("Istmina", "27361")]},
    "Córdoba": {"codigo": "23", "municipios": [("Montería", "23001"), ("Lorica", "23417"), ("Sahagún", "23660")]},
    "Cundinamarca": {"codigo": "25", "municipios": [
        ("Fusagasugá", "25290"), ("Girardot", "25307"), ("Facatativá", "25269"),
        ("Zipaquirá", "25899"), ("Soacha", "25754"), ("Chía", "25175"),
        ("Mosquera", "25473"), ("Madrid", "25430"),
    ]},
    "Guajira": {"codigo": "44", "municipios": [("Riohacha", "44001"), ("Maicao", "44430")]},
    "Huila": {"codigo": "41", "municipios": [("Neiva", "41001"), ("Pitalito", "41551"), ("Garzón", "41298")]},
    "Magdalena": {"codigo": "47", "municipios": [("Santa Marta", "47001"), ("Ciénaga", "47189")]},
    "Meta": {"codigo": "50", "municipios": [("Villavicencio", "50001"), ("Acacías", "50006"), ("Granada", "50313")]},
    "Nariño": {"codigo": "52", "municipios": [("Pasto", "52001"), ("Tumaco", "52835"), ("Ipiales", "52356")]},
    "Norte de Santander": {"codigo": "54", "municipios": [("Cúcuta", "54001"), ("Ocaña", "54498"), ("Pamplona", "54518")]},
    "Putumayo": {"codigo": "86", "municipios": [("Mocoa", "86001"), ("Puerto Asís", "86568")]},
    "Quindío": {"codigo": "63", "municipios": [("Armenia", "63001"), ("Calarcá", "63130"), ("Montenegro", "63470")]},
    "Risaralda": {"codigo": "66", "municipios": [("Pereira", "66001"), ("Dosquebradas", "66170"), ("Santa Rosa de Cabal", "66682")]},
    "San Andrés y Providencia": {"codigo": "88", "municipios": [("San Andrés", "88001")]},
    "Santander": {"codigo": "68", "municipios": [
        ("Bucaramanga", "68001"), ("Floridablanca", "68276"), ("Girón", "68307"),
        ("Piedecuesta", "68547"), ("Barrancabermeja", "68081"),
    ]},
    "Sucre": {"codigo": "70", "municipios": [("Sincelejo", "70001"), ("Corozal", "70215")]},
    "Tolima": {"codigo": "73", "municipios": [("Ibagué", "73001"), ("Espinal", "73268"), ("Honda", "73349")]},
    "Valle del Cauca": {"codigo": "76", "municipios": [
        ("Cali", "76001"), ("Buenaventura", "76109"), ("Palmira", "76520"),
        ("Tuluá", "76834"), ("Buga", "76111"), ("Cartago", "76147"),
    ]},
    "Vaupés": {"codigo": "97", "municipios": [("Mitú", "97001")]},
    "Vichada": {"codigo": "99", "municipios": [("Puerto Carreño", "99001")]},
}


class Command(BaseCommand):
    help = 'Carga datos iniciales de departamentos y municipios de Colombia'

    def handle(self, *args, **options):
        self.stdout.write('Cargando departamentos y municipios de Colombia...')
        creados_dep = 0
        creados_mun = 0

        for nombre_dep, info in DEPARTAMENTOS_MUNICIPIOS.items():
            dep, created = Departamento.objects.get_or_create(
                codigo=info["codigo"],
                defaults={"nombre": nombre_dep}
            )
            if created:
                creados_dep += 1

            for nombre_mun, codigo_mun in info["municipios"]:
                _, mc = Municipio.objects.get_or_create(
                    departamento=dep,
                    codigo=codigo_mun,
                    defaults={"nombre": nombre_mun}
                )
                if mc:
                    creados_mun += 1

        self.stdout.write(self.style.SUCCESS(
            f'✅ Listo! Departamentos creados: {creados_dep} | Municipios creados: {creados_mun}'
        ))
