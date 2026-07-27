# Manipulação de erros { #handling-errors }

Há diversas situações em que você precisa notificar um erro a um cliente que está utilizando a sua API.

Esse cliente pode ser um browser com um frontend, o código de outra pessoa, um dispositivo IoT, etc.

Pode ser que você precise comunicar ao cliente que:

* O cliente não tem privilégios suficientes para aquela operação.
* O cliente não tem acesso aquele recurso.
* O item que o cliente estava tentando acessar não existe.
* etc.

Nesses casos, você normalmente retornaria um **HTTP status code** na faixa de **400** (do 400 ao 499).

Isso é similar aos status codes HTTP 200 (do 200 ao 299). Esses status codes "200" significam que, de algum modo, houve um "sucesso" na request.

Os status codes na faixa dos 400 significam que houve um erro por parte do cliente.

Você se lembra de todos aqueles erros **"404 Not Found"** (e piadas)?

## Use o `HTTPException` { #use-httpexception }

Para retornar responses HTTP com erros ao cliente, use o `HTTPException`.

### Importe `HTTPException` { #import-httpexception }

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[1] *}

### Lance uma `HTTPException` no seu código { #raise-an-httpexception-in-your-code }

`HTTPException` é uma exceção normal do Python com dados adicionais relevantes para APIs.

Como é uma exceção do Python, você não dá `return` nela, você dá `raise` nela.

Isso também significa que, se você está dentro de uma função de utilidade que está chamando dentro da sua *função de operação de rota*, e lança a `HTTPException` dentro dessa função de utilidade, o restante do código na *função de operação de rota* não será executado, a request será encerrada imediatamente e o erro HTTP da `HTTPException` será enviado ao cliente.

O benefício de lançar uma exceção em vez de retornar um valor ficará mais evidente na seção sobre Dependências e Segurança.

Neste exemplo, quando o cliente solicita um item por um ID que não existe, lance uma exceção com status code `404`:

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[11] *}

### A response resultante { #the-resulting-response }

Se o cliente solicita `http://example.com/items/foo` (um `item_id` `"foo"`), esse cliente receberá um status code HTTP 200 e uma response JSON de:

```JSON
{
  "item": "The Foo Wrestlers"
}
```

Mas se o cliente solicita `http://example.com/items/bar` (um `item_id` `"bar"` inexistente), esse cliente receberá um status code HTTP 404 (o erro "not found") e uma response JSON de:

```JSON
{
  "detail": "Item not found"
}
```

/// tip | Dica

Ao lançar uma `HTTPException`, você pode passar qualquer valor que possa ser convertido para JSON como parâmetro `detail`, não apenas `str`.

Você pode passar um `dict`, uma `list`, etc.

Eles são manipulados automaticamente pelo **FastAPI** e convertidos para JSON.

///

## Adicione headers customizados { #add-custom-headers }

Há algumas situações em que é útil poder adicionar headers customizados ao erro HTTP. Por exemplo, para alguns tipos de segurança.

Você provavelmente não precisará usar isso diretamente no seu código.

Mas caso precise em um cenário avançado, você pode adicionar headers customizados:

{* ../../docs_src/handling_errors/tutorial002_py310.py hl[14] *}

## Instale manipuladores de exceções customizados { #install-custom-exception-handlers }

Você pode adicionar manipuladores de exceção customizados com [as mesmas utilidades de exceção do Starlette](https://www.starlette.dev/exceptions/).

Digamos que você tenha uma exceção customizada `UnicornException` que você (ou uma biblioteca que você usa) possa lançar com `raise`.

E você quer manipular essa exceção globalmente com o FastAPI.

Você poderia adicionar um manipulador de exceção customizado com `@app.exception_handler()`:

{* ../../docs_src/handling_errors/tutorial003_py310.py hl[5:7,13:18,24] *}

Aqui, se você fizer uma request para `/unicorns/yolo`, a *operação de rota* vai lançar com `raise` uma `UnicornException`.

Mas ela será manipulada pelo `unicorn_exception_handler`.

Assim, você receberá um erro limpo, com um status code HTTP `418` e um conteúdo JSON de:

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

/// note | Detalhes Técnicos

Você também pode usar `from starlette.requests import Request` e `from starlette.responses import JSONResponse`.

**FastAPI** fornece o mesmo `starlette.responses` como `fastapi.responses` apenas como uma conveniência para você, a pessoa desenvolvedora. Mas a maior parte das responses disponíveis vem diretamente do Starlette. O mesmo acontece com `Request`.

///

## Sobrescreva os manipuladores de exceções padrão { #override-the-default-exception-handlers }

**FastAPI** tem alguns manipuladores padrão de exceções.

Esses manipuladores são responsáveis por retornar as responses JSON padrão quando você lança com `raise` uma `HTTPException` e quando a request tem dados inválidos.

Você pode sobrescrever esses manipuladores de exceção com os seus próprios.

### Sobrescreva exceções de validação da request { #override-request-validation-exceptions }

Quando uma request contém dados inválidos, **FastAPI** internamente lança um `RequestValidationError`.

E também inclui um manipulador de exceções padrão para ele.

Para sobrescrevê-lo, importe o `RequestValidationError` e use-o com `@app.exception_handler(RequestValidationError)` para decorar o manipulador de exceções.

O manipulador de exceções receberá um `Request` e a exceção.

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[2,14:19] *}

Agora, se você for para `/items/foo`, em vez de receber o erro JSON padrão com:

```JSON
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

você receberá uma versão em texto, com:

```
Validation errors:
Field: ('path', 'item_id'), Error: Input should be a valid integer, unable to parse string as an integer
```

### Sobrescreva o manipulador de erro `HTTPException` { #override-the-httpexception-error-handler }

Do mesmo modo, você pode sobrescrever o manipulador de `HTTPException`.

Por exemplo, você poderia querer retornar uma response em texto simples em vez de JSON para estes erros:

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[3:4,9:11,25] *}

/// note | Detalhes Técnicos

Você também pode usar `from starlette.responses import PlainTextResponse`.

**FastAPI** fornece o mesmo `starlette.responses` como `fastapi.responses` apenas como uma conveniência para você, a pessoa desenvolvedora. Mas a maior parte das responses disponíveis vem diretamente do Starlette.

///

/// warning | Atenção

Tenha em mente que o `RequestValidationError` contém as informações do nome do arquivo e da linha onde o erro de validação acontece, para que você possa mostrá-las nos seus logs com as informações relevantes, se quiser.

Mas isso significa que, se você simplesmente convertê-lo para uma string e retornar essa informação diretamente, você poderia acabar vazando um pouco de informação sobre o seu sistema; por isso, aqui o código extrai e mostra cada erro de forma independente.

///

### Use o body do `RequestValidationError` { #use-the-requestvalidationerror-body }

O `RequestValidationError` contém o `body` que ele recebeu com dados inválidos.

Você poderia usá-lo enquanto desenvolve sua aplicação para registrar o body e depurá-lo, retorná-lo ao usuário, etc.

{* ../../docs_src/handling_errors/tutorial005_py310.py hl[14] *}

Agora tente enviar um item inválido como:

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

Você receberá uma response dizendo que os dados são inválidos contendo o body recebido:

```JSON hl_lines="12-15"
{
  "detail": [
    {
      "loc": [
        "body",
        "size"
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ],
  "body": {
    "title": "towel",
    "size": "XL"
  }
}
```

#### `HTTPException` do FastAPI vs `HTTPException` do Starlette { #fastapis-httpexception-vs-starlettes-httpexception }

**FastAPI** tem a sua própria `HTTPException`.

E a classe de erro `HTTPException` do **FastAPI** herda da classe de erro `HTTPException` do Starlette.

A única diferença é que a `HTTPException` do **FastAPI** aceita qualquer dado que possa ser convertido para JSON no campo `detail`, enquanto a `HTTPException` do Starlette aceita apenas strings para ele.

Portanto, você pode continuar lançando a `HTTPException` do **FastAPI** normalmente no seu código.

Mas quando registrar um manipulador de exceção, você deveria registrá-lo para a `HTTPException` do Starlette.

Dessa forma, se qualquer parte do código interno do Starlette, ou uma extensão ou plug-in do Starlette, lançar uma `HTTPException` do Starlette, seu manipulador poderá capturá-la e tratá-la.

Neste exemplo, para poder ter ambas as `HTTPException`s no mesmo código, a exceção do Starlette é renomeada para `StarletteHTTPException`:

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### Reutilize os manipuladores de exceção do **FastAPI** { #reuse-fastapis-exception-handlers }

Se você quiser usar a exceção junto com os mesmos manipuladores de exceção padrão do **FastAPI**, você pode importar e reutilizar os manipuladores de exceção padrão de `fastapi.exception_handlers`:

{* ../../docs_src/handling_errors/tutorial006_py310.py hl[2:5,15,21] *}

Neste exemplo, você está apenas imprimindo o erro com uma mensagem muito expressiva, mas a ideia é essa. Você pode usar a exceção e então simplesmente reutilizar os manipuladores de exceção padrão.
