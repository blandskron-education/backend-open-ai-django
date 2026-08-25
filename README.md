# Movie Recommendations API con Django y OpenAI

API educativa que recibe una preferencia, solicita una recomendación a OpenAI y
la cruza con un catálogo local de películas guardado en SQLite. El repositorio
está pensado como laboratorio introductorio de Django REST Framework: se puede
ejecutar de forma local o con Docker y explorar sus datos desde Django Admin.

## Qué aprenderás

- El recorrido `URL → view → serializer → modelo → respuesta JSON`.
- Validación de entrada y códigos HTTP con Django REST Framework (DRF).
- Modelos, migraciones, consultas ORM y administración de Django.
- Integración segura con una API externa mediante variables de entorno.
- Management commands idempotentes para datos iniciales y superusuarios.
- Tests que aíslan la red con mocks.
- Empaquetado de una aplicación Django pequeña con Docker y Compose.

## Funcionalidades

- `GET /api/health/`: comprueba que el servicio responde.
- `POST /api/recommend/`: recomienda películas a partir de `message`.
- `/admin/`: permite buscar y filtrar el catálogo.
- `seed_movies`: carga o actualiza 30 entradas sin duplicarlas.
- `ensure_superuser`: crea opcionalmente un administrador desde el entorno.

La aplicación no incluye frontend, templates propios ni formularios HTML. La
interfaz web existente es Django Admin; `postman.json` permite importar ejemplos
de la API en Postman.

## Tecnologías

- Python 3.12
- Django 5.1 y Django REST Framework 3.15
- SDK de OpenAI y Chat Completions
- SQLite
- django-cors-headers
- Docker y Docker Compose
- GitHub Actions para checks automáticos

## Requisitos

- Git
- Python 3.12 para la instalación local
- Docker con el plugin Compose para la alternativa en contenedores
- Una API key de OpenAI para probar la recomendación (health, admin y tests no la
  necesitan)

## Instalación local

```bash
git clone https://github.com/Blandskron/backend-open-ai-django.git
cd backend-open-ai-django
python -m venv .venv
```

Activa el entorno:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Instala las dependencias y prepara la configuración:

```bash
python -m pip install -r requirements.txt

# Linux/macOS
cp .env.example .env

# Windows PowerShell
Copy-Item .env.example .env
```

Edita `.env` y reemplaza `OPENAI_API_KEY`. La librería `python-dotenv` carga ese
archivo desde la raíz; `.env` está ignorado por Git.

Prepara la base de datos:

```bash
cd backendChatOpenAi
python manage.py migrate
python manage.py seed_movies
python manage.py ensure_superuser
```

`seed_movies` es idempotente: puedes repetirlo y actualizará los registros. El
último comando usa las tres variables `DJANGO_SUPERUSER_*` de `.env`; también
puedes omitirlas y ejecutar `python manage.py createsuperuser` de forma interactiva.

Inicia Django:

```bash
python manage.py runserver
```

Abre `http://localhost:8000/api/health/` y
`http://localhost:8000/admin/`.

## Probar la API

```bash
curl -X POST http://localhost:8000/api/recommend/ \
  -H "Content-Type: application/json" \
  -d '{"message":"Quiero ciencia ficción con mucha acción"}'
```

Respuesta resumida:

```json
{
  "response": "Puedo recomendarte estas películas...",
  "movies": [
    {
      "title": "The Matrix",
      "genre": "Science Fiction",
      "overview": "...",
      "poster_url": "https://..."
    }
  ]
}
```

Un `400` indica entrada inválida, `503` que falta la API key y `502` que el
servicio externo no respondió. El modelo se configura con `OPENAI_MODEL`; el
valor educativo inicial es `gpt-4o-mini`. Consulta el catálogo y disponibilidad
actual en la [documentación oficial de modelos de OpenAI](https://developers.openai.com/api/docs/models).

## Docker

Desde la raíz:

```bash
docker compose up --build
```

Compose lee `.env` si existe. Si todavía no lo creaste, la aplicación arranca y
health/admin funcionan, pero `/api/recommend/` devuelve `503` hasta configurar
`OPENAI_API_KEY` y reiniciar. El entrypoint ejecuta, en este orden:

1. `migrate`;
2. `seed_movies`;
3. `ensure_superuser`;
4. el servidor indicado por la imagen.

Para la experiencia de aula, Compose crea por defecto `admin` / `admin123`. Son
credenciales públicas y deliberadamente inseguras: cámbialas en `.env` y nunca
las uses en producción.

```bash
docker compose logs -f web   # observar el servidor
docker compose down          # detener y conservar SQLite
docker compose down -v       # reiniciar datos; elimina el volumen local
```

SQLite persiste en el volumen `django_data`. La imagen se ejecuta con un usuario
sin privilegios y expone un healthcheck sobre `/api/health/`.

## Tests y quality checks

Ejecuta desde `backendChatOpenAi/`, con el entorno virtual activo:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Los tests no consumen créditos ni requieren una API key: reemplazan la llamada a
OpenAI con un mock. El workflow `.github/workflows/django.yml` repite estos tres
comandos en cada push y pull request.

## Estructura

```text
backend-open-ai-django/
├── .github/workflows/django.yml  # validación continua
├── backendChatOpenAi/
│   ├── backendChatOpenAi/        # settings, URLs raíz, ASGI y WSGI
│   ├── chatOpenAi/               # modelo, API, admin, datos, comandos y tests
│   └── manage.py
├── docs/                         # arquitectura, troubleshooting y estado
├── .env.example                  # configuración segura de ejemplo
├── compose.yaml
├── docker-entrypoint.sh
├── Dockerfile
├── postman.json
└── requirements.txt
```

En `chatOpenAi/`, modifica `models.py` para cambiar los datos persistidos,
`serializers.py` para cambiar el contrato JSON, `views.py` para el flujo de la
petición, `urls.py` para las rutas, `admin.py` para la exploración y
`movie_list.py` para el catálogo inicial. Después de un cambio de modelo crea una
migración; no edites ni borres las históricas.

## Flujo educativo

```text
POST /api/recommend/
        ↓
RecommendationRequestSerializer valida message
        ↓
recommend_movie llama a OpenAI
        ↓
Movie.objects compara la respuesta con SQLite
        ↓
MovieRecommendationSerializer construye movies
        ↓
DRF devuelve JSON y un estado HTTP
```

Este es un proyecto de desarrollo educativo, no una receta de producción. Antes
de publicar un servicio real debes usar `DEBUG=False`, una `SECRET_KEY` única,
hosts y orígenes CORS explícitos, HTTPS, un servidor de aplicación de producción,
observabilidad y una base de datos adecuada a la carga.

## Documentación adicional

- [Arquitectura y guía de modificación](docs/ARCHITECTURE.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Estado y próximos pasos](docs/PROJECT_STATUS.md)
- [Instrucciones para agentes](AGENTS.md)

## Licencia

Consulta [LICENSE](LICENSE).
