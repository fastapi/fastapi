# Dependências em decoradores de operações de rota { #dependencies-in-path-operation-decorators }

Em alguns casos você não precisa necessariamente retornar o valor de uma dependência dentro de uma *função de operação de rota*.

Ou a dependência não retorna nenhum valor.

Mas você ainda precisa que ela seja executada/resolvida.

Para esses casos, em vez de declarar um parâmetro em uma *função de operação de rota* com `Depends`, você pode adicionar um argumento `dependencies` do tipo `list` ao decorador da operação de rota.

## Adicione `dependencies` ao decorador da operação de rota { #add-dependencies-to-the-path-operation-decorator }

O *decorador da operação de rota* recebe um argumento opcional `dependencies`.

Ele deve ser uma lista de `Depends()`:

{* ../../docs_src/dependencies/tutorial006_an_py39.py hl[19] *}

Essas dependências serão executadas/resolvidas da mesma forma que dependências comuns. Mas o valor delas (se existir algum) não será passado para a sua *função de operação de rota*.

/// tip | Dica

Alguns editores de texto checam parâmetros de funções não utilizados, e os mostram como erros.

Utilizando `dependencies` no *decorador da operação de rota* você pode garantir que elas serão executadas enquanto evita erros de editores/ferramentas.

Isso também pode ser útil para evitar confundir novos desenvolvedores que ao ver um parâmetro não usado no seu código podem pensar que ele é desnecessário.

///

/// info | Informação

Neste exemplo utilizamos cabeçalhos personalizados inventados `X-Key` e `X-Token`.

Mas em situações reais, como implementações de segurança, você pode obter mais vantagens em usar as [Ferramentas de segurança integradas (o próximo capítulo)](../security/index.md){.internal-link target=_blank}.

///

## Erros das dependências e valores de retorno { #dependencies-errors-and-return-values }

Você pode utilizar as mesmas *funções* de dependências que você usaria normalmente.

### Requisitos de Dependências { #dependency-requirements }

Dependências podem declarar requisitos de requisições (como cabeçalhos) ou outras subdependências:

{* ../../docs_src/dependencies/tutorial006_an_py39.py hl[8,13] *}

### Levantar exceções { #raise-exceptions }

Essas dependências podem `raise` exceções, da mesma forma que dependências comuns:

{* ../../docs_src/dependencies/tutorial006_an_py39.py hl[10,15] *}

### Valores de retorno { #return-values }

E elas também podem ou não retornar valores, eles não serão utilizados.

Então, você pode reutilizar uma dependência comum (que retorna um valor) que já seja utilizada em outro lugar, e mesmo que o valor não seja utilizado, a dependência será executada:

{* ../../docs_src/dependencies/tutorial006_an_py39.py hl[11,16] *}

## Dependências para um grupo de *operações de rota* { #dependencies-for-a-group-of-path-operations }

Mais a frente, quando você ler sobre como estruturar aplicações maiores ([Aplicações maiores - Múltiplos arquivos](../../tutorial/bigger-applications.md){.internal-link target=_blank}), possivelmente com múltiplos arquivos, você aprenderá a declarar um único parâmetro `dependencies` para um grupo de *operações de rota*.

## Dependências globais { #global-dependencies }

No próximo passo veremos como adicionar dependências para uma aplicação `FastAPI` inteira, para que elas sejam aplicadas em toda *operação de rota*.
