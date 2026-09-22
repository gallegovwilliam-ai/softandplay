# Auditoría 19 — PostgreSQL, concurrencia y preparación de producción

## Objetivo
Llevar la revisión desde controles estáticos hacia una base preparada para staging real, reforzando endpoints destructivos, configuración operativa e invariantes financieras.

## Correcciones aplicadas

### 1. Clientes
- `ClienteDelete` ahora exige POST.
- Solo el propietario puede desactivar su cliente; el superusuario conserva administración global.
- `ClienteUpdate` limita el queryset al propietario salvo superusuario.

### 2. Lectura de partidas
Se eliminó `select_for_update()` de las vistas GET de compra donde no había una transacción. El bloqueo se conserva en los endpoints que realmente crean/aprueban operaciones y están dentro de `transaction.atomic()`.

### 3. Zona horaria configurable
`TIME_ZONE` ahora acepta `DJANGO_TIME_ZONE`. El valor heredado `America/Mexico_City` se conserva por compatibilidad hasta confirmar la zona operativa.

### 4. Auditor automático
Se añadió `core/management/commands/auditoria19.py` para revisar:
- migraciones duplicadas;
- base de datos y configuración de producción;
- endpoints destructivos;
- importes y cantidades financieras inválidas;
- pagos aprobados sin fecha de aprobación.

### 5. Simulación
Se añadió `audit19_simulation.py` con pruebas de:
- últimos cartones disponibles;
- conservación financiera;
- idempotencia de claves;
- PayPal pendiente.

## Validación disponible en este entorno
- Compilación Python: se ejecuta como control estático.
- Simulación pura Python: `AUDITORIA 19 SIMULACION: OK`.
- No se afirma una prueba PostgreSQL real porque el entorno de trabajo no tiene configurado el runtime Django compatible ni una instancia PostgreSQL de staging.

## Bloqueadores antes de producción
1. Django 3.0.7 y varias dependencias son antiguas; debe planificarse una actualización por etapas.
2. Ejecutar `manage.py check`, `migrate` y tests sobre PostgreSQL real.
3. Ejecutar concurrencia real con dos o más transacciones simultáneas.
4. Confirmar `DJANGO_TIME_ZONE` y los dominios HTTPS/CSRF.
5. Completar la integración real de proveedor de pagos/webhook antes de aceptar pagos externos.
