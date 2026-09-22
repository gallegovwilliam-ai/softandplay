# AUDITORÍA 22 — Instalación staging y pruebas reales

## Objetivo

Convertir la preparación tecnológica de la Auditoría 21 en un entorno reproducible para ejecutar la migración real de Django 5.2/PostgreSQL/Redis.

## Cambios

- Eliminados settings obsoletos de Django moderno: `USE_L10N` y `SECURE_BROWSER_XSS_FILTER`.
- Declarado `DEFAULT_AUTO_FIELD = BigAutoField` para nuevos modelos.
- Añadido `DJANGO_LANGUAGE_CODE` configurable.
- Añadido Dockerfile reproducible con Python 3.13.
- Añadido Compose de staging con PostgreSQL 16, Redis 7, Gunicorn, Daphne y RQ Worker.
- Añadido ejemplo de variables de staging.
- Añadido CI para instalar dependencias, compilar, ejecutar `check`, `makemigrations --check --dry-run` y tests.
- Añadido `audit22_static.py` para validación sin Django instalado.

## Pruebas ejecutadas en este entorno

- Python 3.13.5: OK.
- `py_compile` de todos los Python: OK.
- `audit21_simulation.py`: OK.
- `audit22_static.py`: OK.

## Pruebas NO ejecutadas

No fue posible instalar Django/psycopg2 desde PyPI porque este entorno no tiene salida de red. Tampoco hay Docker/PostgreSQL disponibles localmente. Por ello NO se declara todavía que `manage.py check`, `migrate` o `test` hayan pasado sobre PostgreSQL real.

## Protocolo obligatorio de staging

1. Copiar `deploy/.env.staging.example` a un archivo privado.
2. Generar secretos nuevos.
3. Levantar PostgreSQL/Redis con Compose.
4. Ejecutar migraciones.
5. Ejecutar `python manage.py check`.
6. Ejecutar `python manage.py check --deploy` con la configuración de producción.
7. Ejecutar `python manage.py makemigrations --check --dry-run`.
8. Ejecutar `python manage.py test`.
9. Probar ventas concurrentes y liquidación.
10. Respaldar la base antes de cualquier migración sobre datos históricos.

Django recomienda `check --deploy` y una revisión específica de seguridad, HTTPS, rendimiento y operación antes del despliegue. La documentación oficial de Django 5.2 confirma además que 5.2 es una versión LTS y soporta Python 3.10–3.14. 
