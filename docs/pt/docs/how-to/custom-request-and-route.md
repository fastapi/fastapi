# Request e classe APIRoute personalizadas { #custom-request-and-apiroute-class }

Em alguns casos, você pode querer sobrescrever a lógica usada pelas classes `Request` e `APIRoute`.

Em particular, isso pode ser uma boa alternativa para uma lógica em um middleware.

Por exemplo, se você quiser ler ou manipular o corpo da requisição antes que ele seja processado pela sua aplicação.

/// danger | Cuidado

Isso é um recurso "avançado".

Se você for um iniciante em **FastAPI** você deve considerar pular essa seção.

///

## Casos de Uso { #use-cases }

Alguns casos de uso incluem:

* Converter requisições não-JSON para JSON (por exemplo, <a href="https://msgpack.org/index.html" class="external-link" target="_blank">`msgpack`</a>).
* Descomprimir corpos de requisição comprimidos com gzip.
* Registrar automaticamente todos os corpos de requisição.

## Manipulando codificações de corpo de requisição personalizadas { #handling-custom-request-body-encodings }

Vamos ver como usar uma subclasse personalizada de `Request` para descomprimir requisições gzip.

E uma subclasse de `APIRoute` para usar essa classe de requisição personalizada.

### Criar uma classe `GzipRequest` personalizada { #create-a-custom-gziprequest-class }

/// tip | Dica

Isso é um exemplo de brincadeira para demonstrar como funciona, se você precisar de suporte para Gzip, você pode usar o [`GzipMiddleware`](../advanced/middleware.md#gzipmiddleware){.internal-link target=_blank} fornecido.

///

Primeiro, criamos uma classe `GzipRequest`, que irá sobrescrever o método `Request.body()` para descomprimir o corpo na presença de um cabeçalho apropriado.

Se não houver `gzip` no cabeçalho, ele não tentará descomprimir o corpo.

Dessa forma, a mesma classe de rota pode lidar com requisições comprimidas ou não comprimidas.

{* ../../docs_src/custom_request_and_route/tutorial001.py hl[8:15] *}

### Criar uma classe `GzipRoute` personalizada { #create-a-custom-gziproute-class }

Em seguida, criamos uma subclasse personalizada de `fastapi.routing.APIRoute` que fará uso do `GzipRequest`.

Dessa vez, ele irá sobrescrever o método `APIRoute.get_route_handler()`.

Esse método retorna uma função. E essa função é o que irá receber uma requisição e retornar uma resposta.

Aqui nós usamos para criar um `GzipRequest` a partir da requisição original.

{* ../../docs_src/custom_request_and_route/tutorial001.py hl[18:26] *}

/// note | Detalhes Técnicos

Um `Request` tem um atributo `request.scope`, que é apenas um `dict` do Python contendo os metadados relacionados à requisição.

Um `Request` também tem um `request.receive`, que é uma função para "receber" o corpo da requisição.

O dicionário `scope` e a função `receive` são ambos parte da especificação ASGI.

E essas duas coisas, `scope` e `receive`, são o que é necessário para criar uma nova instância de `Request`.

Para aprender mais sobre o `Request` confira a <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">documentação do Starlette sobre Requests</a>.

///

A única coisa que a função retornada por `GzipRequest.get_route_handler` faz de diferente é converter o `Request` para um `GzipRequest`.

Fazendo isso, nosso `GzipRequest` irá cuidar de descomprimir os dados (se necessário) antes de passá-los para nossas *operações de rota*.

Depois disso, toda a lógica de processamento é a mesma.

Mas por causa das nossas mudanças em `GzipRequest.body`, o corpo da requisição será automaticamente descomprimido quando for carregado pelo **FastAPI** quando necessário.

## Acessando o corpo da requisição em um manipulador de exceção { #accessing-the-request-body-in-an-exception-handler }

/// tip | Dica

Para resolver esse mesmo problema, é provavelmente muito mais fácil usar o `body` em um manipulador personalizado para `RequestValidationError` ([Tratando Erros](../tutorial/handling-errors.md#use-the-requestvalidationerror-body){.internal-link target=_blank}).

Mas esse exemplo ainda é valido e mostra como interagir com os componentes internos.

///

Também podemos usar essa mesma abordagem para acessar o corpo da requisição em um manipulador de exceção.

Tudo que precisamos fazer é manipular a requisição dentro de um bloco `try`/`except`:

{* ../../docs_src/custom_request_and_route/tutorial002.py hl[13,15] *}

Se uma exceção ocorrer, a instância `Request` ainda estará em escopo, então podemos ler e fazer uso do corpo da requisição ao lidar com o erro:

{* ../../docs_src/custom_request_and_route/tutorial002.py hl[16:18] *}

## Classe `APIRoute` personalizada em um router { #custom-apiroute-class-in-a-router }

Você também pode definir o parâmetro `route_class` de uma `APIRouter`:

{* ../../docs_src/custom_request_and_route/tutorial003.py hl[26] *}

Nesse exemplo, as *operações de rota* sob o `router` irão usar a classe `TimedRoute` personalizada, e terão um cabeçalho extra `X-Response-Time` na resposta com o tempo que levou para gerar a resposta:

{* ../../docs_src/custom_request_and_route/tutorial003.py hl[13:20] *}
