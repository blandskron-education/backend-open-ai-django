# Troubleshooting

## `ModuleNotFoundError`

**Síntoma:** Django, DRF, `corsheaders`, `dotenv` u `openai` no se pueden importar.

**Causa probable:** entorno virtual sin activar o dependencias no instaladas.

**Solución:** activa `.venv` y ejecuta `python -m pip install -r requirements.txt`
desde la raíz.

## `no such table` o migraciones pendientes

**Síntoma:** SQLite informa que una tabla o columna no existe.

**Causa probable:** se clonó el proyecto o cambió el modelo sin aplicar migraciones.

**Solución:** desde `backendChatOpenAi/`, ejecuta `python manage.py migrate`. Si
cambiaste modelos, primero usa `python manage.py makemigrations` y revisa el archivo.

## La API responde `503`

**Síntoma:** `/api/recommend/` dice que `OPENAI_API_KEY` no está configurada.

**Causa probable:** falta `.env`, conserva el placeholder o Docker no se reinició.

**Solución:** copia `.env.example` a `.env`, agrega una key válida y reinicia el
servidor o ejecuta `docker compose up --build` otra vez. No publiques la key.

## La API responde `502`

**Síntoma:** no fue posible obtener una recomendación.

**Causa probable:** key inválida, modelo no disponible para la cuenta, cuota,
rate limit o conectividad.

**Solución:** revisa los logs del servidor, la cuenta y `OPENAI_MODEL`. El detalle
se registra en consola pero no se expone al cliente para no filtrar información.

## La recomendación no contiene películas

**Síntoma:** OpenAI responde, pero `movies` es una lista vacía.

**Causa probable:** no se ejecutó el seed o el texto no menciona literalmente un
título del catálogo.

**Solución:** ejecuta `python manage.py seed_movies`, comprueba `/admin/` y prueba
una preferencia distinta. La comparación textual es una limitación educativa
intencional y un buen próximo ejercicio de mejora.

## El superusuario no aparece

**Síntoma:** no puedes iniciar sesión en `/admin/`.

**Causa probable:** falta alguna variable `DJANGO_SUPERUSER_*` o el volumen ya
contiene un usuario con otras credenciales.

**Solución:** localmente usa `python manage.py createsuperuser`. En Docker revisa
`docker compose logs web`; para un reinicio total usa `docker compose down -v`
(esto elimina toda la base de datos del volumen) y vuelve a levantar.

## Puerto 8000 ocupado

**Síntoma:** `Address already in use` o Docker no puede publicar el puerto.

**Solución:** detén el proceso anterior o cambia Compose a `"8001:8000"` y visita
`http://localhost:8001/`.

## `docker compose` no existe

**Síntoma:** Docker responde que `compose` es un comando desconocido.

**Causa probable:** está instalado el cliente/daemon sin el plugin Compose.

**Solución:** instala Docker Desktop o el plugin oficial Compose. Mientras tanto,
usa la instalación local con Python.

## Archivos estáticos del admin en producción

**Síntoma:** `/admin/` carga sin estilos con `DEBUG=False`.

**Causa probable:** `runserver` sirve estáticos en desarrollo, no es una solución
de producción.

**Solución:** define una estrategia real de `collectstatic` y servidor de archivos
antes de desplegar. El Compose incluido es exclusivamente educativo.
