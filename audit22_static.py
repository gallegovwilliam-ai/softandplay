from pathlib import Path
import ast
import re

ROOT = Path(__file__).resolve().parent
errors=[]
warnings=[]

req=(ROOT/'requeriments').read_text(encoding='utf-8')
for pin in ('django==5.2.17','channels==4.3.2','channels-redis==4.3.0','daphne==4.2.3','psycopg2-binary>=2.9.10'):
    if pin.lower() not in req.lower(): errors.append('Falta requisito: '+pin)

settings=(ROOT/'app/settings.py').read_text(encoding='utf-8')
for old in ('USE_L10N','SECURE_BROWSER_XSS_FILTER'):
    if re.search(r'^\s*'+re.escape(old)+r'\s*=', settings, re.M): errors.append('Setting obsoleto: '+old)
if "DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'" not in settings:
    errors.append('Falta DEFAULT_AUTO_FIELD')

for p in ROOT.rglob('*.py'):
    if any(part in {'migrations','__pycache__'} for part in p.parts) or p.name.startswith('audit') or p.name.startswith('auditoria'): continue
    try: text=p.read_text(encoding='utf-8')
    except UnicodeDecodeError: continue
    for old in ('django.core.urlresolvers','ugettext','force_text','smart_text','request.is_ajax','django.conf.urls'):
        if old in text: errors.append(f'API legacy {old}: {p.relative_to(ROOT)}')
    try: ast.parse(text)
    except SyntaxError as exc: errors.append(f'SyntaxError {p.relative_to(ROOT)}: {exc}')

if not (ROOT/'.python-version').exists() or (ROOT/'.python-version').read_text().strip() not in {'3.13','3.13.0'}:
    errors.append('Python objetivo no es 3.13')
if not (ROOT/'deploy/docker-compose.staging.yml').exists(): errors.append('Falta compose staging')
if not (ROOT/'.github/workflows/audit22.yml').exists(): errors.append('Falta CI Audit 22')

print('AUDITORIA 22 ESTATICA')
if errors:
    for e in errors: print('ERROR:',e)
    raise SystemExit(1)
print('OK: stack objetivo, APIs modernas, settings y artefactos staging/CI validados.')
if warnings:
    for w in warnings: print('WARN:',w)
