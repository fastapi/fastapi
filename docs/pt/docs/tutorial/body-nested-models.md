# Corpo - Modelos aninhados

Com o **FastAPI**, você pode definir, validar, documentar e usar modelos profundamente aninhados de forma arbitrária (graças ao Pydantic).

## Campos do tipo Lista

Você pode definir um atributo como um subtipo. Por exemplo, uma `list` do Python:

```Python hl_lines="14"
{!../../../docs_src/body_nested_models/tutorial001.py!}
```

Isso fará com que tags seja uma lista de itens mesmo sem declarar o tipo dos elementos desta lista.

## Campos do tipo Lista com um parâmetro de tipo

Mas o Python tem uma maneira específica de declarar listas com tipos internos ou "parâmetros de tipo":

### Importe `List` do typing

Primeiramente, importe `List` do módulo `typing` que já vem por padrão no Python:

```Python hl_lines="1"
{!../../../docs_src/body_nested_models/tutorial002.py!}
```

### Declare a `List` com um parâmetro de tipo

Para declarar tipos que têm parâmetros de tipo(tipos internos), como `list`, `dict`, `tuple`:

* Importe os do modulo `typing`
* Passe o(s) tipo(s) interno(s) como "parâmetros de tipo" usando colchetes: `[` e `]`

```Python
from typing import List

my_list: List[str]
```

Essa é a sintaxe padrão do Python para declarações de tipo.

Use a mesma sintaxe padrão para atributos de modelo com tipos internos.

Portanto, em nosso exemplo, podemos fazer com que `tags` sejam especificamente uma "lista de strings":


```Python hl_lines="14"
{!../../../docs_src/body_nested_models/tutorial002.py!}
```

## Tipo "set"


Mas então, quando nós pensamos mais, percebemos que as tags não devem se repetir, elas provavelmente devem ser strings únicas.

E que o Python tem um tipo de dados especial para conjuntos de itens únicos, o `set`.

Então podemos importar `Set` e declarar `tags` como um `set` de `str`s:


```Python hl_lines="1  14"
{!../../../docs_src/body_nested_models/tutorial003.py!}
```

Com isso, mesmo que você receba uma requisição contendo dados duplicados, ela será convertida em um conjunto de itens exclusivos.

E sempre que você enviar esses dados como resposta, mesmo se a fonte tiver duplicatas, eles serão gerados como um conjunto de itens exclusivos.

E também teremos anotações/documentação em conformidade.

## Modelos aninhados

Cada atributo de um modelo Pydantic tem um tipo.

Mas esse tipo pode ser outro modelo Pydantic.

Portanto, você pode declarar "objects" JSON profundamente aninhados com nomes, tipos e validações de atributos específicos.

Tudo isso, aninhado arbitrariamente.

### Defina um sub-modelo

Por exemplo, nós podemos definir um modelo `Image`:

```Python hl_lines="9-11"
{!../../../docs_src/body_nested_models/tutorial004.py!}
```

### Use o sub-modelo como um tipo

E então podemos usa-lo como o tipo de um atributo:

```Python hl_lines="20"
{!../../../docs_src/body_nested_models/tutorial004.py!}
```

Isso significa que o **FastAPI** vai esperar um corpo similar à:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
```

Novamente, apenas fazendo essa declaração, com o **FastAPI**, você ganha:

* Suporte do editor de texto (compleção, etc), inclusive para modelos aninhados
* Conversão de dados
* Validação de dados
* Documentação automatica

## Tipos especiais e validação

Além dos tipos singulares normais como `str`, `int`, `float`, etc. Você também pode usar tipos singulares mais complexos que herdam de `str`.

Para ver todas as opções possíveis, cheque a documentação para os<a href="https://pydantic-docs.helpmanual.io/usage/types/" class="external-link" target="_blank">tipos exoticos do Pydantic</a>. Você verá alguns exemplos no próximo capitulo.

Por exemplo, no modelo `Image` nós temos um campo `url`, nós podemos declara-lo como um `HttpUrl` do Pydantic invés de como uma `str`:

```Python hl_lines="4  10"
{!../../../docs_src/body_nested_models/tutorial005.py!}
```

A string será verificada para se tornar uma URL válida e documentada no esquema JSON/1OpenAPI como tal.

## Atributos como listas de submodelos

Você também pode usar modelos Pydantic como subtipos de `list`, `set`, etc:

```Python hl_lines="20"
{!../../../docs_src/body_nested_models/tutorial006.py!}
```

Isso vai esperar(converter, validar, documentar, etc) um corpo JSON tal qual:

```JSON hl_lines="11"
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": [
        "rock",
        "metal",
        "bar"
    ],
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}
```

!!! Informação
    Note como o campo `images` agora tem uma lista de objetos de image.

## Modelos profundamente aninhados

Você pode definir modelos profundamente aninhados de forma arbitrária:

```Python hl_lines="9  14  20  23  27"
{!../../../docs_src/body_nested_models/tutorial007.py!}
```

!!! Informação
    Note como `Offer` tem uma lista de `Item`s, que por sua vez possui opcionalmente uma lista `Image`s

## Corpos de listas puras

Se o valor de primeiro nível do corpo JSON que você espera for um `array` do JSON (uma` lista` do Python), você pode declarar o tipo no parâmetro da função, da mesma forma que nos modelos do Pydantic:


```Python
images: List[Image]
```

como em:

```Python hl_lines="15"
{!../../../docs_src/body_nested_models/tutorial008.py!}
```

## Suporte de editor em todo canto

E você obtém suporte do editor em todos os lugares.

Mesmo para itens dentro de listas:

<img src="/img/tutorial/body-nested-models/image01.png">

Você não conseguiria este tipo de suporte de editor se estivesse trabalhando diretamente com `dict` em vez de modelos Pydantic.

Mas você também não precisa se preocupar com eles, os dicts de entrada são convertidos automaticamente e sua saída é convertida automaticamente para JSON também.

## Corpos de `dict`s arbitrários

Você também pode declarar um corpo como um `dict` com chaves de algum tipo e valores de outro tipo.

Sem ter que saber de antemão quais são os nomes de campos/atributos válidos (como seria o caso dos modelos Pydantic).

Isso seria útil se você deseja receber chaves que ainda não conhece.

---

Outro caso útil é quando você deseja ter chaves de outro tipo, por exemplo, `int`.

É isso que vamos ver aqui.

Neste caso, você aceitaria qualquer `dict`, desde que tenha chaves` int` com valores `float`:

```Python hl_lines="9"
{!../../../docs_src/body_nested_models/tutorial009.py!}
```

!!! Dica
    Leve em condideração que o JSON só suporta `str` como chaves.

    Mas o Pydantic tem conversão automática de dados.

    Isso significa que, embora os clientes da API só possam enviar strings como chaves, desde que essas strings contenham inteiros puros, o Pydantic irá convertê-los e validá-los.

    E o `dict` que você recebe como `weights` terá, na verdade, chaves `int` e valores` float`.

## Recapitulação

Com **FastAPI** você tem a flexibilidade máxima fornecida pelos modelos Pydantic, enquanto seu código é mantido simples, curto e elegante.

Mas com todos os benefícios:

* Suporte do editor (compleção em todo canto!)
* Conversão de dados (leia-se parsing/serialização)
* Validação de dados
* Documentação dos esquemas
* Documentação automática
