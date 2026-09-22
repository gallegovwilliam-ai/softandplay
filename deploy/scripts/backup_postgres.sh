#!/bin/sh
set -eu
mkdir -p backups
STAMP="$(date +%Y%m%d_%H%M%S)"
FILE="backups/softandplay_${STAMP}.dump"
docker compose --env-file deploy/production/.env.production -f deploy/production/docker-compose.yml exec -T postgres pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc > "$FILE"
echo "Backup creado: $FILE"
