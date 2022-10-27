# Arquivos estáticos

Você pode acessar arquivos estáticos automaticamente de um diretório usando `StaticFiles`.

## Use `StaticFiles`

* Import `StaticFiles`.
* Use "Mount" e a instância `StaticFiles()` em um caminho específico.

```Python hl_lines="2  6"
{!../../../docs_src/static_files/tutorial001.py!}
```

!!! note "Detalhes Técnicos"
    Você também poderia usar `from starlette.staticfiles import StaticFiles`. 

    A **FastAPI** fornece `starlette.staticfiles` como `fastapi.staticfiles` apenas por conveniência para você. Mas na verdade ele vem da Starlette.

### O que é "Mounting"

"Mounting" significa adicionar uma aplicação completamente independente em um caminho específico, que então cuida de todos os caminhos independentes.

Isso é diferente de usar uma `APIRouter` já que uma aplicação em que se usou "mount" é completamente independente. Ambas a OpenAPI e os docs da sua aplicação principal não vão incluir nada da aplicação com "mount".

Você pode ler mais sobre isso em **Advanced User Guide**.

## Detalhes

O primeiro `"/static"` se refere ao sub-caminho que essa "sub-aplicação" será "mounted". Então, qualquer caminho que comece com `"/static"` será tratado por ela.

O `directory="static"` se refere ao nome do diretório que contém seus arquivos estáticos.

O `name="static"` dá um nome que pode ser usado internamente pelo **FastAPI**.

Todos esses parâmetros podem ser diferentes de "`static`", você pode ajustá-los de acordo com suas necessidades e detalhes específicos da sua aplicação.

## Mais informações

Para mais detalhes e opções confira <a href="https://www.starlette.io/staticfiles/" class="external-link" target="_blank">Starlette's docs about Static Files</a>.