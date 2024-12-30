# Parâmetros de Cookie

Você pode definir parâmetros de Cookie da mesma maneira que define paramêtros com `Query` e `Path`.

## Importe `Cookie`

Primeiro importe `Cookie`:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## Declare parâmetros de `Cookie`

Então declare os paramêtros de cookie usando a mesma estrutura que em `Path` e `Query`.

Você pode definir o valor padrão, assim como todas as validações extras ou parâmetros de anotação:


{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | Detalhes Técnicos

`Cookie` é uma classe "irmã" de `Path` e `Query`. Ela também herda da mesma classe em comum `Param`.

Mas lembre-se que quando você importa `Query`, `Path`, `Cookie` e outras de `fastapi`, elas são na verdade funções que retornam classes especiais.

///

/// info | Informação

Para declarar cookies, você precisa usar `Cookie`, pois caso contrário, os parâmetros seriam interpretados como parâmetros de consulta.

///

## Recapitulando

Declare cookies com `Cookie`, usando o mesmo padrão comum que utiliza-se em `Query` e `Path`.
