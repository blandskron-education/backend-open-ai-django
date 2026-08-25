# AGENTS.md

## Proyecto

API educativa Django/DRF que solicita recomendaciones a OpenAI y cruza títulos
con un catálogo SQLite. Lee primero `README.md`, `docs/ARCHITECTURE.md` y
`docs/PROJECT_STATUS.md`.

## Mapa rápido

- Proyecto Django y `manage.py`: `backendChatOpenAi/`.
- Settings y URLs raíz: `backendChatOpenAi/backendChatOpenAi/`.
- Dominio, API, admin, comandos, migraciones y tests: `backendChatOpenAi/chatOpenAi/`.
- Datos iniciales: `chatOpenAi/movie_list.py` → comando `seed_movies` → SQLite.
- Infraestructura local: `Dockerfile`, `compose.yaml`, `docker-entrypoint.sh`.
- Contrato manual de API: `postman.json` y README.

## Configuración

Python objetivo: 3.12. Dependencias fijadas en `requirements.txt`. `.env.example`
es versionable; `.env`, bases SQLite, estáticos generados y entornos virtuales no.
Nunca registres keys, contraseñas reales o bases locales.

Variables críticas: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, opciones CORS,
`OPENAI_API_KEY`, `OPENAI_MODEL`, `DB_PATH` y `DJANGO_SUPERUSER_*`.

## Comandos esenciales

Desde `backendChatOpenAi/`, con dependencias instaladas:

```bash
python manage.py migrate
python manage.py seed_movies
python manage.py ensure_superuser
python manage.py runserver
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Desde la raíz: `docker compose up --build`, `docker compose config` y
`docker compose down`.

## Reglas de modificación

1. Conserva el enfoque Django idiomático y proporcional; no agregues capas por
   anticipación.
2. No borres ni reescribas migraciones históricas. Crea una migración nueva y
   revisa sus operaciones.
3. Mantén el contrato de `POST /api/recommend/` o documenta y prueba cualquier
   cambio intencional.
4. No realices llamadas reales a OpenAI en tests; parchea
   `chatOpenAi.views.generate_recommendation`.
5. Mantén `seed_movies` y `ensure_superuser` idempotentes.
6. Si cambias variables, comandos, rutas o respuestas, sincroniza README, docs,
   `.env.example`, Compose y Postman según corresponda.
7. El Docker incluido es educativo. No presentes `runserver`, CORS abierto ni las
   credenciales de aula como configuración de producción.

## Criterio de terminado

Ejecuta como mínimo los tres checks Django indicados. Para cambios de Docker,
valida también configuración, build y healthcheck si el entorno lo permite.
Revisa `git diff`, secretos, caches, logs y archivos generados antes de cerrar.
Documenta con exactitud cualquier validación que no haya podido ejecutarse.
