# WebSockets

Você pode usar  <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API" class="external-link" target="_blank">WebSockets</a> com **FastAPI**.

## Instalando `WebSockets`

Garanta que você criou um [ambiente virtual](../virtual-environments.md){.internal-link target=_blank}, o ativou e instalou o `websockets`:

<div class="termy">

```console
$ pip install websockets

---> 100%
```

</div>

## Cliente WebSockets

### Em produção

Em seu sistema de produção, você provavelmente tem um frontend criado com um framework moderno como React, Vue.js ou Angular.

E para comunicar usando WebSockets com seu backend, você provavelmente usaria as utilidades do seu frontend.

Ou você pode ter um aplicativo móvel nativo que se comunica diretamente com seu backend WebSocket, em código nativo.

Ou você pode ter qualquer outra forma de comunicar com o endpoint WebSocket.

---

Mas para este exemplo, usaremos um documento HTML muito simples com algum JavaScript, tudo dentro de uma string longa.

Esse, é claro, não é o ideal e você não o usaria para produção.

Na produção, você teria uma das opções acima.

Mas é a maneira mais simples de focar no lado do servidor de WebSockets e ter um exemplo funcional:

```Python hl_lines="2  6-38  41-43"
{!../../docs_src/websockets/tutorial001.py!}
```

## Criando um `websocket`

Em sua aplicação **FastAPI**, crie um `websocket`:

```Python hl_lines="1  46-47"
{!../../docs_src/websockets/tutorial001.py!}
```

/// note | "Detalhes Técnicos"

Você também poderia usar `from starlette.websockets import WebSocket`.

A **FastAPI** fornece o mesmo `WebSocket` diretamente apenas como uma conveniência para você, o desenvolvedor. Mas ele vem diretamente do Starlette.

///

## Aguardar por mensagens e enviar mensagens

Em seu rota WebSocket você pode `await` por mensagens e enviar mensagens.

```Python hl_lines="48-52"
{!../../docs_src/websockets/tutorial001.py!}
```

Você pode receber e enviar dados binários, de texto e JSON.

## Tente você mesmo

Se seu arquivo for nomeado `main.py`, execute sua aplicação com:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Abra seu broser em: <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Você verá uma página simples como:

<img src="/img/tutorial/websockets/image01.png">

Você pode digitar mensagens na caixa de entrada e enviá-las:

<img src="/img/tutorial/websockets/image02.png">

E sua aplicação **FastAPI** com WebSockets responderá de volta:

<img src="/img/tutorial/websockets/image03.png">

Você pode enviar (e receber) muitas mensagens:

<img src="/img/tutorial/websockets/image04.png">

E todas elas usarão a mesma conexão WebSocket.

## Usando `Depends` e outros

Nos endpoints WebSocket você pode importar do `fastapi` e usar:

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

They work the same way as for other FastAPI endpoints/*path operations*:
Eles funcionam da mesma forma que para outros endpoints FastAPI/*operações de rota*:

//// tab | Python 3.10+

```Python hl_lines="68-69  82"
{!> ../../docs_src/websockets/tutorial002_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="68-69  82"
{!> ../../docs_src/websockets/tutorial002_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="69-70  83"
{!> ../../docs_src/websockets/tutorial002_an.py!}
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | dica

Tente usar a versão `Annotated` se possível.

///

```Python hl_lines="66-67  79"
{!> ../../docs_src/websockets/tutorial002_py310.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | dica

Tente usar a versão `Annotated` se possível.

///

```Python hl_lines="68-69  81"
{!> ../../docs_src/websockets/tutorial002.py!}
```

////

/// info

Como isso é um WebSocket, não faz muito sentido levantar uma `HTTPException`, em vez disso levantamos uma `WebSocketException`.

Você pode usar um código de fechamento dos <a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">códigos válidos definidos na especificação</a>.

///

### Tente os WebSockets com dependências

Se seu arquivo for nomeado `main.py`, execute sua aplicação com:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Abrar seu browser em: <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Lá você pode definir:

* O "Item ID", usado na rota.
* O "Token" usado como um parâmetro de consulta.

/// tip | dica

Perceba que a consulta `token` será manipulada por uma dependência.

///

Com isso você pode conectar o WebSocket e então enviar e receber mensagens:

<img src="/img/tutorial/websockets/image05.png">

## Lidando com desconexões e múltiplos clientes

Quando uma conexão WebSocket é fechada, o `await websocket.receive_text()` levantará uma exceção `WebSocketDisconnect`, que você pode então capturar e lidar como neste exemplo.

//// tab | Python 3.9+

```Python hl_lines="79-81"
{!> ../../docs_src/websockets/tutorial003_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="81-83"
{!> ../../docs_src/websockets/tutorial003.py!}
```

////

Para testar:

* Abrar o aplicativo com várias abas do navegador.
* Escreva mensagens a partir delas.
* Então feche uma das abas.

Isso levantará a exceção `WebSocketDisconnect`, e todos os outros clientes receberão uma mensagem como:

```
Client #1596980209979 left the chat
```

/// tip | dica

O app acima é um exemplo mínimo e simples para demonstrar como lidar e transmitir mensagens para várias conexões WebSocket.

Mas tenha em mente que, como tudo é manipulado na memória, em uma única lista, ele só funcionará enquanto o processo estiver em execução e só funcionará com um único processo.

Se você precisa de algo fácil de integrar com o FastAPI, mas que seja mais robusto, suportado por Redis, PostgreSQL ou outros, verifique o <a href="https://github.com/encode/broadcaster" class="external-link" target="_blank">encode/broadcaster</a>.

///

## Mais informações

Para aprender mais sobre as opções, verifique a documentação do Starlette para:

* <a href="https://www.starlette.io/websockets/" class="external-link" target="_blank">A classe `WebSocket`</a>.
* <a href="https://www.starlette.io/endpoints/#websocketendpoint" class="external-link" target="_blank">Manipulação de WebSockets baseada em classes</a>.
