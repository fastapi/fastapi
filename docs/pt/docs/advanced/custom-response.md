# Resposta Personalizada - HTML, Stream, File e outras { #custom-response-html-stream-file-others }

Por padrão, o **FastAPI** retornará respostas JSON.

Você pode sobrescrever isso retornando uma `Response` diretamente, como visto em [Retornando uma Resposta Diretamente](response-directly.md).

Mas se você retornar uma `Response` diretamente (ou qualquer subclasse, como `JSONResponse`), os dados não serão convertidos automaticamente (mesmo que você declare um `response_model`), e a documentação não será gerada automaticamente (por exemplo, incluindo o "media type" específico, no cabeçalho HTTP `Content-Type` como parte do OpenAPI gerado).

Mas você também pode declarar a `Response` que deseja utilizar (e.g. qualquer subclasse de `Response`), no *decorador de operação de rota* usando o parâmetro `response_class`.

O conteúdo que você retorna da sua *função de operação de rota* será colocado dentro dessa `Response`.

/// note | Nota

Se você utilizar uma classe de resposta sem media type, o FastAPI esperará que sua resposta não tenha conteúdo, então ele não irá documentar o formato da resposta na documentação OpenAPI gerada.

///

## Respostas JSON { #json-responses }

Por padrão, o FastAPI retorna respostas JSON.

Se você declarar um [Modelo de Resposta](../tutorial/response-model.md), o FastAPI irá usá-lo para serializar os dados para JSON, usando Pydantic.

Se você não declarar um modelo de resposta, o FastAPI usará o `jsonable_encoder` explicado em [Codificador Compatível com JSON](../tutorial/encoder.md) e o colocará em uma `JSONResponse`.

Se você declarar uma `response_class` com um media type JSON (`application/json`), como no caso de `JSONResponse`, os dados que você retorna serão automaticamente convertidos (e filtrados) com qualquer `response_model` do Pydantic que você declarou no *decorador de operação de rota*. Mas os dados não serão serializados para bytes JSON com Pydantic; em vez disso, serão convertidos com o `jsonable_encoder` e então passados para a classe `JSONResponse`, que fará a serialização para bytes usando a biblioteca padrão de JSON do Python.

### Performance com JSON { #json-performance }

Resumindo, se você quer o máximo de performance, use um [Modelo de Resposta](../tutorial/response-model.md) e não declare uma `response_class` no *decorador de operação de rota*.

{* ../../docs_src/response_model/tutorial001_01_py310.py ln[15:17] hl[16] *}

## Resposta HTML { #html-response }

Para retornar uma resposta com HTML diretamente do **FastAPI**, utilize `HTMLResponse`.

* Importe `HTMLResponse`.
* Passe `HTMLResponse` como o parâmetro de `response_class` do seu *decorador de operação de rota*.

{* ../../docs_src/custom_response/tutorial002_py310.py hl[2,7] *}

/// info | Informação

O parâmetro `response_class` também será usado para definir o "media type" da resposta.

Neste caso, o cabeçalho HTTP `Content-Type` será definido como `text/html`.

E será documentado como tal no OpenAPI.

///

### Retornando uma `Response` { #return-a-response }

Como visto em [Retornando uma Resposta Diretamente](response-directly.md), você também pode sobrescrever a resposta diretamente na sua *operação de rota*, ao retornar ela.

O mesmo exemplo de antes, retornando uma `HTMLResponse`, poderia parecer com:

{* ../../docs_src/custom_response/tutorial003_py310.py hl[2,7,19] *}

/// warning | Atenção

Uma `Response` retornada diretamente em sua *função de operação de rota* não será documentada no OpenAPI (por exemplo, o `Content-Type` não será documentado) e não será visível na documentação interativa automática.

///

/// info | Informação

Obviamente, o cabeçalho `Content-Type`, o código de status, etc, virão do objeto `Response` que você retornou.

///

### Documentar no OpenAPI e sobrescrever `Response` { #document-in-openapi-and-override-response }

Se você deseja sobrescrever a resposta dentro de uma função, mas ao mesmo tempo documentar o "media type" no OpenAPI, você pode utilizar o parâmetro `response_class` E retornar um objeto `Response`.

A `response_class` será usada apenas para documentar o OpenAPI da *operação de rota*, mas sua `Response` será usada como foi definida.

#### Retornando uma `HTMLResponse` diretamente { #return-an-htmlresponse-directly }

Por exemplo, poderia ser algo como:

{* ../../docs_src/custom_response/tutorial004_py310.py hl[7,21,23] *}

Neste exemplo, a função `generate_html_response()` já cria e retorna uma `Response` em vez de retornar o HTML em uma `str`.

Ao retornar o resultado chamando `generate_html_response()`, você já está retornando uma `Response` que irá sobrescrever o comportamento padrão do **FastAPI**.

Mas como você passou `HTMLResponse` em `response_class` também, o **FastAPI** saberá como documentar isso no OpenAPI e na documentação interativa como um HTML com `text/html`:

<img src="/img/tutorial/custom-response/image01.png">

## Respostas disponíveis { #available-responses }

Aqui estão algumas das respostas disponíveis.

Lembre-se que você pode utilizar `Response` para retornar qualquer outra coisa, ou até mesmo criar uma subclasse personalizada.

/// note | Detalhes Técnicos

Você também pode utilizar `from starlette.responses import HTMLResponse`.

O **FastAPI** provê a mesma `starlette.responses` como `fastapi.responses` apenas como uma facilidade para você, desenvolvedor. Mas a maioria das respostas disponíveis vêm diretamente do Starlette.

///

### `Response` { #response }

A classe principal de respostas, todas as outras respostas herdam dela.

Você pode retorná-la diretamente.

Ela aceita os seguintes parâmetros:

* `content` - Uma `str` ou `bytes`.
* `status_code` - Um código de status HTTP do tipo `int`.
* `headers` - Um `dict` de strings.
* `media_type` - Uma `str` informando o media type. E.g. `"text/html"`.

O FastAPI (Starlette, na verdade) irá incluir o cabeçalho Content-Length automaticamente. Ele também irá incluir o cabeçalho Content-Type, baseado no `media_type` e acrescentando uma codificação para tipos textuais.

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

### `HTMLResponse` { #htmlresponse }

Usa algum texto ou sequência de bytes e retorna uma resposta HTML. Como você leu acima.

### `PlainTextResponse` { #plaintextresponse }

Usa algum texto ou sequência de bytes para retornar uma resposta de texto não formatado.

{* ../../docs_src/custom_response/tutorial005_py310.py hl[2,7,9] *}

### `JSONResponse` { #jsonresponse }

Pega alguns dados e retorna uma resposta com codificação `application/json`.

É a resposta padrão utilizada no **FastAPI**, como você leu acima.

/// note | Detalhes Técnicos

Mas se você declarar um modelo de resposta ou tipo de retorno, isso será usado diretamente para serializar os dados para JSON, e uma resposta com o media type correto para JSON será retornada diretamente, sem usar a classe `JSONResponse`.

Esta é a forma ideal para obter a melhor performance.

///

### `RedirectResponse` { #redirectresponse }

Retorna um redirecionamento HTTP. Utiliza o código de status 307 (Redirecionamento Temporário) por padrão.

Você pode retornar uma `RedirectResponse` diretamente:

{* ../../docs_src/custom_response/tutorial006_py310.py hl[2,9] *}

---

Ou você pode utilizá-la no parâmetro `response_class`:

{* ../../docs_src/custom_response/tutorial006b_py310.py hl[2,7,9] *}

Se você fizer isso, então você pode retornar a URL diretamente da sua *função de operação de rota*.

Neste caso, o `status_code` utilizado será o padrão de `RedirectResponse`, que é `307`.

---

Você também pode utilizar o parâmetro `status_code` combinado com o parâmetro `response_class`:

{* ../../docs_src/custom_response/tutorial006c_py310.py hl[2,7,9] *}

### `StreamingResponse` { #streamingresponse }

Recebe um gerador assíncrono ou um gerador/iterador comum (uma função com `yield`) e transmite (stream) o corpo da resposta.

{* ../../docs_src/custom_response/tutorial007_py310.py hl[3,16] *}

/// note | Detalhes Técnicos

Uma tarefa `async` só pode ser cancelada quando alcança um `await`. Se não houver `await`, o gerador (função com `yield`) não pode ser cancelado adequadamente e pode continuar executando mesmo após o cancelamento ser solicitado.

Como este pequeno exemplo não precisa de nenhuma instrução `await`, adicionamos um `await anyio.sleep(0)` para dar ao event loop a chance de lidar com o cancelamento.

Isso seria ainda mais importante com streams grandes ou infinitos.

///

/// tip | Dica

Em vez de retornar uma `StreamingResponse` diretamente, você deveria provavelmente seguir o estilo em [Transmitir Dados](./stream-data.md), é muito mais conveniente e lida com cancelamento nos bastidores para você.

Se você estiver transmitindo JSON Lines, siga o tutorial [Transmitir JSON Lines](../tutorial/stream-json-lines.md).

///

### `FileResponse` { #fileresponse }

Envia um arquivo de forma assíncrona e contínua (stream).

Recebe um conjunto de argumentos do construtor diferente dos outros tipos de resposta:

* `path` - O caminho do arquivo que será transmitido.
* `headers` - Quaisquer cabeçalhos personalizados a serem incluídos, como um dicionário.
* `media_type` - Uma string com o media type. Se não for definida, o nome do arquivo ou path será usado para inferir um media type.
* `filename` - Se definido, será incluído no cabeçalho `Content-Disposition`.

Respostas de arquivos incluirão os cabeçalhos apropriados `Content-Length`, `Last-Modified` e `ETag`.

{* ../../docs_src/custom_response/tutorial009_py310.py hl[2,10] *}

Você também pode usar o parâmetro `response_class`:

{* ../../docs_src/custom_response/tutorial009b_py310.py hl[2,8,10] *}

Nesse caso, você pode retornar o path do arquivo diretamente da sua *função de operação de rota*.

## Classe de resposta personalizada { #custom-response-class }

Você pode criar sua própria classe de resposta personalizada, herdando de `Response` e usando-a.

Por exemplo, vamos supor que você queira usar [`orjson`](https://github.com/ijl/orjson) com algumas configurações.

Vamos supor que você queira retornar um JSON indentado e formatado, então você quer utilizar a opção `orjson.OPT_INDENT_2` do orjson.

Você poderia criar uma `CustomORJSONResponse`. A principal coisa que você tem que fazer é criar um método `Response.render(content)` que retorne o conteúdo como `bytes`:

{* ../../docs_src/custom_response/tutorial009c_py310.py hl[9:14,17] *}

Agora em vez de retornar:

```json
{"message": "Hello World"}
```

...essa resposta retornará:

```json
{
  "message": "Hello World"
}
```

Obviamente, você provavelmente vai encontrar maneiras muito melhores de se aproveitar disso do que a formatação de JSON. 😉

### `orjson` ou Modelo de Resposta { #orjson-or-response-model }

Se o que você procura é performance, provavelmente é melhor usar um [Modelo de Resposta](../tutorial/response-model.md) do que uma resposta com `orjson`.

Com um modelo de resposta, o FastAPI usará o Pydantic para serializar os dados para JSON, sem passos intermediários, como convertê-los com `jsonable_encoder`, o que aconteceria em qualquer outro caso.

E, por baixo dos panos, o Pydantic usa os mesmos mecanismos em Rust que o `orjson` para serializar para JSON, então você já terá a melhor performance com um modelo de resposta.

## Classe de resposta padrão { #default-response-class }

Quando você criar uma instância da classe **FastAPI** ou um `APIRouter` você pode especificar qual classe de resposta utilizar por padrão.

O parâmetro que define isso é o `default_response_class`.

No exemplo abaixo, o **FastAPI** utilizará `HTMLResponse` por padrão, em todas as *operações de rota*, em vez de JSON.

{* ../../docs_src/custom_response/tutorial010_py310.py hl[2,4] *}

/// tip | Dica

Você ainda pode substituir `response_class` em *operações de rota* como antes.

///

## Documentação adicional { #additional-documentation }

Você também pode declarar o media type e muitos outros detalhes no OpenAPI utilizando `responses`: [Respostas Adicionais no OpenAPI](additional-responses.md).
