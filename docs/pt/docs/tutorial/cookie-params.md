# Parâmetros de Cookie

Você pode definir parâmetros de Cookie da mesma maneira que define paramêtros com `Query` e `Path`.

## Importe `Cookie`

Primeiro importe `Cookie`:

//// tab | Python 3.10+

```Python hl_lines="3"
{!> ../../docs_src/cookie_params/tutorial001_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="3"
{!> ../../docs_src/cookie_params/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="3"
{!> ../../docs_src/cookie_params/tutorial001_an.py!}
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | Dica

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="1"
{!> ../../docs_src/cookie_params/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="3"
{!> ../../docs_src/cookie_params/tutorial001.py!}
```

////

## Declare parâmetros de `Cookie`

Então declare os paramêtros de cookie usando a mesma estrutura que em `Path` e `Query`.

Você pode definir o valor padrão, assim como todas as validações extras ou parâmetros de anotação:


//// tab | Python 3.10+

```Python hl_lines="9"
{!> ../../docs_src/cookie_params/tutorial001_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../docs_src/cookie_params/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="10"
{!> ../../docs_src/cookie_params/tutorial001_an.py!}
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | Dica

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="7"
{!> ../../docs_src/cookie_params/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="9"
{!> ../../docs_src/cookie_params/tutorial001.py!}
```

////

/// note | Detalhes Técnicos

`Cookie` é uma classe "irmã" de `Path` e `Query`. Ela também herda da mesma classe em comum `Param`.

Mas lembre-se que quando você importa `Query`, `Path`, `Cookie` e outras de `fastapi`, elas são na verdade funções que retornam classes especiais.

///

/// info | Informação

Para declarar cookies, você precisa usar `Cookie`, pois caso contrário, os parâmetros seriam interpretados como parâmetros de consulta.

///

## Recapitulando

Declare cookies com `Cookie`, usando o mesmo padrão comum que utiliza-se em `Query` e `Path`.
