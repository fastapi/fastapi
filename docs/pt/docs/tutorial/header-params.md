# Parâmetros de Cabeçalho

Você pode definir parâmetros de Cabeçalho da mesma maneira que define paramêtros com `Query`, `Path` e `Cookie`.

## importe `Header`

Primeiro importe `Header`:

=== "Python 3.10+"

    ```Python hl_lines="1"
    {!> ../../../docs_src/header_params/tutorial001_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="3"
    {!> ../../../docs_src/header_params/tutorial001.py!}
    ```

## Declare parâmetros de `Header`

Então declare os paramêtros de cabeçalho usando a mesma estrutura que em `Path`, `Query` e `Cookie`.

O primeiro valor é o valor padrão, você pode passar todas as validações adicionais ou parâmetros de anotação:

=== "Python 3.10+"

    ```Python hl_lines="7"
    {!> ../../../docs_src/header_params/tutorial001_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/header_params/tutorial001.py!}
    ```

!!! note "Detalhes Técnicos"
    `Header` é uma classe "irmã" de `Path`, `Query` e `Cookie`. Ela também herda da mesma classe em comum `Param`.

    Mas lembre-se que quando você importa `Query`, `Path`, `Header`, e outras de `fastapi`, elas são na verdade funções que retornam classes especiais.

!!! info
    Para declarar headers, você precisa usar `Header`, caso contrário, os parâmetros seriam interpretados como parâmetros de consulta.

## Conversão automática

`Header` tem algumas funcionalidades a mais em relação a `Path`, `Query` e `Cookie`.

A maioria dos cabeçalhos padrão são separados pelo caractere "hífen", também conhecido como "sinal de menos" (`-`).

Mas uma variável como `user-agent` é inválida em Python.

Portanto, por padrão, `Header` converterá os caracteres de nomes de parâmetros de sublinhado (`_`) para hífen (`-`) para extrair e documentar os cabeçalhos.

Além disso, os cabeçalhos HTTP não diferenciam maiúsculas de minúsculas, portanto, você pode declará-los com o estilo padrão do Python (também conhecido como "snake_case").

Portanto, você pode usar `user_agent` como faria normalmente no código Python, em vez de precisar colocar as primeiras letras em maiúsculas como `User_Agent` ou algo semelhante.

Se por algum motivo você precisar desabilitar a conversão automática de sublinhados para hífens, defina o parâmetro `convert_underscores` de `Header` para `False`:

=== "Python 3.10+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/header_params/tutorial002_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/header_params/tutorial002.py!}
    ```

!!! warning "Aviso"
    Antes de definir `convert_underscores` como `False`, lembre-se de que alguns proxies e servidores HTTP não permitem o uso de cabeçalhos com sublinhados.

## Cabeçalhos duplicados

É possível receber cabeçalhos duplicados. Isso significa, o mesmo cabeçalho com vários valores.

Você pode definir esses casos usando uma lista na declaração de tipo.

Você receberá todos os valores do cabeçalho duplicado como uma `list` Python.

Por exemplo, para declarar um cabeçalho de `X-Token` que pode aparecer mais de uma vez, você pode escrever:

=== "Python 3.10+"

    ```Python hl_lines="7"
    {!> ../../../docs_src/header_params/tutorial003_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/header_params/tutorial003_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/header_params/tutorial003.py!}
    ```

Se você se comunicar com essa *operação de caminho* enviando dois cabeçalhos HTTP como:

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

## Recapitulando

Declare cabeçalhos com `Header`, usando o mesmo padrão comum que utiliza-se em `Query`, `Path` e `Cookie`.

E não se preocupe com sublinhados em suas variáveis, FastAPI cuidará da conversão deles.
