# CORS (Cross-Origin Resource Sharing)

<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">CORS ou "Cross-Origin Resource Sharing"</a> refere-se às situações em que um frontend rodando em um navegador possui um código JavaScript que se comunica com um backend, e o backend está em uma "origem" diferente do frontend.

## Origem

Uma origem é a combinação de protocolo (`http`, `https`), domínio (`myapp.com`, `localhost`, `localhost.tiangolo.com`), e porta (`80`, `443`, `8080`).

Então, todos estes são origens diferentes:

* `http://localhost`
* `https://localhost`
* `http://localhost:8080`

Mesmo se todos estiverem em `localhost`, eles usam diferentes protocolos e portas, portanto, são "origens" diferentes.

## Passos

Então, digamos que você tenha um frontend rodando no seu navegador em `http://localhost:8080`, e seu JavaScript esteja tentando se comunicar com um backend rodando em http://localhost (como não especificamos uma porta, o navegador assumirá a porta padrão `80`).

Portanto, o navegador irá enviar uma requisição HTTP `OPTIONS` ao backend, e se o backend enviar os cabeçalhos apropriados autorizando a comunicação a partir de uma origem diferente (`http://localhost:8080`) então o navegador deixará o JavaScript no frontend enviar sua requisição para o backend.

Para conseguir isso, o backend deve ter uma lista de "origens permitidas".

Neste caso, ele terá que incluir `http://localhost:8080` para o frontend funcionar corretamente.

## Curingas

É possível declarar uma lista com `"*"` (um "curinga") para dizer que tudo está permitido.

Mas isso só permitirá certos tipos de comunicação, excluindo tudo que envolva credenciais: cookies, cabeçalhos de autorização como aqueles usados ​​com Bearer Tokens, etc.

Então, para que tudo funcione corretamente, é melhor especificar explicitamente as origens permitidas.

## Usar `CORSMiddleware`

Você pode configurá-lo em sua aplicação **FastAPI** usando o `CORSMiddleware`.

* Importe `CORSMiddleware`.
* Crie uma lista de origens permitidas (como strings).
* Adicione-a como um "middleware" à sua aplicação **FastAPI**.

Você também pode especificar se o seu backend permite:

* Credenciais (Cabeçalhos de autorização, Cookies, etc).
* Métodos HTTP específicos (`POST`, `PUT`) ou todos eles com o curinga `"*"`.
* Cabeçalhos HTTP específicos ou todos eles com o curinga `"*"`.

{* ../../docs_src/cors/tutorial001.py hl[2,6:11,13:19] *}

Os parâmetros padrão usados ​​pela implementação `CORSMiddleware` são restritivos por padrão, então você precisará habilitar explicitamente as origens, métodos ou cabeçalhos específicos para que os navegadores tenham permissão para usá-los em um contexto de domínios diferentes.

Os seguintes argumentos são suportados:

* `allow_origins` - Uma lista de origens que devem ter permissão para fazer requisições de origem cruzada. Por exemplo, `['https://example.org', 'https://www.example.org']`. Você pode usar `['*']` para permitir qualquer origem.
* `allow_origin_regex` - Uma string regex para corresponder às origens que devem ter permissão para fazer requisições de origem cruzada. Por exemplo, `'https://.*\.example\.org'`.
* `allow_methods` - Uma lista de métodos HTTP que devem ser permitidos para requisições de origem cruzada. O padrão é `['GET']`. Você pode usar `['*']` para permitir todos os métodos padrão.
* `allow_headers` - Uma lista de cabeçalhos de solicitação HTTP que devem ter suporte para requisições de origem cruzada. O padrão é `[]`. Você pode usar `['*']` para permitir todos os cabeçalhos. Os cabeçalhos `Accept`, `Accept-Language`, `Content-Language` e `Content-Type` são sempre permitidos para <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests" class="external-link" rel="noopener" target="_blank">requisições CORS simples</a>.
* `allow_credentials` - Indica que os cookies devem ser suportados para requisições de origem cruzada. O padrão é `False`. Além disso, `allow_origins` não pode ser definido como `['*']` para que as credenciais sejam permitidas, as origens devem ser especificadas.
* `expose_headers` - Indica quaisquer cabeçalhos de resposta que devem ser disponibilizados ao navegador. O padrão é `[]`.
* `max_age` - Define um tempo máximo em segundos para os navegadores armazenarem em cache as respostas CORS. O padrão é `600`.

O middleware responde a dois tipos específicos de solicitação HTTP...

### Requisições CORS pré-voo (preflight)

Estas são quaisquer solicitações `OPTIONS` com cabeçalhos `Origin` e `Access-Control-Request-Method`.

Nesse caso, o middleware interceptará a solicitação recebida e responderá com cabeçalhos CORS apropriados e uma resposta `200` ou `400` para fins informativos.

### Requisições Simples

Qualquer solicitação com um cabeçalho `Origin`. Neste caso, o middleware passará a solicitação normalmente, mas incluirá cabeçalhos CORS apropriados na resposta.

## Mais informações

Para mais informações <abbr title="Cross-Origin Resource Sharing">CORS</abbr>, acesse <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">Mozilla CORS documentation</a>.

/// note | Detalhes técnicos

Você também pode usar `from starlette.middleware.cors import CORSMiddleware`.

**FastAPI** fornece vários middlewares em `fastapi.middleware` apenas como uma conveniência para você, o desenvolvedor. Mas a maioria dos middlewares disponíveis vêm diretamente da Starlette.

///
