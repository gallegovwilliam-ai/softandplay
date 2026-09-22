# AUDITORÍA 10 — Producción, reversos e integridad financiera

## Objetivo
Cerrar el circuito de correcciones financieras sin borrar ni modificar el histórico y reforzar el entorno de producción.

## Cambios aplicados

1. **Reversos compensatorios**
   - `pagos/reversals.py` agrega reversos para ventas y pagos.
   - Nunca modifica ni elimina el asiento original.
   - La clave `REVERSO:<unique_key>` hace el reverso idempotente.
   - `FinancialReversal` documenta la relación entre asiento original y compensatorio.

2. **Integridad del ledger**
   - `FinancialLedger.amount` exige valor positivo mediante restricción de base de datos.
   - La aplicación exige `unique_key` no vacío.
   - Los asientos continúan siendo inmutables.

3. **Conciliación de caja**
   - La caja diaria cuenta ventas aprobadas y pagos reales.
   - Los antiguos asientos de premio referenciados por `Impresion/Impresion75` ya no se suman como pagos de caja para evitar doble conteo.

4. **Producción**
   - Channels usa `REDIS_URL` o `REDIS_HOST/REDIS_PORT` en vez de una dirección fija.
   - Redis RQ admite DB y contraseña por variables de entorno.
   - `SECURE_SSL_REDIRECT` queda activado por defecto cuando `DEBUG=False`.
   - Se añadieron políticas de cookies y `SECURE_REFERRER_POLICY`.
   - Nuevo comando `python manage.py check_produccion` bloquea configuraciones con DEBUG activo, secret insegura o SQLite.

5. **Administración**
   - Los reversos financieros son de solo lectura en el admin.

## Pruebas realizadas

- Simulación de venta y pago.
- Reverso de crédito a débito.
- Reverso de débito a crédito.
- Segundo intento de reverso rechazado por idempotencia.
- Conciliación conceptual de créditos y débitos.
- `compileall` sobre todo el proyecto.

Resultado:

`AUDITORIA 10: REVERSOS, CAJA Y GATE DE PRODUCCION SUPERADOS`

## Limitación importante

El entorno de auditoría no tiene Django instalado ni un PostgreSQL de ejecución, por lo que no se ejecutaron aquí `manage.py test`, migraciones reales ni pruebas de bloqueo sobre PostgreSQL. Antes de operar con dinero real se debe ejecutar en un entorno de staging con PostgreSQL, Redis y las mismas variables de producción.

## Bloqueadores antes de producción

- El proyecto mantiene Django 3.0.7 y Python 3.8.10 por compatibilidad con el código legado. Ambas versiones son antiguas y deben actualizarse en una fase de modernización antes de una exposición pública prolongada.
- Los campos monetarios históricos `CharField` siguen presentes por compatibilidad. Los `DecimalField` son la fuente usada por el circuito financiero nuevo; su eliminación definitiva requiere migración de formularios, vistas, plantillas e importadores.
- Deben probarse las rutas reales de anulación desde la interfaz antes de habilitarlas a operadores.
- Deben configurarse PostgreSQL, Redis, HTTPS, backups, rotación de secretos y monitoreo en staging.
