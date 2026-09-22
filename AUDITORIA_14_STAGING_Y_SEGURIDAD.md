# AUDITORÍA 14 — STAGING, MIGRACIONES Y SEGURIDAD DE PAGOS

## Objetivo
Preparar SoftAndPlay para la siguiente etapa: ejecutar migraciones sobre PostgreSQL de staging y cerrar superficies que podían permitir datos inconsistentes o entrega de cartones sin confirmación financiera.

## Correcciones realizadas

### 1. Conflicto de migraciones `core.0005`
Se detectaron dos archivos con el mismo número `0005`:
- `0005_remove_legacy_settlements.py`
- `0005_ledger_positive.py`

Esto podía romper el grafo de migraciones. La migración de restricción financiera fue renumerada a `0006_ledger_positive.py` y ahora depende de `0005_remove_legacy_settlements`.

### 2. AJAX legacy
Se eliminaron las llamadas a `request.is_ajax()` y se utiliza el encabezado `X-Requested-With`.

### 3. Mensajería
`sendMessage` ahora exige usuario autenticado, petición POST AJAX y utiliza como emisor al usuario autenticado, no un nombre enviado por el navegador.

### 4. Pago PayPal
Se encontró un problema crítico: el endpoint podía recibir una referencia enviada desde el navegador, crear los cartones, marcar la compra como verificada y registrar la venta sin una confirmación real del proveedor.

La Auditoría 14 cambia el flujo a **PENDIENTE**. La referencia del navegador no autoriza la entrega de cartones. La confirmación debe llegar mediante API/webhook del proveedor antes de aprobar la venta.

### 5. Preflight automatizado
Se agregó:

`python manage.py auditoria14`

Comprueba duplicidad de números de migración, AJAX legacy, configuración de base de datos en producción y superficie PayPal.

## Validaciones ejecutadas

- AST de Python: OK.
- `py_compile`: OK.
- Simulación financiera: OK.
- Simulación de PayPal no verificado: OK.
- Migraciones `core`: numeración única: OK.

## Bloqueadores todavía abiertos

1. No se ejecutó `manage.py migrate` sobre PostgreSQL real porque este entorno no dispone del runtime Django 3.0.7.
2. Django 3.0.7 es una versión antigua y la documentación oficial la identifica como no soportada. La actualización debe hacerse por etapas, no reemplazando la versión de golpe. citeturn0search0turn0search1
3. El proyecto usa `TIME_ZONE='America/Mexico_City'`; no debe cambiarse a otra zona hasta confirmar la zona de negocio.
4. Falta implementar la confirmación real de PayPal/webhook antes de considerar pagos online terminados.
5. Debe probarse una copia de la base histórica antes de tocar producción.

## Plan de Auditoría 15

- Crear PostgreSQL de staging.
- Restaurar una copia de la base histórica.
- Ejecutar `migrate` completo.
- Ejecutar `check` y toda la suite de tests.
- Comparar conteos antes/después.
- Conciliar wallets, ventas, pagos, ledger y liquidaciones.
- Simular dos compras concurrentes del último cartón disponible.
- Simular dos liquidaciones concurrentes de la misma partida.
- Probar backup y rollback.
- Revisar la integración real del proveedor de pagos.
