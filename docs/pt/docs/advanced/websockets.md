# WebSockets { #websockets }

Você pode usar <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API" class="external-link" target="_blank">WebSockets</a> com **FastAPI**.

## Instale `websockets` { #install-websockets }

Garanta que você criou um [ambiente virtual](../virtual-environments.md){.internal-link target=_blank}, o ativou e instalou o `websockets` (uma biblioteca Python que facilita o uso do protocolo "WebSocket"):

<div class="termy">

```console
$ pip install websockets

---> 100%
```

</div>

## Cliente WebSockets { #websockets-client }

### Em produção { #in-production }

Em seu sistema de produção, você provavelmente tem um frontend criado com um framework moderno como React, Vue.js ou Angular.

E para comunicar usando WebSockets com seu backend, você provavelmente usaria as utilidades do seu frontend.

Ou você pode ter um aplicativo móvel nativo que se comunica diretamente com seu backend WebSocket, em código nativo.

Ou você pode ter qualquer outra forma de comunicar com o endpoint WebSocket.

---

Mas para este exemplo, usaremos um documento HTML muito simples com algum JavaScript, tudo dentro de uma string longa.

Esse, é claro, não é o ideal e você não o usaria para produção.

Na produção, você teria uma das opções acima.

Mas é a maneira mais simples de focar no lado do servidor de WebSockets e ter um exemplo funcional:

{* ../../docs_src/websockets/tutorial001.py hl[2,6:38,41:43] *}

## Crie um `websocket` { #create-a-websocket }

Em sua aplicação **FastAPI**, crie um `websocket`:

{* ../../docs_src/websockets/tutorial001.py hl[1,46:47] *}

/// note | Detalhes Técnicos

Você também poderia usar `from starlette.websockets import WebSocket`.

A **FastAPI** fornece o mesmo `WebSocket` diretamente apenas como uma conveniência para você, o desenvolvedor. Mas ele vem diretamente do Starlette.

///

## Aguarde mensagens e envie mensagens { #await-for-messages-and-send-messages }

Em sua rota WebSocket você pode esperar (`await`) por mensagens e enviar mensagens.

{* ../../docs_src/websockets/tutorial001.py hl[48:52] *}

Você pode receber e enviar dados binários, de texto e JSON.

## Tente { #try-it }

Se seu arquivo for nomeado `main.py`, execute sua aplicação com:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Abra seu navegador em: <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Você verá uma página simples como:

<img src="/img/tutorial/websockets/image01.png">

Você pode digitar mensagens na caixa de entrada e enviá-las:

<img src="/img/tutorial/websockets/image02.png">

E sua aplicação **FastAPI** com WebSockets responderá de volta:

<img src="/img/tutorial/websockets/image03.png">

Você pode enviar (e receber) muitas mensagens:

<img src="/img/tutorial/websockets/image04.png">

E todas elas usarão a mesma conexão WebSocket.

## Usando `Depends` e outros { #using-depends-and-others }

Nos endpoints WebSocket você pode importar do `fastapi` e usar:

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

Eles funcionam da mesma forma que para outros endpoints FastAPI/*operações de rota*:

{* ../../docs_src/websockets/tutorial002_an_py310.py hl[68:69,82] *}

/// info | Informação

Como isso é um WebSocket, não faz muito sentido levantar uma `HTTPException`, em vez disso levantamos uma `WebSocketException`.

Você pode usar um código de fechamento dos <a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">códigos válidos definidos na especificação</a>.

///

### Tente os WebSockets com dependências { #try-the-websockets-with-dependencies }

Se seu arquivo for nomeado `main.py`, execute sua aplicação com:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Abra seu navegador em: <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Lá você pode definir:

* O "Item ID", usado no path.
* O "Token" usado como um parâmetro de consulta.

/// tip | Dica

Perceba que a consulta `token` será manipulada por uma dependência.

///

Com isso você pode conectar o WebSocket e então enviar e receber mensagens:

<img src="/img/tutorial/websockets/image05.png">

## Lidando com desconexões e múltiplos clientes { #handling-disconnections-and-multiple-clients }

Quando uma conexão WebSocket é fechada, o `await websocket.receive_text()` levantará uma exceção `WebSocketDisconnect`, que você pode então capturar e lidar como neste exemplo.

{* ../../docs_src/websockets/tutorial003_py39.py hl[79:81] *}

Para testar:

* Abra o aplicativo com várias abas do navegador.
* Escreva mensagens a partir delas.
* Então feche uma das abas.

Isso levantará a exceção `WebSocketDisconnect`, e todos os outros clientes receberão uma mensagem como:

```
Client #1596980209979 left the chat
```

/// tip | Dica

O app acima é um exemplo mínimo e simples para demonstrar como lidar e transmitir mensagens para várias conexões WebSocket.

Mas tenha em mente que, como tudo é manipulado na memória, em uma única list, ele só funcionará enquanto o processo estiver em execução e só funcionará com um único processo.

Se você precisa de algo fácil de integrar com o FastAPI, mas que seja mais robusto, suportado por Redis, PostgreSQL ou outros, verifique o <a href="https://github.com/encode/broadcaster" class="external-link" target="_blank">encode/broadcaster</a>.

///

## Mais informações { #more-info }

Para aprender mais sobre as opções, verifique a documentação do Starlette para:

* <a href="https://www.starlette.dev/websockets/" class="external-link" target="_blank">A classe `WebSocket`</a>.
* <a href="https://www.starlette.dev/endpoints/#websocketendpoint" class="external-link" target="_blank">Manipulação de WebSockets baseada em classes</a>.
