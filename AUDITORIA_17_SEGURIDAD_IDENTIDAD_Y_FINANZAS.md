# Auditoría 17 — Seguridad de identidad y finanzas

## Objetivo
Reforzar la validación de correo y revisar que la capa financiera no dependa de identificadores manipulables por URL.

## Cambios
- Se eliminó el antiguo enlace de validación basado en `pk + email`.
- La validación usa `default_token_generator` de Django y `uidb64/token`.
- El endpoint de validación ya no inicia sesión automáticamente en ninguna cuenta.
- Se añadió endpoint autenticado para solicitar nuevamente el correo de validación.
- Los usuarios nuevos quedan `validado=False` y reciben el enlace al registrarse.
- Se protegió el acceso de `HTTP_USER_AGENT` con `.get()`.
- Se conserva la idempotencia de `SaleRecord`/`SaleRecord75` y la asignación transaccional de cartones de Auditorías anteriores.
- Se añadió `core/management/commands/auditoria17.py`.
- Se añadió `audit17_simulation.py`.

## Pruebas ejecutadas
- Compilación sintáctica de todos los `.py`.
- Simulación de asignación sin duplicados.
- Simulación de idempotencia financiera.
- Revisión AST para evitar `request.is_ajax()`.
- Revisión de migraciones duplicadas.

## Limitación
No se ejecutó `manage.py test/check/migrate` contra PostgreSQL real en este entorno. La validación definitiva debe hacerse en staging con PostgreSQL y datos de prueba.
