import glob
import os
import ast
from collections import defaultdict
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Auditoría 14: preflight de staging, migraciones y superficies de pago.'

    def handle(self, *args, **options):
        root = str(settings.BASE_DIR)
        errors, warnings = [], []

        # 1) No debe haber dos migraciones con el mismo número dentro de una app.
        for app_path in glob.glob(os.path.join(root, '*', 'migrations')):
            app = os.path.basename(os.path.dirname(app_path))
            numbers = defaultdict(list)
            for path in glob.glob(os.path.join(app_path, '[0-9][0-9][0-9][0-9]_*.py')):
                name = os.path.basename(path)
                numbers[name[:4]].append(name)
            for number, names in numbers.items():
                if len(names) > 1:
                    errors.append('{} tiene migraciones duplicadas: {}'.format(app, ', '.join(names)))

        # 2) Rechazar restos de la API AJAX eliminada en Django moderno.
        legacy_ajax = []
        for path in glob.glob(os.path.join(root, '**', '*.py'), recursive=True):
            if os.sep + 'migrations' + os.sep in path:
                continue
            try:
                text = open(path, encoding='utf-8').read()
                tree = ast.parse(text, filename=path)
            except (OSError, SyntaxError):
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'is_ajax':
                    legacy_ajax.append(path)
                    break
        if legacy_ajax:
            errors.append('Quedan llamadas request.is_ajax(): {}'.format(', '.join(legacy_ajax)))

        # 3) PayPal no puede confiar en una referencia enviada por el navegador.
        bancos = os.path.join(root, 'bancos', 'views.py')
        if os.path.exists(bancos):
            text = open(bancos, encoding='utf-8').read()
            if 'verficado = True' in text[text.find('def _crear_solicitud_paypal'):]:
                errors.append('El flujo PayPal marca pagos como verificados sin confirmación externa.')
            if "banco='paypal'" not in text:
                warnings.append('No se encontró el marcador de solicitud PayPal; revisar integración.')

        # 4) Producción debe usar PostgreSQL y variables de entorno.
        if not settings.DEBUG and not os.environ.get('DATABASE_URL'):
            errors.append('Producción sin DATABASE_URL.')
        if not settings.DEBUG and 'sqlite3' in str(settings.DATABASES['default'].get('ENGINE', '')):
            errors.append('Producción configurada con SQLite.')

        # 5) Este proyecto todavía está sobre Django 3.0.7; es bloqueo de actualización.
        try:
            import django
            if django.VERSION < (3, 2):
                warnings.append('Django {} es una rama antigua; planificar actualización escalonada.'.format(django.get_version()))
        except Exception:
            warnings.append('No fue posible consultar la versión de Django en este entorno.')

        for warning in warnings:
            self.stdout.write(self.style.WARNING('ADVERTENCIA: ' + warning))
        if errors:
            for error in errors:
                self.stdout.write(self.style.ERROR('ERROR: ' + error))
            raise CommandError('AUDITORIA 14 NO SUPERADA')
        self.stdout.write(self.style.SUCCESS('AUDITORIA 14: PREFLIGHT SUPERADO'))
