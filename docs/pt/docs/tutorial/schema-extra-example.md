# Declarar dados de exemplo da requisição { #declare-request-example-data }

Você pode declarar exemplos dos dados que sua aplicação pode receber.

Aqui estão várias maneiras de fazer isso.

## Dados extras de JSON Schema em modelos Pydantic { #extra-json-schema-data-in-pydantic-models }

Você pode declarar `examples` para um modelo Pydantic que serão adicionados ao JSON Schema gerado.

//// tab | Pydantic v2

{* ../../docs_src/schema_extra_example/tutorial001_py310.py hl[13:24] *}

////

//// tab | Pydantic v1

{* ../../docs_src/schema_extra_example/tutorial001_pv1_py310.py hl[13:23] *}

////

Essas informações extras serão adicionadas como estão ao **JSON Schema** de saída para esse modelo e serão usadas na documentação da API.

//// tab | Pydantic v2

Na versão 2 do Pydantic, você usaria o atributo `model_config`, que recebe um `dict`, conforme descrito na <a href="https://docs.pydantic.dev/latest/api/config/" class="external-link" target="_blank">documentação do Pydantic: Configuration</a>.

Você pode definir `"json_schema_extra"` com um `dict` contendo quaisquer dados adicionais que você queira que apareçam no JSON Schema gerado, incluindo `examples`.

////

//// tab | Pydantic v1

Na versão 1 do Pydantic, você usaria uma classe interna `Config` e `schema_extra`, conforme descrito na <a href="https://docs.pydantic.dev/1.10/usage/schema/#schema-customization" class="external-link" target="_blank">documentação do Pydantic: Schema customization</a>.

Você pode definir `schema_extra` com um `dict` contendo quaisquer dados adicionais que você queira que apareçam no JSON Schema gerado, incluindo `examples`.

////

/// tip | Dica

Você pode usar a mesma técnica para estender o JSON Schema e adicionar suas próprias informações extras personalizadas.

Por exemplo, você poderia usá-la para adicionar metadados para uma interface de usuário de front-end, etc.

///

/// info | Informação

O OpenAPI 3.1.0 (usado desde o FastAPI 0.99.0) adicionou suporte a `examples`, que faz parte do padrão **JSON Schema**.

Antes disso, ele suportava apenas a palavra‑chave `example` com um único exemplo. Isso ainda é suportado pelo OpenAPI 3.1.0, mas é descontinuado e não faz parte do padrão JSON Schema. Portanto, é recomendado migrar de `example` para `examples`. 🤓

Você pode ler mais no final desta página.

///

## Argumentos adicionais de `Field` { #field-additional-arguments }

Ao usar `Field()` com modelos Pydantic, você também pode declarar `examples` adicionais:

{* ../../docs_src/schema_extra_example/tutorial002_py310.py hl[2,8:11] *}

## `examples` no JSON Schema - OpenAPI { #examples-in-json-schema-openapi }

Ao usar qualquer um de:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

você também pode declarar um grupo de `examples` com informações adicionais que serão adicionadas aos seus **JSON Schemas** dentro do **OpenAPI**.

### `Body` com `examples` { #body-with-examples }

Aqui passamos `examples` contendo um exemplo dos dados esperados em `Body()`:

{* ../../docs_src/schema_extra_example/tutorial003_an_py310.py hl[22:29] *}

### Exemplo na UI da documentação { #example-in-the-docs-ui }

Com qualquer um dos métodos acima, ficaria assim em `/docs`:

<img src="/img/tutorial/body-fields/image01.png">

### `Body` com vários `examples` { #body-with-multiple-examples }

Você também pode, é claro, passar vários `examples`:

{* ../../docs_src/schema_extra_example/tutorial004_an_py310.py hl[23:38] *}

Quando fizer isso, os exemplos farão parte do **JSON Schema** interno para esses dados do body.

No entanto, <abbr title="2023-08-26">no momento em que isto foi escrito</abbr>, o Swagger UI, a ferramenta responsável por exibir a UI da documentação, não suporta mostrar vários exemplos para os dados no **JSON Schema**. Mas leia abaixo para uma solução alternativa.

### `examples` específicos do OpenAPI { #openapi-specific-examples }

Antes do **JSON Schema** suportar `examples`, o OpenAPI já tinha suporte para um campo diferente também chamado `examples`.

Esse `examples` específico do OpenAPI vai em outra seção da especificação. Ele fica nos **detalhes de cada função de operação de rota**, não dentro de cada JSON Schema.

E o Swagger UI tem suportado esse campo `examples` particular há algum tempo. Então, você pode usá-lo para **mostrar** diferentes **exemplos na UI da documentação**.

O formato desse campo `examples` específico do OpenAPI é um `dict` com **vários exemplos** (em vez de uma `list`), cada um com informações extras que também serão adicionadas ao **OpenAPI**.

Isso não vai dentro de cada JSON Schema contido no OpenAPI, vai fora, diretamente na *operação de rota*.

### Usando o parâmetro `openapi_examples` { #using-the-openapi-examples-parameter }

Você pode declarar o `examples` específico do OpenAPI no FastAPI com o parâmetro `openapi_examples` para:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

As chaves do `dict` identificam cada exemplo, e cada valor é outro `dict`.

Cada `dict` de exemplo específico em `examples` pode conter:

* `summary`: Descrição curta do exemplo.
* `description`: Uma descrição longa que pode conter texto em Markdown.
* `value`: Este é o exemplo em si, por exemplo, um `dict`.
* `externalValue`: Alternativa a `value`, uma URL apontando para o exemplo. Embora isso possa não ser suportado por tantas ferramentas quanto `value`.

Você pode usá-lo assim:

{* ../../docs_src/schema_extra_example/tutorial005_an_py310.py hl[23:49] *}

### Exemplos do OpenAPI na UI da documentação { #openapi-examples-in-the-docs-ui }

Com `openapi_examples` adicionado a `Body()`, o `/docs` ficaria assim:

<img src="/img/tutorial/body-fields/image02.png">

## Detalhes Técnicos { #technical-details }

/// tip | Dica

Se você já está usando o **FastAPI** na versão **0.99.0 ou superior**, você provavelmente pode **pular** esses detalhes.

Eles são mais relevantes para versões antigas, antes de o OpenAPI 3.1.0 estar disponível.

Você pode considerar isto uma breve **aula de história** sobre OpenAPI e JSON Schema. 🤓

///

/// warning | Atenção

Estes são detalhes muito técnicos sobre os padrões **JSON Schema** e **OpenAPI**.

Se as ideias acima já funcionam para você, isso pode ser suficiente, e você provavelmente não precisa desses detalhes, sinta-se à vontade para pular.

///

Antes do OpenAPI 3.1.0, o OpenAPI usava uma versão mais antiga e modificada do **JSON Schema**.

O JSON Schema não tinha `examples`, então o OpenAPI adicionou seu próprio campo `example` à sua versão modificada.

O OpenAPI também adicionou os campos `example` e `examples` a outras partes da especificação:

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#parameter-object" class="external-link" target="_blank">`Parameter Object` (na especificação)</a>, usado no FastAPI por:
    * `Path()`
    * `Query()`
    * `Header()`
    * `Cookie()`
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#media-type-object" class="external-link" target="_blank">`Request Body Object`, no campo `content`, no `Media Type Object` (na especificação)</a>, usado no FastAPI por:
    * `Body()`
    * `File()`
    * `Form()`

/// info | Informação

Esse parâmetro antigo `examples` específico do OpenAPI agora é `openapi_examples` desde o FastAPI `0.103.0`.

///

### Campo `examples` do JSON Schema { #json-schemas-examples-field }

Depois, o JSON Schema adicionou um campo <a href="https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5" class="external-link" target="_blank">`examples`</a> em uma nova versão da especificação.

E então o novo OpenAPI 3.1.0 passou a se basear na versão mais recente (JSON Schema 2020-12), que incluiu esse novo campo `examples`.

Agora, esse novo campo `examples` tem precedência sobre o antigo (e customizado) campo único `example`, que agora está descontinuado.

Esse novo campo `examples` no JSON Schema é **apenas uma `list`** de exemplos, não um `dict` com metadados extras como nos outros lugares do OpenAPI (descritos acima).

/// info | Informação

Mesmo após o lançamento do OpenAPI 3.1.0 com essa nova integração mais simples com o JSON Schema, por um tempo o Swagger UI, a ferramenta que fornece a documentação automática, não suportava OpenAPI 3.1.0 (passou a suportar desde a versão 5.0.0 🎉).

Por causa disso, versões do FastAPI anteriores à 0.99.0 ainda usavam versões do OpenAPI inferiores à 3.1.0.

///

### `examples` no Pydantic e no FastAPI { #pydantic-and-fastapi-examples }

Quando você adiciona `examples` dentro de um modelo Pydantic, usando `schema_extra` ou `Field(examples=["something"])`, esse exemplo é adicionado ao **JSON Schema** para esse modelo Pydantic.

E esse **JSON Schema** do modelo Pydantic é incluído no **OpenAPI** da sua API e, então, é usado na UI da documentação.

Em versões do FastAPI anteriores à 0.99.0 (0.99.0 e superiores usam o novo OpenAPI 3.1.0), quando você usava `example` ou `examples` com qualquer uma das outras utilidades (`Query()`, `Body()`, etc.), esses exemplos não eram adicionados ao JSON Schema que descreve esses dados (nem mesmo à versão própria do JSON Schema do OpenAPI), eles eram adicionados diretamente à declaração da *operação de rota* no OpenAPI (fora das partes do OpenAPI que usam o JSON Schema).

Mas agora que o FastAPI 0.99.0 e superiores usam o OpenAPI 3.1.0, que usa o JSON Schema 2020-12, e o Swagger UI 5.0.0 e superiores, tudo é mais consistente e os exemplos são incluídos no JSON Schema.

### Swagger UI e `examples` específicos do OpenAPI { #swagger-ui-and-openapi-specific-examples }

Como o Swagger UI não suportava vários exemplos no JSON Schema (em 2023-08-26), os usuários não tinham uma forma de mostrar vários exemplos na documentação.

Para resolver isso, o FastAPI `0.103.0` **adicionou suporte** para declarar o mesmo antigo campo **específico do OpenAPI** `examples` com o novo parâmetro `openapi_examples`. 🤓

### Resumo { #summary }

Eu costumava dizer que não gostava tanto de história... e olha eu aqui agora dando aulas de "história tech". 😅

Em resumo, **atualize para o FastAPI 0.99.0 ou superior**, e as coisas ficam muito mais **simples, consistentes e intuitivas**, e você não precisa saber todos esses detalhes históricos. 😎
