# Corpo - Múltiplos parâmetros

Agora que nós vimos como usar `Path` e `Query`, veremos usos mais avançados de declarações no corpo da requisição.

## Misture `Path`, `Query` e parâmetros de corpo

Primeiro, é claro, você pode misturar `Path`, `Query` e declarações de parâmetro no corpo da requisição livremente e o **FastAPI** saberá o que fazer.

E você também pode declarar parâmetros de corpo como opcionais, definindo o valor padrão com `None`:

=== "Python 3.6 e superiores"

    ```Python hl_lines="19-21"
    {!> ../../../docs_src/body_multiple_params/tutorial001.py!}
    ```

=== "Python 3.10 e superiores"

    ```Python hl_lines="17-19"
    {!> ../../../docs_src/body_multiple_params/tutorial001_py310.py!}
    ```

!!! nota
    Repare que, neste caso, o `item` que seria capturado a partir do corpo é opcional. Visto que ele possui `None` como valor padrão.

## Múltiplos parâmetros de corpo

No exemplo anterior, as *operações de rota* esperariam um JSON no corpo contendo os atributos de um `Item`, exemplo:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

Mas você pode também declarar múltiplos parâmetros de corpo, por exemplo, `item` e `user`:

=== "Python 3.6 e superiores"

    ```Python hl_lines="22"
    {!> ../../../docs_src/body_multiple_params/tutorial002.py!}
    ```

=== "Python 3.10 e superiores"

    ```Python hl_lines="20"
    {!> ../../../docs_src/body_multiple_params/tutorial002_py310.py!}
    ```

Neste caso, o **FastAPI** perceberá que existe mais de um parâmetro de corpo na função (dois parâmetros que são modelos Pydantic).

Então, ele usará o nome dos parâmetros como chaves (nome dos campos) no corpo, e espera um corpo como:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
```

!!! nota
    Repare que mesmo que o `item` esteja declarado da mesma maneira que antes, agora é esperado que ele esteja dentro do corpo com uma chave `item`.


O **FastAPI** fará a conversão automática a partir da requisição, assim esse parâmetro `item` receberá seu respectivo conteúdo e o mesmo ocorrerá com `user`.

Ele executará a validação dos dados compostos e irá documentá-los de maneira compatível com o esquema OpenAPI e documentação automática.

## Valores singulares no corpo

Assim como existem uma `Query` e uma `Path` para definir dados adicionais para parâmetros de consulta e de rota, o **FastAPI** provê o equivalente para `Body`.

Por exemplo, extendendo o modelo anterior, você poder decidir por ter uma outra chave `importance` no mesmo corpo, além de `item` e `user`.

Se você declará-lo como é, porque é um valor singular, o **FastAPI** assumirá que se trata de um parâmetro de consulta.

Mas você pode instruir o **FastAPI** para tratá-lo como outra chave do corpo usando `Body`:

=== "Python 3.6 e superiores"

    ```Python hl_lines="22"
    {!> ../../../docs_src/body_multiple_params/tutorial003.py!}
    ```

=== "Python 3.10 e superiores"

    ```Python hl_lines="20"
    {!> ../../../docs_src/body_multiple_params/tutorial003_py310.py!}
    ```

Neste caso, o **FastAPI** esperará um corpo como:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
```

Mais uma vez, ele converterá os tipos de dados, validar, documentar, etc.

## Múltiplos parâmetros de corpo e consulta

Obviamente, você também pode declarar parâmetros de consulta assim que você precisar, de modo adicional a quaisquer parâmetros de corpo.

Dado que, por padrão, valores singulares são interpretados como parâmetros de consulta, você não precisa explicitamente adicionar uma `Query`, você pode somente:

```Python
q: Union[str, None] = None
```

Ou como em Python 3.10 e versões superiores:

```Python
q: str | None = None
```

Por exemplo:

=== "Python 3.6 e superiores"

    ```Python hl_lines="27"
    {!> ../../../docs_src/body_multiple_params/tutorial004.py!}
    ```

=== "Python 3.10 e superiores"

    ```Python hl_lines="26"
    {!> ../../../docs_src/body_multiple_params/tutorial004_py310.py!}
    ```

!!! info "Informação"
    `Body` também possui todas as validações adicionais e metadados de parâmetros como em `Query`,`Path` e outras que você verá depois.

## Declare um único parâmetro de corpo indicando sua chave

Suponha que você tem um único parâmetro de corpo `item`, a partir de um modelo Pydantic `Item`.

Por padrão, o **FastAPI** esperará que seu conteúdo venha no corpo diretamente.

Mas se você quiser que ele espere por um JSON com uma chave `item` e dentro dele os conteúdos do modelo, como ocorre ao declarar vários parâmetros de corpo, você pode usar o parâmetro especial de `Body` chamado `embed`:

```Python
item: Item = Body(embed=True)
```

como em:

=== "Python 3.6 e superiores"

    ```Python hl_lines="17"
    {!> ../../../docs_src/body_multiple_params/tutorial005.py!}
    ```

=== "Python 3.10 e superiores"

    ```Python hl_lines="15"
    {!> ../../../docs_src/body_multiple_params/tutorial005_py310.py!}
    ```

Neste caso o **FastAPI** esperará um corpo como:

```JSON hl_lines="2"
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
```

ao invés de:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

## Recapitulando

Você pode adicionar múltiplos parâmetros de corpo para sua *função de operação de rota*, mesmo que a requisição possa ter somente um único corpo.

E o **FastAPI** vai manipulá-los, mandar para você os dados corretos na sua função, e validar e documentar o schema correto na *operação de rota*.

Você também pode declarar valores singulares para serem recebidos como parte do corpo.

E você pode instruir o **FastAPI** para requisitar no corpo a indicação de chave mesmo quando existe somente um único parâmetro declarado.
