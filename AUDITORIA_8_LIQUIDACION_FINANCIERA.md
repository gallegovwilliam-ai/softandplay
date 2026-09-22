# AUDITORÍA 8 — LIQUIDACIÓN FINANCIERA

Cambios aplicados:

- Liquidación formal e idempotente para Partida y Bingo 75.
- El cierre de partida ejecuta la liquidación dentro de la misma transacción.
- Los premios se calculan y registran al cerrar la partida, no al consultar la pantalla del ganador.
- Settlement y PaymentRecord quedan en administración como solo lectura.
- Se protege el consecutivo diario mediante PartidaSequence.
- Se mantiene Decimal como fuente financiera y los campos antiguos como compatibilidad temporal.
- Se valida pozo, porcentajes, impuesto y conciliación a centavos.
- El historial financiero conserva claves únicas para evitar doble registro.

Limitación del entorno de auditoría: no fue posible ejecutar la suite Django completa porque el entorno de análisis no tiene Django instalado. Se ejecutaron compilación estática y simulaciones puras.
