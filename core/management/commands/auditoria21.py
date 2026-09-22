import ast
import os
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection


class Command(BaseCommand):
    help = 'Auditoria 21: compatibilidad para migracion a Django 5.2/Channels 4/Python 3.13.'

    def handle(self, *args, **options):
        root = Path(settings.BASE_DIR)
        errors = []
        warnings = []

        # 1) Python objetivo
        pyversion = (root / '.python-version').read_text().strip() if (root / '.python-version').exists() else ''
        if pyversion not in ('3.13', '3.13.0'):
            warnings.append('Python objetivo no es 3.13: {}'.format(pyversion or 'no definido'))

        # 2) Django/Channels target en requirements
        req = (root / 'requeriments').read_text().lower() if (root / 'requeriments').exists() else ''
        for required in ('django==5.2.17', 'channels==4.3.2', 'channels-redis==4.3.0', 'daphne==4.2.3'):
            if required.lower() not in req:
                errors.append('Falta pin objetivo {}'.format(required))

        # 3) APIs removidas de Django moderno en codigo propio.
        forbidden = {
            'django.conf.urls': 'Usar django.urls',
            'django.core.urlresolvers': 'Usar django.urls',
            'ugettext': 'Usar gettext/gettext_lazy',
            'force_text': 'Usar force_str',
            'smart_text': 'Usar smart_str',
            'request.is_ajax': 'Usar request.headers.get("X-Requested-With")',
        }
        for path in root.rglob('*.py'):
            if 'migrations' in path.parts or path.name.startswith('auditoria'):
                continue
            try:
                text = path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                continue
            for needle, message in forbidden.items():
                if needle in text:
                    errors.append('{} en {} ({})'.format(needle, path.relative_to(root), message))

            # AST: detectar llamadas url(...) que dependan de django.conf.urls.
            try:
                tree = ast.parse(text)
            except SyntaxError as exc:
                errors.append('SyntaxError en {}: {}'.format(path.relative_to(root), exc))
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'url':
                    errors.append('llamada url() legacy en {}'.format(path.relative_to(root)))

        # 4) ASGI moderno
        asgi = (root / 'app' / 'asgi.py').read_text(encoding='utf-8') if (root / 'app' / 'asgi.py').exists() else ''
        routing = (root / 'app' / 'routing.py').read_text(encoding='utf-8') if (root / 'app' / 'routing.py').exists() else ''
        if 'get_default_application' in asgi:
            errors.append('app/asgi.py aun usa get_default_application()')
        if 'get_asgi_application' not in asgi:
            errors.append('app/asgi.py no usa get_asgi_application()')
        if '"http"' not in asgi:
            errors.append('ASGI no declara handler HTTP')
        if '.as_asgi()' not in routing:
            errors.append('Consumers WebSocket no usan as_asgi()')

        # 5) Base de datos
        if connection.vendor == 'sqlite3' and not settings.DEBUG:
            errors.append('Produccion no puede usar SQLite')
        if connection.vendor == 'postgresql':
            warnings.append('PostgreSQL detectado: ejecutar migraciones y pruebas reales en staging.')

        # 6) secretos
        if settings.SECRET_KEY == 'CHANGE-ME-IN-PRODUCTION' and not settings.DEBUG:
            errors.append('SECRET_KEY de produccion no esta configurada')

        if errors:
            for item in errors:
                self.stdout.write(self.style.ERROR('ERROR: ' + item))
            for item in warnings:
                self.stdout.write(self.style.WARNING('WARN: ' + item))
            raise SystemExit(1)

        for item in warnings:
            self.stdout.write(self.style.WARNING('WARN: ' + item))
        self.stdout.write(self.style.SUCCESS('AUDITORIA 21: compatibilidad estatica OK'))
