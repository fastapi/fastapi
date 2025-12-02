# Manipulação de erros { #handling-errors }

Há diversas situações em que você precisa notificar um erro a um cliente que está utilizando a sua API.

Esse cliente pode ser um browser com um frontend, o código de outra pessoa, um dispositivo IoT, etc.

Pode ser que você precise comunicar ao cliente que:

* O cliente não tem direitos para realizar aquela operação.
* O cliente não tem acesso aquele recurso.
* O item que o cliente está tentando acessar não existe.
* etc.


Nesses casos, você normalmente retornaria um **HTTP status code** próximo ao status code na faixa do status code **400** (do 400 ao 499).

Isso é bastante similar ao caso do HTTP status code 200 (do 200 ao 299). Esses "200" status codes significam que, de algum modo, houve sucesso na requisição.

Os status codes na faixa dos 400 significam que houve um erro por parte do cliente.

Você se lembra de todos aqueles erros (e piadas) a respeito do "**404 Not Found**"?

## Use o `HTTPException` { #use-httpexception }

Para retornar ao cliente *responses* HTTP com erros, use o `HTTPException`.

### Import `HTTPException` { #import-httpexception }

{* ../../docs_src/handling_errors/tutorial001.py hl[1] *}

### Lance o `HTTPException` no seu código. { #raise-an-httpexception-in-your-code }

`HTTPException`, ao fundo, nada mais é do que a conjunção entre uma exceção comum do Python e informações adicionais relevantes para APIs.

E porque é uma exceção do Python, você não **retorna** (return) o `HTTPException`, você lança o (raise) no seu código.

Isso também significa que, se você está escrevendo uma função de utilidade, a qual você está chamando dentro da sua função de operações de caminhos, e você lança o `HTTPException` dentro da função de utilidade, o resto do seu código não será executado dentro da função de operações de caminhos. Ao contrário, o `HTTPException` irá finalizar a requisição no mesmo instante e enviará o erro HTTP oriundo do `HTTPException` para o cliente.

O benefício de lançar uma exceção em vez de retornar um valor ficará mais evidente na seção sobre Dependências e Segurança.

Neste exemplo, quando o cliente pede, na requisição, por um item cujo ID não existe, a exceção com o status code `404` é lançada:

{* ../../docs_src/handling_errors/tutorial001.py hl[11] *}

### A response resultante { #the-resulting-response }

Se o cliente faz uma requisição para `http://example.com/items/foo` (um `item_id` `"foo"`), esse cliente receberá um HTTP status code 200, e uma resposta JSON:


```JSON
{
  "item": "The Foo Wrestlers"
}
```

Mas se o cliente faz uma requisição para `http://example.com/items/bar` (ou seja, um não existente `item_id "bar"`), esse cliente receberá um HTTP status code 404 (o erro "não encontrado" — *not found error*), e uma resposta JSON:

```JSON
{
  "detail": "Item not found"
}
```

/// tip | Dica

Quando você lançar um `HTTPException`, você pode passar qualquer valor convertível em JSON como parâmetro de `detail`, e não apenas `str`.

Você pode passar um `dict` ou um `list`, etc.
Esses tipos de dados são manipulados automaticamente pelo **FastAPI** e convertidos em JSON.

///

## Adicione headers customizados { #add-custom-headers }

Há certas situações em que é bastante útil poder adicionar headers customizados no HTTP error. Exemplo disso seria adicionar headers customizados para tipos de segurança.

Você provavelmente não precisará utilizar esses headers diretamente no seu código.

Mas caso você precise, para um cenário mais complexo, você pode adicionar headers customizados:

{* ../../docs_src/handling_errors/tutorial002.py hl[14] *}

## Instale manipuladores de exceções customizados { #install-custom-exception-handlers }

Você pode adicionar manipuladores de exceção customizados com <a href="https://www.starlette.dev/exceptions/" class="external-link" target="_blank">a mesma seção de utilidade de exceções presentes no Starlette</a>

Digamos que você tenha uma exceção customizada `UnicornException` que você (ou uma biblioteca que você use) precise lançar (`raise`).

Nesse cenário, se você precisa manipular essa exceção de modo global com o FastAPI, você pode adicionar um manipulador de exceção customizada com `@app.exception_handler()`.

{* ../../docs_src/handling_errors/tutorial003.py hl[5:7,13:18,24] *}

Nesse cenário, se você fizer uma requisição para `/unicorns/yolo`, a *operação de caminho* vai lançar (`raise`) o `UnicornException`.

Essa exceção será manipulada, contudo, pelo `unicorn_exception_handler`.

Dessa forma você receberá um erro "limpo", com o HTTP status code `418` e um JSON com o conteúdo:

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

/// note | Detalhes Técnicos

Você também pode usar `from starlette.requests import Request` and `from starlette.responses import JSONResponse`.

**FastAPI** disponibiliza o mesmo `starlette.responses` através do `fastapi.responses` por conveniência ao desenvolvedor. Contudo, a maior parte das respostas disponíveis vem diretamente do Starlette. O mesmo acontece com o `Request`.

///

## Sobrescreva os manipuladores de exceções padrão { #override-the-default-exception-handlers }

**FastAPI** tem alguns manipuladores padrão de exceções.

Esses manipuladores são os responsáveis por retornar o JSON padrão de respostas quando você lança (`raise`) o `HTTPException` e quando a requisição tem dados invalidos.

Você pode sobrescrever esses manipuladores de exceção com os seus próprios manipuladores.

### Sobrescreva exceções de validação da requisição { #override-request-validation-exceptions }

Quando a requisição contém dados inválidos, **FastAPI** internamente lança para o `RequestValidationError`.

E também inclui um manipulador de exceções padrão para ele.

Para sobrescrevê-lo, importe o `RequestValidationError` e use-o com o `@app.exception_handler(RequestValidationError)` para decorar o manipulador de exceções.

O manipulador de exceções receberá um `Request` e a exceção.

{* ../../docs_src/handling_errors/tutorial004.py hl[2,14:16] *}

Se você for ao `/items/foo`, em vez de receber o JSON padrão com o erro:

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

você receberá a versão em texto:

```
1 validation error
path -> item_id
  value is not a valid integer (type=type_error.integer)
```

#### `RequestValidationError` vs `ValidationError` { #requestvalidationerror-vs-validationerror }

/// warning | Atenção

Você pode pular estes detalhes técnicos caso eles não sejam importantes para você neste momento.

///

`RequestValidationError` é uma subclasse do <a href="https://docs.pydantic.dev/latest/concepts/models/#error-handling" class="external-link" target="_blank">`ValidationError`</a> existente no Pydantic.

**FastAPI** faz uso dele para que você veja o erro no seu log, caso você utilize um modelo de Pydantic em `response_model`, e seus dados tenham erro.

Contudo, o cliente ou usuário não terão acesso a ele. Ao contrário, o cliente receberá um "Internal Server Error" com o HTTP status code `500`.

E assim deve ser porque seria um bug no seu código ter o `ValidationError` do Pydantic na sua *response*, ou em qualquer outro lugar do seu código (que não na requisição do cliente).

E enquanto você conserta o bug, os clientes / usuários não deveriam ter acesso às informações internas do erro, porque, desse modo, haveria exposição de uma vulnerabilidade de segurança.

### Sobrescreva o manipulador de erro `HTTPException` { #override-the-httpexception-error-handler }

Do mesmo modo, você pode sobreescrever o `HTTPException`.

Por exemplo, você pode querer retornar uma *response* em *plain text* ao invés de um JSON para os seguintes erros:

{* ../../docs_src/handling_errors/tutorial004.py hl[3:4,9:11,22] *}

/// note | Detalhes Técnicos

Você pode usar `from starlette.responses import PlainTextResponse`.

**FastAPI** disponibiliza o mesmo `starlette.responses` como `fastapi.responses`, como conveniência a você, desenvolvedor. Contudo, a maior parte das respostas disponíveis vem diretamente do Starlette.

///

### Use o body do `RequestValidationError`. { #use-the-requestvalidationerror-body }

O `RequestValidationError` contém o `body` que ele recebeu de dados inválidos.

Você pode utilizá-lo enquanto desenvolve seu app para conectar o *body* e debugá-lo, e assim retorná-lo ao usuário, etc.

{* ../../docs_src/handling_errors/tutorial005.py hl[14] *}

Tente enviar um item inválido como este:

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

Você receberá uma *response* informando-o de que os dados são inválidos, e contendo o *body* recebido:

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

#### O `HTTPException` do FastAPI vs o `HTTPException` do Starlette { #fastapis-httpexception-vs-starlettes-httpexception }

O **FastAPI** tem o seu próprio `HTTPException`.

E a classe de erro `HTTPException` do **FastAPI** herda da classe de erro do `HTTPException` do Starlette.

A única diferença é que o `HTTPException` do **FastAPI** aceita qualquer dado que possa ser convertido em JSON para o campo `detail`, enquanto o `HTTPException` do Starlette aceita apenas strings para esse campo.

Portanto, você pode continuar lançando o `HTTPException` do **FastAPI** normalmente no seu código.

Porém, quando você registrar um manipulador de exceção, você deve registrá-lo através do `HTTPException` do Starlette.

Dessa forma, se qualquer parte do código interno, extensão ou plug-in do Starlette lançar um `HTTPException` do Starlette, o seu manipulador poderá capturar e tratá-lo.

Neste exemplo, para poder ter ambos os `HTTPException` no mesmo código, a exceção do Starlette é renomeada para `StarletteHTTPException`:

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### Reutilize os manipuladores de exceção do **FastAPI** { #reuse-fastapis-exception-handlers }

Se você quer usar a exceção em conjunto com o mesmo manipulador de exceção *default* do **FastAPI**, você pode importar e re-usar esses manipuladores de exceção do `fastapi.exception_handlers`:

{* ../../docs_src/handling_errors/tutorial006.py hl[2:5,15,21] *}

Nesse exemplo você apenas imprime (`print`) o erro com uma mensagem expressiva. Mesmo assim, dá para pegar a ideia. Você pode usar a exceção e então apenas re-usar o manipulador de exceção *default*.
