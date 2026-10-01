# OpenTelemetry { #opentelemetry }

Cuando tu API está ejecutándose, puede que quieras saber cuánto tráfico recibe, qué requests son lentas y cuándo ocurren errores.

La **telemetría** son datos sobre el comportamiento de tu aplicación que te ayudan a responder estas preguntas. Los tipos comunes incluyen:

- **Métricas**: mediciones que puedes resumir a lo largo del tiempo, como los tiempos de response y el número de requests que se están manejando.
- **Trazas**: registros de requests individuales y las operaciones realizadas para manejarlas. Cada operación cronometrada se llama un **span**.
- **Logs**: registros de eventos con timestamp, como el inicio de una aplicación o el fallo de una operación.

[**OpenTelemetry**](https://opentelemetry.io/) es un conjunto de estándares y herramientas para recopilar telemetría y enviarla a un servicio de monitoreo, donde puedes explorarla en dashboards.

**FastAPI proporciona soporte para OpenTelemetry por defecto** para trazas, métricas y logs de requests HTTP. Las conexiones WebSocket también proporcionan trazas y logs. Para ver esos datos, configura un servicio de monitoreo para recibirlos.

## Instala FastAPI { #install-fastapi }

Instala FastAPI con los extras `standard`, que incluyen los paquetes para enviar telemetría:

<div class="termy">

```console
$ uv add "fastapi[standard]"
---> 100%
```

</div>

## Crea la app { #create-the-app }

Crea un archivo `main.py`:

{* ../../docs_src/opentelemetry/tutorial001_py310.py *}

Observa que todo funciona por defecto, no necesitas escribir ningún código personalizado para que la telemetría funcione.

## FastAPI Cloud { #fastapi-cloud }

Cuando haces deploy en [FastAPI Cloud](https://fastapicloud.com) con `fastapi[standard]`, las métricas funcionan automáticamente. No tienes que configurar nada más.

En planes Pro, puedes ver conteos de requests, tasas de error y tiempos de response en el [dashboard de métricas](https://fastapicloud.com/docs/monitoring-and-performance/metrics/).

<img src="/img/tutorial/opentelemetry/image01.png" alt="Dashboard de métricas de FastAPI Cloud Pro con datos de ejemplo">

## Otros servicios de monitoreo { #other-monitoring-services }

Para enviar telemetría a otro servicio de monitoreo, configura un endpoint que acepte **OTLP**, el protocolo de OpenTelemetry para enviar telemetría. Usa el endpoint base HTTP/protobuf del servicio.

Define estas variables de entorno, reemplazando la URL de ejemplo por tu endpoint:

```bash
export OTEL_SERVICE_NAME=my-api
export OTEL_EXPORTER_OTLP_ENDPOINT=https://collector.example.com
```

`OTEL_SERVICE_NAME` identifica tu app en el servicio de monitoreo. El endpoint es la URL base para recibir datos. Las trazas se envían a `/v1/traces`, las métricas a `/v1/metrics` y los logs a `/v1/logs` bajo esa URL.

Si tu servicio requiere autenticación, define `OTEL_EXPORTER_OTLP_HEADERS` con los headers que especifique, por ejemplo `api-key=YOUR_API_KEY`.

## Ejecuta la app { #run-the-app }

Inicia la app en la misma terminal:

<div class="termy">

```console
$ uv run fastapi run
```

</div>

En otra terminal, envía una request:

```console
$ curl http://127.0.0.1:8000/items/1
{"item_id":1}
```

Abre tu servicio de monitoreo y busca `my-api`. Después de la siguiente exportación, puedes ver una traza con un span `GET /items/{item_id}`, junto con métricas para conteos de requests, duración de response y requests activas.

## Personaliza la telemetría { #customize-telemetry }

### Configura providers y exporters { #configure-providers-and-exporters }

Un **provider** suministra los objetos que registran trazas, métricas o logs. Su configuración controla cómo se procesan y exportan esos datos.

Los paquetes de telemetría pueden configurar los providers globales de OpenTelemetry. Configura el paquete antes de que la app inicie, y FastAPI usa esos providers automáticamente.

Cuando se define un endpoint OTLP en el entorno, FastAPI añade un exporter para ese destino a cada provider habilitado. Los exporters existentes continúan enviando datos a sus destinos.

Configura cada destino una vez. Si otro paquete ya maneja el destino del entorno, deshabilita su exportación de entorno o desactiva la configuración automática de FastAPI:

```python
app = FastAPI(telemetry={"auto_configure": False})
```

También puedes pasar un provider directamente en el diccionario `telemetry`. Por ejemplo, este provider usa el console exporter de OpenTelemetry para imprimir spans de requests en tu terminal:

{* ../../docs_src/opentelemetry/tutorial002_py310.py hl[2:8] *}

El **exporter** envía los spans a su destino. `BatchSpanProcessor` agrupa spans y los envía en segundo plano. Reemplaza el console exporter por uno proporcionado por tu paquete de monitoreo para usar su destino. Consulta la [guía de instrumentación de Python de OpenTelemetry](https://opentelemetry.io/docs/languages/python/instrumentation/) para más opciones de configuración.

Usa `meter_provider` o `logger_provider` en el mismo diccionario para suministrar un provider de métricas o logs. La aplicación o el paquete que crea un provider gestiona su cierre. FastAPI gestiona los componentes de exportación que añade.

/// warning | Advertencia

OpenTelemetry usa providers globales por defecto. La configuración independiente de telemetría para [sub-aplicaciones montadas](sub-applications.md) no está garantizada.

///

### Traza operaciones de requests { #trace-request-operations }

Por defecto, las trazas de requests incluyen spans para resolver dependencias, ejecutar tu path operation function, serializar la response y ejecutar cada tarea en `BackgroundTasks` de FastAPI. Estos spans usan el mismo provider y exporters.

Los spans de tareas en segundo plano siguen siendo parte de la traza de la request. Se ejecutan después de que termina el span de response HTTP, así que no aumentan el tiempo de response medido.

Para registrar solo el span de la request HTTP, define `operation_spans` como `False`:

{* ../../docs_src/opentelemetry/tutorial003_py310.py hl[3] *}


### Traza conexiones WebSocket { #trace-websocket-connections }

Cada conexión WebSocket tiene un span como `WS /ws/{room}`, que cubre el handler y la limpieza de dependencias. Usa los mismos providers y configuraciones, incluyendo `operation_spans` para la resolución de dependencias y la ejecución del endpoint.

Las métricas de requests HTTP cubren solo requests HTTP. Las desconexiones WebSocket normales con códigos `1000` o `1001` no producen logs de error.

### Inspecciona errores { #inspect-errors }

FastAPI registra excepciones no manejadas como logs de OpenTelemetry, vinculadas a la traza de la request o de la conexión. Los logs de error se registran incluso cuando la traza no se muestrea.

Los logs de excepciones incluyen el tipo, mensaje y stack trace de la excepción. Los mensajes y stack traces pueden contener información sensible. Usa los procesadores de logs de tu provider para filtrarlos o redactarlos, o define `logs` como `False` para deshabilitar estos logs.

FastAPI también registra fallos de validación de requests como logs de advertencia con la route y el conteo de errores. Estos logs no incluyen la entrada inválida.

## Elige qué registrar { #choose-what-to-record }

El diccionario `telemetry` también acepta estas configuraciones:

| Configuración | Propósito | Por defecto |
| --- | --- | --- |
| `tracing` | Registrar spans de requests HTTP y conexiones WebSocket | `True` |
| `metrics` | Registrar métricas de requests HTTP | `True` |
| `logs` | Registrar fallos de validación y excepciones no manejadas | `True` |
| `operation_spans` | Añadir spans para operaciones de requests | `True` |
| `exclude` | Omitir requests cuando una función que recibe el scope ASGI devuelve `True` | `None` |
| `auto_configure` | Añadir exporters para endpoints definidos en variables de entorno | `True` |

Por ejemplo, para recopilar métricas excluyendo health checks:

```python
from fastapi import FastAPI

app = FastAPI(
    telemetry={
        "tracing": False,
        "exclude": lambda scope: scope["path"] == "/health",
    }
)
```

Define `auto_configure` como `False` cuando tu aplicación maneja por sí misma la configuración del provider, como dentro de su función lifespan.
