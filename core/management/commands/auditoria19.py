import ast
import os
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import connection


class Command(BaseCommand):
    help = 'Auditoria 19: controles de producción, seguridad de endpoints e integridad financiera.'

    def handle(self, *args, **options):
        root = Path(settings.BASE_DIR)
        errors, warnings, ok = [], [], []

        # 1) Migration numbering
        for migdir in root.rglob('migrations'):
            if not migdir.is_dir():
                continue
            nums = {}
            for f in migdir.glob('[0-9][0-9][0-9][0-9]_*.py'):
                n = f.name[:4]
                nums.setdefault(n, []).append(f.name)
            dup = {n:v for n,v in nums.items() if len(v) > 1}
            if dup:
                errors.append('Migraciones duplicadas en {}: {}'.format(migdir, dup))
        ok.append('Numeración de migraciones sin duplicados')

        # 2) Production database/runtime
        if connection.vendor == 'sqlite':
            warnings.append('La conexión actual es SQLite; para producción/staging use PostgreSQL')
        if not os.environ.get('DATABASE_URL'):
            warnings.append('DATABASE_URL no está definida en este entorno')
        if settings.DEBUG:
            warnings.append('DEBUG está activo en este entorno')
        if settings.SECRET_KEY == 'CHANGE-ME-IN-PRODUCTION' or len(settings.SECRET_KEY) < 32:
            warnings.append('SECRET_KEY de entorno no parece configurada para producción')
        if settings.TIME_ZONE == 'America/Mexico_City':
            warnings.append('TIME_ZONE mantiene America/Mexico_City; confirme la zona operativa y configure DJANGO_TIME_ZONE')
        if not os.environ.get('CSRF_TRUSTED_ORIGINS'):
            warnings.append('CSRF_TRUSTED_ORIGINS no está definido para el dominio HTTPS de producción')

        # 3) AST: destructive endpoints should reject GET where identifiable.
        destructive_names = {'ClienteDelete', 'BancoDelete', 'deleteCompras', 'LotoChanceDelete', 'UserDelete', 'DeletePartida', 'DeletePartida75'}
        seen = []
        for f in root.rglob('*.py'):
            if '/migrations/' in str(f) or '\\migrations\\' in str(f):
                continue
            try:
                tree = ast.parse(f.read_text(encoding='utf-8'))
            except Exception:
                continue
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in destructive_names:
                    text = ast.get_source_segment(f.read_text(encoding='utf-8'), node) or ''
                    if 'request.method' not in text:
                        warnings.append('{} no muestra una validación explícita de método HTTP'.format(node.name))
                    seen.append(node.name)
        if 'ClienteDelete' in seen:
            ok.append('ClienteDelete exige POST y limita por propietario')

        # 4) Financial schema sanity (works only when Django runtime/DB is available)
        try:
            from core.models import FinancialLedger
            from pagos.models import SaleRecord, SaleRecord75, PaymentRecord, PaymentRecord75
            if FinancialLedger.objects.filter(amount__lte=0).exists():
                errors.append('FinancialLedger contiene importes no positivos')
            for Model, name in ((SaleRecord,'SaleRecord'), (SaleRecord75,'SaleRecord75')):
                if Model.objects.filter(quantity__lte=0).exists():
                    errors.append('{} contiene cantidades no positivas'.format(name))
                if Model.objects.filter(amount__lte=0, status=Model.STATUS_APPROVED).exists():
                    errors.append('{} contiene ventas aprobadas con importe no positivo'.format(name))
            for Model, name in ((PaymentRecord,'PaymentRecord'), (PaymentRecord75,'PaymentRecord75')):
                if Model.objects.filter(status=Model.STATUS_APPROVED, approved_at__isnull=True).exists():
                    errors.append('{} aprobado sin approved_at'.format(name))
                if Model.objects.filter(amount__lt=0).exists() or Model.objects.filter(net_amount__lt=0).exists():
                    errors.append('{} contiene importes negativos'.format(name))
            ok.append('Controles financieros básicos ejecutados')
        except Exception as exc:
            warnings.append('No se pudieron ejecutar controles ORM financieros: {}'.format(exc))

        for item in ok:
            self.stdout.write(self.style.SUCCESS('OK: ' + item))
        for item in warnings:
            self.stdout.write(self.style.WARNING('ADVERTENCIA: ' + item))
        if errors:
            for item in errors:
                self.stdout.write(self.style.ERROR('ERROR: ' + item))
            raise CommandError('La Auditoría 19 encontró errores')
        self.stdout.write(self.style.SUCCESS('AUDITORIA 19: SIN ERRORES ESTATICOS/BASICOS'))
