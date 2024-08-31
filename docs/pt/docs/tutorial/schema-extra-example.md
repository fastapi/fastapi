# Declare um exemplo dos dados da requisição

Você pode declarar exemplos dos dados que a sua aplicação pode receber.

Aqui estão várias formas de se fazer isso.

## `schema_extra` do Pydantic

Você pode declarar um `example` para um modelo Pydantic usando `Config` e `schema_extra`, conforme descrito em <a href="https://docs.pydantic.dev/latest/concepts/json_schema/#schema-customization" class="external-link" target="_blank">Documentação do Pydantic: Schema customization</a>:

```Python hl_lines="15-23"
{!../../../docs_src/schema_extra_example/tutorial001.py!}
```

Essas informações extras serão adicionadas como se encontram no **JSON Schema** de resposta desse modelo e serão usadas na documentação da API.

/// tip | "Dica"

Você pode usar a mesma técnica para estender o JSON Schema e adicionar suas próprias informações extras de forma personalizada.

Por exemplo, você pode usar isso para adicionar metadados para uma interface de usuário de front-end, etc.

///

## `Field` de argumentos adicionais

Ao usar `Field ()` com modelos Pydantic, você também pode declarar informações extras para o **JSON Schema** passando quaisquer outros argumentos arbitrários para a função.

Você pode usar isso para adicionar um `example` para cada campo:

```Python hl_lines="4  10-13"
{!../../../docs_src/schema_extra_example/tutorial002.py!}
```

/// warning | "Atenção"

Lembre-se de que esses argumentos extras passados ​​não adicionarão nenhuma validação, apenas informações extras, para fins de documentação.

///

## `example` e `examples` no OpenAPI

Ao usar quaisquer dos:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

você também pode declarar um dado `example` ou um grupo de `examples` com informações adicionais que serão adicionadas ao **OpenAPI**.

### `Body` com `example`

Aqui nós passamos um `example` dos dados esperados por `Body()`:

```Python hl_lines="21-26"
{!../../../docs_src/schema_extra_example/tutorial003.py!}
```

### Exemplo na UI da documentação

Com qualquer um dos métodos acima, os `/docs` vão ficar assim:

<img src="/img/tutorial/body-fields/image01.png">

### `Body` com vários `examples`

Alternativamente ao único `example`, você pode passar `examples` usando um `dict` com **vários examples**, cada um com informações extras que serão adicionadas no **OpenAPI** também.

As chaves do `dict` identificam cada exemplo, e cada valor é outro `dict`.

Cada `dict` de exemplo específico em `examples` pode conter:

* `summary`: Pequena descrição do exemplo.
* `description`: Uma descrição longa que pode conter texto em Markdown.
* `value`: O próprio exemplo mostrado, ex: um `dict`.
* `externalValue`: alternativa ao `value`, uma URL apontando para o exemplo. Embora isso possa não ser suportado por tantas ferramentas quanto `value`.

```Python hl_lines="22-48"
{!../../../docs_src/schema_extra_example/tutorial004.py!}
```

### Exemplos na UI da documentação

Com `examples` adicionado a `Body()`, os `/docs` vão ficar assim:

<img src="/img/tutorial/body-fields/image02.png">

## Detalhes técnicos

/// warning | "Atenção"

Esses são detalhes muito técnicos sobre os padrões **JSON Schema** e **OpenAPI**.

Se as ideias explicadas acima já funcionam para você, isso pode ser o suficiente, e você provavelmente não precisa desses detalhes, fique à vontade para pular.

///

Quando você adiciona um exemplo dentro de um modelo Pydantic, usando `schema_extra` ou` Field(example="something") `esse exemplo é adicionado ao **JSON Schema** para esse modelo Pydantic.

E esse **JSON Schema** do modelo Pydantic está incluído no **OpenAPI** da sua API e, em seguida, é usado na UI da documentação.

O **JSON Schema** na verdade não tem um campo `example` nos padrões. Versões recentes do JSON Schema definem um campo <a href="https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5" class="external-link" target="_blank">`examples`</a>, mas o OpenAPI 3.0.3 é baseado numa versão mais antiga do JSON Schema que não tinha `examples`.

Por isso, o OpenAPI 3.0.3 definiu o seu próprio <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#fixed-fields-20" class="external-link" target="_blank">`example`</a> para a versão modificada do **JSON Schema** que é usada, para o mesmo próposito (mas é apenas `example` no singular, não `examples`), e é isso que é usado pela UI da documentação da API(usando o Swagger UI).

Portanto, embora `example` não seja parte do JSON Schema, é parte da versão customizada do JSON Schema usada pelo OpenAPI, e é isso que vai ser usado dentro da UI de documentação.

Mas quando você usa `example` ou `examples` com qualquer um dos outros utilitários (`Query()`, `Body()`, etc.) esses exemplos não são adicionados ao JSON Schema que descreve esses dados (nem mesmo para versão própria do OpenAPI do JSON Schema), eles são adicionados diretamente à declaração da *operação de rota* no OpenAPI (fora das partes do OpenAPI que usam o JSON Schema).

Para `Path()`, `Query()`, `Header()`, e `Cookie()`, o `example` e `examples` são adicionados a <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#parameter-object" class="external-link" target="_blank">definição do OpenAPI, dentro do `Parameter Object` (na especificação)</a>.

E para `Body()`, `File()`, e `Form()`, o `example` e `examples` são de maneira equivalente adicionados para a <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#mediaTypeObject" class="external-link" target="_blank">definição do OpenAPI, dentro do `Request Body Object`, no campo `content`, no `Media Type Object` (na especificação)</a>.

Por outro lado, há uma versão mais recente do OpenAPI: **3.1.0**, lançada recentemente. Baseado no JSON Schema mais recente e a maioria das modificações da versão customizada do OpenAPI do JSON Schema são removidas, em troca dos recursos das versões recentes do JSON Schema, portanto, todas essas pequenas diferenças são reduzidas. No entanto, a UI do Swagger atualmente não oferece suporte a OpenAPI 3.1.0, então, por enquanto, é melhor continuar usando as opções acima.
