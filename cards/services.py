from django.db import transaction
from .models import Carton, Carton75, Impresion, Impresion75


def _allocate(partida, header, quantity, *, is75=False):
    """Allocate unique cartons while the caller holds the partida lock."""
    if quantity <= 0:
        raise ValueError('La cantidad de cartones debe ser positiva')

    Card = Carton75 if is75 else Carton
    Impression = Impresion75 if is75 else Impresion

    # The partida lock serializes every allocation path for that game.
    # Lock the candidate carton rows as an additional DB-level safeguard.
    used = Impression.objects.filter(propietario__partida=partida).values('carton_id')
    available = list(
        Card.objects.select_for_update()
        .exclude(pk__in=used)
        .order_by('pk')[:quantity]
    )
    if len(available) != quantity:
        raise ValueError('No hay suficientes cartones disponibles')

    return [
        Impression.objects.create(propietario=header, carton=carton)
        for carton in available
    ]


def allocate_cartons(partida, header, quantity, *, is75=False):
    """Public transactional allocation API for future payment providers."""
    with transaction.atomic():
        return _allocate(partida, header, quantity, is75=is75)
