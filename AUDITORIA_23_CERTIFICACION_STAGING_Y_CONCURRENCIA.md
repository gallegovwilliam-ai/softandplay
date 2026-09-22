# AUDITORIA 23 — CERTIFICACIÓN DE STAGING Y CONCURRENCIA

## Objetivo
Pasar de validaciones estáticas a una preparación reproducible para ejecutar PostgreSQL, Redis, Gunicorn, Daphne, RQ y Nginx en staging.

## Hallazgos corregidos
1. `pagarcompra` comprobaba el estado de la partida sin bloquearla; ahora usa `select_for_update()` dentro de `transaction.atomic()`.
2. `pagarcompra` y `pagarcompra75` ahora exigen autenticación.
3. Las vistas de compra de solo lectura dejaron de usar `select_for_update()` fuera de una transacción.
4. Docker Compose ya no publica directamente Gunicorn/Daphne; quedan detrás de Nginx.
5. Se añadió Nginx para HTTP y WebSocket.
6. `collectstatic` se ejecuta en la etapa de migración y comparte el volumen estático.
7. PostgreSQL y `DJANGO_SECRET_KEY` son obligatorios en el compose de staging.
8. Se añadió `SOFTANDPLAY_STRICT_CONFIG` para impedir configuraciones de producción inseguras.
9. Django se fijó en 5.2.18.

## Pruebas disponibles en este entorno
- Compilación Python: ejecutable localmente.
- Auditoría estática: `audit23_static.py`.
- Simulación de 10 vendedores contra los últimos 10 cartones: `audit23_simulation.py`.
- Simulación financiera e idempotencia.
- Verificación de APIs Django obsoletas.

## Limitación
Esta máquina no dispone de Docker/PostgreSQL y no pudo descargar paquetes desde PyPI por resolución DNS. Por ello no se certifican todavía `manage.py check`, `migrate`, `test` ni una concurrencia PostgreSQL real.

## Criterio para certificación real
La certificación final debe ejecutarse en un host con Docker o PostgreSQL + Redis y debe comprobar:
- migraciones limpias;
- `check --deploy`;
- suite Django;
- 10+ vendedores simultáneos con últimos cartones;
- una sola asignación por cartón;
- una sola venta/asiento por operación;
- liquidación y reversos conciliados;
- WebSocket/Redis/Daphne;
- backups y recuperación.
