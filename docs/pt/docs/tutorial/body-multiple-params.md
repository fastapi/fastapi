# Corpo - Múltiplos parâmetros

Agora que nós vimos como usar `Path` e `Query`, veremos usos mais avançados de declarações no corpo da requisição.

## Misture `Path`, `Query` e parâmetros de corpo

Primeiro, é claro, você pode misturar `Path`, `Query` e declarações de parâmetro no corpo da requisição livremente e **FastAPI** saberá o que fazer.

E você também pode declarar parâmetros de corpo como opcionais, definindo o valor padrão com `None`:

```Python hl_lines="19-21"
{!../../../docs_src/body_multiple_params/tutorial001.py!}
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

Mas você pode também declarar múltiplos parâmetros de corpo, e.g. `item` e `user`:

```Python hl_lines="22"
{!../../../docs_src/body_multiple_params/tutorial002.py!}
```

Neste caso, **FastAPI** vai perceber que existe mais de um parâmetro de corpo na função (dois parâmetros que são modelos Pydantic).

Então, ele vai usar o nome dos parâmetros como chaves (nome dos campos) no corpo, e espera um corpo como:

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
    Repare que mesmo que o `item` esteja declarado da mesma maneira que antes, agora ele é esperado esteja dentro do corpo com uma chave `item`.


**FastAPI** vai fazer a conversão automática a partir da requisição, assim esse parâmetro `item` receberá seu respectivo conteúdo específico e o mesmo ocorre com `user`.

Ele vai realizar a validação dos dados compostos, e vai documentá-los de maneira compatível com `OpenAPI schema` e documentação automática.

## Valores singulares no corpo

Assim como existem uma `Query` e uma `Path` para definir dados adicionais para parâmetros de consulta e de rota, **FastAPI** provê o equivalente para `Body`.

Por exemplo, extendendo o modelo anterior, você poder decidir por ter uma outra chave `importance` no mesmo corpo, além de `item` e `user`.

Se você declará-lo como é, porque é um valor singular, **FastAPI** vai assumir que se trata de um parâmetro de consulta.

Mas você pode instruir **FastAPI** para tratá-lo como outra chave do corpo usando `Body`:


```Python hl_lines="23"
{!../../../docs_src/body_multiple_params/tutorial003.py!}
```

Neste caso, **FastAPI** vai esperar um corpo como:


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

Mais uma vez, ele vai converter os tipos de dados, validar, documentar, etc.

## Múltiplos parâmetros de corpo e consulta

Obviamente, você pode também declarar parâmetros de consulta assim que você precisar, de modo adicional a quaisquer parâmetros de corpo.

Dado que, por padrão, valores singulares são interpretados como parâmetros de consulta, você não precisa explicitamente adicionar uma `Query`, você pode somente:

```Python
q: Optional[str] = None
```

como em:

```Python hl_lines="28"
{!../../../docs_src/body_multiple_params/tutorial004.py!}
```

!!! info
    `Body` também possui todas as validações adicionais e metadados de parâmetros como em `Query`,`Path` e outras que você verá depois.


## Requisite a indicação da chave para um único parâmetro de corpo

Suponha que você tem um único `item` parâmetro de corpo a partir de um modelo Pydantic `Item`.

Por padrão, **FastAPI** vai então esperar que seu conteúdo venha no corpo diretamente.

Mas se você quiser que ele requisite por um JSON com uma chave `item` e dentro dele os conteúdos do modelo, como ocorre ao declarar vários parâmetros de corpo, você pode usar o parâmetro especial de `Body` chamado `embed`:

```Python
item: Item = Body(..., embed=True)
```

como em:

```Python hl_lines="17"
{!../../../docs_src/body_multiple_params/tutorial005.py!}
```

Neste caso **FastAPI** vai esperar um corpo como:

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

E você pode instruir **FastAPI** para requisitar no corpo a indicação de chave mesmo quando existe somente um parâmetro declarado.
