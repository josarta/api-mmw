<p align="center">
  <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI">
   <img src="https://media.licdn.com/dms/image/C4D03AQGXXWWF1xD26Q/profile-displayphoto-shrink_200_200/0/1648651603418?e=1726099200&v=beta&t=TM5Aej05IRxztlIlxg08OJgtvZdeF0P0h4m2948KMM8" alt="Developer">
</p>
<p align="center">
    <em>Repository technical test python backend developer implementing FastAPI framework.</em>
</p>
<p align="center">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/tiangolo/fastapi.svg" alt="Coverage">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</p>

---

🚀 🚀 **Check -- Proyect in Live**: <a href="https://api-mmw.onrender.com/docs" target="_blank">https://api-mmw.onrender.com/docs/</a>

✅  **username**: lion_king
✅  **password**: secret

**Documentation**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Source Code**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

**Data base**: <a href="https://scalegrid.io/?utm_term=&utm_campaign=Pricing+Page+-+REMARKETING&utm_source=adwords&utm_medium=ppc&hsa_mt=&hsa_ad=&hsa_net=adwords&hsa_src=x&hsa_kw=&hsa_tgt=&hsa_cam=21410336109&hsa_acc=2428435206&hsa_ver=3&hsa_grp=&gad_source=1&gclid=CjwKCAjwnK60BhA9EiwAmpHZw-mZ4_LjulmzojNHd2-bk3qZybGzBICliDhgtzXothX3QNHdJReveBoClEUQAvD_BwE" target="_blank">https://scalegrid.io/</a>

**CI/CD**: <a href="https://render.com/" target="_blank">https://render.com/</a>

---

technical test for ORBIDI used FastAPI web framework for building APIs with Python based on standard Python type hints.

Technical test:

* **Introducción al Desafío**: Imagina que estás construyendo el backend para 'Map My World', una aplicación destinada a explorar y revisar diferentes ubicaciones y categorías del mundo, como restaurantes, parques y museos. La meta es ofrecer a los usuarios un mapa interactivo donde puedan descubrir nuevas ubicaciones y ver recomendaciones basadas en categorías específicas. Pero hay un giro: queremos asegurarnos de que las recomendaciones estén siempre actualizadas y sean relevantes.
* **Tu Misión**: Como parte del equipo de desarrollo de 'Map My World', tu tarea es construir el corazón de nuestra aplicación: una API REST que maneje la lógica para añadir nuevas ubicaciones y categorías, y más importante aún, una característica especial que nos permita mantener nuestras recomendaciones frescas y atractivas para nuestros usuarios.

Especificaciones Técnicas:

**Modelos de Datos**
- **Ubicaciones (`locations`)**: Cada ubicación tiene una longitud y latitud.
- **Categorías (`categories`)**: Cada categoría representa un tipo de lugar para explorar.
- **Revisiones de Ubicación-Categoría (`location_category_reviewed`)**: Este registro es nuestro control de calidad, asegurándonos de que cada combinación de ubicación y categoría sea revisada regularmente.

**Funcionalidades Clave**
- **Gestión de Ubicaciones y Categorías**: Permite a los usuarios de nuestra API añadir nuevas ubicaciones y categorías.
- **Recomendador de Exploración**: Un endpoint especial que sugiere 10 combinaciones de ubicación-categoría que no han sido revisadas en los últimos 30 días, priorizando las que nunca se han revisado.

**Objetivos**

- Claridad y Estructura: Tu código debe ser claro y estar bien estructurado. Queremos ver cómo organizas tu proyecto y cómo aplicas las buenas prácticas de codificación.
- Eficiencia y Optimización: Las recomendaciones deben ser generadas de manera eficiente, teniendo en cuenta tanto la velocidad de respuesta como el uso de recursos.
- Documentación: Una buena API no es solo sobre el código; también es sobre cómo comunicas su uso a otros desarrolladores. Esperamos ver cómo documentas los endpoints y modelos.

<small>* estimated time of dedication 24 hours.</small>

## Considerations
<!-- considerations -->
**Database MySql**

```SQL
-- To create the data base
CREATE DATABASE MMW-PRO;

-- Use the created database
USE MMW-PRO;;

-- Create the tables
CREATE TABLE locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    latitude DECIMAL(9, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE location_category_reviewed (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    location_id INT NOT NULL,
    category_id INT NOT NULL,
    reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (location_id) REFERENCES locations(location_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE audit (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    action VARCHAR(255) NOT NULL,
    entity VARCHAR(255) NOT NULL,
    entity_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create triggers for the audit
CREATE TRIGGER after_location_insert
AFTER INSERT ON locations
FOR EACH ROW
BEGIN
    INSERT INTO audit (action, entity, entity_id) 
    VALUES ('INSERT', 'locations', NEW.location_id);
END;

CREATE TRIGGER after_category_insert
AFTER INSERT ON categories
FOR EACH ROW
BEGIN
    INSERT INTO audit (action, entity, entity_id) 
    VALUES ('INSERT', 'categories', NEW.category_id);
END;

-- Insert test data into tables
INSERT INTO locations (latitude, longitude) VALUES 
(40.712776, -74.005974), (34.052235, -118.243683), (51.507351, -0.127758), 
(48.856613, 2.352222), (35.689487, 139.691711), (55.755825, 37.617298), 
(52.520008, 13.404954), (39.904202, 116.407394), (37.774929, -122.419418), 
(28.613939, 77.209023);

INSERT INTO categories (name) VALUES 
('Museum'), ('Park'), ('Restaurant'), ('Theater'), ('Monument'), 
('Library'), ('Zoo'), ('Aquarium'), ('Mall'), ('Beach');

INSERT INTO location_category_reviewed (location_id, category_id, reviewed_at) VALUES 
(1, 1, '2023-06-01'), (2, 2, '2023-06-15'), (3, 3, '2023-07-01'), 
(4, 4, '2023-07-15'), (5, 5, '2023-08-01'), (6, 6, '2023-08-15'), 
(7, 7, '2023-09-01'), (8, 8, '2023-09-15'), (9, 9, '2023-10-01'), 
(10, 10, '2023-10-15');
```
<!-- /sponsors -->
## Query **Scan Recommender**
```SQL
SELECT 
    l.location_id, 
    l.latitude, 
    l.longitude, 
    c.category_id, 
    c.name
FROM 
    locations l
CROSS JOIN 
    categories c
LEFT JOIN 
    location_category_reviewed r
    ON l.location_id = r.location_id AND c.category_id = r.category_id
WHERE 
    r.reviewed_at IS NULL 
    OR r.reviewed_at < NOW() - INTERVAL '30 days'
ORDER BY 
    r.reviewed_at IS NULL DESC, 
    r.reviewed_at ASC
LIMIT 10;
```
---
## Installation

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

## Example

### Create it

* Create a file `main.py` with:

```Python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Or use <code>async def</code>...</summary>

If your code uses `async` / `await`, use `async def`:

```Python hl_lines="9  14"
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

**Note**:

If you don't know, check the _"In a hurry?"_ section about <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` and `await` in the docs</a>.

</details>

### Run it

Run the server with:

<div class="termy">

```console
$ fastapi dev main.py

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>About the command <code>fastapi dev main.py</code>...</summary>

The command `fastapi dev` reads your `main.py` file, detects the **FastAPI** app in it, and starts a server using <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a>.

By default, `fastapi dev` will start with auto-reload enabled for local development.

You can read more about it in the <a href="https://fastapi.tiangolo.com/fastapi-cli/" target="_blank">FastAPI CLI docs</a>.

</details>

### Check it

Open your browser at <a href="http://127.0.0.1:8000/api/v1/locations

You will see the JSON response as:

```JSON
{"detail":"Not authenticated"}
```

### Interactive API docs

Now go to <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

You will see the automatic interactive API documentation (provided by <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://i.postimg.cc/4xZXh6jr/pantalla-inicial.png)

### Alternative API docs

And now, go to <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

You will see the alternative automatic documentation (provided by <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://i.postimg.cc/ZYBNfm0J/redoc.png)

## Implemented functionalities and patterns

- Was implement the Circuit Breaker pattern in Python, we can use the `pybreaker` library. Below is an example of how you could implement the Circuit Breaker pattern

```Python hl_lines="4  9-12  25-27"
from datetime import timedelta
from aiobreaker import CircuitBreaker, CircuitBreakerListener
from fastapi import logger


circuit_breaker = CircuitBreaker(fail_max=5, timeout_duration=timedelta(seconds=60))


class LogListener(CircuitBreakerListener):
    """Class listerner circuitbraker for print logs

    Args:
        CircuitBreakerListener (_type_): configiration mac pool connetiones an timeout
    """
    def state_change(self, breaker, old, new):
        logger.info(f"{old.state} -> {new.state}")


breaker = CircuitBreaker(listeners=[LogListener()])
```

- Was implement as a parallel application for error handling
```Python hl_lines="4  9-12  25-27"

from fastapi import HTTPException, Request , status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from config.logger import logger , data , genericLoadRequest 
from aiobreaker.state import CircuitBreakerError

class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """Function implemented as a parallel application for exception handling

        Args:
            request (Request): _description_
            call_next (_type_): request for entry that failed

        Returns:
            JSONResponse: returns json, captures the exception in the http code message and creates a log
        """
        try:
            return await call_next(request)
        except HTTPException as http_exception:
            genericLoadRequest(request)
            data['status_code'] = http_exception.status_code
            logger.info(f"Request receivet at {request.url}" , extra=data)
            return JSONResponse(
                status_code=http_exception.status_code,
                content={"error": "Client Error", "message": str(http_exception.detail)},
            )
        except Exception as e:
           genericLoadRequest(request)
           print(e)
           data['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
           logger.error(f"Request receivet at {request.url}" , extra=data)
           return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Internal Server Error", "message": "An unexpected error occurred."},
            )
        except CircuitBreakerError as e:
            print(e)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Internal Server Error", "message": "CircuitBreakerError.", "code":-20005},
            )
```

- Security levels with JWT
- Unit tests are performed
- Comments for all modules in their functions and classes Docstrings


## License

This project is licensed under the terms of the MIT license.