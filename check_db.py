"""
Ejecuta esto en Railway para verificar qué base de datos está usando:
  python check_db.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
db = settings.DATABASES['default']
print("=" * 50)
print("BASE DE DATOS EN USO:")
print(f"  ENGINE : {db['ENGINE']}")
print(f"  NAME   : {db.get('NAME', 'N/A')}")
print(f"  HOST   : {db.get('HOST', 'N/A')}")
print(f"  PORT   : {db.get('PORT', 'N/A')}")
print()
print(f"DATABASE_URL env: {os.environ.get('DATABASE_URL', '❌ NO ENCONTRADA')}")
print("=" * 50)
