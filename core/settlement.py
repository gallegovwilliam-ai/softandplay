"""Compatibilidad histórica: la liquidación financiera vive en pagos.settlement."""
from pagos.settlement import settle_partida, settle_partida75

__all__ = ['settle_partida', 'settle_partida75']
