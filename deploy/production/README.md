# Lanzamiento de SoftAndPlay

## Orden recomendado

1. Preparar un VPS Ubuntu LTS actualizado.
2. Instalar Docker Engine y Docker Compose Plugin.
3. Apuntar `appsoftandplay.com` y `www.appsoftandplay.com` a la IP del VPS.
4. Copiar `.env.production.example` a `.env.production` y cambiar todos los secretos.
5. Crear los directorios `certbot/www` y `certbot/conf`.
6. Emitir el certificado TLS de Let's Encrypt antes de levantar el nginx HTTPS definitivo.
7. Ejecutar `deploy/scripts/deploy_production.sh`.
8. Crear el superusuario con `python manage.py createsuperuser` dentro del contenedor web.
9. Probar login, compra, partida, WebSocket, liquidación y pagos.
10. Programar backups de PostgreSQL y comprobar periódicamente una restauración.

## Comandos útiles

```bash
docker compose --env-file deploy/production/.env.production -f deploy/production/docker-compose.yml ps
docker compose --env-file deploy/production/.env.production -f deploy/production/docker-compose.yml logs --tail=200 web
docker compose --env-file deploy/production/.env.production -f deploy/production/docker-compose.yml logs --tail=200 asgi
```

No guardar `.env.production`, claves, certificados privados ni backups en Git.
