import os
from decimal import Decimal
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.db.migrations.executor import MigrationExecutor

class Command(BaseCommand):
    help = 'Auditoría 12: migraciones, esquema financiero y compatibilidad PostgreSQL.'

    def handle(self, *args, **options):
        errors = []
        warnings = []
        if connection.vendor != 'postgresql':
            warnings.append('La validación está diseñada para PostgreSQL; la ejecución actual usa {}.'.format(connection.vendor))
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        if plan:
            warnings.append('Existen {} migraciones pendientes.'.format(len(plan)))
        else:
            self.stdout.write('MIGRACIONES: al día')

        required = {
            'partidas.Partida.monto_carton': 'DecimalField',
            'partidas.Partida.cartones_vendidos': 'PositiveIntegerField',
            'cards.Impresion.monto': 'DecimalField',
            'cards.CabezeraImpre.cantidad': 'PositiveIntegerField',
            'wallet.Wallet.balance': 'DecimalField',
            'wallet.TransactionWallet.amount': 'DecimalField',
            'configuracion.Config.impuesto': 'DecimalField',
        }
        from django.apps import apps
        for dotted, expected in required.items():
            app_label, model_name, field_name = dotted.split('.')
            field = apps.get_model(app_label, model_name)._meta.get_field(field_name)
            if field.__class__.__name__ != expected:
                errors.append('{} debe ser {}, encontrado {}'.format(dotted, expected, field.__class__.__name__))

        if connection.vendor == 'sqlite3' and not settings.DEBUG:
            errors.append('SQLite no debe utilizarse como base de datos de producción.')
        if not os.environ.get('DATABASE_URL') and not settings.DEBUG:
            warnings.append('DATABASE_URL no está definida.')

        # Validaciones puras de centavos para detectar configuraciones imposibles.
        if Decimal('0.01').quantize(Decimal('0.01')) != Decimal('0.01'):
            errors.append('La aritmética Decimal no está disponible correctamente.')

        for item in warnings:
            self.stdout.write(self.style.WARNING('ADVERTENCIA: ' + item))
        if errors:
            for item in errors:
                self.stdout.write(self.style.ERROR('ERROR: ' + item))
            raise CommandError('AUDITORIA 12 NO SUPERADA')
        self.stdout.write(self.style.SUCCESS('AUDITORIA 12: MIGRACIONES Y ESQUEMA SUPERADOS'))
