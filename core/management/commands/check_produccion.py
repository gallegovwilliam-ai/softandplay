import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import connection

class Command(BaseCommand):
    help = 'Audita la configuración mínima de producción de SoftAndPlay.'

    def handle(self, *args, **options):
        errors = []
        warnings = []
        if settings.DEBUG:
            errors.append('DJANGO_DEBUG debe ser False en producción')
        if settings.SECRET_KEY == 'CHANGE-ME-IN-PRODUCTION' or len(settings.SECRET_KEY) < 32:
            errors.append('DJANGO_SECRET_KEY no está configurada con una clave suficientemente robusta')
        if not settings.ALLOWED_HOSTS or settings.ALLOWED_HOSTS == ['localhost', '127.0.0.1']:
            warnings.append('DJANGO_ALLOWED_HOSTS debe contener los dominios reales')
        if connection.vendor == 'sqlite3':
            errors.append('Producción requiere PostgreSQL; SQLite queda solo para desarrollo')
        if not os.environ.get('DATABASE_URL'):
            warnings.append('DATABASE_URL no está definida')
        if not os.environ.get('REDIS_URL') and os.environ.get('REDIS_HOST', 'localhost') == 'localhost':
            warnings.append('Configure REDIS_URL/REDIS_HOST para el servicio Redis de producción')
        if not os.environ.get('CSRF_TRUSTED_ORIGINS'):
            warnings.append('Configure CSRF_TRUSTED_ORIGINS con los dominios HTTPS reales')
        for item in warnings:
            self.stdout.write(self.style.WARNING('ADVERTENCIA: ' + item))
        if errors:
            for item in errors:
                self.stdout.write(self.style.ERROR('ERROR: ' + item))
            raise CommandError('La configuración no supera el control de producción')
        self.stdout.write(self.style.SUCCESS('CONTROL DE PRODUCCION SUPERADO'))
