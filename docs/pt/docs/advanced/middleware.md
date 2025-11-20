# Middleware Avançado { #advanced-middleware }

No tutorial principal você leu como adicionar [Middleware Personalizado](../tutorial/middleware.md){.internal-link target=_blank} à sua aplicação.

E então você também leu como lidar com [CORS com o `CORSMiddleware`](../tutorial/cors.md){.internal-link target=_blank}.

Nesta seção, veremos como usar outros middlewares.

## Adicionando middlewares ASGI { #adding-asgi-middlewares }

Como o **FastAPI** é baseado no Starlette e implementa a especificação <abbr title="Asynchronous Server Gateway Interface – Interface de Gateway de Servidor Assíncrona">ASGI</abbr>, você pode usar qualquer middleware ASGI.

O middleware não precisa ser feito para o FastAPI ou Starlette para funcionar, desde que siga a especificação ASGI.

No geral, os middlewares ASGI são classes que esperam receber um aplicativo ASGI como o primeiro argumento.

Então, na documentação de middlewares ASGI de terceiros, eles provavelmente dirão para você fazer algo como:

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

Mas, o FastAPI (na verdade, o Starlette) fornece uma maneira mais simples de fazer isso que garante que os middlewares internos lidem com erros do servidor e que os manipuladores de exceções personalizados funcionem corretamente.

Para isso, você usa `app.add_middleware()` (como no exemplo para CORS).

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()` recebe uma classe de middleware como o primeiro argumento e quaisquer argumentos adicionais a serem passados para o middleware.

## Middlewares Integrados { #integrated-middlewares }

**FastAPI** inclui vários middlewares para casos de uso comuns, veremos a seguir como usá-los.

/// note | Detalhes Técnicos

Para os próximos exemplos, você também poderia usar `from starlette.middleware.something import SomethingMiddleware`.

**FastAPI** fornece vários middlewares em `fastapi.middleware` apenas como uma conveniência para você, o desenvolvedor. Mas a maioria dos middlewares disponíveis vem diretamente do Starlette.

///

## `HTTPSRedirectMiddleware` { #httpsredirectmiddleware }

Garante que todas as requisições devem ser `https` ou `wss`.

Qualquer requisição para `http` ou `ws` será redirecionada para o esquema seguro.

{* ../../docs_src/advanced_middleware/tutorial001.py hl[2,6] *}

## `TrustedHostMiddleware` { #trustedhostmiddleware }

Garante que todas as requisições recebidas tenham um cabeçalho `Host` corretamente configurado, a fim de proteger contra ataques de cabeçalho de host HTTP.

{* ../../docs_src/advanced_middleware/tutorial002.py hl[2,6:8] *}

Os seguintes argumentos são suportados:

* `allowed_hosts` - Uma lista de nomes de domínio que são permitidos como nomes de host. Domínios com coringa, como `*.example.com`, são suportados para corresponder a subdomínios. Para permitir qualquer nome de host, use `allowed_hosts=["*"]` ou omita o middleware.
* `www_redirect` - Se definido como True, as requisições para versões sem www dos hosts permitidos serão redirecionadas para suas versões com www. O padrão é `True`.

Se uma requisição recebida não for validada corretamente, uma resposta `400` será enviada.

## `GZipMiddleware` { #gzipmiddleware }

Gerencia respostas GZip para qualquer requisição que inclua `"gzip"` no cabeçalho `Accept-Encoding`.

O middleware lidará com respostas padrão e de streaming.

{* ../../docs_src/advanced_middleware/tutorial003.py hl[2,6] *}

Os seguintes argumentos são suportados:

* `minimum_size` - Não comprima respostas menores que este tamanho mínimo em bytes. O padrão é `500`.
* `compresslevel` - Usado durante a compressão GZip. É um inteiro variando de 1 a 9. O padrão é `9`. Um valor menor resulta em uma compressão mais rápida, mas em arquivos maiores, enquanto um valor maior resulta em uma compressão mais lenta, mas em arquivos menores.

## Outros middlewares { #other-middlewares }

Há muitos outros middlewares ASGI.

Por exemplo:

* <a href="https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py" class="external-link" target="_blank">Uvicorn's `ProxyHeadersMiddleware`</a>
* <a href="https://github.com/florimondmanca/msgpack-asgi" class="external-link" target="_blank">MessagePack</a>

Para checar outros middlewares disponíveis, confira <a href="https://www.starlette.dev/middleware/" class="external-link" target="_blank">Documentação de Middlewares do Starlette</a> e a  <a href="https://github.com/florimondmanca/awesome-asgi" class="external-link" target="_blank">Lista Incrível do ASGI</a>.
