# SoftAndPlay — Auditoría 4: integridad financiera y trazabilidad

## Mejoras incorporadas

1. **Registro de auditoría**
   - Nuevo modelo `core.AuditLog`.
   - Registra actor, acción, objeto, metadatos, IP y fecha.

2. **Registro de pagos independiente**
   - `pagos.PaymentRecord` para cartones de lotería.
   - `pagos.PaymentRecord75` para Bingo 75.
   - Estados: PENDIENTE, APROBADO, RECHAZADO, ANULADO.
   - Importe, impuesto, neto, método, referencia y administrador que procesa.
   - Un registro de pago por cartón mediante `OneToOneField`.

3. **Pagos idempotentes y transaccionales**
   - El pago se procesa con `transaction.atomic()` y `select_for_update()`.
   - Un segundo intento no genera un segundo pago.
   - El monto se toma del cartón, no de parámetros enviados por el navegador.
   - Se valida que el cartón sea ganador y que los importes no sean negativos.
   - Método y referencia tienen límites de longitud.

4. **Dinero en Decimal (fase de transición)**
   - `Wallet.balance_decimal`.
   - `TransactionWallet.amount_decimal`.
   - Migración que copia los valores históricos desde los campos enteros.
   - Se mantienen temporalmente los campos antiguos para no romper el sistema existente.

5. **Cálculo de ganador protegido**
   - Las vistas de ganador usan transacción y bloqueo de fila para reducir carreras concurrentes durante el cálculo existente.

6. **Middleware de sesión corregido**
   - Se corrigieron imports e indentación del middleware `LIMITARUSER` y se utiliza la propiedad moderna `is_authenticated`.

## Próximo paso recomendado

La siguiente fase debe migrar progresivamente `monto`, `impuesto`, `total`, `monto_carton`, `monto_acumulado` y porcentajes a `DecimalField`, ejecutar una migración de datos verificable y sustituir los cálculos con `float` por `Decimal`. Después se puede construir el ledger completo de ventas/premios/pagos y pruebas de conciliación.
