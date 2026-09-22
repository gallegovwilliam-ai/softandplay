# AUDITORIA 21 — Migración tecnológica especial

## Objetivo

Preparar SoftAndPlay para abandonar el stack obsoleto de Django 3.0.7/Python 3.8 y pasar a un stack moderno sin tocar todavía la lógica financiera de negocio de las auditorías anteriores.

## Hallazgos

### 1. Django 3.0.7 estaba fuera de soporte

El proyecto usaba Django 3.0.7. La documentación oficial de Django identifica la serie 3.0 como insegura y fuera de soporte. Se selecciona Django 5.2 LTS como destino, no Django 6.x, para reducir el salto de compatibilidad durante esta etapa.

### 2. Python 3.8.10 era insuficiente para el objetivo moderno

El proyecto declaraba Python 3.8.10. El objetivo pasa a Python 3.13. Django 5.2 soporta Python 3.10–3.14 y Channels 4.2.1 añadió soporte oficial para Django 5.2/Python 3.13.

### 3. ASGI/Channels era legado

`get_default_application()` de Channels 2 fue sustituido por el patrón ASGI moderno de Django + Channels: `get_asgi_application()`, `ProtocolTypeRouter` con handler HTTP explícito y consumidores mediante `.as_asgi()`.

### 4. APIs eliminadas de Django moderno

Se corrigieron:

- `ugettext_lazy` → `gettext_lazy`.
- `django.core.urlresolvers` → `django.urls`.
- `django.conf.urls.url` → `django.urls.re_path`.
- imports obsoletos de handlers.

### 5. Importación de cartones

La carga de los archivos `.xlsx` dejó de depender de `xlrd.open_workbook()` y usa `openpyxl.load_workbook()`, coherente con los archivos `DB.xlsx`/`DB75.xlsx` del proyecto.

### 6. Dependencias antiguas

Se actualizó el archivo `requeriments` a una base moderna, conservando `requeriments-legacy-auditoria20.txt` como referencia histórica.

## Stack objetivo

- Python 3.13
- Django 5.2.17 LTS
- Channels 4.3.2
- channels-redis 4.3.0
- Daphne 4.2.3
- Pillow 12.3.0
- django-rq 4.1.1
- django-cors-headers 4.9.0
- django REST Framework 3.16.1
- social-auth-app-django 6.0.1

## Verificaciones realizadas

- `py_compile` de todos los archivos Python: OK.
- Simulaciones Auditorías 18, 19 y 20: OK.
- Simulación específica Auditoría 21: OK.
- Búsqueda estática de APIs legacy en código propio: sin resultados.
- Configuración ASGI moderna: validada estáticamente.

## Limitación crítica

No fue posible ejecutar `pip install` ni `manage.py check/migrate/test` en este entorno porque no existe acceso de red al índice de paquetes y el entorno no tiene Django instalado. Por tanto, esta auditoría es una **preparación de migración y compatibilidad estática**, no una certificación de migración ejecutada.

## Próximo paso obligatorio

Crear un entorno staging con Python 3.13, instalar el stack objetivo, ejecutar:

1. `python manage.py check`
2. `python manage.py check --deploy`
3. `python manage.py makemigrations --check --dry-run`
4. `python manage.py migrate`
5. `python manage.py test`
6. pruebas PostgreSQL reales.

No se recomienda activar producción con el stack anterior.
