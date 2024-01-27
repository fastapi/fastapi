# Parâmetros de Cookie

Você pode definir parâmetros de Cookie da mesma maneira que define paramêtros com `Query` e `Path`.

## Importe `Cookie`

Primeiro importe `Cookie`:

```Python hl_lines="3"
{!../../../docs_src/cookie_params/tutorial001.py!}
```

## Declare parâmetros de `Cookie`

Então declare os paramêtros de cookie usando a mesma estrutura que em `Path` e `Query`.

O primeiro valor é o valor padrão, você pode passar todas as validações adicionais ou parâmetros de anotação:

```Python hl_lines="9"
{!../../../docs_src/cookie_params/tutorial001.py!}
```

!!! note "Detalhes Técnicos"
    `Cookie` é uma classe "irmã" de `Path` e `Query`. Ela também herda da mesma classe em comum `Param`.

    Mas lembre-se que quando você importa `Query`, `Path`, `Cookie` e outras de `fastapi`, elas são na verdade funções que retornam classes especiais.

!!! info "Informação"
    Para declarar cookies, você precisa usar `Cookie`, caso contrário, os parâmetros seriam interpretados como parâmetros de consulta.

## Recapitulando

Declare cookies com `Cookie`, usando o mesmo padrão comum que utiliza-se em `Query` e `Path`.
