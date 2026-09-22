# Auditoría 18 — Ciclo financiero y operación segura

## Objetivo
Revisar la base de Auditoría 17 concentrándose en integridad del ciclo venta → registro financiero → pago → reverso, además de operaciones administrativas peligrosas y solicitudes de pago externas.

## Correcciones aplicadas

### 1. Eliminación de compras pendientes
Se detectó una condición invertida en `deleteCompras`: una petición no autorizada podía entrar en la rama que borraba registros. Ahora exige POST + superusuario y solamente elimina encabezados aún no verificados.

### 2. Reprocesamiento de pagos anulados
Se detectó que `void_payment` marca el pago como ANULADO y libera `carton.pago`, mientras `_payment` podía volver a reutilizar ese mismo registro OneToOne. Eso podía producir un reintento contable con la misma clave de ledger.

Ahora un `PaymentRecord` ANULADO no puede ser reaprobado por `_payment`; debe existir un proceso explícito de nuevo pago/recovery antes de volver a pagar.

### 3. Auditoría ORM 18
Se añadió `core/management/commands/auditoria18.py` para revisar:
- cantidades e importes inválidos en ventas;
- importes negativos en pagos;
- pagos aprobados sin fecha de aprobación;
- referencias incompletas en reversos;
- ventas aprobadas sin asiento financiero VENTA;
- solicitudes PayPal que permanecen pendientes.

### 4. PayPal
La solicitud PayPal continúa deliberadamente en estado PENDIENTE hasta contar con confirmación real del proveedor. No se entrega cartón ni se registra una venta por una referencia enviada desde el navegador.

## Pruebas estáticas
- `python3 -m py_compile $(find . -name '*.py' -type f)` → OK.
- `python3 audit18_simulation.py` → `AUDITORIA 18 SIMULACION: OK`.

## Limitación
No se ejecutaron `manage.py check`, migraciones ni pruebas transaccionales reales sobre PostgreSQL porque este entorno no contiene el runtime Django compatible ni una base PostgreSQL de staging configurada.

## Recomendación Auditoría 19
Completar el adaptador real del proveedor de pagos/webhook, preparar staging PostgreSQL y ejecutar pruebas de concurrencia reales con transacciones simultáneas.
