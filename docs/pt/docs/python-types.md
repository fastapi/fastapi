# Introdução aos tipos Python { #python-types-intro }

O Python possui suporte para "dicas de tipo" ou "type hints" (também chamado de "anotações de tipo" ou "type annotations")

Esses **"type hints"** são uma sintaxe especial que permite declarar o <abbr title = "por exemplo: str, int, float, bool">tipo</abbr> de uma variável.

Ao declarar tipos para suas variáveis, editores e ferramentas podem oferecer um melhor suporte.

Este é apenas um **tutorial rápido / atualização** sobre type hints do Python. Ele cobre apenas o mínimo necessário para usá-los com o **FastAPI**... que é realmente muito pouco.

O **FastAPI** é baseado nesses type hints, eles oferecem muitas vantagens e benefícios.

Mas mesmo que você nunca use o **FastAPI**, você se beneficiaria de aprender um pouco sobre eles.

/// note | Nota

Se você é um especialista em Python e já sabe tudo sobre type hints, pule para o próximo capítulo.

///

## Motivação { #motivation }

Vamos começar com um exemplo simples:

{* ../../docs_src/python_types/tutorial001.py *}

A chamada deste programa gera:

```
John Doe
```

A função faz o seguinte:

* Pega um `first_name` e `last_name`.
* Converte a primeira letra de cada uma em maiúsculas com `title()`.
* <abbr title = "Agrupa-os, como um. Com o conteúdo de um após o outro.">Concatena</abbr> com um espaço no meio.

{* ../../docs_src/python_types/tutorial001.py hl[2] *}

### Edite-o { #edit-it }

É um programa muito simples.

Mas agora imagine que você estava escrevendo do zero.

Em algum momento você teria iniciado a definição da função, já tinha os parâmetros prontos...

Mas então você deve chamar "esse método que converte a primeira letra em maiúscula".

Era `upper`? Era `uppercase`? `first_uppercase`? `capitalize`?

Em seguida, tente com o velho amigo do programador, o preenchimento automático do editor.

Você digita o primeiro parâmetro da função, `first_name`, depois um ponto (`.`) e, em seguida, pressiona `Ctrl + Space` para acionar a conclusão.

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

{* ../../docs_src/python_types/tutorial002.py hl[1] *}

Isso não é o mesmo que declarar valores padrão como seria com:

```Python
    first_name="john", last_name="doe"
```

É uma coisa diferente.

Estamos usando dois pontos (`:`), não é igual a (`=`).

E adicionar type hints normalmente não muda o que acontece do que aconteceria sem eles.

Mas agora, imagine que você está novamente no meio da criação dessa função, mas com type hints.

No mesmo ponto, você tenta acionar o preenchimento automático com o `Ctrl+Space` e vê:

<img src="/img/python-types/image02.png">

Com isso, você pode rolar, vendo as opções, até encontrar o que "soa familiar":

<img src="/img/python-types/image03.png">

## Mais motivação { #more-motivation }

Verifique esta função, ela já possui type hints:

{* ../../docs_src/python_types/tutorial003.py hl[1] *}

Como o editor conhece os tipos de variáveis, você não obtém apenas o preenchimento automático, mas também as verificações de erro:

<img src="/img/python-types/image04.png">

Agora você sabe que precisa corrigí-lo, converta `age` em uma string com `str(age)`:

{* ../../docs_src/python_types/tutorial004.py hl[2] *}

## Declarando Tipos { #declaring-types }

Você acabou de ver o local principal para declarar type hints. Como parâmetros de função.

Este também é o principal local em que você os usaria com o **FastAPI**.

### Tipos simples { #simple-types }

Você pode declarar todos os tipos padrão de Python, não apenas `str`.

Você pode usar, por exemplo:

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005.py hl[1] *}

### Tipos genéricos com parâmetros de tipo { #generic-types-with-type-parameters }

Existem algumas estruturas de dados que podem conter outros valores, como `dict`, `list`, `set` e `tuple`. E os valores internos também podem ter seu próprio tipo.

Estes tipos que possuem tipos internos são chamados de tipos "**genéricos**". E é possível declará-los mesmo com os seus tipos internos.

Para declarar esses tipos e os tipos internos, você pode usar o módulo Python padrão `typing`. Ele existe especificamente para suportar esses type hints.

#### Versões mais recentes do Python { #newer-versions-of-python }

A sintaxe utilizando `typing` é **compatível** com todas as versões, desde o Python 3.6 até as últimas, incluindo o Python 3.9, 3.10, etc.

Conforme o Python evolui, **novas versões** chegam com suporte melhorado para esses type annotations, e em muitos casos, você não precisará nem importar e utilizar o módulo `typing` para declarar os type annotations.

Se você pode escolher uma versão mais recente do Python para o seu projeto, você poderá aproveitar isso ao seu favor.

Em todos os documentos existem exemplos compatíveis com cada versão do Python (quando existem diferenças).

Por exemplo, "**Python 3.6+**" significa que é compatível com o Python 3.6 ou superior (incluindo o 3.7, 3.8, 3.9, 3.10, etc). E "**Python 3.9+**" significa que é compatível com o Python 3.9 ou mais recente (incluindo o 3.10, etc).

Se você pode utilizar a **versão mais recente do Python**, utilize os exemplos para as últimas versões. Eles terão as **melhores e mais simples sintaxes**, como por exemplo, "**Python 3.10+**".

#### List { #list }

Por exemplo, vamos definir uma variável para ser uma `list` de `str`.

//// tab | Python 3.9+

Declare uma variável com a mesma sintaxe com dois pontos (`:`)

Como tipo, coloque `list`.

Como a lista é o tipo que contém algum tipo interno, você coloca o tipo dentro de colchetes:

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial006_py39.py!}
```

////

//// tab | Python 3.8+

De `typing`, importe `List` (com o `L` maiúsculo):

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial006.py!}
```

Declare uma variável com a mesma sintaxe com dois pontos (`:`)

Como tipo, coloque o `List` que você importou de `typing`.

Como a lista é o tipo que contém algum tipo interno, você coloca o tipo dentro de colchetes:

```Python hl_lines="4"
{!> ../../docs_src/python_types/tutorial006.py!}
```

////

/// info | Informação

Estes tipos internos dentro dos colchetes são chamados "parâmetros de tipo" (type parameters).

Neste caso, `str` é o parâmetro de tipo passado para `List` (ou `list` no Python 3.9 ou superior).

///

Isso significa: "a variável `items` é uma `list`, e cada um dos itens desta lista é uma `str`".

/// tip | Dica

Se você usa o Python 3.9 ou superior, você não precisa importar `List` de `typing`. Você pode utilizar o mesmo tipo `list` no lugar.

///

Ao fazer isso, seu editor pode fornecer suporte mesmo durante o processamento de itens da lista:

<img src="/img/python-types/image05.png">

Sem tipos, isso é quase impossível de alcançar.

Observe que a variável `item` é um dos elementos da lista `items`.

E, ainda assim, o editor sabe que é um `str` e fornece suporte para isso.

#### Tuple e Set { #tuple-and-set }

Você faria o mesmo para declarar `tuple`s e `set`s:

//// tab | Python 3.9+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial007_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial007.py!}
```

////

Isso significa que:

* A variável `items_t` é uma `tuple` com 3 itens, um `int`, outro `int` e uma `str`.
* A variável `items_s` é um `set`, e cada um de seus itens é do tipo `bytes`.

#### Dict { #dict }

Para definir um `dict`, você passa 2 parâmetros de tipo, separados por vírgulas.

O primeiro parâmetro de tipo é para as chaves do `dict`.

O segundo parâmetro de tipo é para os valores do `dict`:

//// tab | Python 3.9+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial008.py!}
```

////

Isso significa que:

* A variável `prices` é um `dict`:
    * As chaves deste `dict` são do tipo `str` (digamos, o nome de cada item).
    * Os valores deste `dict` são do tipo `float` (digamos, o preço de cada item).

#### Union { #union }

Você pode declarar que uma variável pode ser de qualquer um dentre **diversos tipos**. Por exemplo, um `int` ou um `str`.

No Python 3.6 e superior (incluindo o Python 3.10), você pode utilizar o tipo `Union` de `typing`, e colocar dentro dos colchetes os possíveis tipos aceitáveis.

No Python 3.10 também existe uma **nova sintaxe** onde você pode colocar os possíveis tipos separados por uma <abbr title='também chamado de "bitwise ou operador", mas o significado é irrelevante aqui'>barra vertical (`|`)</abbr>.

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial008b.py!}
```

////

Em ambos os casos, isso significa que `item` poderia ser um `int` ou um `str`.

#### Possivelmente `None` { #possibly-none }

Você pode declarar que um valor pode ter um tipo, como `str`, mas que ele também pode ser `None`.

No Python 3.6 e superior (incluindo o Python 3.10) você pode declará-lo importando e utilizando `Optional` do módulo `typing`.

```Python hl_lines="1  4"
{!../../docs_src/python_types/tutorial009.py!}
```

O uso de `Optional[str]` em vez de apenas `str` permitirá que o editor o ajude a detectar erros, onde você pode estar assumindo que um valor é sempre um `str`, quando na verdade também pode ser `None`.

`Optional[Something]` é na verdade um atalho para `Union[Something, None]`, eles são equivalentes.

Isso também significa que no Python 3.10, você pode utilizar `Something | None`:

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial009.py!}
```

////

//// tab | Python 3.8+ alternativa

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial009b.py!}
```

////

#### Utilizando `Union` ou `Optional` { #using-union-or-optional }

Se você está utilizando uma versão do Python abaixo da 3.10, aqui vai uma dica do meu ponto de vista bem **subjetivo**:

* 🚨 Evite utilizar `Optional[SomeType]`
* No lugar, ✨ **use `Union[SomeType, None]`** ✨.

Ambos são equivalentes, e no final das contas, eles são o mesmo. Mas eu recomendaria o `Union` ao invés de `Optional` porque a palavra **Optional** parece implicar que o valor é opcional, quando na verdade significa "isso pode ser `None`", mesmo que ele não seja opcional e ainda seja obrigatório.

Eu penso que `Union[SomeType, None]` é mais explícito sobre o que ele significa.

Isso é apenas sobre palavras e nomes. Mas estas palavras podem afetar como os seus colegas de trabalho pensam sobre o código.

Por exemplo, vamos pegar esta função:

{* ../../docs_src/python_types/tutorial009c.py hl[1,4] *}

O parâmetro `name` é definido como `Optional[str]`, mas ele **não é opcional**, você não pode chamar a função sem o parâmetro:

```Python
say_hi()  # Oh, no, this throws an error! 😱
```

O parâmetro `name` **ainda é obrigatório** (não *opcional*) porque ele não possui um valor padrão. Mesmo assim, `name` aceita `None` como valor:

```Python
say_hi(name=None)  # This works, None is valid 🎉
```

A boa notícia é, quando você estiver no Python 3.10 você não precisará se preocupar mais com isso, pois você poderá simplesmente utilizar o `|` para definir uniões de tipos:

{* ../../docs_src/python_types/tutorial009c_py310.py hl[1,4] *}

E então você não precisará mais se preocupar com nomes como `Optional` e `Union`. 😎

#### Tipos genéricos { #generic-types }

Esses tipos que usam parâmetros de tipo entre colchetes são chamados **tipos genéricos** ou **genéricos**. Por exemplo:

//// tab | Python 3.10+

Você pode utilizar os mesmos tipos internos como genéricos (com colchetes e tipos dentro):

* `list`
* `tuple`
* `set`
* `dict`

E o mesmo como no Python 3.8, do módulo `typing`:

* `Union`
* `Optional` (o mesmo que com o 3.8)
* ...entre outros.

No Python 3.10, como uma alternativa para a utilização dos genéricos `Union` e `Optional`, você pode usar a <abbr title='também chamado de "bitwise ou operador", mas o significado não é relevante aqui'>barra vertical (`|`)</abbr> para declarar uniões de tipos. Isso é muito melhor e mais simples.

////

//// tab | Python 3.9+

Você pode utilizar os mesmos tipos internos como genéricos (com colchetes e tipos dentro):

* `list`
* `tuple`
* `set`
* `dict`

E o mesmo como no Python 3.8, do módulo `typing`:

* `Union`
* `Optional`
* ...entre outros.

////

//// tab | Python 3.8+

* `List`
* `Tuple`
* `Set`
* `Dict`
* `Union`
* `Optional`
* ...entre outros.

////

### Classes como tipos { #classes-as-types }

Você também pode declarar uma classe como o tipo de uma variável.

Digamos que você tenha uma classe `Person`, com um nome:

{* ../../docs_src/python_types/tutorial010.py hl[1:3] *}

Então você pode declarar que uma variável é do tipo `Person`:

{* ../../docs_src/python_types/tutorial010.py hl[6] *}

E então, novamente, você recebe todo o suporte do editor:

<img src="/img/python-types/image06.png">

Perceba que isso significa que "`one_person` é uma **instância** da classe `Person`".

Isso não significa que "`one_person` é a **classe** chamada `Person`".

## Modelos Pydantic { #pydantic-models }

O <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> é uma biblioteca Python para executar a validação de dados.

Você declara a "forma" dos dados como classes com atributos.

E cada atributo tem um tipo.

Em seguida, você cria uma instância dessa classe com alguns valores e ela os validará, os converterá para o tipo apropriado (se for esse o caso) e fornecerá um objeto com todos os dados.

E você recebe todo o suporte do editor com esse objeto resultante.

Retirado dos documentos oficiais dos Pydantic:

//// tab | Python 3.10+

```Python
{!> ../../docs_src/python_types/tutorial011_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!> ../../docs_src/python_types/tutorial011_py39.py!}
```

////

//// tab | Python 3.8+

```Python
{!> ../../docs_src/python_types/tutorial011.py!}
```

////

/// info | Informação

Para saber mais sobre o <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic, verifique a sua documentação</a>.

///

O **FastAPI** é todo baseado em Pydantic.

Você verá muito mais disso na prática no [Tutorial - Guia do usuário](tutorial/index.md){.internal-link target=_blank}.

/// tip | Dica

O Pydantic tem um comportamento especial quando você usa `Optional` ou `Union[Something, None]` sem um valor padrão. Você pode ler mais sobre isso na documentação do Pydantic sobre <a href="https://docs.pydantic.dev/2.3/usage/models/#required-fields" class="external-link" target="_blank">campos Opcionais Obrigatórios</a>.

///

## Type Hints com Metadados de Anotações { #type-hints-with-metadata-annotations }

O Python possui uma funcionalidade que nos permite incluir **<abbr title="Informação sobre a informação, neste caso, informação sobre o tipo, e.g. uma descrição.">metadados</abbr> adicionais** nos type hints utilizando `Annotated`.

//// tab | Python 3.9+

No Python 3.9, `Annotated` é parte da biblioteca padrão, então você pode importá-lo de `typing`.

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial013_py39.py!}
```

////

//// tab | Python 3.8+

Em versões abaixo do Python 3.9, você importa `Annotated` de `typing_extensions`.

Ele já estará instalado com o **FastAPI**.

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial013.py!}
```

////

O Python em si não faz nada com este `Annotated`. E para editores e outras ferramentas, o tipo ainda é `str`.

Mas você pode utilizar este espaço dentro do `Annotated` para fornecer ao **FastAPI** metadata adicional sobre como você deseja que a sua aplicação se comporte.

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

* **Definir requisitos**: dos parâmetros de rota, parâmetros da consulta, cabeçalhos, corpos, dependências, etc.
* **Converter dados**: da solicitação para o tipo necessário.
* **Validar dados**: provenientes de cada solicitação:
    * Gerando **erros automáticos** retornados ao cliente quando os dados são inválidos.
* **Documentar** a API usando OpenAPI:
    * que é usado pelas interfaces de usuário da documentação interativa automática.

Tudo isso pode parecer abstrato. Não se preocupe. Você verá tudo isso em ação no [Tutorial - Guia do usuário](tutorial/index.md){.internal-link target=_blank}.

O importante é que, usando tipos padrão de Python, em um único local (em vez de adicionar mais classes, decoradores, etc.), o **FastAPI** fará muito trabalho para você.

/// info | Informação

Se você já passou por todo o tutorial e voltou para ver mais sobre os tipos, um bom recurso é <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank"> a "cheat sheet" do `mypy` </a>.

///
