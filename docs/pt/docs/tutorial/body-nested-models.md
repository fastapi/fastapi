# Corpo - Modelos aninhados { #body-nested-models }

Com o **FastAPI**, você pode definir, validar, documentar e usar modelos arbitrariamente e profundamente aninhados (graças ao Pydantic).

## Campos do tipo Lista { #list-fields }

Você pode definir um atributo como um subtipo. Por exemplo, uma `list` do Python:

{* ../../docs_src/body_nested_models/tutorial001_py310.py hl[12] *}

Isso fará com que tags seja uma lista de itens mesmo sem declarar o tipo dos elementos desta lista.

## Campos do tipo Lista com um parâmetro de tipo { #list-fields-with-type-parameter }

Mas o Python tem uma maneira específica de declarar listas com tipos internos ou "parâmetros de tipo":

### Importe `List` do typing { #import-typings-list }

No Python 3.9 e superior você pode usar a `list` padrão para declarar essas anotações de tipo, como veremos abaixo. 💡

Mas nas versões do Python anteriores à 3.9 (3.6 e superiores), primeiro é necessário importar `List` do módulo padrão `typing` do Python:

{* ../../docs_src/body_nested_models/tutorial002.py hl[1] *}

### Declare uma `list` com um parâmetro de tipo { #declare-a-list-with-a-type-parameter }

Para declarar tipos que têm parâmetros de tipo (tipos internos), como `list`, `dict`, `tuple`:

* Se você estiver em uma versão do Python inferior a 3.9, importe a versão equivalente do módulo `typing`
* Passe o(s) tipo(s) interno(s) como "parâmetros de tipo" usando colchetes: `[` e `]`

No Python 3.9, seria:

```Python
my_list: list[str]
```

Em versões do Python anteriores à 3.9, seria:

```Python
from typing import List

my_list: List[str]
```

Essa é a sintaxe padrão do Python para declarações de tipo.

Use a mesma sintaxe padrão para atributos de modelo com tipos internos.

Portanto, em nosso exemplo, podemos fazer com que `tags` sejam especificamente uma "lista de strings":

{* ../../docs_src/body_nested_models/tutorial002_py310.py hl[12] *}

## Tipos "set" { #set-types }

Mas então, quando nós pensamos mais, percebemos que as tags não devem se repetir, elas provavelmente devem ser strings únicas.

E que o Python tem um tipo de dados especial para conjuntos de itens únicos, o `set`.

Então podemos declarar `tags` como um conjunto de strings:

{* ../../docs_src/body_nested_models/tutorial003_py310.py hl[12] *}

Com isso, mesmo que você receba uma requisição contendo dados duplicados, ela será convertida em um conjunto de itens exclusivos.

E sempre que você enviar esses dados como resposta, mesmo se a fonte tiver duplicatas, eles serão gerados como um conjunto de itens exclusivos.

E também teremos anotações/documentação em conformidade.

## Modelos aninhados { #nested-models }

Cada atributo de um modelo Pydantic tem um tipo.

Mas esse tipo pode ser outro modelo Pydantic.

Portanto, você pode declarar "objects" JSON profundamente aninhados com nomes, tipos e validações de atributos específicos.

Tudo isso, aninhado arbitrariamente.

### Defina um sub-modelo { #define-a-submodel }

Por exemplo, nós podemos definir um modelo `Image`:

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[7:9] *}

### Use o sub-modelo como um tipo { #use-the-submodel-as-a-type }

E então podemos usa-lo como o tipo de um atributo:

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[18] *}

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

* Suporte do editor (preenchimento automático, etc.), inclusive para modelos aninhados
* Conversão de dados
* Validação de dados
* Documentação automatica

## Tipos especiais e validação { #special-types-and-validation }

Além dos tipos singulares normais como `str`, `int`, `float`, etc. Você também pode usar tipos singulares mais complexos que herdam de `str`.

Para ver todas as opções possíveis, consulte a <a href="https://docs.pydantic.dev/latest/concepts/types/" class="external-link" target="_blank">Visão geral dos tipos do Pydantic</a>. Você verá alguns exemplos no próximo capítulo.

Por exemplo, no modelo `Image` nós temos um campo `url`, nós podemos declara-lo como um `HttpUrl` do Pydantic invés de como uma `str`:

{* ../../docs_src/body_nested_models/tutorial005_py310.py hl[2,8] *}

A string será verificada para se tornar uma URL válida e documentada no JSON Schema / OpenAPI como tal.

## Atributos como listas de submodelos { #attributes-with-lists-of-submodels }

Você também pode usar modelos Pydantic como subtipos de `list`, `set`, etc:

{* ../../docs_src/body_nested_models/tutorial006_py310.py hl[18] *}

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

/// info | Informação

Observe como a chave `images` agora tem uma lista de objetos de imagem.

///

## Modelos profundamente aninhados { #deeply-nested-models }

Você pode definir modelos profundamente aninhados de forma arbitrária:

{* ../../docs_src/body_nested_models/tutorial007_py310.py hl[7,12,18,21,25] *}

/// info | Informação

Observe como `Offer` tem uma lista de `Item`s, que por sua vez têm uma lista opcional de `Image`s

///

## Corpos de listas puras { #bodies-of-pure-lists }

Se o valor de primeiro nível do corpo JSON que você espera for um `array` do JSON (uma` lista` do Python), você pode declarar o tipo no parâmetro da função, da mesma forma que nos modelos do Pydantic:

```Python
images: List[Image]
```

ou no Python 3.9 e superior:

```Python
images: list[Image]
```

como em:

{* ../../docs_src/body_nested_models/tutorial008_py39.py hl[13] *}

## Suporte de editor em todo canto { #editor-support-everywhere }

E você obtém suporte do editor em todos os lugares.

Mesmo para itens dentro de listas:

<img src="/img/tutorial/body-nested-models/image01.png">

Você não conseguiria este tipo de suporte de editor se estivesse trabalhando diretamente com `dict` em vez de modelos Pydantic.

Mas você também não precisa se preocupar com eles, os dicts de entrada são convertidos automaticamente e sua saída é convertida automaticamente para JSON também.

## Corpos de `dict`s arbitrários { #bodies-of-arbitrary-dicts }

Você também pode declarar um corpo como um `dict` com chaves de algum tipo e valores de outro tipo.

Sem ter que saber de antemão quais são os nomes de campos/atributos válidos (como seria o caso dos modelos Pydantic).

Isso seria útil se você deseja receber chaves que ainda não conhece.

---

Outro caso útil é quando você deseja ter chaves de outro tipo, por exemplo, `int`.

É isso que vamos ver aqui.

Neste caso, você aceitaria qualquer `dict`, desde que tenha chaves` int` com valores `float`:

{* ../../docs_src/body_nested_models/tutorial009_py39.py hl[7] *}

/// tip | Dica

Leve em condideração que o JSON só suporta `str` como chaves.

Mas o Pydantic tem conversão automática de dados.

Isso significa que, embora os clientes da API só possam enviar strings como chaves, desde que essas strings contenham inteiros puros, o Pydantic irá convertê-los e validá-los.

E o `dict` que você recebe como `weights` terá, na verdade, chaves `int` e valores` float`.

///

## Recapitulação { #recap }

Com **FastAPI** você tem a flexibilidade máxima fornecida pelos modelos Pydantic, enquanto seu código é mantido simples, curto e elegante.

Mas com todos os benefícios:

* Suporte do editor (preenchimento automático em todo canto!)
* Conversão de dados (parsing/serialização)
* Validação de dados
* Documentação dos esquemas
* Documentação automática
