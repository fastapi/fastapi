# Modelo de Resposta - Tipo de Retorno

Você pode declarar o tipo usado para a resposta anotando a *função de operação de caminho* **tipo de retorno**.

Você pode usar **anotações de tipo** da mesma forma que você faria para inserir dados em função **parâmetros**, você pode usar modelos Pydantic, listas, dicionários, valores escalares como inteiros, booleanos, etc.

=== "Python 3.6 e superior"

    ```Python hl_lines="18  23"
    {!> ../../../docs_src/response_model/tutorial001_01.py!}
    ```

=== "Python 3.9 e superior"

    ```Python hl_lines="18  23"
    {!> ../../../docs_src/response_model/tutorial001_01_py39.py!}
    ```

=== "Python 3.10 e superior"

    ```Python hl_lines="16  21"
    {!> ../../../docs_src/response_model/tutorial001_01_py310.py!}
    ```

FastAPI usará esse tipo de retorno para:

* **Validar** o retorno do dado.
    * Se o dado for inválido (por exemplo, você esquecendo um campo), isso significa que o *seu* código está quebrado, não retornando o que deveria, e retornará um erro de servidor em vez de retornar dados incorretos. Dessa forma, você e seus clientes podem ter certeza de que receberão os dados e a forma de dados esperada.
* Adicionar um **Esquema JSON** para a resposta, na *operação de caminho* da OpenAPI.
    * Isso será usado pela **documentação automática**.
    * Ele também será usado por ferramentas automáticas de geração de código do cliente.

Mas o mais importante:

* Ele irá **limitar e filtrar** os dados de saída para o que está definido no tipo de retorno.
    * Isso é particularmente importante para **segurança**, veremos mais sobre isso abaixo.

## Parâmetro `response_model`

Existem alguns casos em que você precisa ou deseja retornar alguns dados que não são exatamente o que o tipo declara.

Por exemplo, você pode querer **retornar um dicionário** ou um objeto de banco de dados, mas **declará-lo como um modelo Pydantic**. Desta forma, o modelo Pydantic faria toda a documentação de dados, validação, etc. para o objeto que você retornou (por exemplo, um dicionário ou objeto de banco de dados).

Se você adicionasse a anotação de tipo de retorno, ferramentas e editores reclamariam com um erro (correto) informando que sua função está retornando um tipo (por exemplo, um dict) diferente do que você declarou (por exemplo, um modelo Pydantic).

Nesses casos, você pode usar o parâmetro `response_model` do *decorador de operação de caminho* em vez do tipo de retorno.

Você pode usar o parâmetro `response_model` em qualquer uma das *operações de caminho*:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* etc.

=== "Python 3.6 e superior"

    ```Python hl_lines="17  22  24-27"
    {!> ../../../docs_src/response_model/tutorial001.py!}
    ```

=== "Python 3.9 e superior"

    ```Python hl_lines="17  22  24-27"
    {!> ../../../docs_src/response_model/tutorial001_py39.py!}
    ```

=== "Python 3.10 e superior"

    ```Python hl_lines="17  22  24-27"
    {!> ../../../docs_src/response_model/tutorial001_py310.py!}
    ```

!!! note
    Observe que `response_model` é um parâmetro do método "*decorator*" (`get`, `post`, etc). Não da sua *função de operação de caminho*, como todos os parâmetros e corpo.

`response_model` recebe o mesmo tipo que você declararia para um campo de modelo Pydantic, portanto, pode ser um modelo Pydantic, mas também pode ser, por exemplo um `list` de modelos Pydantic, como `List[Item]`.

FastAPI usará este `response_model` para fazer toda a documentação de dados, validação, etc. e também para **converter e filtrar os dados de saída** para sua declaração de tipo.

!!! tip
    Se você tiver verificações de tipo rígidas em seu editor, mypy, etc, poderá declarar o tipo de retorno da função como `Any`.

    Dessa forma, você diz ao editor que está retornando qualquer coisa intencionalmente. Mas FastAPI ainda fará a documentação de dados, validação, filtragem, etc. com o `response_model`.

### Prioridade do `response_model`

Se você declarar um tipo de retorno e um `response_model`, o `response_model` terá prioridade e será usado pelo FastAPI.

Dessa forma, você pode adicionar anotações de tipo corretas às suas funções, mesmo quando estiver retornando um tipo diferente do modelo de resposta, para ser usado pelo editor e ferramentas como mypy. E você ainda pode fazer com que FastAPI faça a validação de dados, documentação, etc. usando o `response_model`.

## Retornar os mesmos dados de entrada

Aqui estamos declarando um modelo `UserIn`, ele conterá uma senha em texto simples:

=== "Python 3.6 e superior"

    ```Python hl_lines="9  11"
    {!> ../../../docs_src/response_model/tutorial002.py!}
    ```

=== "Python 3.10 e superior"

    ```Python hl_lines="7  9"
    {!> ../../../docs_src/response_model/tutorial002_py310.py!}
    ```

!!! info
    Para usar `EmailStr`, primeiro instale <a href="https://github.com/JoshData/python-email-validator" class="external-link" target="_blank">`email_validator`</a>.

    Por exemplo, com `pip install email-validator`
    ou `pip install pydantic[email]`.

E estamos usando este modelo para declarar nossa entrada e o mesmo modelo para declarar nossa saída:

=== "Python 3.6 e superior"

    ```Python hl_lines="18"
    {!> ../../../docs_src/response_model/tutorial002.py!}
    ```

=== "Python 3.10 e superior"

    ```Python hl_lines="16"
    {!> ../../../docs_src/response_model/tutorial002_py310.py!}
    ```

Agora, sempre que um navegador estiver criando um usuário com uma senha, a API retornará a mesma senha na resposta.

Nesse caso, pode não ser um problema, pois é o mesmo usuário que está enviando a senha.

Mas se usarmos o mesmo modelo para outra *operação de caminho*, poderíamos estar enviando as senhas de nossos usuários para todos os clientes.

!!! danger
    Nunca armazene a senha simples de um usuário ou envie-a em uma resposta como esta, a menos que você conheça todas as advertências e saiba o que está fazendo.

## Adicionar um modelo de saída

Em vez disso, podemos criar um modelo de entrada com a senha em texto simples e um modelo de saída sem ela:

=== "Python 3.6 e superior"

    ```Python hl_lines="9  11  16"
    {!> ../../../docs_src/response_model/tutorial003.py!}
    ```

=== "Python 3.10 e superior"

    ```Python hl_lines="9  11  16"
    {!> ../../../docs_src/response_model/tutorial003_py310.py!}
    ```

Aqui, mesmo que nossa *função de operação de caminho* esteja retornando o mesmo usuário de entrada que contém a senha:

=== "Python 3.6 e superior"

    ```Python hl_lines="24"
    {!> ../../../docs_src/response_model/tutorial003.py!}
    ```

=== "Python 3.10 e superior"

    ```Python hl_lines="24"
    {!> ../../../docs_src/response_model/tutorial003_py310.py!}
    ```

...we declared the `response_model` to be our model `UserOut`, that doesn't include the password:

=== "Python 3.6 e superior"

    ```Python hl_lines="22"
    {!> ../../../docs_src/response_model/tutorial003.py!}
    ```

=== "Python 3.10 e superior"

    ```Python hl_lines="22"
    {!> ../../../docs_src/response_model/tutorial003_py310.py!}
    ```

Portanto, **FastAPI** cuidará de filtrar todos os dados que não forem declarados no modelo de saída (usando Pydantic).

### `response_model` ou Tipo de Retorno

Neste caso, como os dois modelos são diferentes, se anotarmos o tipo de retorno da função como `UserOut`, o editor e as ferramentas reclamariam que estamos retornando um tipo inválido, pois são classes diferentes.

É por isso que neste exemplo temos que declarar no parâmetro `response_model`.

...mas continue lendo abaixo para ver como superar isso.

## Tipo de Retorno e Filtragem de Dados


Vamos continuar do exemplo anterior. Queríamos **anotar a função com um tipo**, mas retornar algo que incluísse **mais dados**.

Queremos que o FastAPI continue **filtrando** os dados usando o modelo de resposta.

No exemplo anterior, como as classes eram diferentes, tivemos que usar o parâmetro `response_model`. Mas isso também significa que não temos o suporte do editor e das ferramentas que verificam o tipo de retorno da função.

Mas, na maioria dos casos em que precisamos fazer algo assim, queremos que o modelo apenas **filtre/remova** alguns dos dados, como neste exemplo.

E, nesses casos, podemos usar classes e herança para tirar proveito das **anotações de tipo** de função para obter melhor suporte no editor e nas ferramentas e ainda obter a **filtragem de dados** do FastAPI.

=== "Python 3.6 e superior"

    ```Python hl_lines="9-13  15-16  20"
    {!> ../../../docs_src/response_model/tutorial003_01.py!}
    ```

=== "Python 3.10 e superior"

    ```Python hl_lines="7-10  13-14  18"
    {!> ../../../docs_src/response_model/tutorial003_01_py310.py!}
    ```

Com isso, obtemos suporte de ferramentas, de editores e mypy, pois esse código está correto em termos de tipos, mas também obtemos a filtragem de dados do FastAPI.

Como é que isso funciona? Vamos checar. 🤓

### Anotações de Tipo e Ferramentas

Primeiro, vamos ver como os editores, mypy e outras ferramentas veriam isso.

`BaseUser` tem os campos base. Então `UserIn` herda de `BaseUser` e adiciona o campo `password`, então, ele incluirá todos os campos de ambos os modelos.

Anotamos o tipo de retorno da função como `BaseUser`, mas na verdade estamos retornando uma instância `UserIn`.

O editor, mypy e outras ferramentas não reclamarão disso porque, em termos de digitação, `UserIn` é uma subclasse de `BaseUser`, o que significa que é um tipo *válido* quando o esperado é qualquer coisa que seja um `BaseUser `.

### Filtragem de Dados FastAPI

Agora, para FastAPI, ele verá o tipo de retorno e garantirá que o que você retorna inclua **apenas** os campos declarados no tipo.

FastAPI faz várias coisas internamente com Pydantic para garantir que essas mesmas regras de herança de classe não sejam usadas para a filtragem de dados retornados, caso contrário, você pode acabar retornando muito mais dados do que o esperado.

Dessa forma, você pode obter o melhor dos dois mundos: digite anotações com **suporte de ferramentas** e **filtragem de dados**.

## Veja na documentação

Ao ver a documentação automática, você pode verificar se o modelo de entrada e o modelo de saída terão seus próprios esquemas JSON:

<img src="https://fastapi.tiangolo.com/img/tutorial/response-model/image01.png">

E ambos os modelos serão usados para a documentação interativa da API:

<img src="https://fastapi.tiangolo.com/img/tutorial/response-model/image02.png">

## Parâmetros de codificação do Modelo de Resposta

Seu modelo de resposta pode ter valores padrão, como:

=== "Python 3.6 e superior"

    ```Python hl_lines="11  13-14"
    {!> ../../../docs_src/response_model/tutorial004.py!}
    ```

=== "Python 3.9 e superior"

    ```Python hl_lines="11  13-14"
    {!> ../../../docs_src/response_model/tutorial004_py39.py!}
    ```

=== "Python 3.10 e superior"

    ```Python hl_lines="9  11-12"
    {!> ../../../docs_src/response_model/tutorial004_py310.py!}
    ```

* `description: Union[str, None] = None` (ou `str | None = None` no Python 3.10) tem valor padrão de `None`.
* `tax: float = 10.5` tem valor padrão de `10.5`.
* `tags: List[str] = []` tem como valor padrão uma lista vazia: `[]`.

mas você pode querer omiti-los do resultado se eles não foram realmente armazenados.

For example, if you have models with many optional attributes in a NoSQL database, but you don't want to send very long JSON responses full of default values.

### Use o parâmetro `response_model_exclude_unset`

Você pode definir o parâmetro *path operation decorator* `response_model_exclude_unset=True`:

=== "Python 3.6 e superior"

    ```Python hl_lines="24"
    {!> ../../../docs_src/response_model/tutorial004.py!}
    ```

=== "Python 3.9 e superior"

    ```Python hl_lines="24"
    {!> ../../../docs_src/response_model/tutorial004_py39.py!}
    ```

=== "Python 3.10 e superior"

    ```Python hl_lines="22"
    {!> ../../../docs_src/response_model/tutorial004_py310.py!}
    ```

e esses valores padrão não serão incluídos na resposta, apenas os valores realmente definidos.

Portanto, se você enviar uma solicitação para essa *operação de caminho* para o item com ID `foo`, a resposta (sem incluir valores padrão) será:

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

!!! info
    FastAPI usa modelos Pydantic `.dict()` com <a href="https://pydantic-docs.helpmanual.io/usage/exporting_models/#modeldict" class="external-link" target="_blank">seu parâmetro `exclude_unset`</a> para conseguir isso.

!!! info
    Você também pode usar:

    * `response_model_exclude_defaults=True`
    * `response_model_exclude_none=True`

    conforme descrito na <a href="https://pydantic-docs.helpmanual.io/usage/exporting_models/#modeldict" class="external-link" target="_blank">documentação do Pydantic</a> para `exclude_defaults ` e `exclude_none`.

#### Dados com valores para campos com valores padrão

Mas se seus dados tiverem valores para os campos do modelo com valores padrão, como o item com ID `bar`:

```Python hl_lines="3  5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```

eles serão incluídos na resposta.

#### Dados com os mesmos valores que os valores padrão

Se os dados tiverem os mesmos valores que os valores padrão, como o item com ID `baz`:

```Python hl_lines="3  5-6"
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```

FastAPI é inteligente o suficiente (na verdade, Pydantic é inteligente o suficiente) para perceber que, embora `description`, `tax` e `tags` tenham os mesmos valores que os valores padrão, eles foram definidos explicitamente (em vez de retirados dos valores padrão) .

Portanto, eles serão incluídos na resposta JSON.

!!! tip
    Observe que os valores padrão podem ser qualquer coisa, não apenas `None`.

    Eles podem ser uma lista (`[]`), um `float` de `10.5`, etc.

### `response_model_include` and `response_model_exclude`

Você também pode usar os parâmetros do *path operation decorator* `response_model_include` e `response_model_exclude`.

Eles pegam um `conjunto` de `str` com o nome dos atributos a incluir (omitindo o restante) ou a excluir (incluindo o restante).

Isso pode ser usado como um atalho rápido se você tiver apenas um modelo Pydantic e quiser remover alguns dados da saída.

!!! tip
    Mas ainda é recomendável usar as ideias acima, usando várias classes, em vez desses parâmetros.

    Isso ocorre porque o JSON Schema gerado no OpenAPI do seu aplicativo (e os documentos) ainda será o modelo completo, mesmo se você usar `response_model_include` ou `response_model_exclude` para omitir alguns atributos.

    Isso também se aplica a `response_model_by_alias` que funciona de forma semelhante.

=== "Python 3.6 e superior"

    ```Python hl_lines="31  37"
    {!> ../../../docs_src/response_model/tutorial005.py!}
    ```

=== "Python 3.10 e superior"

    ```Python hl_lines="29  35"
    {!> ../../../docs_src/response_model/tutorial005_py310.py!}
    ```

!!! tip
    A sintaxe `{"name", "description"}` cria um `set` com esses dois valores.

    É equivalente a `set(["name", "description"])`.

#### Usando `list`s em vez de `set`s

Se você esquecer de usar um `set` e usar uma `list` ou `tuple`, o FastAPI ainda o converterá em um `set` e funcionará corretamente:

=== "Python 3.6 e superior"

    ```Python hl_lines="31  37"
    {!> ../../../docs_src/response_model/tutorial006.py!}
    ```

=== "Python 3.10 e superior"

    ```Python hl_lines="29  35"
    {!> ../../../docs_src/response_model/tutorial006_py310.py!}
    ```

## Recapitulando

Use o parâmetro `response_model` do *decorador de operação de caminho* para definir modelos de resposta e especialmente para garantir que os dados privados sejam filtrados.

Use `response_model_exclude_unset` para retornar apenas os valores definidos explicitamente.
