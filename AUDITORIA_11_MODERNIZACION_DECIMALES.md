# AUDITORÍA 11 — Modernización de datos financieros

## Objetivo
Convertir el núcleo financiero a tipos numéricos nativos y eliminar la dependencia operativa de `CharField`/`float` para dinero y porcentajes.

## Cambios
- `Partida` y `Partida75`: montos de premios, precio de cartón, acumulado, impuesto y total pasan a `DecimalField(14,2)`.
- Los 10 porcentajes de premio pasan a `DecimalField(5,2)` y se validan entre 0 y 100.
- `Impresion` e `Impresion75`: monto, impuesto y total pasan a `DecimalField(14,2)`.
- `Config.impuesto` pasa a `DecimalField(5,2)` con restricción 0–100.
- `Wallet.balance` y `TransactionWallet.amount` pasan a `DecimalField(14,2)`.
- `cartones_vendidos` pasa a `PositiveIntegerField`.
- Las migraciones copian primero los valores de los campos `_decimal` existentes y luego convierten los campos canónicos; los campos temporales `_decimal` se eliminan.
- Los servicios financieros ya trabajan directamente con los campos canónicos.
- Se eliminaron conversiones `float()` del núcleo financiero/reports revisados.
- Las reglas de creación/modificación de partidas validan precio y suma de porcentajes antes de consumir el consecutivo.
- No se permite modificar configuración financiera de una partida iniciada o finalizada.
- Se añadieron restricciones de base de datos para impedir montos negativos y porcentajes fuera de rango.
- `wallet.move_wallet` ahora usa una clave idempotente antes de mover saldo, evitando aplicar dos veces un mismo movimiento.
- Fechas de wallet/notificaciones/mensajes usan `timezone.now()`.

## Pruebas disponibles
`audit11_simulation.py` verifica cálculo de pozo, impuesto, conciliación y rechazo de configuraciones inválidas.

Resultado: `AUDITORIA 11: DECIMALES, REGLAS Y VALIDACIONES SUPERADAS`

## Limitación
El entorno de revisión no tiene Django 3.0.7 instalado, por lo que no se ejecutó `manage.py migrate` ni la suite Django contra una base real. Antes de producción debe hacerse una copia de seguridad y probar las migraciones primero en una copia de PostgreSQL.
