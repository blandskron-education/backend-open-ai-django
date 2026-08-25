# Arquitectura y guía de aprendizaje

## Alcance

El repositorio contiene un único proyecto Django (`backendChatOpenAi`) y una app
de dominio (`chatOpenAi`). Es una API deliberadamente pequeña: usa DRF para JSON,
el ORM con SQLite y Django Admin para gestionar datos. No existen frontend,
templates propios, forms, uploads, signals ni middleware personalizado.

## Responsabilidades

| Archivo | Responsabilidad | Concepto que enseña |
| --- | --- | --- |
| `backendChatOpenAi/settings.py` | Configuración y entorno | settings, seguridad, SQLite, CORS |
| `backendChatOpenAi/urls.py` | Entradas `/api/` y `/admin/` | URL dispatcher e `include` |
| `chatOpenAi/models.py` | Película persistente | ORM, constraint y `__str__` |
| `chatOpenAi/serializers.py` | Entrada y salida JSON | validación y representación DRF |
| `chatOpenAi/views.py` | Orquestación de la petición | FBV, API externa y estados HTTP |
| `chatOpenAi/urls.py` | Rutas con namespace | URLs nombradas y `reverse` |
| `chatOpenAi/admin.py` | Exploración del catálogo | `ModelAdmin` |
| `chatOpenAi/movie_list.py` | Fuente inicial estática | separación de datos y persistencia |
| `management/commands/` | Seed y superusuario | automatización explícita e idempotente |
| `chatOpenAi/tests.py` | Casos automáticos | test database, client y mocks |

## Recorrido de una petición

1. La URL raíz delega `/api/` en las URLs de la app.
2. `RecommendationRequestSerializer` exige un `message` no vacío de hasta 500
   caracteres. Si falla, DRF responde `400` antes de tocar la red.
3. La view comprueba la API key y llama a `generate_recommendation`.
4. Esa función es la frontera externa: crea el cliente OpenAI y devuelve texto.
5. La view compara los títulos persistidos con ese texto y limita a tres matches.
6. `MovieRecommendationSerializer` conserva el contrato público
   `overview`/`poster_url` aunque el modelo use `description`/`image_url`.
7. DRF serializa el diccionario final como JSON.

La llamada externa está aislada en una función para que el test pueda parchearla.
Eso hace los tests rápidos, deterministas y sin coste.

## Ciclo de datos

`movie_list.py` es la fuente legible del catálogo de aula. `python manage.py
seed_movies` usa `update_or_create(title, genre, defaults=...)`: la pareja título
y género identifica cada entrada y el constraint de base de datos impide
duplicados. Cambiar un modelo exige `makemigrations`; cambiar solo el catálogo
exige volver a ejecutar el seed.

## Decisiones conscientes

- **Function-Based Views:** hay dos endpoints simples; una CBV añadiría estructura
  sin aportar claridad aquí.
- **SQLite:** suficiente para una práctica individual y fácil de reiniciar.
- **Un solo settings:** el proyecto aún no necesita módulos por entorno; las
  variables ya separan secretos y diferencias de ejecución.
- **Chat Completions:** preserva la integración existente. El modelo está en
  `OPENAI_MODEL` para evitar editar código cuando cambie la disponibilidad.
- **Sin capa service completa:** solo se aisló la frontera de red; más capas
  ocultarían el flujo que el alumno debe aprender.

## Cómo extenderlo

Un siguiente ejercicio razonable es dejar que el modelo seleccione identificadores
mediante salida estructurada y comparar por ID, no por texto. Después pueden
agregarse autenticación, cuotas por usuario y una entidad `Recommendation` que
registre historial. Cada cambio debe incluir migración cuando corresponda, tests
de éxito/error y actualización del contrato documentado.
