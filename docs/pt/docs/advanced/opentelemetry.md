# OpenTelemetry { #opentelemetry }

Quando sua API está em execução, você pode querer saber quanto tráfego ela recebe, quais requests são lentos e quando ocorrem erros.

**Telemetria** são dados sobre o comportamento da sua aplicação que ajudam a responder a essas perguntas. Os tipos comuns incluem:

- **Métricas**: medições que você pode resumir ao longo do tempo, como os tempos de response e o número de requests em processamento.
- **Traces**: registros de requests individuais e das operações realizadas para processá-los. Cada operação cronometrada é chamada de **span**.
- **Logs**: registros de eventos com marcação de tempo, como a inicialização de uma aplicação ou a falha de uma operação.

[**OpenTelemetry**](https://opentelemetry.io/) é um conjunto de padrões e ferramentas para coletar telemetria e enviá-la a um serviço de monitoramento, onde você pode explorá-la em painéis.

**O FastAPI oferece suporte a OpenTelemetry por padrão** para traces de requests HTTP, métricas e logs. As conexões WebSocket também fornecem traces e logs. Para visualizar esses dados, configure um serviço de monitoramento para recebê-los.

## Instale o FastAPI { #install-fastapi }

Instale o FastAPI com os extras `standard`, que incluem os pacotes para enviar telemetria:

<div class="termy">

```console
$ uv add "fastapi[standard]"
---> 100%
```

</div>

## Crie a aplicação { #create-the-app }

Crie um arquivo `main.py`:

{* ../../docs_src/opentelemetry/tutorial001_py310.py *}

Observe que tudo funciona por padrão, sem precisar escrever código personalizado para a telemetria funcionar.

## FastAPI Cloud { #fastapi-cloud }

Ao fazer o deploy no [FastAPI Cloud](https://fastapicloud.com) com `fastapi[standard]`, as métricas funcionam automaticamente. Não é necessário configurar mais nada.

Nos planos Pro, você pode visualizar contagens de requests, taxas de erro e tempos de response no [painel de métricas](https://fastapicloud.com/docs/monitoring-and-performance/metrics/).

<img src="/img/tutorial/opentelemetry/image01.png" alt="Painel de métricas do FastAPI Cloud Pro com dados de exemplo">

## Outros serviços de monitoramento { #other-monitoring-services }

Para enviar telemetria a outro serviço de monitoramento, configure um endpoint que aceite **OTLP**, o protocolo do OpenTelemetry para enviar telemetria. Use o endpoint base HTTP/protobuf do serviço.

Defina estas variáveis de ambiente, substituindo a URL de exemplo pelo seu endpoint:

```bash
export OTEL_SERVICE_NAME=my-api
export OTEL_EXPORTER_OTLP_ENDPOINT=https://collector.example.com
```

`OTEL_SERVICE_NAME` identifica sua aplicação no serviço de monitoramento. O endpoint é a URL base para receber dados. Os traces são enviados para `/v1/traces`, as métricas para `/v1/metrics` e os logs para `/v1/logs` nessa URL.

Se o serviço exigir autenticação, defina `OTEL_EXPORTER_OTLP_HEADERS` com os cabeçalhos especificados por ele, por exemplo, `api-key=YOUR_API_KEY`.

## Execute a aplicação { #run-the-app }

Inicie a aplicação no mesmo terminal:

<div class="termy">

```console
$ uv run fastapi run
```

</div>

Em outro terminal, envie um request:

```console
$ curl http://127.0.0.1:8000/items/1
{"item_id":1}
```

Abra seu serviço de monitoramento e procure `my-api`. Após a próxima exportação, você poderá ver um trace com um span `GET /items/{item_id}`, junto com métricas de contagem de requests, duração de responses e requests ativos.

## Personalize a telemetria { #customize-telemetry }

### Configure provedores e exportadores { #configure-providers-and-exporters }

Um **provedor** fornece os objetos que registram traces, métricas ou logs. Sua configuração controla como esses dados são processados e exportados.

Bibliotecas de telemetria podem configurar os provedores globais do OpenTelemetry. Configure a biblioteca antes de iniciar a aplicação, e o FastAPI usará esses provedores automaticamente.

Quando um endpoint OTLP é definido no ambiente, o FastAPI adiciona um exportador para esse destino a cada provedor habilitado. Os exportadores existentes continuam enviando dados aos seus destinos.

Configure cada destino uma única vez. Se outra biblioteca já cuida do destino definido no ambiente, desabilite a exportação dela para esse destino ou desative a configuração automática do FastAPI:

```python
app = FastAPI(telemetry={"auto_configure": False})
```

Você também pode passar um provedor diretamente no dicionário `telemetry`. Por exemplo, este provedor usa o exportador de console do OpenTelemetry para exibir spans de requests no seu terminal:

{* ../../docs_src/opentelemetry/tutorial002_py310.py hl[2:8] *}

O **exportador** envia os spans ao destino. `BatchSpanProcessor` agrupa spans e os envia em segundo plano. Substitua o exportador de console por um fornecido pela sua biblioteca de monitoramento para usar o destino dela. Consulte o [tutorial de instrumentação Python do OpenTelemetry](https://opentelemetry.io/docs/languages/python/instrumentation/) para mais opções de configuração.

Use `meter_provider` ou `logger_provider` no mesmo dicionário para fornecer um provedor de métricas ou logs. A aplicação ou biblioteca que cria um provedor gerencia seu encerramento. O FastAPI gerencia os componentes de exportação que adiciona.

/// warning | Atenção

O OpenTelemetry usa provedores globais por padrão. A configuração independente de telemetria para [subaplicações montadas](sub-applications.md) não é garantida.

///

### Rastreie operações de requests { #trace-request-operations }

Por padrão, os traces de requests incluem spans para resolver dependências, executar sua função de operação de rota, serializar a response e executar cada tarefa em `BackgroundTasks` do FastAPI. Esses spans usam o mesmo provedor e os mesmos exportadores.

Os spans de tarefas em segundo plano continuam fazendo parte do trace do request. Eles são executados após o término do span da response HTTP, portanto não aumentam o tempo de response medido.

Para registrar apenas o span do request HTTP, defina `operation_spans` como `False`:

{* ../../docs_src/opentelemetry/tutorial003_py310.py hl[3] *}


### Rastreie conexões WebSocket { #trace-websocket-connections }

Cada conexão WebSocket tem um span como `WS /ws/{room}`, que abrange o manipulador e a limpeza das dependências. Ele usa os mesmos provedores e configurações, incluindo `operation_spans` para a resolução de dependências e a execução do endpoint.

As métricas de requests HTTP abrangem apenas requests HTTP. Desconexões normais de WebSocket com os códigos `1000` ou `1001` não produzem logs de erro.

### Inspecione erros { #inspect-errors }

O FastAPI registra exceções não tratadas como logs do OpenTelemetry, vinculados ao trace do request ou da conexão. Os logs de erro são registrados mesmo quando o trace não é selecionado na amostragem.

Os logs de exceções incluem o tipo, a mensagem e o stack trace da exceção. Mensagens e stack traces podem conter informações sensíveis. Use os processadores de logs do seu provedor para filtrar ou ocultar essas informações, ou defina `logs` como `False` para desabilitar esses logs.

O FastAPI também registra falhas de validação de requests como logs de aviso com a rota e a contagem de erros. Esses logs não incluem os dados de entrada inválidos.

## Escolha o que registrar { #choose-what-to-record }

O dicionário `telemetry` também aceita estas configurações:

| Configuração | Finalidade | Padrão |
| --- | --- | --- |
| `tracing` | Registrar spans de requests HTTP e conexões WebSocket | `True` |
| `metrics` | Registrar métricas de requests HTTP | `True` |
| `logs` | Registrar falhas de validação e exceções não tratadas | `True` |
| `operation_spans` | Adicionar spans para operações de requests | `True` |
| `exclude` | Ignorar requests quando uma função que recebe o escopo ASGI retorna `True` | `None` |
| `auto_configure` | Adicionar exportadores para endpoints definidos em variáveis de ambiente | `True` |

Por exemplo, para coletar métricas excluindo verificações de integridade:

```python
from fastapi import FastAPI

app = FastAPI(
    telemetry={
        "tracing": False,
        "exclude": lambda scope: scope["path"] == "/health",
    }
)
```

Defina `auto_configure` como `False` quando sua aplicação cuidar da configuração dos provedores por conta própria, por exemplo, dentro da função lifespan.
