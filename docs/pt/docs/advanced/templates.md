# Templates { #templates }

Você pode usar qualquer template engine com o **FastAPI**.

Uma escolha comum é o Jinja2, o mesmo usado pelo Flask e outras ferramentas.

Existem utilitários para configurá-lo facilmente que você pode usar diretamente em sua aplicação **FastAPI** (fornecidos pelo Starlette).

## Instalar dependências { #install-dependencies }

Adicione `jinja2` ao seu projeto:

<div class="termy">

```console
$ uv add jinja2

---> 100%
```

</div>

## Usando `Jinja2Templates` { #using-jinja2templates }

* Importe `Jinja2Templates`.
* Crie um objeto `templates` que você possa reutilizar posteriormente.
* Declare um parâmetro `Request` na *operação de rota* que retornará um template.
* Use o `templates` que você criou para renderizar e retornar uma `TemplateResponse`, passe o nome do template, o objeto request e um dicionário "context" com pares chave-valor a serem usados dentro do template do Jinja2.

{* ../../docs_src/templates/tutorial001_py310.py hl[4,11,15:18] *}

/// note | Nota

Antes do FastAPI 0.108.0, Starlette 0.29.0, o `name` era o primeiro parâmetro.

Além disso, antes disso, em versões anteriores, o objeto `request` era passado como parte dos pares chave-valor no context para o Jinja2.

///

/// tip | Dica

Ao declarar `response_class=HTMLResponse`, a interface da documentação poderá saber que a resposta será HTML.

///

/// note | Detalhes Técnicos

Você também poderia usar `from starlette.templating import Jinja2Templates`.

**FastAPI** fornece o mesmo `starlette.templating` como `fastapi.templating` apenas como uma conveniência para você, o desenvolvedor. Mas a maioria das respostas disponíveis vêm diretamente do Starlette. O mesmo acontece com `Request` e `StaticFiles`.

///

## Escrevendo templates { #writing-templates }

Então você pode escrever um template em `templates/item.html` com, por exemplo:

```jinja hl_lines="7"
{!../../docs_src/templates/templates/item.html!}
```

### Valores de contexto do template { #template-context-values }

No código HTML que contém:

{% raw %}

```jinja
Item ID: {{ id }}
```

{% endraw %}

...aparecerá o `id` obtido do "context" `dict` que você passou:

```Python
{"id": id}
```

Por exemplo, com um ID de `42`, isso renderizará:

```html
Item ID: 42
```

### Argumentos do `url_for` no template { #template-url-for-arguments }

Você também pode usar `url_for()` dentro do template, ele recebe como argumentos os mesmos argumentos que seriam usados pela sua *função de operação de rota*.

Logo, a seção com:

{% raw %}

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

{% endraw %}

...irá gerar um link para a mesma URL que será tratada pela *função de operação de rota* `read_item(id=id)`.

Por exemplo, com um ID de `42`, isso renderizará:

```html
<a href="/items/42">
```

## Templates e arquivos estáticos { #templates-and-static-files }

Você também pode usar `url_for()` dentro do template e usá-lo, por exemplo, com o `StaticFiles` que você montou com o `name="static"`.

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

Neste exemplo, ele seria vinculado a um arquivo CSS em `static/styles.css` com:

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

E como você está usando `StaticFiles`, este arquivo CSS será automaticamente servido pela sua aplicação **FastAPI** na URL `/static/styles.css`.

## Mais detalhes { #more-details }

Para obter mais detalhes, incluindo como testar templates, consulte a [documentação da Starlette sobre templates](https://starlette.dev/templates/).
