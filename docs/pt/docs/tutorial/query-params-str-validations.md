# Parâmetros de consulta e validações de string { #query-parameters-and-string-validations }

O **FastAPI** permite declarar informações adicionais e validações para os seus parâmetros.

Vamos usar esta aplicação como exemplo:

{* ../../docs_src/query_params_str_validations/tutorial001_py310.py hl[7] *}

O parâmetro de consulta `q` é do tipo `str | None`, isso significa que é do tipo `str`, mas também pode ser `None`, e de fato, o valor padrão é `None`, então o FastAPI saberá que não é obrigatório.

/// note | Nota

O FastAPI saberá que o valor de `q` não é obrigatório por causa do valor padrão `= None`.

Ter `str | None` permitirá que seu editor lhe ofereça melhor suporte e detecte erros.

///

## Validação adicional { #additional-validation }

Vamos impor que, embora `q` seja opcional, sempre que for fornecido, seu comprimento não exceda 50 caracteres.

### Importe `Query` e `Annotated` { #import-query-and-annotated }

Para isso, primeiro importe:

* `Query` de `fastapi`
* `Annotated` de `typing`

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[1,3] *}

/// info | Informação

O FastAPI adicionou suporte a `Annotated` (e passou a recomendá-lo) na versão 0.95.0.

Se você tiver uma versão mais antiga, teria erros ao tentar usar `Annotated`.

Certifique-se de [Atualizar a versão do FastAPI](../deployment/versions.md#upgrading-the-fastapi-versions) para pelo menos 0.95.1 antes de usar `Annotated`.

///

## Use `Annotated` no tipo do parâmetro `q` { #use-annotated-in-the-type-for-the-q-parameter }

Lembra que eu disse antes que `Annotated` pode ser usado para adicionar metadados aos seus parâmetros na [Introdução aos tipos do Python](../python-types.md#type-hints-with-metadata-annotations)?

Agora é a hora de usá-lo com FastAPI. 🚀

Tínhamos esta anotação de tipo:

```Python
q: str | None = None
```

O que faremos é envolver isso com `Annotated`, para que fique assim:

```Python
q: Annotated[str | None] = None
```

Ambas as versões significam a mesma coisa, `q` é um parâmetro que pode ser `str` ou `None`, e por padrão é `None`.

Agora vamos pular para a parte divertida. 🎉

## Adicione `Query` ao `Annotated` no parâmetro `q` { #add-query-to-annotated-in-the-q-parameter }

Agora que temos esse `Annotated` onde podemos colocar mais informações (neste caso, uma validação adicional), adicione `Query` dentro de `Annotated` e defina o parâmetro `max_length` como `50`:

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[9] *}

Perceba que o valor padrão continua sendo `None`, então o parâmetro ainda é opcional.

Mas agora, com `Query(max_length=50)` dentro de `Annotated`, estamos dizendo ao FastAPI que queremos validação adicional para este valor, queremos que tenha no máximo 50 caracteres. 😎

/// tip | Dica

Aqui estamos usando `Query()` porque este é um parâmetro de consulta. Mais adiante veremos outros como `Path()`, `Body()`, `Header()` e `Cookie()`, que também aceitam os mesmos argumentos que `Query()`.

///

Agora o FastAPI vai:

* Validar os dados garantindo que o comprimento máximo seja de 50 caracteres
* Mostrar um erro claro para o cliente quando os dados não forem válidos
* Documentar o parâmetro na operação de rota do esquema OpenAPI (então ele aparecerá na UI de docs automática)

## Alternativa (antiga): `Query` como valor padrão { #alternative-old-query-as-the-default-value }

Versões anteriores do FastAPI (antes de <dfn title="antes de 2023-03">0.95.0</dfn>) exigiam que você usasse `Query` como valor padrão do seu parâmetro, em vez de colocá-lo em `Annotated`, há uma grande chance de você ver código usando isso por aí, então vou explicar.

/// tip | Dica

Para código novo e sempre que possível, use `Annotated` como explicado acima. Há múltiplas vantagens (explicadas abaixo) e nenhuma desvantagem. 🍰

///

É assim que você usaria `Query()` como valor padrão do parâmetro da sua função, definindo o parâmetro `max_length` como 50:

{* ../../docs_src/query_params_str_validations/tutorial002_py310.py hl[7] *}

Como neste caso (sem usar `Annotated`) temos que substituir o valor padrão `None` na função por `Query()`, agora precisamos definir o valor padrão com o parâmetro `Query(default=None)`, ele serve ao mesmo propósito de definir esse valor padrão (pelo menos para o FastAPI).

Então:

```Python
q: str | None = Query(default=None)
```

...torna o parâmetro opcional, com um valor padrão de `None`, o mesmo que:


```Python
q: str | None = None
```

Mas a versão com `Query` o declara explicitamente como sendo um parâmetro de consulta.

Então, podemos passar mais parâmetros para `Query`. Neste caso, o parâmetro `max_length` que se aplica a strings:

```Python
q: str | None = Query(default=None, max_length=50)
```

Isso validará os dados, mostrará um erro claro quando os dados não forem válidos e documentará o parâmetro na operação de rota do esquema OpenAPI.

### `Query` como valor padrão ou em `Annotated` { #query-as-the-default-value-or-in-annotated }

Tenha em mente que, ao usar `Query` dentro de `Annotated`, você não pode usar o parâmetro `default` de `Query`.

Em vez disso, use o valor padrão real do parâmetro da função. Caso contrário, haveria inconsistência.

Por exemplo, isto não é permitido:

```Python
q: Annotated[str, Query(default="rick")] = "morty"
```

...porque não está claro se o valor padrão deveria ser `"rick"` ou `"morty"`.

Então, você usaria (preferencialmente):

```Python
q: Annotated[str, Query()] = "rick"
```

...ou em bases de código mais antigas você encontrará:

```Python
q: str = Query(default="rick")
```

### Vantagens de `Annotated` { #advantages-of-annotated }

Usar `Annotated` é recomendado em vez do valor padrão nos parâmetros da função, é melhor por vários motivos. 🤓

O valor padrão do parâmetro da função é o valor padrão real, isso é mais intuitivo com Python em geral. 😌

Você poderia chamar essa mesma função em outros lugares sem FastAPI, e ela funcionaria como esperado. Se houver um parâmetro obrigatório (sem valor padrão), seu editor vai avisar com um erro, e o Python também reclamará se você executá-la sem passar o parâmetro obrigatório.

Quando você não usa `Annotated` e em vez disso usa o estilo de valor padrão (antigo), se você chamar essa função sem FastAPI em outros lugares, terá que lembrar de passar os argumentos para a função para que funcione corretamente, caso contrário os valores serão diferentes do esperado (por exemplo, `QueryInfo` ou algo parecido em vez de `str`). E seu editor não vai avisar, e o Python também não vai reclamar ao executar a função, apenas quando as operações internas falharem.

Como `Annotated` pode ter mais de uma anotação de metadados, você agora pode até usar a mesma função com outras ferramentas, como o [Typer](https://typer.tiangolo.com/). 🚀

## Adicione mais validações { #add-more-validations }

Você também pode adicionar um parâmetro `min_length`:

{* ../../docs_src/query_params_str_validations/tutorial003_an_py310.py hl[10] *}

## Adicione expressões regulares { #add-regular-expressions }

Você pode definir um `pattern` de <dfn title="Uma expressão regular (regex ou regexp) é uma sequência de caracteres que define um padrão de busca para strings.">expressão regular</dfn> que o parâmetro deve corresponder:

{* ../../docs_src/query_params_str_validations/tutorial004_an_py310.py hl[11] *}

Esse padrão específico de expressão regular verifica se o valor recebido no parâmetro:

* `^`: começa com os caracteres seguintes, não tem caracteres antes.
* `fixedquery`: tem exatamente o valor `fixedquery`.
* `$`: termina ali, não tem mais caracteres depois de `fixedquery`.

Se você se sentir perdido com essas ideias de "expressão regular", não se preocupe. Esse é um assunto difícil para muitas pessoas. Você ainda pode fazer muitas coisas sem precisar de expressões regulares por enquanto.

Agora você sabe que, sempre que precisar delas, pode usá-las no FastAPI.

## Valores padrão { #default-values }

Você pode, claro, usar valores padrão diferentes de `None`.

Digamos que você queira declarar o parâmetro de consulta `q` com `min_length` de `3` e ter um valor padrão de `"fixedquery"`:

{* ../../docs_src/query_params_str_validations/tutorial005_an_py310.py hl[9] *}

/// note | Nota

Ter um valor padrão de qualquer tipo, incluindo `None`, torna o parâmetro opcional (não obrigatório).

///

## Parâmetros obrigatórios { #required-parameters }

Quando não precisamos declarar mais validações ou metadados, podemos tornar o parâmetro de consulta `q` obrigatório simplesmente não declarando um valor padrão, assim:

```Python
q: str
```

em vez de:

```Python
q: str | None = None
```

Mas agora estamos declarando com `Query`, por exemplo assim:

```Python
q: Annotated[str | None, Query(min_length=3)] = None
```

Então, quando você precisa declarar um valor como obrigatório usando `Query`, você pode simplesmente não declarar um valor padrão:

{* ../../docs_src/query_params_str_validations/tutorial006_an_py310.py hl[9] *}

### Obrigatório, pode ser `None` { #required-can-be-none }

Você pode declarar que um parâmetro pode aceitar `None`, mas que ainda assim é obrigatório. Isso forçaria os clientes a enviarem um valor, mesmo que o valor seja `None`.

Para isso, você pode declarar que `None` é um tipo válido, mas simplesmente não declarar um valor padrão:

{* ../../docs_src/query_params_str_validations/tutorial006c_an_py310.py hl[9] *}

## Lista de parâmetros de consulta / múltiplos valores { #query-parameter-list-multiple-values }

Quando você define explicitamente um parâmetro de consulta com `Query`, você também pode declará-lo para receber uma lista de valores, ou seja, receber múltiplos valores.

Por exemplo, para declarar um parâmetro de consulta `q` que pode aparecer várias vezes na URL, você pode escrever:

{* ../../docs_src/query_params_str_validations/tutorial011_an_py310.py hl[9] *}

Então, com uma URL como:

```
http://localhost:8000/items/?q=foo&q=bar
```

você receberia os múltiplos valores dos parâmetros de consulta `q` (`foo` e `bar`) em uma `list` Python dentro da sua função de operação de rota, no parâmetro da função `q`.

Assim, a resposta para essa URL seria:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

/// tip | Dica

Para declarar um parâmetro de consulta com tipo `list`, como no exemplo acima, você precisa usar explicitamente `Query`, caso contrário seria interpretado como um corpo da requisição.

///

A documentação interativa da API será atualizada de acordo, permitindo múltiplos valores:

<img src="/img/tutorial/query-params-str-validations/image02.png">

### Lista de parâmetros de consulta / múltiplos valores com valores padrão { #query-parameter-list-multiple-values-with-defaults }

Você também pode definir uma `list` de valores padrão caso nenhum seja fornecido:

{* ../../docs_src/query_params_str_validations/tutorial012_an_py310.py hl[9] *}

Se você for até:

```
http://localhost:8000/items/
```

o valor padrão de `q` será: `["foo", "bar"]` e sua resposta será:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### Usando apenas `list` { #using-just-list }

Você também pode usar `list` diretamente em vez de `list[str]`:

{* ../../docs_src/query_params_str_validations/tutorial013_an_py310.py hl[9] *}

/// note | Nota

Tenha em mente que, neste caso, o FastAPI não verificará o conteúdo da lista.

Por exemplo, `list[int]` verificaria (and documentaria) que os conteúdos da lista são inteiros. Mas `list` sozinho não.

///

## Declare mais metadados { #declare-more-metadata }

Você pode adicionar mais informações sobre o parâmetro.

Essas informações serão incluídas no OpenAPI gerado e usadas pelas interfaces de documentação e por ferramentas externas.

/// note | Nota

Tenha em mente que ferramentas diferentes podem ter níveis diferentes de suporte ao OpenAPI.

Algumas delas podem ainda não mostrar todas as informações extras declaradas, embora na maioria dos casos a funcionalidade ausente já esteja planejada para desenvolvimento.

///

Você pode adicionar um `title`:

{* ../../docs_src/query_params_str_validations/tutorial007_an_py310.py hl[10] *}

E uma `description`:

{* ../../docs_src/query_params_str_validations/tutorial008_an_py310.py hl[14] *}

## Parâmetros com alias { #alias-parameters }

Imagine que você queira que o parâmetro seja `item-query`.

Assim:

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

Mas `item-query` não é um nome de variável Python válido.

O mais próximo seria `item_query`.

Mas você ainda precisa que seja exatamente `item-query`...

Então você pode declarar um `alias`, e esse alias será usado para encontrar o valor do parâmetro:

{* ../../docs_src/query_params_str_validations/tutorial009_an_py310.py hl[9] *}

## Descontinuando parâmetros { #deprecating-parameters }

Agora digamos que você não gosta mais desse parâmetro.

Você tem que deixá-lo por um tempo, pois há clientes usando-o, mas quer que a documentação mostre claramente que ele está <dfn title="obsoleto, recomenda-se não usá-lo">descontinuado</dfn>.

Então passe o parâmetro `deprecated=True` para `Query`:

{* ../../docs_src/query_params_str_validations/tutorial010_an_py310.py hl[19] *}

A documentação vai mostrar assim:

<img src="/img/tutorial/query-params-str-validations/image01.png">

## Excluir parâmetros do OpenAPI { #exclude-parameters-from-openapi }

Para excluir um parâmetro de consulta do OpenAPI gerado (e portanto, dos sistemas de documentação automáticos), defina o parâmetro `include_in_schema` de `Query` como `False`:

{* ../../docs_src/query_params_str_validations/tutorial014_an_py310.py hl[10] *}

## Validação personalizada { #custom-validation }

Podem existir casos em que você precise fazer alguma validação personalizada que não pode ser feita com os parâmetros mostrados acima.

Nesses casos, você pode usar uma função validadora personalizada que é aplicada após a validação normal (por exemplo, depois de validar que o valor é uma `str`).

Você pode fazer isso usando o [`AfterValidator` do Pydantic](https://docs.pydantic.dev/latest/concepts/validators/#field-after-validator) dentro de `Annotated`.

/// tip | Dica

O Pydantic também tem [`BeforeValidator`](https://docs.pydantic.dev/latest/concepts/validators/#field-before-validator) e outros. 🤓

///

Por exemplo, este validador personalizado verifica se o ID do item começa com `isbn-` para um número de livro <abbr title="International Standard Book Number - Número Padrão Internacional de Livro">ISBN</abbr> ou com `imdb-` para um ID de URL de filme <abbr title="Internet Movie Database - Base de Dados de Filmes da Internet: um site com informações sobre filmes">IMDB</abbr>:

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py hl[5,16:19,24] *}

/// info | Informação

Isso está disponível com a versão 2 do Pydantic ou superior. 😎

///

/// tip | Dica

Se você precisar fazer qualquer tipo de validação que exija comunicação com algum componente externo, como um banco de dados ou outra API, você deveria usar Dependências do FastAPI em vez disso; você aprenderá sobre elas mais adiante.

Esses validadores personalizados são para coisas que podem ser verificadas apenas com os mesmos dados fornecidos na requisição.

///

### Entenda esse código { #understand-that-code }

O ponto importante é apenas usar `AfterValidator` com uma função dentro de `Annotated`. Sinta-se à vontade para pular esta parte. 🤸

---

Mas se você estiver curioso sobre este exemplo de código específico e ainda entretido, aqui vão alguns detalhes extras.

#### String com `value.startswith()` { #string-with-value-startswith }

Percebeu? Uma string usando `value.startswith()` pode receber uma tupla, e verificará cada valor na tupla:

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[16:19] hl[17] *}

#### Um item aleatório { #a-random-item }

Com `data.items()` obtemos um <dfn title="Algo que podemos iterar com um laço for, como uma list, set, etc.">objeto iterável</dfn> com tuplas contendo a chave e o valor de cada item do dicionário.

Convertimos esse objeto iterável em uma `list` adequada com `list(data.items())`.

Em seguida, com `random.choice()` podemos obter um valor aleatório da lista, então obtemos uma tupla com `(id, name)`. Será algo como `("imdb-tt0371724", "The Hitchhiker's Guide to the Galaxy")`.

Depois atribuímos esses dois valores da tupla às variáveis `id` e `name`.

Assim, se o usuário não fornecer um ID de item, ele ainda receberá uma sugestão aleatória.

...fazemos tudo isso em uma única linha simples. 🤯 Você não ama Python? 🐍

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[22:30] hl[29] *}

## Recapitulando { #recap }

Você pode declarar validações adicionais e metadados para seus parâmetros.

Validações e metadados genéricos:

* `alias`
* `title`
* `description`
* `deprecated`

Validações específicas para strings:

* `min_length`
* `max_length`
* `pattern`

Validações personalizadas usando `AfterValidator`.

Nestes exemplos você viu como declarar validações para valores `str`.

Veja os próximos capítulos para aprender a declarar validações para outros tipos, como números.
