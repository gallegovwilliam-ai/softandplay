# AUDITORÍA 15 — Concurrencia, integridad y staging

## Objetivo

Reducir el riesgo de doble asignación de cartones y preparar comprobaciones ejecutables en un staging PostgreSQL real.

## Cambios realizados

1. Se centralizó la asignación de cartones en `cards/services.py`.
2. La asignación utiliza `select_for_update()` sobre los cartones candidatos y debe ejecutarse dentro de la transacción que mantiene bloqueada la partida.
3. Las ventas directas de revendedor y las aprobaciones bancarias utilizan el mismo servicio de asignación.
4. Se endurecieron los endpoints de administración bancaria: modificación, consulta de datos bancarios, revisión y eliminación de compras requieren superusuario; las eliminaciones requieren POST.
5. La generación masiva de cartones desde Excel requiere POST, superusuario y rutas configuradas mediante variables de entorno.
6. Se corrigió el falso positivo de Auditoría 14 que detectaba su propia cadena `request.is_ajax()`; ahora el análisis se realiza mediante AST.
7. Se corrigieron los endpoints de Chance para usar POST + AJAX + CSRF, limitar el acceso a personal autorizado y respetar correctamente el cliente seleccionado.
8. Se añadieron validaciones de cantidad, número, monto y loterías en Chance.
9. Se añadió `auditoria15`, que comprueba migraciones, PostgreSQL, asignaciones duplicadas, ventas inválidas, Wallet y tablas históricas de Settlement.
10. Se añadió `audit15_simulation.py` para validaciones lógicas rápidas.

## Pruebas ejecutadas en este entorno

- `py_compile` sobre todos los archivos Python: OK.
- Simulación de Auditoría 15: OK.
- Revisión AST de llamadas reales a `request.is_ajax()`: OK.
- Revisión de numeración duplicada de migraciones: OK.

## Bloqueo pendiente

Este entorno no dispone de un servidor PostgreSQL ni de un runtime Python 3.8/Django 3.0.7 compatible con la aplicación histórica. Por ello no se debe afirmar que `manage.py migrate`, `manage.py check` o las pruebas transaccionales hayan sido ejecutadas realmente sobre PostgreSQL.

## Prueba obligatoria en staging

1. Crear una copia de la base de datos histórica.
2. Restaurarla en PostgreSQL de staging.
3. Configurar `DATABASE_URL` de staging.
4. Ejecutar `python manage.py migrate`.
5. Ejecutar `python manage.py check --deploy`.
6. Ejecutar `python manage.py auditoria15`.
7. Comparar usuarios, partidas, cartones, ventas, pagos, Wallet, ledger y liquidaciones antes/después.
8. Ejecutar pruebas concurrentes con dos o más procesos intentando vender los últimos cartones de una partida.
9. Ejecutar dos liquidaciones simultáneas de la misma partida y comprobar que solo existe una liquidación.
10. Tomar backup antes de cualquier migración productiva y definir rollback.

## Riesgos que siguen abiertos

- Django 3.0.7 necesita una actualización escalonada antes de producción.
- La integración real de PayPal/webhook todavía debe implementarse con verificación del proveedor.
- La zona horaria debe confirmarse antes de cambiar `TIME_ZONE`.
- La geolocalización externa de IP debe tratarse como servicio no crítico y con timeout.
