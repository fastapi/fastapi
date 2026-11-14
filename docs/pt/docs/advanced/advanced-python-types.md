# Tipos Avançados de Python { #advanced-python-types }

Aqui estão algumas ideias adicionais que podem ser úteis ao trabalhar com tipos em Python.

## Usando `Union` ou `Optional` { #using-union-or-optional }

Se, por algum motivo, seu código não puder usar `|`, por exemplo, se não for em uma anotação de tipo, mas em algo como `response_model=`, em vez de usar a barra vertical (`|`) você pode usar `Union` do `typing`.

Por exemplo, você poderia declarar que algo pode ser `str` ou `None`:

```python
from typing import Union


def say_hi(name: Union[str, None]):
    print(f"Hi {name}!")
```

O `typing` também tem um atalho para declarar que algo pode ser `None`, com `Optional`.

Aqui vai uma dica do meu ponto de vista bem **subjetivo**:

* 🚨 Evite usar `Optional[SomeType]`
* Em vez disso ✨ **use `Union[SomeType, None]`** ✨.

Ambos são equivalentes e, por baixo, são a mesma coisa, mas eu recomendaria `Union` em vez de `Optional` porque a palavra "**opcional**" sugere que o valor é opcional; na verdade, significa "pode ser `None`", mesmo quando não é opcional e continua sendo obrigatório.

Acho que `Union[SomeType, None]` é mais explícito quanto ao significado.

É apenas uma questão de palavras e nomes. Mas essas palavras podem influenciar como você e sua equipe pensam sobre o código.

Como exemplo, veja esta função:

```python
from typing import Optional


def say_hi(name: Optional[str]):
    print(f"Hey {name}!")
```

O parâmetro `name` é definido como `Optional[str]`, mas **não é opcional**; não é possível chamar a função sem o parâmetro:

```Python
say_hi()  # Ah, não, isso gera um erro! 😱
```

O parâmetro `name` **continua obrigatório** (não é *opcional*) porque não tem valor padrão. Ainda assim, `name` aceita `None` como valor:

```Python
say_hi(name=None)  # Isso funciona, None é válido 🎉
```

A boa notícia é que, na maioria dos casos, você poderá simplesmente usar `|` para definir uniões de tipos:

```python
def say_hi(name: str | None):
    print(f"Hey {name}!")
```

Então, normalmente você não precisa se preocupar com nomes como `Optional` e `Union`. 😎
