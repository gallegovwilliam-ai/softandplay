# SoftAndPlay — demo gratuita en Render

Esta configuracion esta pensada para una demostracion de aproximadamente una semana, no para operar dinero real.

## Servicios

- Web Django/Channels con Daphne.
- PostgreSQL gratuito.
- Render Key Value (Redis-compatible) para Channels.
- HTTPS automatico de Render.

## Importante

- El servicio web gratuito puede dormirse despues de 15 minutos sin trafico y tardar alrededor de un minuto en volver a iniciar.
- El PostgreSQL gratuito tiene limite de 1 GB y caduca a los 30 dias.
- El Key Value gratuito no persiste datos tras reinicios.
- El almacenamiento local del servicio web es efimero. No confiar en el para archivos permanentes.
- No usar esta demo para cobros reales.

## Publicacion

1. Crear una cuenta gratuita en GitHub.
2. Crear un repositorio nuevo, por ejemplo `softandplay-demo`.
3. Subir todos los archivos de este proyecto al repositorio, incluido `render.yaml`.
4. En Render: New -> Blueprint y conectar el repositorio.
5. Revisar los tres recursos gratuitos: `softandplay-demo`, `softandplay-demo-db`, `softandplay-demo-redis`.
6. Cuando Render pida secretos, crear un usuario administrador de demostracion:
   - DEMO_ADMIN_USERNAME: el usuario que quieras
   - DEMO_ADMIN_EMAIL: un correo tuyo
   - DEMO_ADMIN_PASSWORD: una contraseña temporal fuerte
7. Aplicar el Blueprint.
8. Abrir la URL `https://softandplay-demo.onrender.com` que Render asigne.

El arranque ejecuta migraciones, recopila estáticos, crea/actualiza el superusuario de demo si se proporcionan las tres variables y arranca Daphne.
