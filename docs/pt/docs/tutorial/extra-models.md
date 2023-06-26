# Modelos Adicionais

Continuando com o exemplo anterior, será comum ter mais de um modelo relacionado.

Isso é especialmente o caso para modelos de usuários, porque:

* O **modelo de entrada** precisa ser capaz de ter uma senha.
* O **modelo de saída** não deve ter uma senha.
* O **modelo de banco de dados** provavelmente precisaria ter uma senha criptografada.

!!! danger
    Nunca armazene senhas em texto simples dos usuários. Sempre armazene uma "hash segura" que você pode verificar depois.

    Se não souber, você aprenderá o que é uma "senha hash" nos [capítulos de segurança](security/simple-oauth2.md#password-hashing){.internal-link target=_blank}.

## Múltiplos modelos

Aqui está uma ideia geral de como os modelos poderiam parecer com seus campos de senha e os lugares onde são usados:

=== "Python 3.6 and above"

    ```Python hl_lines="9  11  16  22  24  29-30  33-35  40-41"
    {!> ../../../docs_src/extra_models/tutorial001.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="7  9  14  20  22  27-28  31-33  38-39"
    {!> ../../../docs_src/extra_models/tutorial001_py310.py!}
    ```

### Sobre `**user_in.dict()`

#### O `.dict()` do Pydantic

`user_in` é um modelo Pydantic da classe `UserIn`.

Os modelos Pydantic possuem um método `.dict()` que retorna um `dict` com os dados do modelo.

Então, se criarmos um objeto Pydantic `user_in` como:

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

e depois chamarmos:

```Python
user_dict = user_in.dict()
```

agora temos um `dict` com os dados na variável `user_dict` (é um `dict` em vez de um objeto de modelo Pydantic).

E se chamarmos:

```Python
print(user_dict)
```

teríamos um `dict` Python com:

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### Desembrulhando um `dict`

Se tomarmos um `dict` como `user_dict` e passarmos para uma função (ou classe) com `**user_dict`, o Python irá "desembrulhá-lo". Ele passará as chaves e valores do `user_dict` diretamente como argumentos chave-valor.

Então, continuando com o `user_dict` acima, escrevendo:

```Python
UserInDB(**user_dict)
```

Resultaria em algo equivalente a:

```Python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

Ou mais exatamente, usando `user_dict` diretamente, com qualquer conteúdo que ele possa ter no futuro:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### Um modelo Pydantic a partir do conteúdo de outro

Como no exemplo acima, obtivemos o `user_dict` a partir do `user_in.dict()`, este código:

```Python
user_dict = user_in.dict()
UserInDB(**user_dict)
```

seria equivalente a:

```Python
UserInDB(**user_in.dict())
```

...porque `user_in.dict()` é um `dict`, e depois fazemos o Python "desembrulhá-lo" passando-o para UserInDB precedido por `**`.

Então, obtemos um modelo Pydantic a partir dos dados em outro modelo Pydantic.

#### Desembrulhando um `dict` e palavras-chave extras

E, então, adicionando o argumento de palavra-chave extra `hashed_password=hashed_password`, como em:

```Python
UserInDB(**user_in.dict(), hashed_password=hashed_password)
```

...acaba sendo como:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
```

!!! warning
    As funções adicionais de suporte são apenas para demonstração de um fluxo possível dos dados, mas é claro que elas não fornecem segurança real.

## Reduzir duplicação

Reduzir a duplicação de código é uma das ideias principais no **FastAPI**.

A duplicação de código aumenta as chances de bugs, problemas de segurança, problemas de desincronização de código (quando você atualiza em um lugar, mas não em outros), etc.

E esses modelos estão compartilhando muitos dos dados e duplicando nomes e tipos de atributos.

Nós poderíamos fazer melhor.

Podemos declarar um modelo `UserBase` que serve como base para nossos outros modelos. E então podemos fazer subclasses desse modelo que herdam seus atributos (declarações de tipo, validação, etc.).

Toda conversão de dados, validação, documentação, etc. ainda funcionará normalmente.

Dessa forma, podemos declarar apenas as diferenças entre os modelos (com `password` em texto claro, com `hashed_password` e sem senha):

=== "Python 3.6 and above"

    ```Python hl_lines="9  15-16  19-20  23-24"
    {!> ../../../docs_src/extra_models/tutorial002.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="7  13-14  17-18  21-22"
    {!> ../../../docs_src/extra_models/tutorial002_py310.py!}
    ```

## `Union` ou `anyOf`

Você pode declarar uma resposta como o `Union` de dois tipos, o que significa que a resposta seria qualquer um dos dois.

Isso será definido no OpenAPI com `anyOf`.

Para fazer isso, use a dica de tipo padrão do Python <a href="https://docs.python.org/3/library/typing.html#typing.Union" class="external-link" target="_blank">`typing.Union`</a>:

!!! note
    Ao definir um <a href="https://pydantic-docs.helpmanual.io/usage/types/#unions" class="external-link" target="_blank">`Union`</a>, inclua o tipo mais específico primeiro, seguido pelo tipo menos específico. No exemplo abaixo, o tipo mais específico `PlaneItem` vem antes de `CarItem` em `Union[PlaneItem, CarItem]`.

=== "Python 3.6 and above"

    ```Python hl_lines="1  14-15  18-20  33"
    {!> ../../../docs_src/extra_models/tutorial003.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="1  14-15  18-20  33"
    {!> ../../../docs_src/extra_models/tutorial003_py310.py!}
    ```

### `Union` no Python 3.10

Neste exemplo, passamos `Union[PlaneItem, CarItem]` como o valor do argumento `response_model`.

Dado que estamos passando-o como um **valor para um argumento** em vez de colocá-lo em uma **anotação de tipo**, precisamos usar `Union` mesmo no Python 3.10.

Se estivesse em uma anotação de tipo, poderíamos ter usado a barra vertical, como:

```Python
some_variable: PlaneItem | CarItem
```

Mas se colocarmos isso em `response_model=PlaneItem | CarItem` teríamos um erro, pois o Python tentaria executar uma **operação inválida** entre `PlaneItem` e `CarItem` em vez de interpretar isso como uma anotação de tipo.

## Lista de modelos

Da mesma forma, você pode declarar respostas de listas de objetos.

Para isso, use o padrão Python `typing.List` (ou simplesmente `list` no Python 3.9 e superior):

=== "Python 3.6 and above"

    ```Python hl_lines="1  20"
    {!> ../../../docs_src/extra_models/tutorial004.py!}
    ```

=== "Python 3.9 and above"

    ```Python hl_lines="18"
    {!> ../../../docs_src/extra_models/tutorial004_py39.py!}
    ```

## Resposta com `dict` arbitrário

Você também pode declarar uma resposta usando um simples `dict` arbitrário, declarando apenas o tipo das chaves e valores, sem usar um modelo Pydantic.

Isso é útil se você não souber os nomes de campo / atributo válidos (que seriam necessários para um modelo Pydantic) antecipadamente.

Neste caso, você pode usar `typing.Dict` (ou simplesmente dict no Python 3.9 e superior):

=== "Python 3.6 and above"

    ```Python hl_lines="1  8"
    {!> ../../../docs_src/extra_models/tutorial005.py!}
    ```

=== "Python 3.9 and above"

    ```Python hl_lines="6"
    {!> ../../../docs_src/extra_models/tutorial005_py39.py!}
    ```

## Em resumo

Use vários modelos Pydantic e herde livremente para cada caso.

Não é necessário ter um único modelo de dados por entidade se essa entidade precisar ter diferentes "estados". No caso da "entidade" de usuário com um estado que inclui `password`, `password_hash` e sem senha.
