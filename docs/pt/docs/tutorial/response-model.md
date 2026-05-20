# Modelo de resposta - Tipo de retorno { #response-model-return-type }

Você pode declarar o tipo usado para a resposta anotando o **tipo de retorno** da *função de operação de rota*.

Você pode usar **anotações de tipo** da mesma forma que usaria para dados de entrada em **parâmetros** de função, você pode usar modelos Pydantic, listas, dicionários, valores escalares como inteiros, booleanos, etc.

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

O FastAPI usará este tipo de retorno para:

* **Validar** os dados retornados.
    * Se os dados forem inválidos (por exemplo, se estiver faltando um campo), significa que o código do *seu* aplicativo está quebrado, não retornando o que deveria, e retornará um erro de servidor em vez de retornar dados incorretos. Dessa forma, você e seus clientes podem ter certeza de que receberão os dados e o formato de dados esperados.
* Adicionar um **JSON Schema** para a resposta, na *operação de rota* do OpenAPI.
    * Isso será usado pela **documentação automática**.
    * Também será usado por ferramentas de geração automática de código do cliente.
* **Serializar** os dados retornados para JSON usando Pydantic, que é escrito em **Rust**, então será **muito mais rápido**.

Mas o mais importante:

* Ele **limitará e filtrará** os dados de saída para o que está definido no tipo de retorno.
    * Isso é particularmente importante para a **segurança**, veremos mais sobre isso abaixo.

## Parâmetro `response_model` { #response-model-parameter }

Existem alguns casos em que você precisa ou deseja retornar alguns dados que não são exatamente o que o tipo declara.

Por exemplo, você pode querer **retornar um dicionário** ou um objeto de banco de dados, mas **declará-lo como um modelo Pydantic**. Dessa forma, o modelo Pydantic faria toda a documentação de dados, validação, etc. para o objeto que você retornou (por exemplo, um dicionário ou objeto de banco de dados).

Se você adicionasse a anotação do tipo de retorno, ferramentas e editores reclamariam com um erro (correto) informando que sua função está retornando um tipo (por exemplo, um dict) diferente do que você declarou (por exemplo, um modelo Pydantic).

Nesses casos, você pode usar o parâmetro `response_model` do *decorador de operação de rota* em vez do tipo de retorno.

Você pode usar o parâmetro `response_model` em qualquer uma das *operações de rota*:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* etc.

{* ../../docs_src/response_model/tutorial001_py310.py hl[17,22,24:27] *}

/// note | Nota

Observe que `response_model` é um parâmetro do método "decorator" (`get`, `post`, etc). Não da sua *função de operação de rota*, como todos os parâmetros e corpo.

///

`response_model` recebe o mesmo tipo que você declararia para um campo de modelo Pydantic, então, pode ser um modelo Pydantic, mas também pode ser, por exemplo, uma `list` de modelos Pydantic, como `List[Item]`.

O FastAPI usará este `response_model` para fazer toda a documentação de dados, validação, etc. e também para **converter e filtrar os dados de saída** para sua declaração de tipo.

/// tip | Dica

Se você tiver verificações de tipo rigorosas em seu editor, mypy, etc, você pode declarar o tipo de retorno da função como `Any`.

Dessa forma, você diz ao editor que está retornando qualquer coisa intencionalmente. Mas o FastAPI ainda fará a documentação de dados, validação, filtragem, etc. com o `response_model`.

///

### Prioridade `response_model` { #response-model-priority }

Se você declarar tanto um tipo de retorno quanto um `response_model`, o `response_model` terá prioridade e será usado pelo FastAPI.

Dessa forma, você pode adicionar anotações de tipo corretas às suas funções, mesmo quando estiver retornando um tipo diferente do modelo de resposta, para ser usado pelo editor e ferramentas como mypy. E ainda assim você pode fazer com que o FastAPI faça a validação de dados, documentação, etc. usando o `response_model`.

Você também pode usar `response_model=None` para desabilitar a criação de um modelo de resposta para essa *operação de rota*, você pode precisar fazer isso se estiver adicionando anotações de tipo para coisas que não são campos Pydantic válidos, você verá um exemplo disso em uma das seções abaixo.

## Retorne os mesmos dados de entrada { #return-the-same-input-data }

Aqui estamos declarando um modelo `UserIn`, ele conterá uma senha em texto simples:

{* ../../docs_src/response_model/tutorial002_py310.py hl[7,9] *}

/// info | Informação

Para usar `EmailStr`, primeiro instale [`email-validator`](https://github.com/JoshData/python-email-validator).

Certifique-se de criar um [ambiente virtual](../virtual-environments.md), ative-o e então instale-o, por exemplo:

```console
$ pip install email-validator
```

ou com:

```console
$ pip install "pydantic[email]"
```

///

E estamos usando este modelo para declarar nossa entrada e o mesmo modelo para declarar nossa saída:

{* ../../docs_src/response_model/tutorial002_py310.py hl[16] *}

Agora, sempre que um navegador estiver criando um usuário com uma senha, a API retornará a mesma senha na resposta.

Neste caso, pode não ser um problema, porque é o mesmo usuário enviando a senha.

Mas se usarmos o mesmo modelo para outra *operação de rota*, poderíamos estar enviando as senhas dos nossos usuários para todos os clientes.

/// danger | Cuidado

Nunca armazene a senha simples de um usuário ou envie-a em uma resposta como esta, a menos que você saiba todas as ressalvas e saiba o que está fazendo.

///

## Adicione um modelo de saída { #add-an-output-model }

Podemos, em vez disso, criar um modelo de entrada com a senha em texto simples e um modelo de saída sem ela:

{* ../../docs_src/response_model/tutorial003_py310.py hl[9,11,16] *}

Aqui, embora nossa *função de operação de rota* esteja retornando o mesmo usuário de entrada que contém a senha:

{* ../../docs_src/response_model/tutorial003_py310.py hl[24] *}

...declaramos o `response_model` como nosso modelo `UserOut`, que não inclui a senha:

{* ../../docs_src/response_model/tutorial003_py310.py hl[22] *}

Então, **FastAPI** cuidará de filtrar todos os dados que não são declarados no modelo de saída (usando Pydantic).

### `response_model` ou Tipo de Retorno { #response-model-or-return-type }

Neste caso, como os dois modelos são diferentes, se anotássemos o tipo de retorno da função como `UserOut`, o editor e as ferramentas reclamariam que estamos retornando um tipo inválido, pois são classes diferentes.

É por isso que neste exemplo temos que declará-lo no parâmetro `response_model`.

...mas continue lendo abaixo para ver como superar isso.

## Tipo de Retorno e Filtragem de Dados { #return-type-and-data-filtering }

Vamos continuar do exemplo anterior. Queríamos **anotar a função com um tipo**, mas queríamos poder retornar da função algo que realmente incluísse **mais dados**.

Queremos que o FastAPI continue **filtrando** os dados usando o modelo de resposta. Para que, embora a função retorne mais dados, a resposta inclua apenas os campos declarados no modelo de resposta.

No exemplo anterior, como as classes eram diferentes, tivemos que usar o parâmetro `response_model`. Mas isso também significa que não temos suporte do editor e das ferramentas verificando o tipo de retorno da função.

Mas na maioria dos casos em que precisamos fazer algo assim, queremos que o modelo apenas **filtre/remova** alguns dados como neste exemplo.

E nesses casos, podemos usar classes e herança para aproveitar as **anotações de tipo** de função para obter melhor suporte no editor e nas ferramentas, e ainda obter a **filtragem de dados** FastAPI.

{* ../../docs_src/response_model/tutorial003_01_py310.py hl[7:10,13:14,18] *}

Com isso, temos suporte de ferramentas, de editores e mypy, pois este código está correto em termos de tipos, mas também obtemos a filtragem de dados do FastAPI.

Como isso funciona? Vamos verificar. 🤓

### Anotações de tipo e ferramentas { #type-annotations-and-tooling }

Primeiro, vamos ver como editores, mypy e outras ferramentas veriam isso.

`BaseUser` tem os campos base. Então `UserIn` herda de `BaseUser` e adiciona o campo `password`, então, ele incluirá todos os campos de ambos os modelos.

Anotamos o tipo de retorno da função como `BaseUser`, mas na verdade estamos retornando uma instância `UserIn`.

O editor, mypy e outras ferramentas não reclamarão disso porque, em termos de digitação, `UserIn` é uma subclasse de `BaseUser`, o que significa que é um tipo *válido* quando o que é esperado é qualquer coisa que seja um `BaseUser`.

### Filtragem de dados FastAPI { #fastapi-data-filtering }

Agora, para FastAPI, ele verá o tipo de retorno e garantirá que o que você retornar inclua **apenas** os campos que são declarados no tipo.

O FastAPI faz várias coisas internamente com o Pydantic para garantir que essas mesmas regras de herança de classe não sejam usadas para a filtragem de dados retornados, caso contrário, você pode acabar retornando muito mais dados do que o esperado.

Dessa forma, você pode obter o melhor dos dois mundos: anotações de tipo com **suporte a ferramentas** e **filtragem de dados**.

## Veja na documentação { #see-it-in-the-docs }

Quando você vê a documentação automática, pode verificar se o modelo de entrada e o modelo de saída terão seus próprios esquemas JSON:

<img src="/img/tutorial/response-model/image01.png">

E ambos os modelos serão usados ​​para a documentação interativa da API:

<img src="/img/tutorial/response-model/image02.png">

## Outras anotações de tipo de retorno { #other-return-type-annotations }

Pode haver casos em que você retorna algo que não é um campo Pydantic válido e anota na função, apenas para obter o suporte fornecido pelas ferramentas (o editor, mypy, etc).

### Retorne uma Response diretamente { #return-a-response-directly }

O caso mais comum seria [retornar uma Response diretamente, conforme explicado posteriormente na documentação avançada](../advanced/response-directly.md).

{* ../../docs_src/response_model/tutorial003_02_py310.py hl[8,10:11] *}

Este caso simples é tratado automaticamente pelo FastAPI porque a anotação do tipo de retorno é a classe (ou uma subclasse de) `Response`.

E as ferramentas também ficarão felizes porque `RedirectResponse` e ​​`JSONResponse` são subclasses de `Response`, então a anotação de tipo está correta.

### Anote uma subclasse de Response { #annotate-a-response-subclass }

Você também pode usar uma subclasse de `Response` na anotação de tipo:

{* ../../docs_src/response_model/tutorial003_03_py310.py hl[8:9] *}

Isso também funcionará porque `RedirectResponse` é uma subclasse de `Response`, e o FastAPI tratará automaticamente este caso simples.

### Anotações de Tipo de Retorno Inválido { #invalid-return-type-annotations }

Mas quando você retorna algum outro objeto arbitrário que não é um tipo Pydantic válido (por exemplo, um objeto de banco de dados) e você o anota dessa forma na função, o FastAPI tentará criar um modelo de resposta Pydantic a partir dessa anotação de tipo e falhará.

O mesmo aconteceria se você tivesse algo como uma <dfn title="uma união entre vários tipos significa 'qualquer um desses tipos'.">união</dfn> entre tipos diferentes onde um ou mais deles não são tipos Pydantic válidos, por exemplo, isso falharia 💥:

{* ../../docs_src/response_model/tutorial003_04_py310.py hl[8] *}

...isso falha porque a anotação de tipo não é um tipo Pydantic e não é apenas uma única classe ou subclasse `Response`, é uma união (qualquer uma das duas) entre um `Response` e ​​um `dict`.

### Desative o modelo de resposta { #disable-response-model }

Continuando com o exemplo acima, você pode não querer ter a validação de dados padrão, documentação, filtragem, etc. que é realizada pelo FastAPI.

Mas você pode querer manter a anotação do tipo de retorno na função para obter o suporte de ferramentas como editores e verificadores de tipo (por exemplo, mypy).

Neste caso, você pode desabilitar a geração do modelo de resposta definindo `response_model=None`:

{* ../../docs_src/response_model/tutorial003_05_py310.py hl[7] *}

Isso fará com que o FastAPI pule a geração do modelo de resposta e, dessa forma, você pode ter quaisquer anotações de tipo de retorno que precisar sem afetar seu aplicativo FastAPI. 🤓

## Parâmetros de codificação do modelo de resposta { #response-model-encoding-parameters }

Seu modelo de resposta pode ter valores padrão, como:

{* ../../docs_src/response_model/tutorial004_py310.py hl[9,11:12] *}

* `description: Union[str, None] = None` (ou `str | None = None` no Python 3.10) tem um padrão de `None`.
* `tax: float = 10.5` tem um padrão de `10.5`.
* `tags: List[str] = []` tem um padrão de uma lista vazia: `[]`.

mas você pode querer omiti-los do resultado se eles não foram realmente armazenados.

Por exemplo, se você tem modelos com muitos atributos opcionais em um banco de dados NoSQL, mas não quer enviar respostas JSON muito longas cheias de valores padrão.

### Use o parâmetro `response_model_exclude_unset` { #use-the-response-model-exclude-unset-parameter }

Você pode definir o parâmetro `response_model_exclude_unset=True` do *decorador de operação de rota*:

{* ../../docs_src/response_model/tutorial004_py310.py hl[22] *}

e esses valores padrão não serão incluídos na resposta, apenas os valores realmente definidos.

Então, se você enviar uma solicitação para essa *operação de rota* para o item com ID `foo`, a resposta (sem incluir valores padrão) será:

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

/// info | Informação

Você também pode usar:

* `response_model_exclude_defaults=True`
* `response_model_exclude_none=True`

conforme descrito na [documentação do Pydantic](https://docs.pydantic.dev/1.10/usage/exporting_models/#modeldict) para `exclude_defaults` e `exclude_none`.

///

#### Dados com valores para campos com padrões { #data-with-values-for-fields-with-defaults }

Mas se seus dados tiverem valores para os campos do modelo com valores padrões, como o item com ID `bar`:

```Python hl_lines="3  5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```

eles serão incluídos na resposta.

#### Dados com os mesmos valores que os padrões { #data-with-the-same-values-as-the-defaults }

Se os dados tiverem os mesmos valores que os padrões, como o item com ID `baz`:

```Python hl_lines="3  5-6"
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```

O FastAPI é inteligente o suficiente (na verdade, o Pydantic é inteligente o suficiente) para perceber que, embora `description`, `tax` e `tags` tenham os mesmos valores que os padrões, eles foram definidos explícita e diretamente (em vez de retirados dos padrões).

Portanto, eles serão incluídos na resposta JSON.

/// tip | Dica

Observe que os valores padrão podem ser qualquer coisa, não apenas `None`.

Eles podem ser uma lista (`[]`), um `float` de `10.5`, etc.

///

### `response_model_include` e `response_model_exclude` { #response-model-include-and-response-model-exclude }

Você também pode usar os parâmetros `response_model_include` e `response_model_exclude` do *decorador de operação de rota*.

Eles pegam um `set` de `str` com o nome dos atributos para incluir (omitindo o resto) ou para excluir (incluindo o resto).

Isso pode ser usado como um atalho rápido se você tiver apenas um modelo Pydantic e quiser remover alguns dados da saída.

/// tip | Dica

Mas ainda é recomendado usar as ideias acima, usando várias classes, em vez desses parâmetros.

Isso ocorre porque o JSON Schema gerado no OpenAPI do seu aplicativo (e a documentação) ainda será o único para o modelo completo, mesmo que você use `response_model_include` ou `response_model_exclude` para omitir alguns atributos.

Isso também se aplica ao `response_model_by_alias` que funciona de forma semelhante.

///

{* ../../docs_src/response_model/tutorial005_py310.py hl[29,35] *}

/// tip | Dica

A sintaxe `{"name", "description"}` cria um `set` com esses dois valores.

É equivalente a `set(["name", "description"])`.

///

#### Usando `list`s em vez de `set`s { #using-lists-instead-of-sets }

Se você esquecer de usar um `set` e usar uma `list` ou `tuple` em vez disso, o FastAPI ainda o converterá em um `set` e funcionará corretamente:

{* ../../docs_src/response_model/tutorial006_py310.py hl[29,35] *}

## Recapitulação { #recap }

Use o parâmetro `response_model` do *decorador de operação de rota* para definir modelos de resposta e, especialmente, para garantir que dados privados sejam filtrados.

Use `response_model_exclude_unset` para retornar apenas os valores definidos explicitamente.
