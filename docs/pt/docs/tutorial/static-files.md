# Arquivos Estáticos { #static-files }

Você pode servir arquivos estáticos automaticamente a partir de um diretório usando `StaticFiles`.

## Use `StaticFiles` { #use-staticfiles }

* Importe `StaticFiles`.
* "Monte" uma instância de `StaticFiles()` em um path específico.

{* ../../docs_src/static_files/tutorial001.py hl[2,6] *}

/// note | Detalhes Técnicos

Você também pode usar `from starlette.staticfiles import StaticFiles`.

O **FastAPI** fornece o mesmo que `starlette.staticfiles` como `fastapi.staticfiles` apenas como uma conveniência para você, o desenvolvedor. Mas na verdade vem diretamente da Starlette.

///

### O que é "Montagem" { #what-is-mounting }

"Montagem" significa adicionar uma aplicação completamente "independente" em um path específico, que então cuida de lidar com todos os sub-paths.

Isso é diferente de usar um `APIRouter`, pois uma aplicação montada é completamente independente. A OpenAPI e a documentação da sua aplicação principal não incluirão nada da aplicação montada, etc.

Você pode ler mais sobre isso no [Guia Avançado do Usuário](../advanced/index.md){.internal-link target=_blank}.

## Detalhes { #details }

O primeiro `"/static"` refere-se ao sub-path no qual este "subaplicativo" será "montado". Assim, qualquer path que comece com `"/static"` será tratado por ele.

O `directory="static"` refere-se ao nome do diretório que contém seus arquivos estáticos.

O `name="static"` dá a ele um nome que pode ser usado internamente pelo **FastAPI**.

Todos esses parâmetros podem ser diferentes de "`static`", ajuste-os de acordo com as necessidades e detalhes específicos da sua própria aplicação.

## Mais informações { #more-info }

Para mais detalhes e opções, consulte <a href="https://www.starlette.dev/staticfiles/" class="external-link" target="_blank">a documentação da Starlette sobre Arquivos Estáticos</a>.
