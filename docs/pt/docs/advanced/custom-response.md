# Resposta Personalizada - HTML, Stream, File e outras { #custom-response-html-stream-file-others }

Por padrão, o **FastAPI** irá retornar respostas utilizando `JSONResponse`.

Mas você pode sobrescrever esse comportamento utilizando `Response` diretamente, como visto em [Retornando uma Resposta Diretamente](response-directly.md){.internal-link target=_blank}.

Mas se você retornar uma `Response` diretamente (ou qualquer subclasse, como `JSONResponse`), os dados não serão convertidos automaticamente (mesmo que você declare um `response_model`), e a documentação não será gerada automaticamente (por exemplo, incluindo o "media type", no cabeçalho HTTP `Content-Type` como parte do esquema OpenAPI gerado).

Mas você também pode declarar a `Response` que você deseja utilizar (e.g. qualquer subclasse de `Response`), em um *decorador de operação de rota* utilizando o parâmetro `response_class`.

Os conteúdos que você retorna em sua *função de operação de rota* serão colocados dentro dessa `Response`.

E se a `Response` tiver um media type JSON (`application/json`), como é o caso com `JSONResponse` e `UJSONResponse`, os dados que você retornar serão automaticamente convertidos (e filtrados) com qualquer `response_model` do Pydantic que for declarado no decorador de operação de rota.

/// note | Nota

Se você utilizar uma classe de Resposta sem media type, o FastAPI esperará que sua resposta não tenha conteúdo, então ele não irá documentar o formato da resposta na documentação OpenAPI gerada.

///

## Utilizando `ORJSONResponse` { #use-orjsonresponse }

Por exemplo, se você precisa bastante de performance, você pode instalar e utilizar o <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a> e definir a resposta para ser uma `ORJSONResponse`.

Importe a classe, ou subclasse, de `Response` que você deseja utilizar e declare ela no *decorador de operação de rota*.

Para respostas grandes, retornar uma `Response` diretamente é muito mais rápido que retornar um dicionário.

Isso ocorre por que, por padrão, o FastAPI irá verificar cada item dentro do dicionário e garantir que ele seja serializável para JSON, utilizando o mesmo[Codificador Compatível com JSON](../tutorial/encoder.md){.internal-link target=_blank} explicado no tutorial. Isso permite que você retorne **objetos abstratos**, como modelos do banco de dados, por exemplo.

Mas se você tem certeza que o conteúdo que você está retornando é **serializável com JSON**, você pode passá-lo diretamente para a classe de resposta e evitar o trabalho extra que o FastAPI teria ao passar o conteúdo pelo `jsonable_encoder` antes de passar para a classe de resposta.

{* ../../docs_src/custom_response/tutorial001b.py hl[2,7] *}

/// info | Informação

O parâmetro `response_class` também será usado para definir o "media type" da resposta.

Neste caso, o cabeçalho HTTP `Content-Type` irá ser definido como `application/json`.

E será documentado como tal no OpenAPI.

///

/// tip | Dica

A `ORJSONResponse` está disponível apenas no FastAPI, e não no Starlette.

///

## Resposta HTML { #html-response }

Para retornar uma resposta com HTML diretamente do **FastAPI**, utilize `HTMLResponse`.

* Importe `HTMLResponse`
* Passe `HTMLResponse` como o parâmetro de `response_class` do seu *decorador de operação de rota*.

{* ../../docs_src/custom_response/tutorial002.py hl[2,7] *}

/// info | Informação

O parâmetro `response_class` também será usado para definir o "media type" da resposta.

Neste caso, o cabeçalho HTTP `Content-Type` será definido como `text/html`.

E será documentado como tal no OpenAPI.

///

### Retornando uma `Response` { #return-a-response }

Como visto em [Retornando uma Resposta Diretamente](response-directly.md){.internal-link target=_blank}, você também pode sobrescrever a resposta diretamente na sua *operação de rota*, ao retornar ela.

O mesmo exemplo de antes, retornando uma `HTMLResponse`, poderia parecer com:

{* ../../docs_src/custom_response/tutorial003.py hl[2,7,19] *}

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

{* ../../docs_src/custom_response/tutorial004.py hl[7,21,23] *}

Neste exemplo, a função `generate_html_response()` já cria e retorna uma `Response` em vez de retornar o HTML em uma `str`.

Ao retornar o resultado chamando `generate_html_response()`, você já está retornando uma `Response` que irá sobrescrever o comportamento padrão do **FastAPI**.

Mas se você passasse uma `HTMLResponse` em `response_class` também, o **FastAPI** saberia como documentar isso no OpenAPI e na documentação interativa como um HTML com `text/html`:

<img src="/img/tutorial/custom-response/image01.png">

## Respostas disponíveis { #available-responses }

Aqui estão algumas dos tipos de resposta disponíveis.

Lembre-se que você pode utilizar `Response` para retornar qualquer outra coisa, ou até mesmo criar uma subclasse personalizada.

/// note | Detalhes Técnicos

Você também pode utilizar `from starlette.responses import HTMLResponse`.

O **FastAPI** provê a mesma `starlette.responses` como `fastapi.responses` apenas como uma facilidade para você, desenvolvedor. Mas a maioria das respostas disponíveis vêm diretamente do Starlette.

///

### `Response` { #response }

A classe principal de respostas, todas as outras respostas herdam dela.

Você pode retorná-la diretamente.

Ela aceita os seguintes parâmetros:

* `content` - Uma sequência de caracteres (`str`) ou `bytes`.
* `status_code` - Um código de status HTTP do tipo `int`.
* `headers` - Um dicionário `dict` de strings.
* `media_type` - Uma `str` informando o media type. E.g. `"text/html"`.

O FastAPI (Starlette, na verdade) irá incluir o cabeçalho Content-Length automaticamente. Ele também irá incluir o cabeçalho Content-Type, baseado no `media_type` e acrescentando uma codificação para tipos textuais.

{* ../../docs_src/response_directly/tutorial002.py hl[1,18] *}

### `HTMLResponse` { #htmlresponse }

Usa algum texto ou sequência de bytes e retorna uma resposta HTML. Como você leu acima.

### `PlainTextResponse` { #plaintextresponse }

Usa algum texto ou sequência de bytes para retornar uma resposta de texto não formatado.

{* ../../docs_src/custom_response/tutorial005.py hl[2,7,9] *}

### `JSONResponse` { #jsonresponse }

Pega alguns dados e retorna uma resposta com codificação `application/json`.

É a resposta padrão utilizada no **FastAPI**, como você leu acima.

### `ORJSONResponse` { #orjsonresponse }

Uma alternativa mais rápida de resposta JSON utilizando o <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>, como você leu acima.

/// info | Informação

Essa resposta requer a instalação do pacote `orjson`, com o comando `pip install orjson`, por exemplo.

///

### `UJSONResponse` { #ujsonresponse }

Uma alternativa de resposta JSON utilizando a biblioteca <a href="https://github.com/ultrajson/ultrajson" class="external-link" target="_blank">`ujson`</a>.

/// info | Informação

Essa resposta requer a instalação do pacote `ujson`, com o comando `pip install ujson`, por exemplo.

///

/// warning | Atenção

`ujson` é menos cauteloso que a implementação nativa do Python na forma que os casos especiais são tratados

///

{* ../../docs_src/custom_response/tutorial001.py hl[2,7] *}

/// tip | Dica

É possível que `ORJSONResponse` seja uma alternativa mais rápida.

///

### `RedirectResponse` { #redirectresponse }

Retorna um redirecionamento HTTP. Utiliza o código de status 307 (Redirecionamento Temporário) por padrão.

Você pode retornar uma `RedirectResponse` diretamente:

{* ../../docs_src/custom_response/tutorial006.py hl[2,9] *}

---

Ou você pode utilizá-la no parâmetro `response_class`:

{* ../../docs_src/custom_response/tutorial006b.py hl[2,7,9] *}

Se você fizer isso, então você pode retornar a URL diretamente da sua *função de operação de rota*

Neste caso, o `status_code` utilizada será o padrão de `RedirectResponse`, que é `307`.

---

Você também pode utilizar o parâmetro `status_code` combinado com o parâmetro `response_class`:

{* ../../docs_src/custom_response/tutorial006c.py hl[2,7,9] *}

### `StreamingResponse` { #streamingresponse }

Recebe um gerador assíncrono ou um gerador/iterador comum e retorna o corpo da resposta de forma contínua (stream).

{* ../../docs_src/custom_response/tutorial007.py hl[2,14] *}

#### Utilizando `StreamingResponse` com objetos semelhantes a arquivos { #using-streamingresponse-with-file-like-objects }

Se você tiver um objeto <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">semelhante a um arquivo</a> (e.g. o objeto retornado por `open()`), você pode criar uma função geradora para iterar sobre esse objeto.

Dessa forma, você não precisa ler todo o arquivo na memória primeiro, e você pode passar essa função geradora para `StreamingResponse` e retorná-la.

Isso inclui muitas bibliotecas que interagem com armazenamento em nuvem, processamento de vídeos, entre outras.

{* ../../docs_src/custom_response/tutorial008.py hl[2,10:12,14] *}

1. Essa é a função geradora. É definida como "função geradora" porque contém declarações `yield` nela.
2. Ao utilizar o bloco `with`, nós garantimos que o objeto semelhante a um arquivo é fechado após a função geradora ser finalizada. Isto é, após a resposta terminar de ser enviada.
3. Essa declaração `yield from` informa a função para iterar sobre essa coisa nomeada de `file_like`. E então, para cada parte iterada, fornece essa parte como se viesse dessa função geradora (`iterfile`).

    Então, é uma função geradora que transfere o trabalho de "geração" para alguma outra coisa interna.

    Fazendo dessa forma, podemos colocá-la em um bloco `with`, e assim garantir que o objeto semelhante a um arquivo é fechado quando a função termina.

/// tip | Dica

Perceba que aqui estamos utilizando o `open()` da biblioteca padrão que não suporta `async` e `await`, e declaramos a operação de rota com o `def` básico.

///

### `FileResponse` { #fileresponse }

Envia um arquivo  de forma assíncrona e contínua (stream).

Recebe um conjunto de argumentos do construtor diferente dos outros tipos de resposta:

* `path` - O caminho do arquivo que será transmitido
* `headers` - quaisquer cabeçalhos que serão incluídos, como um dicionário.
* `media_type` - Uma string com o media type. Se não for definida, o media type é inferido a partir do nome ou caminho do arquivo.
* `filename` - Se for definido, é incluído no cabeçalho `Content-Disposition`.

Respostas de Arquivos incluem o tamanho do arquivo, data da última modificação e ETags apropriados, nos cabeçalhos `Content-Length`, `Last-Modified` e `ETag`, respectivamente.

{* ../../docs_src/custom_response/tutorial009.py hl[2,10] *}

Você também pode usar o parâmetro `response_class`:

{* ../../docs_src/custom_response/tutorial009b.py hl[2,8,10] *}

Nesse caso, você pode retornar o caminho do arquivo diretamente da sua *função de operação de rota*.

## Classe de resposta personalizada { #custom-response-class }

Você pode criar sua própria classe de resposta, herdando de `Response` e usando essa nova classe.

Por exemplo, vamos supor que você queira utilizar o <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>, mas com algumas configurações personalizadas que não estão incluídas na classe `ORJSONResponse`.

Vamos supor também que você queira retornar um JSON indentado e formatado, então você quer utilizar a opção `orjson.OPT_INDENT_2` do orjson.

Você poderia criar uma classe `CustomORJSONResponse`. A principal coisa a ser feita é sobrecarregar o método render da classe Response, `Response.render(content)`, que retorna o conteúdo em bytes:

{* ../../docs_src/custom_response/tutorial009c.py hl[9:14,17] *}

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

## Classe de resposta padrão { #default-response-class }

Quando você criar uma instância da classe **FastAPI** ou um `APIRouter` você pode especificar qual classe de resposta utilizar por padrão.

O padrão que define isso é o `default_response_class`.

No exemplo abaixo, o **FastAPI** irá utilizar `ORJSONResponse` por padrão, em todas as *operações de rota*, em vez de `JSONResponse`.

{* ../../docs_src/custom_response/tutorial010.py hl[2,4] *}

/// tip | Dica

Você ainda pode substituir `response_class` em *operações de rota* como antes.

///

## Documentação adicional { #additional-documentation }

Você também pode declarar o media type e muitos outros detalhes no OpenAPI utilizando `responses`: [Retornos Adicionais no OpenAPI](additional-responses.md){.internal-link target=_blank}.
