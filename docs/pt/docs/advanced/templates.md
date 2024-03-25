# Templates

Você pode usar qualquer template engine com o **FastAPI**.

Uma escolha comum é o Jinja2, o mesmo usado pelo Flask e outras ferramentas.

Existem utilitários para configurá-lo facilmente que você pode usar diretamente em sua aplicação **FastAPI** (fornecidos pelo Starlette).

## Instalar dependencias

Para instalar o `jinja2`, siga o código abaixo:

<div class="termy">

```console
$ pip install jinja2
```

</div>

## Usando `Jinja2Templates`

* Importe `Jinja2Templates`.
* Crie um `templates` que você pode reutilizar posteriormente.
* Declare um parâmetro `Request` no *path operation* que retornará um template.
* Use os `templates` que você criou para renderizar e retornar uma `TemplateResponse`, passando o nome do template, o o request object, e um "context" dict com pares key-value a serem usados dentro do template Jinja2.

```Python hl_lines="4  11  15-18"
{!../../../docs_src/templates/tutorial001.py!}
```

!!! Nota
    Antes do FastAPI 0.108.0, Starlette 0.29.0, `name` era o primeiro parâmetro.

    Além disso, em versões anteriores, o objeto `request` era passado como parte dos pares key-value no contexto para Jinja2.


!!! Dica
    Ao declarar `response_class=HTMLResponse`, a interface dos documentos será capaz de saber que a resposta será HTML.


!!! Nota "Detalhes Técnicos"
    Você também poderia usar `from starlette.templating import Jinja2Templates`.

    **FastAPI** fornece o mesmo `starlette.templating` como `fastapi.templating` apenas como uma conveniência para você, o desenvolvedor. Mas a maioria das respostas disponíveis vem diretamente do Starlette. O mesmo acontece com `Request` e `StaticFiles`.

## Escrevento Templates

Então você pode escrever um template em `templates/item.html`, por exemplo:

```jinja hl_lines="7"
{!../../../docs_src/templates/templates/item.html!}
```

### Template Context Values

Nesse HTML que contem:

{% raw %}

```jinja
Item ID: {{ id }}
```

{% endraw %}

...irá mostrar o `id` obtido do "context" `dict` que você passou:

```Python
{"id": id}
```

Por exemplo, com um ID de `42`, deveria mostrar:

```html
Item ID: 42
```

### Template `url_for` Arguments

Você pode também usar `url_for()` dentro do template, ele recebe como argumentos os mesmos argumentos que seriam usados pela sua *path operation function*.

Então, a seção com:

{% raw %}

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

{% endraw %}

...irá gerar um link para a mesma URL que será tratada pela *path operation function* `read_item(id=id)`.

Por exemplo, com um ID de `42`, isso renderizará:

```html
<a href="/items/42">
```

## Templates e Arquivos Estáticos

Você também pode usar `url_for()` dentro do template, e usar, por examplo, com o `StaticFiles` que você montou com o `name="static"`.

```jinja hl_lines="4"
{!../../../docs_src/templates/templates/item.html!}
```

Neste exemplo, ele iria vincular a um arquivo CSS em `static/styles.css` com:

```CSS hl_lines="4"
{!../../../docs_src/templates/static/styles.css!}
```

E como você está usando `StaticFiles`, esse arquivo CSS seria servido automaticamente pela sua aplicação FastAPI na URL `/static/styles.css`.

## Mais detalhes

Para obter mais detalhes, incluindo como testar templates, consulte a <a href="https://www.starlette.io/templates/" class="external-link" target="_blank">documentação da Starlette sobre templates</a>.
