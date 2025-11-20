# Dependências Globais { #global-dependencies }

Para alguns tipos de aplicação você pode querer adicionar dependências para toda a aplicação.

De forma semelhante a [adicionar `dependencies` aos *decoradores de operação de rota*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}, você pode adicioná-las à aplicação `FastAPI`.

Nesse caso, elas serão aplicadas a todas as *operações de rota* da aplicação:

{* ../../docs_src/dependencies/tutorial012_an_py39.py hl[16] *}


E todos os conceitos apresentados na seção sobre [adicionar `dependencies` aos *decoradores de operação de rota*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} ainda se aplicam, mas nesse caso, para todas as *operações de rota* da aplicação.

## Dependências para conjuntos de *operações de rota* { #dependencies-for-groups-of-path-operations }

Mais para a frente, quando você ler sobre como estruturar aplicações maiores ([Aplicações Maiores - Múltiplos Arquivos](../../tutorial/bigger-applications.md){.internal-link target=_blank}), possivelmente com múltiplos arquivos, você irá aprender a declarar um único parâmetro `dependencies` para um conjunto de *operações de rota*.
