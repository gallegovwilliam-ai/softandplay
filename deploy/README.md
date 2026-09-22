# SoftAndPlay — staging local

Este compose crea un entorno de staging con PostgreSQL 16, Redis 7, Gunicorn, Daphne y RQ Worker.

## Uso

1. Copiar `deploy/.env.staging.example` a `deploy/.env.staging`.
2. Sustituir secretos.
3. Desde la raíz del proyecto ejecutar:

```bash
docker compose --env-file deploy/.env.staging -f deploy/docker-compose.staging.yml up --build
```

Antes de usar producción, ejecutar `python manage.py check --deploy` con la configuración real de producción. Django recomienda esta comprobación como parte de la lista de despliegue. 

No se debe reutilizar la contraseña ni el `DJANGO_SECRET_KEY` de staging en producción.
