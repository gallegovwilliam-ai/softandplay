# Auditoría 7 — Concurrencia, integridad e idempotencia

## Objetivo

La Auditoría 7 se concentró en evitar que dos solicitudes simultáneas puedan:

- sacar la misma balota;
- iniciar una partida dos veces;
- procesar dos veces el mismo pago;
- eliminar una partida que ya inició o terminó;
- aceptar una balota manual fuera de rango o ya utilizada;
- registrar movimientos financieros sin clave idempotente.

## Cambios aplicados

### 1. Bloqueo de partida durante el sorteo
`JuegoEnLinea` y `JuegoEnLinea75` ahora cargan la partida con `select_for_update()` dentro de `transaction.atomic()`.

Esto serializa las operaciones de una misma partida en PostgreSQL y evita que dos procesos trabajen sobre el mismo estado de balotas al mismo tiempo.

### 2. Bingo 75: balota manual segura
La balota recibida por `numeroSelecto` se convierte a entero, se valida contra 1–75 y se rechaza si ya salió.

Antes se comparaba una cadena recibida por HTTP contra enteros, lo que podía permitir inconsistencias.

### 3. Inicio de partida idempotente
Las funciones de inicio ahora bloquean la fila, verifican que la partida no esté terminada ni iniciada y devuelven `409` ante un intento duplicado.

### 4. Eliminación protegida
Una partida iniciada o terminada ya no puede eliminarse desde la vista administrativa.

Esto protege el histórico de una partida que puede tener jugadas, ganadores y movimientos financieros asociados.

### 5. Ledger financiero más estricto
`ledger_entry()` ahora exige:

- una `unique_key` no vacía;
- un tipo válido (`CREDITO` o `DEBITO`);
- importe distinto de cero.

### 6. Pago con estado inconsistente
Si un cartón aparece como `pago=True` pero no existe su `PaymentRecord`, el sistema ahora detiene la operación y reporta inconsistencia, en lugar de devolver un pago aparentemente correcto con `payment_id=None`.

### 7. Fechas con timezone
Se sustituyeron varios usos de `datetime.datetime.now()` por `timezone.now()` y las consultas de `DateField` por `timezone.localdate()` en las áreas revisadas.

## Prueba de concurrencia

`audit7_simulation.py` simula múltiples trabajadores concurrentes para:

- extracción de balotas;
- venta/asignación de cartones;
- pago idempotente.

El resultado esperado es:

`AUDITORIA 7: CONCURRENCIA E IDEMPOTENCIA SUPERADAS`

## Limitación importante

Estas pruebas son una simulación de la lógica de exclusión mutua. La validación definitiva debe ejecutarse con Django sobre PostgreSQL, porque allí se comprueba el comportamiento real de `select_for_update()`, restricciones únicas y transacciones bajo concurrencia.

## Próxima auditoría recomendada

1. Crear un servicio formal de **cierre/settlement de partida** para que el premio no dependa de visitar una página.
2. Completar el libro financiero con ventas, recargas, anulaciones y reversos.
3. Hacer inmutable el `FinancialLedger` a nivel de aplicación/admin.
4. Migrar definitivamente los importes antiguos `CharField` a `DecimalField`.
5. Crear conciliación diaria de caja.
6. Ejecutar pruebas reales de carga/concurrencia sobre PostgreSQL.
