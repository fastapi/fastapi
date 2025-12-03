# Parâmetros de Cabeçalho { #header-parameters }

Você pode definir parâmetros de Cabeçalho da mesma maneira que define paramêtros com `Query`, `Path` e `Cookie`.

## Importe `Header` { #import-header }

Primeiro importe `Header`:

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[3] *}

## Declare parâmetros de `Header` { #declare-header-parameters }

Então declare os paramêtros de cabeçalho usando a mesma estrutura que em `Path`, `Query` e `Cookie`.

O primeiro valor é o valor padrão, você pode passar todas as validações adicionais ou parâmetros de anotação:

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[9] *}

/// note | Detalhes Técnicos

`Header` é uma classe "irmã" de `Path`, `Query` e `Cookie`. Ela também herda da mesma classe em comum `Param`.

Mas lembre-se que quando você importa `Query`, `Path`, `Header`, e outras de `fastapi`, elas são na verdade funções que retornam classes especiais.

///

/// info | Informação

Para declarar headers, você precisa usar `Header`, caso contrário, os parâmetros seriam interpretados como parâmetros de consulta.

///

## Conversão automática { #automatic-conversion }

`Header` tem algumas funcionalidades a mais em relação a `Path`, `Query` e `Cookie`.

A maioria dos cabeçalhos padrão são separados pelo caractere "hífen", também conhecido como "sinal de menos" (`-`).

Mas uma variável como `user-agent` é inválida em Python.

Portanto, por padrão, `Header` converterá os caracteres de nomes de parâmetros de sublinhado (`_`) para hífen (`-`) para extrair e documentar os cabeçalhos.

Além disso, os cabeçalhos HTTP não diferenciam maiúsculas de minúsculas, portanto, você pode declará-los com o estilo padrão do Python (também conhecido como "snake_case").

Portanto, você pode usar `user_agent` como faria normalmente no código Python, em vez de precisar colocar as primeiras letras em maiúsculas como `User_Agent` ou algo semelhante.

Se por algum motivo você precisar desabilitar a conversão automática de sublinhados para hífens, defina o parâmetro `convert_underscores` de `Header` para `False`:

{* ../../docs_src/header_params/tutorial002_an_py310.py hl[10] *}

/// warning | Atenção

Antes de definir `convert_underscores` como `False`, lembre-se de que alguns proxies e servidores HTTP não permitem o uso de cabeçalhos com sublinhados.

///

## Cabeçalhos duplicados { #duplicate-headers }

É possível receber cabeçalhos duplicados. Isso significa, o mesmo cabeçalho com vários valores.

Você pode definir esses casos usando uma lista na declaração de tipo.

Você receberá todos os valores do cabeçalho duplicado como uma `list` Python.

Por exemplo, para declarar um cabeçalho de `X-Token` que pode aparecer mais de uma vez, você pode escrever:

{* ../../docs_src/header_params/tutorial003_an_py310.py hl[9] *}

Se você se comunicar com essa *operação de rota* enviando dois cabeçalhos HTTP como:

```
X-Token: foo
X-Token: bar
```

A resposta seria como:

```JSON
{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
```

## Recapitulando { #recap }

Declare cabeçalhos com `Header`, usando o mesmo padrão comum que utiliza-se em `Query`, `Path` e `Cookie`.

E não se preocupe com sublinhados em suas variáveis, **FastAPI** cuidará da conversão deles.
