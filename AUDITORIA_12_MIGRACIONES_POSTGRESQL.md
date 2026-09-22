# AUDITORÍA 12 — Migraciones, PostgreSQL y consistencia del esquema

## Objetivo
Validar que la modernización financiera de Auditoría 11 pueda continuar hacia PostgreSQL sin conservar tipos ambiguos para cantidades o dinero.

## Cambios aplicados
- `CabezeraImpre.cantidad` y `CabezeraImpre75.cantidad` pasan de texto a `PositiveIntegerField`.
- Se agregó migración con conversión defensiva de datos históricos.
- `TransactionWallet.amount` recibe restricción de no negatividad.
- Se corrigió el signal de `Wallet`: únicamente crea la billetera cuando el usuario es nuevo; ya no intenta guardar una relación inexistente en cada `post_save`.
- Se agregó `python manage.py auditoria12` para revisar migraciones pendientes, motor de base de datos y tipos financieros canónicos.

## Criterio de seguridad
Las migraciones de conversión hacen primero el backfill y después alteran el tipo. Los valores no numéricos históricos se convierten a cero y deben revisarse antes de producción; no se deben ejecutar migraciones sobre la base original sin copia de seguridad.

## Estado
La comprobación estática de Python/migraciones fue superada. No se ejecutó `manage.py migrate` contra PostgreSQL real en este entorno porque no está disponible el runtime Django del proyecto.

## Próximo paso recomendado
Crear una copia de la base de datos real, restaurarla en PostgreSQL de staging, ejecutar `migrate`, `check`, `auditoria12` y pruebas de integridad antes de tocar producción.
