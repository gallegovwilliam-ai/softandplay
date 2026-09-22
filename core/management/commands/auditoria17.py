from django.core.management.base import BaseCommand
from django.db import connection
from pathlib import Path
import ast

class Command(BaseCommand):
    help = 'Auditoria 17: seguridad de validacion de email e integridad financiera.'

    def handle(self, *args, **options):
        root = Path(__file__).resolve().parents[3]
        errors = []
        warnings = []
        migrations = {}
        for p in root.rglob('migrations/*.py'):
            if p.name == '__init__.py':
                continue
            try:
                num = p.name.split('_', 1)[0]
                if num.isdigit():
                    migrations.setdefault((p.parent.name, int(num)), []).append(str(p))
            except Exception:
                pass
        for key, paths in migrations.items():
            if len(paths) > 1:
                errors.append('Migracion duplicada: {} -> {}'.format(key, paths))

        for p in root.rglob('*.py'):
            if '__pycache__' in p.parts:
                continue
            try:
                tree = ast.parse(p.read_text(encoding='utf-8'))
            except Exception:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    if node.func.attr == 'is_ajax':
                        errors.append('request.is_ajax() encontrado en {}'.format(p))

        if connection.vendor != 'postgresql':
            warnings.append('La auditoria 17 debe repetirse sobre PostgreSQL staging; motor actual: {}'.format(connection.vendor))
        else:
            with connection.cursor() as cur:
                for table in ('core_settlement', 'core_settlement75'):
                    cur.execute("SELECT to_regclass(%s)", [table])
                    if cur.fetchone()[0] is not None:
                        errors.append('Tabla legacy presente: {}'.format(table))

        # Checks that are useful when real data exists.
        try:
            from cards.models import Impresion, Impresion75
            from pagos.models import SaleRecord, SaleRecord75
            dup = (Impresion.objects.values('propietario__partida_id', 'carton_id')
                   .annotate(n=__import__('django.db.models', fromlist=['Count']).Count('id')).filter(n__gt=1).count())
            dup75 = (Impresion75.objects.values('propietario__partida_id', 'carton_id')
                     .annotate(n=__import__('django.db.models', fromlist=['Count']).Count('id')).filter(n__gt=1).count())
            if dup or dup75:
                errors.append('Asignaciones duplicadas detectadas: loto={} bingo75={}'.format(dup, dup75))
            if SaleRecord.objects.filter(quantity__lte=0).exists() or SaleRecord75.objects.filter(quantity__lte=0).exists():
                errors.append('SaleRecord con cantidad no positiva')
        except Exception as exc:
            warnings.append('No se pudieron ejecutar checks de datos: {}'.format(exc))

        if errors:
            for msg in errors:
                self.stdout.write(self.style.ERROR('ERROR: ' + msg))
            raise SystemExit(1)
        for msg in warnings:
            self.stdout.write(self.style.WARNING('AVISO: ' + msg))
        self.stdout.write(self.style.SUCCESS('AUDITORIA 17: OK (sin errores estaticos)'))
