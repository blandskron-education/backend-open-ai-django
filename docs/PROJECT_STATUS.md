# Estado del proyecto

## Estado actual

API educativa funcional con catálogo persistido, Django Admin, integración OpenAI
configurable, ejecución local/Docker, tests y CI. El comportamiento objetivo está
cubierto sin frontend propio.

## Funcionalidades terminadas

- Healthcheck y recomendación REST con validación.
- Manejo seguro de API key ausente y errores de OpenAI.
- Modelo `Movie`, migraciones históricas y catálogo idempotente.
- Admin con búsqueda, filtros y listado útil.
- Superusuario educativo opcional e idempotente.
- Docker/Compose con SQLite persistente y healthcheck.
- Guías de instalación, arquitectura y troubleshooting.

## Decisiones importantes

- SQLite y FBV mantienen un nivel introductorio.
- OpenAI se simula en tests; nunca se llama a la red durante la suite.
- Las variables se cargan desde `.env` localmente y desde Compose en Docker.
- Las credenciales por defecto de Compose son solo para aula.

## Problemas conocidos y límites

- El match de películas depende de que la respuesta mencione el título literalmente.
- El Compose usa `runserver` y no representa despliegue de producción.
- La app no autentica ni limita el endpoint, por lo que no debe exponerse
  públicamente con una API key de pago.

## Última validación

Ejecutada el 25 de agosto de 2026 con Python 3.12.13 y Docker:

- `python manage.py check`: sin issues.
- `python manage.py makemigrations --check --dry-run`: sin cambios.
- `python manage.py test`: 8 tests aprobados.
- migraciones desde cero y doble ejecución de `seed_movies`: aprobadas.
- `docker-compose config`, build, arranque y healthcheck: aprobados.

El host de validación exponía Compose mediante el binario compatible
`docker-compose` y no mediante `docker compose`; el archivo validado fue el mismo
`compose.yaml` documentado para instalaciones actuales.

## Validación requerida para cambios futuros

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
docker compose config
docker compose build
```

## Próximo paso recomendado

Agregar salida estructurada con identificadores del catálogo y guardar un historial
de recomendaciones asociado a usuarios autenticados.
