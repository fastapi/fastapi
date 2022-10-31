# Templates

Você pode utilizar qualquer *template engine* que desejar com **FastAPI**, como o Jinja2, o mesmo utilizado pelo Flask e outras ferramentas.

Existem recursos para configurar ele facilmente, que você pode usar diretamente na sua aplicação **FastAPI** (fornecido por Starlette).

## Instalar dependências

Instalar `jinja2`:

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## Usando `Jinja2Templates`

* Importe `Jinja2Templates`.
* Crie um objeto `templates`, que você pode reutilzar depois.
* Declare um parâmetro `Request` na *operação de caminho* que irá retornar um template.
* Use o `templates` que você criou para dar render e retornar um `TemplateResponse`, passando o `request` como um par de valores chave no "contexto" do Jinja2.

```Python hl_lines="4  11  15-16"
{!../../../docs_src/templates/tutorial001.py!}
```

!!! note
    Note que você tem que passar o `request` como parte do par de valores chave no contexto para o Jinja2. Então, você também tem que declarar ele na sua *operação de caminho*.

!!! tip "Dica"
    Ao declarar `response_class=HTMLResponse` o docs UI vai ser capaz de saber que a resposta vai ser em HTML.

!!! note "Detalhes Técnicos"
    Você também pode usar `from starlette.templating import Jinja2Templates`.

    O **FastAPI** prove o mesmo `starlette.templating` como `fastapi.templating`, apenas para a sua conveniência, o(a) desenvolvedor(a). Porém, a maioria das respostas disponíveis vem diretamente do Starlette. O mesmo acontece com o `Request` e o `StaticFiles`.

## Escrevendo templates

Então você pode escrever um template em `templates/item.html` com:

```jinja hl_lines="7"
{!../../../docs_src/templates/templates/item.html!}
```

Isso vai mostrar o `id` do `dict` de "contexto" que você passou:

```Python
{"request": request, "id": id}
```

## Templates e arquivos estáticos

E você também pode usar `url_for()` dentro de um template, e usá-lo, por exemplo, com o `StaticFiles` que você montou.

```jinja hl_lines="4"
{!../../../docs_src/templates/templates/item.html!}
```

Nessa exemplo, ele seria vinculado a um arquivo CSS em `static/styles.css` com:

```CSS hl_lines="4"
{!../../../docs_src/templates/static/styles.css!}
```

E por você estar usando `StaticFiles`, esse arquivo CSS deveria ser servido automaticamente pela sua aplicação **FastAPI** na URL `/static/styles.css`.

## Mais detalhes

Para mais detalhes, incluindo como testar templates, cheque a<a href="https://www.starlette.io/templates/" class="external-link" target="_blank">documentação de templates do Starlette</a>.
