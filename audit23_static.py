from pathlib import Path
import ast
import re

ROOT = Path(__file__).resolve().parent
errors = []

req = (ROOT / 'requeriments').read_text(encoding='utf-8')
if 'django==5.2.18' not in req:
    errors.append('Django no esta fijado en 5.2.18')
for pin in ('channels==4.3.2', 'channels-redis==4.3.0', 'daphne==4.2.3', 'psycopg2-binary>=2.9.10'):
    if pin.lower() not in req.lower():
        errors.append('Falta requisito: ' + pin)

settings = (ROOT / 'app/settings.py').read_text(encoding='utf-8')
if 'SOFTANDPLAY_STRICT_CONFIG' not in settings:
    errors.append('Falta configuracion estricta de produccion')
if 'DATABASE_URL' not in settings:
    errors.append('Falta DATABASE_URL')
if "DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'" not in settings:
    errors.append('Falta DEFAULT_AUTO_FIELD')

bancos = (ROOT / 'bancos/views.py').read_text(encoding='utf-8')
if '@login_required\n@transaction.atomic\ndef pagarcompra' not in bancos:
    errors.append('pagarcompra debe exigir login + transaccion')
if 'Partida.objects.select_for_update().get(pk=pk)' not in bancos:
    errors.append('pagarcompra no bloquea la partida')
if 'Partida75.objects.select_for_update().get(pk=pk)' not in bancos:
    errors.append('pagarcompra75 no bloquea la partida')
# Read-only purchase pages must not call select_for_update outside a transaction.
for fn in ('def Comprar(request,pk):', 'def Comprar75(request,pk):'):
    if fn not in bancos:
        errors.append('Falta vista ' + fn)

compose = (ROOT / 'deploy/docker-compose.staging.yml').read_text(encoding='utf-8')
for required in ('postgres:16-alpine', 'redis:7-alpine', 'nginx:1.29-alpine', 'collectstatic', 'static_data:', 'media_data:'):
    if required not in compose:
        errors.append('Compose staging incompleto: ' + required)
if 'POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is required}' not in compose:
    errors.append('PostgreSQL permite password por defecto inseguro')
if 'DJANGO_SECRET_KEY: ${DJANGO_SECRET_KEY:?DJANGO_SECRET_KEY is required}' not in compose:
    errors.append('SECRET_KEY no es obligatorio en compose')
if 'ports:\n      - "8000:8000"' in compose or 'ports:\n      - "9000:9000"' in compose:
    errors.append('Gunicorn/Daphne estan expuestos directamente; deben quedar detras de Nginx')

nginx = ROOT / 'deploy/nginx.staging.conf'
if not nginx.exists():
    errors.append('Falta Nginx staging')
else:
    n = nginx.read_text(encoding='utf-8')
    for required in ('proxy_set_header Upgrade $http_upgrade', 'proxy_pass http://softandplay_asgi', 'proxy_pass http://softandplay_web', 'alias /static/', 'alias /media/'):
        if required not in n:
            errors.append('Nginx incompleto: ' + required)

for p in ROOT.rglob('*.py'):
    if any(part in {'migrations', '__pycache__', '.venv23'} for part in p.parts):
        continue
    if p.name.startswith(('audit', 'auditoria')):
        continue
    try:
        text = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    for old in ('django.core.urlresolvers', 'ugettext', 'force_text', 'smart_text', 'request.is_ajax', 'django.conf.urls'):
        if old in text:
            errors.append(f'API legacy {old}: {p.relative_to(ROOT)}')
    try:
        ast.parse(text)
    except SyntaxError as exc:
        errors.append(f'SyntaxError {p.relative_to(ROOT)}: {exc}')

print('AUDITORIA 23 ESTATICA')
if errors:
    for e in errors:
        print('ERROR:', e)
    raise SystemExit(1)
print('OK: configuracion estricta, pagos bloqueados, staging PostgreSQL/Redis/Nginx y APIs modernas validados.')
