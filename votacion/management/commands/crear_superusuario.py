"""
Crea el superusuario inicial desde variables de entorno.
Uso en Railway: python manage.py crear_superusuario
Variables requeridas: DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD, DJANGO_SUPERUSER_EMAIL
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Crea superusuario desde variables de entorno (para Railway)'

    def handle(self, *args, **options):
        import os
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin1234')
        email    = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@colombiavota.com')

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'ℹ️  El usuario "{username}" ya existe.'))
        else:
            User.objects.create_superuser(username=username, password=password, email=email)
            self.stdout.write(self.style.SUCCESS(f'✅ Superusuario "{username}" creado.'))
