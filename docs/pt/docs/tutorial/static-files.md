# Arquivos Estáticos

Você pode servir arquivos estáticos automaticamente de um diretório usando `StaticFiles`.

## Use `StaticFiles`

* Importe `StaticFiles`.
* "Monte" uma instância de `StaticFiles()` em um caminho específico.

```Python hl_lines="2  6"
{!../../../docs_src/static_files/tutorial001.py!}
```

!!! note "Detalhes técnicos"
    Você também pode usar `from starlette.staticfiles import StaticFiles`.

    O **FastAPI** fornece o mesmo que `starlette.staticfiles` como `fastapi.staticfiles` apenas como uma conveniência para você, o desenvolvedor. Mas na verdade vem diretamente da Starlette.

### O que é "Montagem"

"Montagem" significa adicionar um aplicativo completamente "independente" em uma rota específica, que então cuida de todas as subrotas.

Isso é diferente de usar um `APIRouter`, pois um aplicativo montado é completamente independente. A OpenAPI e a documentação do seu aplicativo principal não incluirão nada do aplicativo montado, etc.

Você pode ler mais sobre isso no **Guia Avançado do Usuário**.

## Detalhes

O primeiro `"/static"` refere-se à subrota em que este "subaplicativo" será "montado". Portanto, qualquer caminho que comece com `"/static"` será tratado por ele.

O `directory="static"` refere-se ao nome do diretório que contém seus arquivos estáticos.

O `name="static"` dá a ela um nome que pode ser usado internamente pelo FastAPI.

Todos esses parâmetros podem ser diferentes de "`static`", ajuste-os de acordo com as necessidades e detalhes específicos de sua própria aplicação.

## Mais informações

Para mais detalhes e opções, verifique <a href="https://www.starlette.io/staticfiles/" class="external-link" target="_blank">Starlette's docs about Static Files</a>.
