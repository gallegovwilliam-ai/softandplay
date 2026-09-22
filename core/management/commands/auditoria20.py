import ast
import os
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

class Command(BaseCommand):
    help = 'Auditoria 20: preparación de despliegue, seguridad y operación.'

    def handle(self, *args, **options):
        root = Path(settings.BASE_DIR)
        errors, warnings, ok = [], [], []

        # Runtime / production settings
        if settings.DEBUG:
            errors.append('DEBUG está activo; producción requiere DJANGO_DEBUG=False')
        if settings.SECRET_KEY in ('CHANGE-ME-IN-PRODUCTION', '') or len(settings.SECRET_KEY) < 50:
            errors.append('SECRET_KEY no cumple el mínimo recomendado de producción')
        if connection.vendor == 'sqlite':
            errors.append('SQLite no es válido como base de datos de producción')
        if not os.environ.get('DATABASE_URL'):
            warnings.append('DATABASE_URL no está definida en este entorno')
        if not os.environ.get('REDIS_URL'):
            warnings.append('REDIS_URL no está definida explícitamente')
        if not settings.ALLOWED_HOSTS or settings.ALLOWED_HOSTS == ['localhost', '127.0.0.1']:
            errors.append('ALLOWED_HOSTS no contiene dominios de producción')
        if not os.environ.get('CSRF_TRUSTED_ORIGINS'):
            errors.append('CSRF_TRUSTED_ORIGINS no está configurado')
        if not os.environ.get('EMAIL_HOST_USER') or not os.environ.get('EMAIL_HOST_PASSWORD'):
            warnings.append('Credenciales SMTP no configuradas en este entorno')
        if settings.TIME_ZONE == 'America/Mexico_City' and os.environ.get('DJANGO_TIME_ZONE') is None:
            warnings.append('Confirme la zona horaria operativa antes de producción')

        # Source-level dangerous endpoints
        destructive = {'ClienteDelete','BancoDelete','deleteCompras','LotoChanceDelete','UserDelete','DeletePartida','DeletePartida75'}
        for f in root.rglob('*.py'):
            if 'migrations' in f.parts or '__pycache__' in f.parts:
                continue
            try:
                text = f.read_text(encoding='utf-8')
                tree = ast.parse(text)
            except Exception:
                continue
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in destructive:
                    src = ast.get_source_segment(text, node) or ''
                    if "request.method" not in src:
                        warnings.append(f'{node.name}: no se detectó validación HTTP explícita')

        # Operational endpoints: test endpoint must not be public mutation.
        try:
            urls = (root / 'app' / 'urls.py').read_text(encoding='utf-8')
            core = (root / 'core' / 'views.py').read_text(encoding='utf-8')
            if "path('test-notify'" in urls and "request.method != 'POST'" not in core:
                errors.append('test-notify sigue expuesto como mutación sin protección')
            else:
                ok.append('Endpoint de prueba protegido')
        except OSError:
            warnings.append('No se pudo inspeccionar endpoint de prueba')

        # Migration numbering
        duplicates = []
        for migdir in root.rglob('migrations'):
            nums = {}
            for f in migdir.glob('[0-9][0-9][0-9][0-9]_*.py'):
                nums.setdefault(f.name[:4], []).append(f.name)
            duplicates.extend((str(migdir), n, fs) for n, fs in nums.items() if len(fs) > 1)
        if duplicates:
            errors.append('Migraciones duplicadas: {}'.format(duplicates))
        else:
            ok.append('Migraciones sin numeración duplicada')

        # ORM financial checks when runtime is available.
        try:
            from core.models import FinancialLedger
            from pagos.models import SaleRecord, SaleRecord75, PaymentRecord, PaymentRecord75, FinancialReversal
            if FinancialLedger.objects.filter(amount__lte=0).exists():
                errors.append('FinancialLedger contiene importes <= 0')
            for Model, name in ((SaleRecord,'SaleRecord'), (SaleRecord75,'SaleRecord75')):
                if Model.objects.filter(quantity__lte=0).exists():
                    errors.append(f'{name} contiene cantidades <= 0')
                if Model.objects.filter(status=Model.STATUS_APPROVED, amount__lte=0).exists():
                    errors.append(f'{name} contiene ventas aprobadas con importe <= 0')
            for Model, name in ((PaymentRecord,'PaymentRecord'), (PaymentRecord75,'PaymentRecord75')):
                if Model.objects.filter(status=Model.STATUS_APPROVED, approved_at__isnull=True).exists():
                    errors.append(f'{name} aprobado sin approved_at')
                if Model.objects.filter(amount__lt=0).exists() or Model.objects.filter(net_amount__lt=0).exists():
                    errors.append(f'{name} contiene importes negativos')
            # Every reversal must have both sides and one original.
            if FinancialReversal.objects.filter(original_entry__isnull=True).exists() or FinancialReversal.objects.filter(reversal_entry__isnull=True).exists():
                errors.append('FinancialReversal contiene referencias incompletas')
            ok.append('Controles financieros ORM ejecutados')
        except Exception as exc:
            warnings.append('ORM financiero no ejecutado en este entorno: {}'.format(exc))

        for x in ok: self.stdout.write(self.style.SUCCESS('OK: ' + x))
        for x in warnings: self.stdout.write(self.style.WARNING('ADVERTENCIA: ' + x))
        for x in errors: self.stdout.write(self.style.ERROR('ERROR: ' + x))
        if errors:
            raise CommandError('Auditoría 20: NO APTO para producción')
        self.stdout.write(self.style.SUCCESS('AUDITORIA 20: CONTROLES SUPERADOS'))
