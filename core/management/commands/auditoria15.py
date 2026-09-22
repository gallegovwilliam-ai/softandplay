import ast
import glob
import os
from collections import defaultdict
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.db.models import Count


class Command(BaseCommand):
    help = 'Auditoría 15: integridad de ventas, cartones, finanzas y preflight de PostgreSQL.'

    def handle(self, *args, **options):
        root = str(settings.BASE_DIR)
        errors, warnings = [], []

        # Migration numbering must be unambiguous.
        for app_path in glob.glob(os.path.join(root, '*', 'migrations')):
            app = os.path.basename(os.path.dirname(app_path))
            numbers = defaultdict(list)
            for path in glob.glob(os.path.join(app_path, '[0-9][0-9][0-9][0-9]_*.py')):
                name = os.path.basename(path)
                numbers[name[:4]].append(name)
            for number, names in numbers.items():
                if len(names) > 1:
                    errors.append('{} tiene migraciones duplicadas: {}'.format(app, ', '.join(names)))

        # Actual legacy AJAX API must not remain in executable code.
        for path in glob.glob(os.path.join(root, '**', '*.py'), recursive=True):
            if os.sep + 'migrations' + os.sep in path:
                continue
            try:
                tree = ast.parse(open(path, encoding='utf-8').read(), filename=path)
            except (OSError, SyntaxError):
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'is_ajax':
                    errors.append('Queda request.is_ajax(): {}'.format(path))
                    break

        # Production/staging DB must not silently fall back to SQLite.
        vendor = getattr(connection, 'vendor', '')
        engine = str(settings.DATABASES['default'].get('ENGINE', ''))
        if not settings.DEBUG and vendor != 'postgresql':
            errors.append('Producción no está conectada a PostgreSQL (vendor={})'.format(vendor or 'desconocido'))
        elif settings.DEBUG and vendor == 'sqlite':
            warnings.append('Entorno DEBUG usando SQLite: válido para desarrollo, no para staging final.')

        if not os.environ.get('DATABASE_URL') and not settings.DEBUG:
            errors.append('Producción sin DATABASE_URL.')
        if not settings.DEBUG and 'sqlite3' in engine:
            errors.append('Producción configurada con SQLite.')

        # Carton assignment integrity: one physical carton may not belong twice to a game.
        try:
            from cards.models import Impresion, Impresion75
            for Model in (Impresion, Impresion75):
                duplicates = (
                    Model.objects.values('propietario__partida_id', 'carton_id')
                    .annotate(n=Count('id'))
                    .filter(n__gt=1)
                    .count()
                )
                if duplicates:
                    errors.append('{} tiene {} asignaciones duplicadas de cartón por partida.'.format(Model.__name__, duplicates))
        except Exception as exc:
            warnings.append('No fue posible auditar asignaciones de cartones: {}'.format(exc))

        # Approved sales must have a positive quantity and positive amount.
        try:
            from pagos.models import SaleRecord, SaleRecord75
            for Model in (SaleRecord, SaleRecord75):
                bad = Model.objects.filter(status=Model.STATUS_APPROVED).filter(quantity__lte=0).count()
                bad_amount = Model.objects.filter(status=Model.STATUS_APPROVED).filter(amount__lte=0).count()
                if bad or bad_amount:
                    errors.append('{} contiene ventas aprobadas inválidas (cantidad={}, importe={}).'.format(Model.__name__, bad, bad_amount))
        except Exception as exc:
            warnings.append('No fue posible auditar ventas: {}'.format(exc))

        # Wallet movements must never have a negative stored transaction amount.
        try:
            from wallet.models import TransactionWallet
            bad = TransactionWallet.objects.filter(amount__lt=0).count()
            if bad:
                errors.append('Wallet tiene {} movimientos con importe negativo.'.format(bad))
        except Exception as exc:
            warnings.append('No fue posible auditar Wallet: {}'.format(exc))

        # Legacy settlement tables should be gone after migration 0005.
        if vendor == 'postgresql':
            with connection.cursor() as cursor:
                for table in ('core_settlement', 'core_settlement75'):
                    cursor.execute("SELECT to_regclass(%s)", [table])
                    if cursor.fetchone()[0] is not None:
                        errors.append('La tabla histórica {} todavía existe.'.format(table))

        for warning in warnings:
            self.stdout.write(self.style.WARNING('ADVERTENCIA: ' + warning))
        if errors:
            for error in errors:
                self.stdout.write(self.style.ERROR('ERROR: ' + error))
            raise CommandError('AUDITORIA 15 NO SUPERADA')
        self.stdout.write(self.style.SUCCESS('AUDITORIA 15: PREFLIGHT SUPERADO'))
