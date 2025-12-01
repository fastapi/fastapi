# Aplicações Maiores - Múltiplos Arquivos { #bigger-applications-multiple-files }

Se você está construindo uma aplicação ou uma API web, é raro que você possa colocar tudo em um único arquivo.

**FastAPI** oferece uma ferramenta conveniente para estruturar sua aplicação, mantendo toda a flexibilidade.

/// info | Informação

Se você vem do Flask, isso seria o equivalente aos Blueprints do Flask.

///

## Um exemplo de estrutura de arquivos { #an-example-file-structure }

Digamos que você tenha uma estrutura de arquivos como esta:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

/// tip | Dica

Existem vários arquivos `__init__.py` presentes em cada diretório ou subdiretório.

Isso permite a importação de código de um arquivo para outro.

Por exemplo, no arquivo `app/main.py`, você poderia ter uma linha como:

```
from app.routers import items
```

///

* O diretório `app` contém todo o código da aplicação. Ele possui um arquivo `app/__init__.py` vazio, o que o torna um "pacote Python" (uma coleção de "módulos Python"): `app`.
* Dentro dele, o arquivo `app/main.py` está localizado em um pacote Python (diretório com  `__init__.py`). Portanto, ele é um "módulo" desse pacote: `app.main`.
* Existem também um arquivo `app/dependencies.py`, assim como o `app/main.py`, ele é um "módulo": `app.dependencies`.
* Há um subdiretório `app/routers/` com outro arquivo `__init__.py`, então ele é um "subpacote Python": `app.routers`.
* O arquivo `app/routers/items.py` está dentro de um pacote, `app/routers/`, portanto, é um "submódulo": `app.routers.items`.
* O mesmo com `app/routers/users.py`,  ele é outro submódulo: `app.routers.users`.
* Há também um subdiretório `app/internal/` com outro arquivo `__init__.py`, então ele é outro "subpacote Python":`app.internal`.
* E o arquivo `app/internal/admin.py` é outro submódulo: `app.internal.admin`.

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

A mesma estrutura de arquivos com comentários:

```
.
├── app                  # "app" é um pacote Python
│   ├── __init__.py      # este arquivo torna "app" um "pacote Python"
│   ├── main.py          # "main" módulo, e.g. import app.main
│   ├── dependencies.py  # "dependencies" módulo, e.g. import app.dependencies
│   └── routers          # "routers" é um  "subpacote Python"
│   │   ├── __init__.py  # torna "routers" um "subpacote Python"
│   │   ├── items.py     # "items" submódulo, e.g. import app.routers.items
│   │   └── users.py     # "users" submódulo, e.g. import app.routers.users
│   └── internal         # "internal" é um  "subpacote Python"
│       ├── __init__.py  # torna "internal" um  "subpacote Python"
│       └── admin.py     # "admin" submódulo, e.g. import app.internal.admin
```

## `APIRouter` { #apirouter }

Vamos supor que o arquivo dedicado a lidar apenas com usuários seja o submódulo em `/app/routers/users.py`.

Você quer manter as *operações de rota* relacionadas aos seus usuários separadas do restante do código, para mantê-lo organizado.

Mas ele ainda faz parte da mesma aplicação/web API **FastAPI** (faz parte do mesmo "pacote Python").

Você pode criar as *operações de rotas* para esse módulo usando o `APIRouter`.

### Importe `APIRouter` { #import-apirouter }

você o importa e cria uma "instância" da mesma maneira que faria com a classe `FastAPI`:

```Python hl_lines="1  3" title="app/routers/users.py"
{!../../docs_src/bigger_applications/app/routers/users.py!}
```

### *Operações de Rota* com `APIRouter` { #path-operations-with-apirouter }

E então você o utiliza para declarar suas *operações de rota*.

Utilize-o da mesma maneira que utilizaria a classe  `FastAPI`:

```Python hl_lines="6  11  16" title="app/routers/users.py"
{!../../docs_src/bigger_applications/app/routers/users.py!}
```

Você pode pensar em `APIRouter` como uma classe "mini `FastAPI`".

Todas as mesmas opções são suportadas.

Todos os mesmos `parameters`, `responses`, `dependencies`, `tags`, etc.

/// tip | Dica

Neste exemplo, a variável é chamada de `router`, mas você pode nomeá-la como quiser.

///

Vamos incluir este `APIRouter` na aplicação principal `FastAPI`, mas primeiro, vamos verificar as dependências e outro `APIRouter`.

## Dependências { #dependencies }

Vemos que precisaremos de algumas dependências usadas em vários lugares da aplicação.

Então, as colocamos em seu próprio módulo de `dependencies` (`app/dependencies.py`).

Agora usaremos uma dependência simples para ler um cabeçalho `X-Token` personalizado:

//// tab | Python 3.9+

```Python hl_lines="3  6-8" title="app/dependencies.py"
{!> ../../docs_src/bigger_applications/app_an_py39/dependencies.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  5-7" title="app/dependencies.py"
{!> ../../docs_src/bigger_applications/app_an/dependencies.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Prefira usar a versão `Annotated` se possível.

///

```Python hl_lines="1  4-6" title="app/dependencies.py"
{!> ../../docs_src/bigger_applications/app/dependencies.py!}
```

////

/// tip | Dica

Estamos usando um cabeçalho inventado para simplificar este exemplo.

Mas em casos reais, você obterá melhores resultados usando os [Utilitários de Segurança](security/index.md){.internal-link target=_blank} integrados.

///

## Outro módulo com `APIRouter` { #another-module-with-apirouter }

Digamos que você também tenha os endpoints dedicados a manipular "itens" do seu aplicativo no módulo em `app/routers/items.py`.

Você tem *operações de rota* para:

* `/items/`
* `/items/{item_id}`

É tudo a mesma estrutura de `app/routers/users.py`.

Mas queremos ser mais inteligentes e simplificar um pouco o código.

Sabemos que todas as *operações de rota* neste módulo têm o mesmo:

* Path `prefix`: `/items`.
* `tags`: (apenas uma tag: `items`).
* Extra `responses`.
* `dependencies`: todas elas precisam da dependência `X-Token` que criamos.

Então, em vez de adicionar tudo isso a cada *operação de rota*, podemos adicioná-lo ao `APIRouter`.

```Python hl_lines="5-10  16  21" title="app/routers/items.py"
{!../../docs_src/bigger_applications/app/routers/items.py!}
```

Como o caminho de cada *operação de rota* deve começar com `/`, como em:

```Python hl_lines="1"
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
```

...o prefixo não deve incluir um `/` final.

Então, o prefixo neste caso é `/items`.

Também podemos adicionar uma lista de `tags` e `responses` extras que serão aplicadas a todas as *operações de rota* incluídas neste roteador.

E podemos adicionar uma lista de `dependencies` que serão adicionadas a todas as *operações de rota* no roteador e serão executadas/resolvidas para cada solicitação feita a elas.

/// tip | Dica

Observe que, assim como [dependências em *decoradores de operação de rota*](dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank}, nenhum valor será passado para sua *função de operação de rota*.

///

O resultado final é que os caminhos dos itens agora são:

* `/items/`
* `/items/{item_id}`

...como pretendíamos.

* Elas serão marcadas com uma lista de tags que contêm uma única string `"items"`.
    * Essas "tags" são especialmente úteis para os sistemas de documentação interativa automática (usando OpenAPI).
* Todas elas incluirão as `responses` predefinidas.
* Todas essas *operações de rota* terão a lista de `dependencies` avaliada/executada antes delas.
    * Se você também declarar dependências em uma *operação de rota* específica, **elas também serão executadas**.
    * As dependências do roteador são executadas primeiro, depois as [`dependencies` no decorador](dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank} e, em seguida, as dependências de parâmetros normais.
    * Você também pode adicionar [dependências de `Segurança` com `scopes`](../advanced/security/oauth2-scopes.md){.internal-link target=_blank}.

/// tip | Dica

Ter `dependencies` no `APIRouter` pode ser usado, por exemplo, para exigir autenticação para um grupo inteiro de *operações de rota*. Mesmo que as dependências não sejam adicionadas individualmente a cada uma delas.

///

/// check | Verifique

Os parâmetros `prefix`, `tags`, `responses` e `dependencies` são (como em muitos outros casos) apenas um recurso do **FastAPI** para ajudar a evitar duplicação de código.

///

### Importe as dependências { #import-the-dependencies }

Este código reside no módulo `app.routers.items`, o arquivo `app/routers/items.py`.

E precisamos obter a função de dependência do módulo `app.dependencies`, o arquivo `app/dependencies.py`.

Então usamos uma importação relativa com `..` para as dependências:

```Python hl_lines="3" title="app/routers/items.py"
{!../../docs_src/bigger_applications/app/routers/items.py!}
```

#### Como funcionam as importações relativas { #how-relative-imports-work }

/// tip | Dica

Se você sabe perfeitamente como funcionam as importações, continue para a próxima seção abaixo.

///

Um único ponto `.`, como em:

```Python
from .dependencies import get_token_header
```

significaria:

* Começando no mesmo pacote em que este módulo (o arquivo `app/routers/items.py`) vive (o diretório `app/routers/`)...
* encontre o módulo `dependencies` (um arquivo imaginário em `app/routers/dependencies.py`)...
* e dele, importe a função `get_token_header`.

Mas esse arquivo não existe, nossas dependências estão em um arquivo em `app/dependencies.py`.

Lembre-se de como nossa estrutura app/file se parece:

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

---

Os dois pontos `..`, como em:

```Python
from ..dependencies import get_token_header
```

significa:

* Começando no mesmo pacote em que este módulo (o arquivo `app/routers/items.py`) reside (o diretório `app/routers/`)...
* vá para o pacote pai (o diretório `app/`)...
* e lá, encontre o módulo `dependencies` (o arquivo em `app/dependencies.py`)...
* e dele, importe a função `get_token_header`.

Isso funciona corretamente! 🎉

---

Da mesma forma, se tivéssemos usado três pontos `...`, como em:

```Python
from ...dependencies import get_token_header
```

isso significaria:

* Começando no mesmo pacote em que este módulo (o arquivo `app/routers/items.py`) vive (o diretório `app/routers/`)...
* vá para o pacote pai (o diretório `app/`)...
* então vá para o pai daquele pacote (não há pacote pai, `app` é o nível superior 😱)...
* e lá, encontre o módulo `dependencies` (o arquivo em `app/dependencies.py`)...
* e dele, importe a função `get_token_header`.

Isso se referiria a algum pacote acima de `app/`, com seu próprio arquivo `__init__.py`, etc. Mas não temos isso. Então, isso geraria um erro em nosso exemplo. 🚨

Mas agora você sabe como funciona, então você pode usar importações relativas em seus próprios aplicativos, não importa o quão complexos eles sejam. 🤓

### Adicione algumas `tags`, `responses` e `dependencies` personalizadas { #add-some-custom-tags-responses-and-dependencies }

Não estamos adicionando o prefixo `/items` nem `tags=["items"]` a cada *operação de rota* porque os adicionamos ao `APIRouter`.

Mas ainda podemos adicionar _mais_ `tags` que serão aplicadas a uma *operação de rota* específica, e também algumas `responses` extras específicas para essa *operação de rota*:

```Python hl_lines="30-31" title="app/routers/items.py"
{!../../docs_src/bigger_applications/app/routers/items.py!}
```

/// tip | Dica

Esta última operação de caminho terá a combinação de tags: `["items", "custom"]`.

E também terá ambas as respostas na documentação, uma para `404` e uma para `403`.

///

## O principal `FastAPI` { #the-main-fastapi }

Agora, vamos ver o módulo em `app/main.py`.

Aqui é onde você importa e usa a classe `FastAPI`.

Este será o arquivo principal em seu aplicativo que une tudo.

E como a maior parte de sua lógica agora viverá em seu próprio módulo específico, o arquivo principal será bem simples.

### Importe o `FastAPI` { #import-fastapi }

Você importa e cria uma classe `FastAPI` normalmente.

E podemos até declarar [dependências globais](dependencies/global-dependencies.md){.internal-link target=_blank} que serão combinadas com as dependências para cada `APIRouter`:

```Python hl_lines="1  3  7" title="app/main.py"
{!../../docs_src/bigger_applications/app/main.py!}
```

### Importe o `APIRouter` { #import-the-apirouter }

Agora importamos os outros submódulos que possuem `APIRouter`s:

```Python hl_lines="4-5" title="app/main.py"
{!../../docs_src/bigger_applications/app/main.py!}
```

Como os arquivos `app/routers/users.py` e `app/routers/items.py` são submódulos que fazem parte do mesmo pacote Python `app`, podemos usar um único ponto `.` para importá-los usando "importações relativas".

### Como funciona a importação { #how-the-importing-works }

A seção:

```Python
from .routers import items, users
```

significa:

* Começando no mesmo pacote em que este módulo (o arquivo `app/main.py`) reside (o diretório `app/`)...
* procure o subpacote `routers` (o diretório em `app/routers/`)...
* e dele, importe o submódulo `items` (o arquivo em `app/routers/items.py`) e `users` (o arquivo em `app/routers/users.py`)...

O módulo `items` terá uma variável `router` (`items.router`). Esta é a mesma que criamos no arquivo `app/routers/items.py`, é um objeto `APIRouter`.

E então fazemos o mesmo para o módulo `users`.

Também poderíamos importá-los como:

```Python
from app.routers import items, users
```

/// info | Informação

A primeira versão é uma "importação relativa":

```Python
from .routers import items, users
```

A segunda versão é uma "importação absoluta":

```Python
from app.routers import items, users
```

Para saber mais sobre pacotes e módulos Python, leia <a href="https://docs.python.org/3/tutorial/modules.html" class="external-link" target="_blank">a documentação oficial do Python sobre módulos</a>.

///

### Evite colisões de nomes { #avoid-name-collisions }

Estamos importando o submódulo `items` diretamente, em vez de importar apenas sua variável `router`.

Isso ocorre porque também temos outra variável chamada `router` no submódulo `users`.

Se tivéssemos importado um após o outro, como:

```Python
from .routers.items import router
from .routers.users import router
```

o `router` de `users` sobrescreveria o de `items` e não poderíamos usá-los ao mesmo tempo.

Então, para poder usar ambos no mesmo arquivo, importamos os submódulos diretamente:

```Python hl_lines="5" title="app/main.py"
{!../../docs_src/bigger_applications/app/main.py!}
```

### Inclua os `APIRouter`s para `usuários` e `itens` { #include-the-apirouters-for-users-and-items }

Agora, vamos incluir os `router`s dos submódulos `users` e `items`:

```Python hl_lines="10-11" title="app/main.py"
{!../../docs_src/bigger_applications/app/main.py!}
```

/// info | Informação

`users.router` contém o `APIRouter` dentro do arquivo `app/routers/users.py`.

E `items.router` contém o `APIRouter` dentro do arquivo `app/routers/items.py`.

///

Com `app.include_router()` podemos adicionar cada `APIRouter` ao aplicativo principal `FastAPI`.

Ele incluirá todas as rotas daquele roteador como parte dele.

/// note | Detalhes Técnicos

Na verdade, ele criará internamente uma *operação de rota* para cada *operação de rota* que foi declarada no `APIRouter`.

Então, nos bastidores, ele realmente funcionará como se tudo fosse o mesmo aplicativo único.

///

/// check | Verifique

Você não precisa se preocupar com desempenho ao incluir roteadores.

Isso levará microssegundos e só acontecerá na inicialização.

Então não afetará o desempenho. ⚡

///

### Inclua um `APIRouter` com um `prefix`, `tags`, `responses` e `dependencies` personalizados { #include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies }

Agora, vamos imaginar que sua organização lhe deu o arquivo `app/internal/admin.py`.

Ele contém um `APIRouter` com algumas *operações de rota* de administração que sua organização compartilha entre vários projetos.

Para este exemplo, será super simples. Mas digamos que, como ele é compartilhado com outros projetos na organização, não podemos modificá-lo e adicionar um `prefix`, `dependencies`, `tags`, etc. diretamente ao `APIRouter`:

```Python hl_lines="3" title="app/internal/admin.py"
{!../../docs_src/bigger_applications/app/internal/admin.py!}
```

Mas ainda queremos definir um `prefix` personalizado ao incluir o `APIRouter` para que todas as suas *operações de rota* comecem com `/admin`, queremos protegê-lo com as `dependencies` que já temos para este projeto e queremos incluir `tags` e `responses`.

Podemos declarar tudo isso sem precisar modificar o `APIRouter` original passando esses parâmetros para `app.include_router()`:

```Python hl_lines="14-17" title="app/main.py"
{!../../docs_src/bigger_applications/app/main.py!}
```

Dessa forma, o `APIRouter` original permanecerá inalterado, para que possamos compartilhar o mesmo arquivo `app/internal/admin.py` com outros projetos na organização.

O resultado é que em nosso aplicativo, cada uma das *operações de rota* do módulo `admin` terá:

* O prefixo `/admin`.
* A tag `admin`.
* A dependência `get_token_header`.
* A resposta `418`. 🍵

Mas isso afetará apenas o `APIRouter` em nosso aplicativo, e não em nenhum outro código que o utilize.

Assim, por exemplo, outros projetos poderiam usar o mesmo `APIRouter` com um método de autenticação diferente.

### Inclua uma *operação de rota* { #include-a-path-operation }

Também podemos adicionar *operações de rota* diretamente ao aplicativo `FastAPI`.

Aqui fazemos isso... só para mostrar que podemos 🤷:

```Python hl_lines="21-23" title="app/main.py"
{!../../docs_src/bigger_applications/app/main.py!}
```

e funcionará corretamente, junto com todas as outras *operações de rota* adicionadas com `app.include_router()`.

/// note | Detalhes Técnicos Avançados

**Observação**: este é um detalhe muito técnico que você provavelmente pode **simplesmente pular**.

---

Os `APIRouter`s não são "montados", eles não são isolados do resto do aplicativo.

Isso ocorre porque queremos incluir suas *operações de rota* no esquema OpenAPI e nas interfaces de usuário.

Como não podemos simplesmente isolá-los e "montá-los" independentemente do resto, as *operações de rota* são "clonadas" (recriadas), não incluídas diretamente.

///

## Verifique a documentação automática da API { #check-the-automatic-api-docs }

Agora, execute sua aplicação:

<div class="termy">

```console
$ fastapi dev app/main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

E abra os documentos em <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Você verá a documentação automática da API, incluindo os caminhos de todos os submódulos, usando os caminhos (e prefixos) corretos e as tags corretas:

<img src="/img/tutorial/bigger-applications/image01.png">

## Inclua o mesmo roteador várias vezes com `prefix` diferentes { #include-the-same-router-multiple-times-with-different-prefix }

Você também pode usar `.include_router()` várias vezes com o *mesmo* roteador usando prefixos diferentes.

Isso pode ser útil, por exemplo, para expor a mesma API sob prefixos diferentes, por exemplo, `/api/v1` e `/api/latest`.

Esse é um uso avançado que você pode não precisar, mas está lá caso precise.

## Inclua um `APIRouter` em outro { #include-an-apirouter-in-another }

Da mesma forma que você pode incluir um `APIRouter` em um aplicativo `FastAPI`, você pode incluir um `APIRouter` em outro `APIRouter` usando:

```Python
router.include_router(other_router)
```

Certifique-se de fazer isso antes de incluir `router` no aplicativo `FastAPI`, para que as *operações de rota* de `other_router` também sejam incluídas.
