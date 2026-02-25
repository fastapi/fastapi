# Parâmetros de Cookie { #cookie-parameters }

Você pode definir parâmetros de Cookie da mesma maneira que define parâmetros com `Query` e `Path`.

## Importe `Cookie` { #import-cookie }

Primeiro importe `Cookie`:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## Declare parâmetros de `Cookie` { #declare-cookie-parameters }

Então declare os parâmetros de cookie usando a mesma estrutura que em `Path` e `Query`.

Você pode definir o valor padrão, assim como todas as validações extras ou parâmetros de anotação:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | Detalhes Técnicos

`Cookie` é uma classe "irmã" de `Path` e `Query`. Ela também herda da mesma classe em comum `Param`.

Mas lembre-se que quando você importa `Query`, `Path`, `Cookie` e outras de `fastapi`, elas são na verdade funções que retornam classes especiais.

///

/// info | Informação

Para declarar cookies, você precisa usar `Cookie`, pois caso contrário, os parâmetros seriam interpretados como parâmetros de consulta.

///

/// info | Informação

Tenha em mente que, como os **navegadores lidam com cookies** de maneiras especiais e nos bastidores, eles **não** permitem facilmente que o **JavaScript** os acesse.

Se você for à **interface de documentação da API** em `/docs`, poderá ver a **documentação** de cookies para suas *operações de rota*.

Mas mesmo que você **preencha os dados** e clique em "Execute", como a interface de documentação funciona com **JavaScript**, os cookies não serão enviados e você verá uma mensagem de **erro** como se você não tivesse escrito nenhum valor.

///

## Recapitulando { #recap }

Declare cookies com `Cookie`, usando o mesmo padrão comum que utiliza-se em `Query` e `Path`.
