# Classes como Dependências { #classes-as-dependencies }

Antes de nos aprofundarmos no sistema de **Injeção de Dependência**, vamos melhorar o exemplo anterior.

## `dict` do exemplo anterior { #a-dict-from-the-previous-example }

No exemplo anterior, nós retornávamos um `dict` da nossa dependência ("injetável"):

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[9] *}

Mas assim obtemos um `dict` como valor do parâmetro `commons` na *função de operação de rota*.

E sabemos que editores de texto não têm como oferecer muitas funcionalidades (como sugestões automáticas) para objetos do tipo `dict`, por que não há como eles saberem o tipo das chaves e dos valores.

Podemos fazer melhor...

## O que caracteriza uma dependência { #what-makes-a-dependency }

Até agora você apenas viu dependências declaradas como funções.

Mas essa não é a única forma de declarar dependências (mesmo que provavelmente seja a mais comum).

O fator principal para uma dependência é que ela deve ser "chamável"

Um objeto "chamável" em Python é qualquer coisa que o Python possa "chamar" como uma função

Então se você tiver um objeto `alguma_coisa` (que pode *não* ser uma função) que você possa "chamar" (executá-lo) dessa maneira:

```Python
something()
```

ou

```Python
something(some_argument, some_keyword_argument="foo")
```

Então esse objeto é um "chamável".

## Classes como dependências { #classes-as-dependencies_1 }

Você deve ter percebido que para criar um instância de uma classe em Python, a mesma sintaxe é utilizada.

Por exemplo:

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

Nesse caso,  `fluffy` é uma instância da classe `Cat`.

E para criar `fluffy`, você está "chamando" `Cat`.

Então, uma classe Python também é "chamável".

Então, no **FastAPI**, você pode utilizar uma classe Python como uma dependência.

O que o FastAPI realmente verifica, é se a dependência é algo chamável (função, classe, ou outra coisa) e os parâmetros que foram definidos.

Se você passar algo "chamável" como uma dependência do **FastAPI**, o framework irá analisar os parâmetros desse "chamável" e processá-los da mesma forma que os parâmetros de uma *função de operação de rota*. Incluindo as sub-dependências.

Isso também se aplica a objetos chamáveis que não recebem nenhum parâmetro. Da mesma forma que uma *função de operação de rota* sem parâmetros.

Então, podemos mudar o "injetável" na dependência `common_parameters` acima para a classe `CommonQueryParams`:

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[11:15] *}

Observe o método `__init__` usado para criar uma instância da classe:

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[12] *}

...ele possui os mesmos parâmetros que nosso `common_parameters` anterior:

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[8] *}

Esses parâmetros são utilizados pelo **FastAPI** para "definir" a dependência.

Em ambos os casos teremos:

* Um parâmetro de consulta `q` opcional do tipo `str`.
* Um parâmetro de consulta `skip` do tipo `int`, com valor padrão `0`.
* Um parâmetro de consulta `limit` do tipo `int`, com valor padrão `100`.

Os dados serão convertidos, validados, documentados no esquema da OpenAPI e etc nos dois casos.

## Utilizando { #use-it }

Agora você pode declarar sua dependência utilizando essa classe.

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[19] *}

O **FastAPI** chama a classe `CommonQueryParams`. Isso cria uma "instância" dessa classe e é a instância que será passada para o parâmetro `commons` na sua função.

## Anotações de Tipo vs `Depends` { #type-annotation-vs-depends }

Perceba como escrevemos `CommonQueryParams` duas vezes no código abaixo:

//// tab | Python 3.8+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

O último `CommonQueryParams`, em:

```Python
... Depends(CommonQueryParams)
```

...é o que o **FastAPI** irá realmente usar para saber qual é a dependência.

É a partir dele que o FastAPI irá extrair os parâmetros passados e será o que o FastAPI irá realmente chamar.

---

Nesse caso, o primeiro `CommonQueryParams`, em:

//// tab | Python 3.8+

```Python
commons: Annotated[CommonQueryParams, ...
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível.

///

```Python
commons: CommonQueryParams ...
```

////

...não tem nenhum signficado especial para o **FastAPI**. O FastAPI não irá utilizá-lo para conversão dos dados, validação, etc (já que ele utiliza `Depends(CommonQueryParams)` para isso).

Na verdade você poderia escrever apenas:

//// tab | Python 3.8+

```Python
commons: Annotated[Any, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível.

///

```Python
commons = Depends(CommonQueryParams)
```

////

...como em:

{* ../../docs_src/dependencies/tutorial003_an_py310.py hl[19] *}

Mas declarar o tipo é encorajado por que é a forma que o seu editor de texto sabe o que será passado como valor do parâmetro `commons`, e assim ele pode ajudar com preenchimento automático, verificações de tipo, etc:

<img src="/img/tutorial/dependencies/image02.png">

## Pegando um Atalho { #shortcut }

Mas você pode ver que temos uma repetição do código neste exemplo, escrevendo `CommonQueryParams` duas vezes:

//// tab | Python 3.8+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

O **FastAPI** nos fornece um atalho para esses casos, onde a dependência é *especificamente* uma classe que o **FastAPI** irá "chamar" para criar uma instância da própria classe.

Para esses casos específicos, você pode fazer o seguinte:

Em vez de escrever:

//// tab | Python 3.8+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

...escreva:

//// tab | Python 3.8+

```Python
commons: Annotated[CommonQueryParams, Depends()]
```

////

//// tab | Python 3.8 non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível.

///

```Python
commons: CommonQueryParams = Depends()
```

////

Você declara a dependência como o tipo do parâmetro, e utiliza `Depends()` sem nenhum parâmetro, em vez de ter que escrever a classe *novamente* dentro de `Depends(CommonQueryParams)`.

O mesmo exemplo ficaria então dessa forma:

{* ../../docs_src/dependencies/tutorial004_an_py310.py hl[19] *}

...e o **FastAPI** saberá o que fazer.

/// tip | Dica

Se isso parece mais confuso do que útil, não utilize, você não *precisa* disso.

É apenas um atalho. Por que o **FastAPI** se preocupa em ajudar a minimizar a repetição de código.

///
