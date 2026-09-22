# Auditoría 9 — circuito financiero y conciliación

## Objetivo
Cerrar el circuito económico de SoftAndPlay y evitar que el pozo se calcule a partir de cartones que todavía están pendientes de aprobación.

## Cambios aplicados

1. **SaleRecord / SaleRecord75**: cada encabezado de venta aprobado tiene un registro financiero inmutable y único.
2. **Venta → ledger**: una venta aprobada genera un crédito en `FinancialLedger` con clave idempotente `VENTA:*`.
3. **Liquidación → ventas aprobadas**: el pozo se calcula usando únicamente las cantidades de `SaleRecord`/`SaleRecord75` con estado `APROBADA`.
4. **Pagos → ledger**: el débito de pago ahora referencia `PaymentRecord`/`PaymentRecord75`, evitando ambigüedad en la conciliación.
5. **Liquidación no genera movimiento de caja**: el premio liquidado es una obligación de pago; el movimiento de caja ocurre cuando se procesa el pago.
6. **Redondeo**: impuesto y neto se acumulan por cartón para que la liquidación cierre exactamente a centavos.
7. **Conciliación diaria**: `CashReconciliation` calcula ventas - pagos - reversos a partir del ledger.
8. **Comando administrativo**: `python manage.py conciliar_caja YYYY-MM-DD --usuario ID` genera/actualiza la conciliación diaria.
9. **Ledger inmutable a nivel de modelo**: no se permite modificar ni eliminar movimientos financieros existentes.
10. **Liquidaciones inmutables a nivel de modelo**.
11. **Aprobación bancaria endurecida**: solo POST y superusuario; bloquea partida y evita aprobar dos veces.
12. **Asignación de cartones bancaria**: usa cartones disponibles y bloqueo transaccional, eliminando el antiguo cálculo `primer_cartón + 1`.
13. **Ventas directas**: guardan cantidad explícita y registran su movimiento financiero dentro de la misma transacción.
14. **PayPal**: al generar cartones aprobados se registra también la venta financiera.
15. **Migración histórica**: las cabeceras ya verificadas se convierten en `SaleRecord` y reciben su asiento de venta idempotente.

## Simulación

Con 100 cartones a $10.000, reparto 50%/30%/20% y 10% de impuesto:

- Pozo: $1.000.000
- Premio bruto: $1.000.000
- Impuesto: $100.000
- Premio neto: $900.000
- Caja neta antes de otros movimientos: $100.000

Resultado: `AUDITORIA 9: CIRCUITO VENTA-LIQUIDACION-PAGO-CONCILIACION SUPERADO`

## Limitación de pruebas

El entorno de revisión no tiene Django instalado ni una instancia PostgreSQL disponible, por lo que no se ejecutaron migraciones ni pruebas ORM contra una base real. Se ejecutó `compileall` sobre el proyecto y una simulación financiera pura en Python.

## Pendientes recomendados

- Implementar flujo formal de anulación/reverso de ventas y pagos con asientos compensatorios.
- Migrar definitivamente los `CharField` monetarios a `DecimalField` como fuente única.
- Añadir pruebas de integración sobre PostgreSQL y concurrencia real.
- Construir panel de conciliación y cierres de caja para administración.
