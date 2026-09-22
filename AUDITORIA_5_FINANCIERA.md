# Auditoría 5 — Fortalecimiento financiero

## Implementado
- Ledger financiero inmutable con clave idempotente.
- Registro de premios y pagos separado del modelo de cartón.
- Montos decimales paralelos para migración segura desde campos históricos de texto.
- Migración de datos existentes hacia los campos Decimal.
- Cálculo de premio con `Decimal` y redondeo a centavos.
- Prevención de valores negativos e inconsistencias básicas de premio/impuesto/neto.
- Pago protegido con transacción y bloqueo del cartón.
- Pago idempotente: repetir la operación no genera un segundo movimiento financiero.
- Registro de quién aprobó el pago, método, referencia, fecha e IP.
- Ledger para generación de premio y desembolso del premio.
- Wallet con saldo decimal y servicio transaccional para movimientos futuros.
- Restricción para impedir saldo decimal negativo.

## Compatibilidad
Los campos históricos de texto se conservan temporalmente para no romper las pantallas existentes. Los nuevos campos Decimal son la fuente financiera recomendada y se mantienen sincronizados en el flujo corregido.

## Pendiente antes de producción
1. Migrar definitivamente las pantallas y formularios para usar únicamente DecimalField.
2. Definir la regla exacta de cartones vendidos: generados, vendidos, verificados o pagados.
3. Definir tratamiento legal/fiscal de impuestos y premios según jurisdicción.
4. Crear conciliación diaria y cierre de caja.
5. Crear pruebas automatizadas de venta, premio, pago duplicado, concurrencia y reversión.
6. Revisar todos los reportes para que lean el ledger y no sumen campos históricos.
7. Ejecutar migraciones en una copia de la base y verificar saldos antes de tocar producción.
