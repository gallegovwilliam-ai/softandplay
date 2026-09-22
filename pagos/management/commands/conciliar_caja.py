from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_date
from django.utils import timezone
from pagos.cash import reconcile_day

class Command(BaseCommand):
    help = 'Genera o actualiza la conciliación de caja de una fecha.'
    def add_arguments(self, parser):
        parser.add_argument('fecha', nargs='?', help='YYYY-MM-DD; por defecto hoy')
        parser.add_argument('--usuario', type=int, required=True, help='ID del usuario administrador que genera la conciliación')
    def handle(self, *args, **options):
        day = parse_date(options['fecha']) if options.get('fecha') else timezone.localdate()
        if day is None:
            raise CommandError('Fecha inválida; use YYYY-MM-DD')
        User = get_user_model()
        user = User.objects.filter(pk=options['usuario'], is_superuser=True).first()
        if not user:
            raise CommandError('El usuario debe ser un superusuario válido')
        obj = reconcile_day(day, user)
        self.stdout.write(self.style.SUCCESS('Conciliación {}: ventas={} pagos={} reversos={} neto={}'.format(day, obj.sales, obj.payouts, obj.refunds, obj.net_cash)))
