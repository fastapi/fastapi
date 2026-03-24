# Introdução aos tipos Python { #python-types-intro }

O Python possui suporte para "type hints" opcionais (também chamados de "type annotations").

Esses **"type hints"** ou anotações são uma sintaxe especial que permite declarar o <dfn title="por exemplo: str, int, float, bool">tipo</dfn> de uma variável.

Ao declarar tipos para suas variáveis, editores e ferramentas podem oferecer um melhor suporte.

Este é apenas um **tutorial rápido / atualização** sobre type hints do Python. Ele cobre apenas o mínimo necessário para usá-los com o **FastAPI**... que é realmente muito pouco.

O **FastAPI** é todo baseado nesses type hints, eles oferecem muitas vantagens e benefícios.

Mas mesmo que você nunca use o **FastAPI**, você se beneficiaria de aprender um pouco sobre eles.

/// note | Nota

Se você é um especialista em Python e já sabe tudo sobre type hints, pule para o próximo capítulo.

///

## Motivação { #motivation }

Vamos começar com um exemplo simples:

{* ../../docs_src/python_types/tutorial001_py310.py *}

A chamada deste programa gera:

```
John Doe
```

A função faz o seguinte:

* Pega um `first_name` e `last_name`.
* Converte a primeira letra de cada uma em maiúsculas com `title()`.
* <dfn title="Coloca-os juntos, como um só. Com o conteúdo de um após o outro.">Concatena</dfn> com um espaço no meio.

{* ../../docs_src/python_types/tutorial001_py310.py hl[2] *}

### Edite-o { #edit-it }

É um programa muito simples.

Mas agora imagine que você estava escrevendo do zero.

Em algum momento você teria iniciado a definição da função, já tinha os parâmetros prontos...

Mas então você deve chamar "esse método que converte a primeira letra em maiúscula".

Era `upper`? Era `uppercase`? `first_uppercase`? `capitalize`?

Em seguida, tente com o velho amigo do programador, o preenchimento automático do editor.

Você digita o primeiro parâmetro da função, `first_name`, depois um ponto (`.`) e, em seguida, pressiona `Ctrl+Space` para acionar o preenchimento automático.

Mas, infelizmente, você não obtém nada útil:

<img src="/img/python-types/image01.png">

### Adicionar tipos { #add-types }

Vamos modificar uma única linha da versão anterior.

Vamos mudar exatamente esse fragmento, os parâmetros da função, de:

```Python
    first_name, last_name
```

para:

```Python
    first_name: str, last_name: str
```

É isso aí.

Esses são os "type hints":

{* ../../docs_src/python_types/tutorial002_py310.py hl[1] *}

Isso não é o mesmo que declarar valores padrão como seria com:

```Python
    first_name="john", last_name="doe"
```

É uma coisa diferente.

Estamos usando dois pontos (`:`), não sinal de igual (`=`).

E adicionar type hints normalmente não muda o que acontece do que aconteceria sem eles.

Mas agora, imagine que você está novamente no meio da criação dessa função, mas com type hints.

No mesmo ponto, você tenta acionar o preenchimento automático com o `Ctrl+Space` e vê:

<img src="/img/python-types/image02.png">

Com isso, você pode rolar, vendo as opções, até encontrar o que "soa familiar":

<img src="/img/python-types/image03.png">

## Mais motivação { #more-motivation }

Verifique esta função, ela já possui type hints:

{* ../../docs_src/python_types/tutorial003_py310.py hl[1] *}

Como o editor conhece os tipos das variáveis, você não obtém apenas o preenchimento automático, mas também as verificações de erro:

<img src="/img/python-types/image04.png">

Agora você sabe que precisa corrigi-la, convertendo `age` em uma string com `str(age)`:

{* ../../docs_src/python_types/tutorial004_py310.py hl[2] *}

## Declarando tipos { #declaring-types }

Você acabou de ver o local principal para declarar type hints. Como parâmetros de função.

Este também é o principal local em que você os usaria com o **FastAPI**.

### Tipos simples { #simple-types }

Você pode declarar todos os tipos padrão de Python, não apenas `str`.

Você pode usar, por exemplo:

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005_py310.py hl[1] *}

### Módulo `typing` { #typing-module }

Para alguns casos adicionais, você pode precisar importar alguns itens do módulo padrão `typing`, por exemplo, quando quiser declarar que algo pode ter "qualquer tipo", você pode usar `Any` de `typing`:

```python
from typing import Any


def some_function(data: Any):
    print(data)
```

### Tipos genéricos { #generic-types }

Alguns tipos podem receber "parâmetros de tipo" entre colchetes, para definir seus tipos internos, por exemplo, uma "lista de strings" seria declarada como `list[str]`.

Esses tipos que podem receber parâmetros de tipo são chamados **tipos genéricos** ou **genéricos**.

Você pode usar os mesmos tipos internos como genéricos (com colchetes e tipos dentro):

* `list`
* `tuple`
* `set`
* `dict`

#### List { #list }

Por exemplo, vamos definir uma variável para ser uma `list` de `str`.

Declare a variável, com a mesma sintaxe com dois pontos (`:`).

Como o tipo, coloque `list`.

Como a lista é um tipo que contém tipos internos, você os coloca entre colchetes:

{* ../../docs_src/python_types/tutorial006_py310.py hl[1] *}

/// info | Informação

Esses tipos internos dentro dos colchetes são chamados de "parâmetros de tipo".

Neste caso, `str` é o parâmetro de tipo passado para `list`.

///

Isso significa: "a variável `items` é uma `list`, e cada um dos itens desta lista é uma `str`".

Ao fazer isso, seu editor pode fornecer suporte mesmo durante o processamento de itens da lista:

<img src="/img/python-types/image05.png">

Sem tipos, isso é quase impossível de alcançar.

Observe que a variável `item` é um dos elementos da lista `items`.

E, ainda assim, o editor sabe que é um `str` e fornece suporte para isso.

#### Tuple e Set { #tuple-and-set }

Você faria o mesmo para declarar `tuple`s e `set`s:

{* ../../docs_src/python_types/tutorial007_py310.py hl[1] *}

Isso significa:

* A variável `items_t` é uma `tuple` com 3 itens, um `int`, outro `int` e uma `str`.
* A variável `items_s` é um `set`, e cada um de seus itens é do tipo `bytes`.

#### Dict { #dict }

Para definir um `dict`, você passa 2 parâmetros de tipo, separados por vírgulas.

O primeiro parâmetro de tipo é para as chaves do `dict`.

O segundo parâmetro de tipo é para os valores do `dict`:

{* ../../docs_src/python_types/tutorial008_py310.py hl[1] *}

Isso significa que:

* A variável `prices` é um `dict`:
    * As chaves deste `dict` são do tipo `str` (digamos, o nome de cada item).
    * Os valores deste `dict` são do tipo `float` (digamos, o preço de cada item).

#### Union { #union }

Você pode declarar que uma variável pode ser de qualquer um dentre **vários tipos**, por exemplo, um `int` ou um `str`.

Para defini-la, você usa a <dfn title='também chamado de "operador OU bit a bit", mas esse significado não é relevante aqui'>barra vertical (`|`)</dfn> para separar ambos os tipos.

Isso é chamado de "união", porque a variável pode ser qualquer coisa na união desses dois conjuntos de tipos.

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

Isso significa que `item` pode ser um `int` ou um `str`.

#### Possivelmente `None` { #possibly-none }

Você pode declarar que um valor pode ter um tipo, como `str`, mas que ele também pode ser `None`.

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

Usar `str | None` em vez de apenas `str` permitirá que o editor o ajude a detectar erros em que você poderia estar assumindo que um valor é sempre um `str`, quando na verdade ele também pode ser `None`.

### Classes como tipos { #classes-as-types }

Você também pode declarar uma classe como o tipo de uma variável.

Digamos que você tenha uma classe `Person`, com um nome:

{* ../../docs_src/python_types/tutorial010_py310.py hl[1:3] *}

Então você pode declarar que uma variável é do tipo `Person`:

{* ../../docs_src/python_types/tutorial010_py310.py hl[6] *}

E então, novamente, você recebe todo o suporte do editor:

<img src="/img/python-types/image06.png">

Perceba que isso significa que "`one_person` é uma **instância** da classe `Person`".

Isso não significa que "`one_person` é a **classe** chamada `Person`".

## Modelos Pydantic { #pydantic-models }

[Pydantic](https://docs.pydantic.dev/) é uma biblioteca Python para executar a validação de dados.

Você declara a "forma" dos dados como classes com atributos.

E cada atributo tem um tipo.

Em seguida, você cria uma instância dessa classe com alguns valores e ela os validará, os converterá para o tipo apropriado (se for esse o caso) e fornecerá um objeto com todos os dados.

E você recebe todo o suporte do editor com esse objeto resultante.

Um exemplo da documentação oficial do Pydantic:

{* ../../docs_src/python_types/tutorial011_py310.py *}

/// info | Informação

Para saber mais sobre o [Pydantic, verifique a documentação](https://docs.pydantic.dev/).

///

O **FastAPI** é todo baseado em Pydantic.

Você verá muito mais disso na prática no [Tutorial - Guia do usuário](tutorial/index.md).

## Type Hints com Metadados de Anotações { #type-hints-with-metadata-annotations }

O Python também possui uma funcionalidade que permite incluir **<dfn title="Informações sobre os dados, neste caso, informações sobre o tipo, por exemplo, uma descrição.">metadados</dfn> adicionais** nesses type hints utilizando `Annotated`.

Você pode importar `Annotated` de `typing`.

{* ../../docs_src/python_types/tutorial013_py310.py hl[1,4] *}

O Python em si não faz nada com este `Annotated`. E para editores e outras ferramentas, o tipo ainda é `str`.

Mas você pode utilizar este espaço dentro do `Annotated` para fornecer ao **FastAPI** metadados adicionais sobre como você deseja que a sua aplicação se comporte.

O importante aqui de se lembrar é que **o primeiro *type parameter*** que você informar ao `Annotated` é o **tipo de fato**. O resto é apenas metadado para outras ferramentas.

Por hora, você precisa apenas saber que o `Annotated` existe, e que ele é Python padrão. 😎

Mais tarde você verá o quão **poderoso** ele pode ser.

/// tip | Dica

O fato de que isso é **Python padrão** significa que você ainda obtém a **melhor experiência de desenvolvedor possível** no seu editor, com as ferramentas que você utiliza para analisar e refatorar o seu código, etc. ✨

E também que o seu código será muito compatível com diversas outras ferramentas e bibliotecas Python. 🚀

///

## Type hints no **FastAPI** { #type-hints-in-fastapi }

O **FastAPI** aproveita esses type hints para fazer várias coisas.

Com o **FastAPI**, você declara parâmetros com type hints e obtém:

* **Suporte ao editor**.
* **Verificações de tipo**.

... e o **FastAPI** usa as mesmas declarações para:

* **Definir requisitos**: dos parâmetros de path da request, parâmetros da query, cabeçalhos, corpos, dependências, etc.
* **Converter dados**: da request para o tipo necessário.
* **Validar dados**: provenientes de cada request:
    * Gerando **erros automáticos** retornados ao cliente quando os dados são inválidos.
* **Documentar** a API usando OpenAPI:
    * que é usada pelas interfaces de usuário da documentação interativa automática.

Tudo isso pode parecer abstrato. Não se preocupe. Você verá tudo isso em ação no [Tutorial - Guia do usuário](tutorial/index.md).

O importante é que, usando tipos padrão de Python, em um único local (em vez de adicionar mais classes, decoradores, etc.), o **FastAPI** fará muito trabalho para você.

/// info | Informação

Se você já passou por todo o tutorial e voltou para ver mais sobre os tipos, um bom recurso é [a "cheat sheet" do `mypy`](https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html).

///
