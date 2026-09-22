from importlib.metadata import version, PackageNotFoundError
from pathlib import Path

from django.conf import settings
from django.core.management import BaseCommand, call_command
from django.db import connection
from django.db.migrations.executor import MigrationExecutor


class Command(BaseCommand):
    help = 'Auditoria 22: staging real, migraciones y compatibilidad del stack Django 5.2/PostgreSQL.'

    def _pkg(self, name):
        try:
            return version(name)
        except PackageNotFoundError:
            return 'NO_INSTALADO'

    def handle(self, *args, **options):
        root = Path(settings.BASE_DIR)
        errors = []
        warnings = []

        expected = {
            'Django': '5.2.17',
            'channels': '4.3.2',
            'channels-redis': '4.3.0',
            'Daphne': '4.2.3',
        }
        for package, wanted in expected.items():
            actual = self._pkg(package)
            if actual != wanted:
                errors.append(f'{package}: esperado {wanted}, encontrado {actual}')

        pyversion = (root / '.python-version').read_text().strip() if (root / '.python-version').exists() else ''
        if pyversion not in ('3.13', '3.13.0'):
            errors.append(f'Python objetivo incorrecto: {pyversion or "no definido"}')

        if connection.vendor != 'postgresql':
            if not settings.DEBUG:
                errors.append(f'Produccion/staging endurecido no puede usar {connection.vendor}')
            else:
                warnings.append(f'Base actual: {connection.vendor}; para certificacion usar PostgreSQL.')

        if not settings.DEBUG and settings.SECRET_KEY == 'CHANGE-ME-IN-PRODUCTION':
            errors.append('SECRET_KEY de produccion sigue usando placeholder')

        # Comprueba que no haya cambios de modelos pendientes de migración.
        try:
            call_command('makemigrations', check=True, dry_run=True, verbosity=0)
        except SystemExit as exc:
            if getattr(exc, 'code', 1):
                errors.append('Existen cambios de modelos que requieren migracion.')
        except Exception as exc:
            errors.append(f'No se pudo ejecutar makemigrations --check --dry-run: {exc}')

        # Comprueba migraciones pendientes en la base actual.
        try:
            executor = MigrationExecutor(connection)
            plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
            if plan:
                errors.append(f'Hay {len(plan)} operaciones de migracion pendientes.')
        except Exception as exc:
            errors.append(f'No se pudo inspeccionar el estado de migraciones: {exc}')

        # Settings retirados de Django moderno.
        if hasattr(settings, 'USE_L10N'):
            warnings.append('USE_L10N ya no es una opcion operativa en Django moderno; eliminar del proyecto.')
        if hasattr(settings, 'SECURE_BROWSER_XSS_FILTER'):
            warnings.append('SECURE_BROWSER_XSS_FILTER ya no proporciona proteccion en Django moderno.')

        if errors:
            for item in errors:
                self.stdout.write(self.style.ERROR('ERROR: ' + item))
            for item in warnings:
                self.stdout.write(self.style.WARNING('WARN: ' + item))
            raise SystemExit(1)

        for item in warnings:
            self.stdout.write(self.style.WARNING('WARN: ' + item))
        self.stdout.write(self.style.SUCCESS('AUDITORIA 22: staging y migraciones reales listos para certificacion.'))
