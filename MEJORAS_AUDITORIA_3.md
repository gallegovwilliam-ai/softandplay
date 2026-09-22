# Mejoras aplicadas - Auditoría 3

Esta versión endurece el proyecto SoftAndPlay antes de una primera puesta en producción.

## Cambios

- Secretos de Django y correo pasan a variables de entorno.
- `DEBUG` queda desactivado por defecto.
- `ALLOWED_HOSTS` deja de aceptar `*`.
- CORS deja de estar abierto globalmente.
- `STATIC_ROOT` y `MEDIA_ROOT` dejan de depender de rutas del equipo del desarrollador.
- Se añade soporte opcional para PostgreSQL mediante `DATABASE_URL`.
- Se incorporan `social-auth-app-django`, `requests`, `dj-database-url` y `psycopg2-binary`.
- Se fija Python 3.8.10 por compatibilidad con el Django 3.0.7 heredado.
- El registro público ya no permite seleccionar Administrador.
- Listado, actualización y baja de usuarios quedan restringidos al superusuario.
- Bajas de usuarios y partidas pasan a POST.
- Inicio de partidas pasa a POST.
- La generación de partidas y su modificación quedan restringidas al superusuario.
- La ejecución de la balota queda restringida al superusuario y protegida con transacción atómica.
- Las ventas de cartones pasan a POST, validan cantidad (1-100), verifican rol y seleccionan cartones disponibles dentro de una transacción.
- El procesamiento de pagos pasa a POST y exige superusuario.
- Los mensajes sobre cartones ganadores pasan a POST y solo pueden enviarlos el propietario o un administrador.
- Las contraseñas de la API se marcan como `write_only` y requieren al menos 8 caracteres.
- Se agregan restricciones únicas para `(fecha, partida)` y `(partida, balota)` para evitar duplicados.
- WebSocket de partidas rechaza usuarios anónimos y no permite que un usuario normal dispare eventos globales.

## Importante antes de desplegar

1. Rotar la contraseña del correo que estaba almacenada en la versión original.
2. Generar una nueva `DJANGO_SECRET_KEY`.
3. Configurar PostgreSQL y Redis en producción.
4. Ejecutar migraciones antes de arrancar el servicio.
5. Ejecutar `collectstatic`.
6. Configurar Nginx/HTTPS y los valores reales de `DJANGO_ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` y `CORS_ALLOWED_ORIGINS`.
7. Hacer pruebas de compra, concurrencia, premios y pagos con una base de datos de prueba antes de usar dinero real.

## Pendiente para la siguiente fase

- Migración de importes de `CharField/float/IntegerField` a `DecimalField/Decimal`.
- Ledger financiero inmutable para pagos y wallet.
- Motor central de premios y patrones.
- Auditoría de acciones administrativas.
- Grupos WebSocket por partida.
- PostgreSQL como base definitiva y estrategia de backups.
