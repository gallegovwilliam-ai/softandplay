# AUDITORÍA 13 — Integridad de migraciones, liquidación legacy y movimientos de wallet

## Objetivo
Continuar desde Auditoría 12 con una revisión orientada a evitar errores silenciosos al pasar el sistema a PostgreSQL y a corregir inconsistencias detectadas en la capa financiera.

## Hallazgos corregidos

### 1. Movimiento negativo de wallet incompatible con la restricción DB
`TransactionWallet.amount` está definido como no negativo, pero `move_wallet()` podía intentar guardar un importe negativo cuando se hacía un débito.

**Corrección:** el saldo continúa moviéndose con signo, mientras que `TransactionWallet.amount` almacena el valor absoluto. La dirección queda registrada por `transaction_type` y por `FinancialLedger.entry_type`.

### 2. Dos familias de tablas Settlement
La historia de migraciones contenía una liquidación antigua en `core` y la implementación funcional actual en `pagos`. Esto podía dejar tablas `core_settlement` y `core_settlement75` innecesarias en una instalación nueva.

**Corrección:** se añadió `core.0005_remove_legacy_settlements`, que:
- comprueba primero si las tablas legacy contienen datos;
- aborta la migración si encuentra registros para evitar pérdida silenciosa;
- elimina las tablas legacy vacías;
- elimina también esos modelos del estado de migraciones.

La liquidación oficial continúa siendo la de `pagos`.

### 3. Fechas y horas sin zona horaria
Se reemplazaron usos de `datetime.datetime.now()` por `timezone.now()` en campos de fecha/hora y por `timezone.localdate()` cuando la comparación corresponde a una fecha de negocio.

Esto reduce inconsistencias con `USE_TZ=True`.

## Simulación
`audit13_simulation.py` valida:
- débito de wallet;
- crédito de wallet;
- saldo resultante;
- importe positivo almacenado en la transacción;
- dirección contable correcta.

## Estado
- AST de Python: correcto.
- Simulación financiera: correcta.
- Migración legacy protegida contra pérdida silenciosa: incorporada.
- No se ejecutó `manage.py migrate` sobre PostgreSQL real porque este entorno no tiene instalado el runtime Django del proyecto.

## Próximo paso
La Auditoría 14 debería ser un **staging real de PostgreSQL**, con una copia de la base histórica, ejecución completa de migraciones, validación de conteos/saldos/liquidaciones y pruebas transaccionales. No ejecutar la nueva migración sobre producción sin respaldo y sin revisar si existen registros en `core_settlement` o `core_settlement75`.
