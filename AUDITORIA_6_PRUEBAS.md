# Auditoría 6 — pruebas de funcionamiento y simulación financiera

## Resultado
La simulación independiente de reglas financieras fue ejecutada correctamente.

Escenarios superados:
- pozo = precio × cartones vendidos;
- distribución con varios patrones y varios ganadores;
- redondeo a centavos con `Decimal`;
- cálculo de impuesto y neto;
- conciliación bruto − impuesto = neto;
- rechazo de porcentajes individuales > 100%;
- rechazo de porcentajes acumulados > 100%;
- rechazo de patrón sin ganadores;
- rechazo de impuesto fuera de rango;
- rechazo de conciliación inconsistente;
- idempotencia conceptual mediante clave única del ledger.

## Cambio adicional integrado
Cuando se aprueba un pago, además del registro `PaymentRecord`, se genera un
movimiento `DEBITO` en `FinancialLedger` con clave única `PAGO:<tipo>:<carton>`.
Esto permite que el pago quede reflejado en la trazabilidad financiera sin crear
un segundo asiento cuando el proceso es reintentado.

El premio ya genera su asiento `CREDITO` con clave única `PREMIO:<tipo>:<carton>`.

## Ejemplo comprobado
Con 100 cartones de $10.000:

- Pozo: $1.000.000,00
- Patrón 1: 50%, 1 ganador → $500.000,00
- Patrón 2: 30%, 2 ganadores → $150.000,00 por ganador
- Patrón 3: 20%, 4 ganadores → $50.000,00 por ganador
- Premio bruto de un cartón que tiene los tres patrones: $700.000,00
- Impuesto 10%: $70.000,00
- Neto: $630.000,00

## Limitación del entorno
No se pudo ejecutar `manage.py test` en este entorno porque no tiene Django
instalado y el proyecto depende de Django 3.0.7. La compilación sintáctica de
los módulos nuevos/modificados sí fue comprobada con `py_compile`.

En el servidor/entorno virtual del proyecto debe ejecutarse:

    python manage.py check
    python manage.py test

y posteriormente las pruebas de concurrencia con PostgreSQL.

## Pendientes críticos antes de dinero real
1. Integrar asientos de ledger para ventas, devoluciones y recargas.
2. Definir formalmente si el pozo se basa en cartones vendidos, verificados o
   pagados.
3. Conciliación por partida, día y revendedor.
4. No borrar físicamente partidas, pagos ni movimientos financieros.
5. Pruebas de concurrencia con PostgreSQL/Redis.
6. Revisión legal, fiscal y de licenciamiento antes de operar dinero real.
