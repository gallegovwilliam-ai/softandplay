# Auditoría 20 — Despliegue y operación

## Objetivo
Convertir las auditorías de integridad anteriores en una base operativa segura, sin afirmar que el sistema está listo para dinero real mientras falte una ejecución real de PostgreSQL/Django.

## Correcciones aplicadas
- Endpoints de administración de Chance: creación y edición restringidas a superusuario autenticado.
- Clientes: creación/listado/verificación limitados al usuario propietario, salvo superusuario.
- `pagarcompra` ahora bloquea la partida con `select_for_update()` como ya ocurría en Bingo 75.
- Endpoint `test-notify` convertido en POST + superusuario; deja de ser una mutación pública.
- Añadidos `auditoria20.py` y `audit20_simulation.py`.
- Añadidos ejemplos endurecidos de systemd para Gunicorn, Daphne y RQ.
- Añadido ejemplo Nginx con redirección HTTP→HTTPS, WebSocket, headers de proxy y rutas estáticas.

## Pruebas ejecutadas en esta máquina
- `py_compile` de todos los Python: OK.
- `audit20_simulation.py`: OK.
- No se pudo ejecutar `manage.py check`, `migrate` o `test` porque esta máquina no tiene Django ni psycopg2 instalados.

## Bloqueadores de producción
1. Django 3.0.7 está fuera de soporte. Debe planificarse una actualización por etapas antes de exponer el sistema a Internet.
2. El proyecto usa un `.python-version` antiguo; el runtime real debe fijarse en un entorno compatible y reproducible.
3. Falta una instancia PostgreSQL de staging para ejecutar migraciones y pruebas reales.
4. PayPal todavía requiere confirmación real mediante API/webhook antes de entregar cartones.
5. Debe confirmarse `DJANGO_TIME_ZONE` con la operación real.
6. Deben configurarse secretos, dominios, SMTP, Redis y certificados fuera del repositorio.

## Secuencia de puesta en producción
1. Crear servidor de staging aislado.
2. Instalar runtime compatible y dependencias bloqueadas.
3. PostgreSQL limpio + `manage.py migrate`.
4. `manage.py check --deploy` y `manage.py check_produccion`.
5. `collectstatic`.
6. Cargar datos de prueba.
7. Ejecutar pruebas de concurrencia con dos o más vendedores y últimos cartones.
8. Probar venta → liquidación → premio → reverso.
9. Configurar Nginx + TLS + WebSocket.
10. Backups automáticos y prueba de restauración.
11. Solo después: producción.
