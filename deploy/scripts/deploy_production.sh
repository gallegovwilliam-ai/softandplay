#!/bin/sh
set -eu
cd "$(dirname "$0")/../.."
ENV_FILE=deploy/production/.env.production
COMPOSE=deploy/production/docker-compose.yml
[ -f "$ENV_FILE" ] || { echo "Falta $ENV_FILE"; exit 1; }
docker compose --env-file "$ENV_FILE" -f "$COMPOSE" config >/dev/null
docker compose --env-file "$ENV_FILE" -f "$COMPOSE" build
docker compose --env-file "$ENV_FILE" -f "$COMPOSE" up -d postgres redis
docker compose --env-file "$ENV_FILE" -f "$COMPOSE" run --rm migrate
docker compose --env-file "$ENV_FILE" -f "$COMPOSE" up -d web asgi worker nginx
docker compose --env-file "$ENV_FILE" -f "$COMPOSE" ps
