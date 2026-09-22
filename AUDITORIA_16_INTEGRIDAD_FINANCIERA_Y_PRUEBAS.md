# AUDITORÍA 16 — Integridad financiera, ventas directas y pruebas

## Cambios realizados

1. **Venta directa de cartones**: `cards.views.tikect` y `tikect75` ahora registran `SaleRecord`/`SaleRecord75` y su asiento de crédito mediante `register_sale`/`register_sale75`, dentro de la misma transacción. Esto corrige una fuga contable donde la venta directa podía imprimir cartones sin entrar al pool financiero de liquidación.
2. **Asignación**: se conserva el servicio centralizado `allocate_cartons`, con bloqueo de partida y cartones candidatos.
3. **Importación Excel**: las cargas de bloques de 1000 cartones quedan dentro de `transaction.atomic()` y validan que el bloque solicitado exista completo antes de insertar.
4. **Pagos**: `PaymentRecord` y `PaymentRecord75` pasan a tener estado inicial `PENDIENTE`; una aprobación debe ser explícita a través del flujo financiero.
5. **Compras bancarias**: las solicitudes quedan bajo transacción y bloqueo de partida, y usan `timezone.localdate()` para campos `DateField`.
6. **Chance**: la eliminación de loterías activas pasa de GET a POST con CSRF.
7. **Prueba reproducible**: se añade `audit16_simulation.py`.

## Riesgos detectados para la siguiente etapa

- `validar_email` conserva un flujo de autenticación por enlace que debe migrarse a un token firmado/expirable para evitar suplantación.
- La integración real de PayPal/webhook sigue pendiente.
- Django 3.0.7 sigue siendo una versión fuera de soporte; se recomienda planificar actualización escalonada.
- Debe ejecutarse `manage.py check`, `migrate` y pruebas reales sobre PostgreSQL de staging antes de producción.
- Debe confirmarse la zona horaria de negocio (`America/Mexico_City`) antes del despliegue definitivo.

## Validaciones realizadas

- `py_compile` de los módulos modificados: OK.
- Simulación pura de concurrencia/idempotencia/estado de pagos: OK.
- Las pruebas Django/PostgreSQL reales no se ejecutaron en este entorno porque no está disponible un runtime Django compatible con el proyecto.
