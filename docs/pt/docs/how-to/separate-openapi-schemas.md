# Esquemas OpenAPI Separados para Entrada e Saída ou Não { #separate-openapi-schemas-for-input-and-output-or-not }


Desde que o **Pydantic v2** foi lançado, o OpenAPI gerado é um pouco mais exato e **correto** do que antes. 😎

De fato, em alguns casos, ele terá até **dois JSON Schemas** no OpenAPI para o mesmo modelo Pydantic, para entrada e saída, dependendo se eles possuem **valores padrão**.

Vamos ver como isso funciona e como alterar se for necessário.

## Modelos Pydantic para Entrada e Saída { #pydantic-models-for-input-and-output }

Digamos que você tenha um modelo Pydantic com valores padrão, como este:

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:7] hl[7] *}

### Modelo para Entrada { #model-for-input }

Se você usar esse modelo como entrada, como aqui:

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:15] hl[14] *}

... então o campo `description` **não será obrigatório**. Porque ele tem um valor padrão de `None`.

### Modelo de Entrada na Documentação { #input-model-in-docs }

Você pode confirmar que na documentação, o campo `description` não tem um **asterisco vermelho**, não é marcado como obrigatório:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image01.png">
</div>

### Modelo para Saída { #model-for-output }

Mas se você usar o mesmo modelo como saída, como aqui:

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py hl[19] *}

... então, como `description` tem um valor padrão, se você **não retornar nada** para esse campo, ele ainda terá o **valor padrão**.

### Modelo para Dados de Resposta de Saída { #model-for-output-response-data }

Se você interagir com a documentação e verificar a resposta, mesmo que o código não tenha adicionado nada em um dos campos `description`, a response JSON contém o valor padrão (`null`):

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image02.png">
</div>

Isso significa que ele **sempre terá um valor**, só que às vezes o valor pode ser `None` (ou `null` em termos de JSON).

Isso quer dizer que, os clientes que usam sua API não precisam verificar se o valor existe ou não, eles podem **assumir que o campo sempre estará lá**, mas que em alguns casos terá o valor padrão de `None`.

A maneira de descrever isso no OpenAPI é marcar esse campo como **obrigatório**, porque ele sempre estará lá.

Por causa disso, o JSON Schema para um modelo pode ser diferente dependendo se ele é usado para **entrada ou saída**:

* para **entrada**, o `description` **não será obrigatório**
* para **saída**, ele será **obrigatório** (e possivelmente `None`, ou em termos de JSON, `null`)

### Modelo para Saída na Documentação { #model-for-output-in-docs }

Você pode verificar o modelo de saída na documentação também, **ambos** `name` e `description` são marcados como **obrigatórios** com um **asterisco vermelho**:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image03.png">
</div>

### Modelo para Entrada e Saída na Documentação { #model-for-input-and-output-in-docs }

E se você verificar todos os Schemas disponíveis (JSON Schemas) no OpenAPI, verá que há dois, um `Item-Input` e um `Item-Output`.

Para `Item-Input`, `description` **não é obrigatório**, não tem um asterisco vermelho.

Mas para `Item-Output`, `description` **é obrigatório**, tem um asterisco vermelho.

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image04.png">
</div>

Com esse recurso do **Pydantic v2**, sua documentação da API fica mais **precisa**, e se você tiver clientes e SDKs gerados automaticamente, eles serão mais precisos também, proporcionando uma melhor **experiência para desenvolvedores** e consistência. 🎉

## Não Separe Schemas { #do-not-separate-schemas }

Agora, há alguns casos em que você pode querer ter o **mesmo esquema para entrada e saída**.

Provavelmente, o principal caso de uso para isso é se você já tem algum código de cliente/SDKs gerado automaticamente e não quer atualizar todo o código de cliente/SDKs gerado ainda, você provavelmente vai querer fazer isso em algum momento, mas talvez não agora.

Nesse caso, você pode desativar esse recurso no **FastAPI**, com o parâmetro `separate_input_output_schemas=False`.

/// note | Nota

O suporte para `separate_input_output_schemas` foi adicionado no FastAPI `0.102.0`. 🤓

///

{* ../../docs_src/separate_openapi_schemas/tutorial002_py310.py hl[10] *}

### Mesmo Esquema para Modelos de Entrada e Saída na Documentação { #same-schema-for-input-and-output-models-in-docs }

E agora haverá um único esquema para entrada e saída para o modelo, apenas `Item`, e ele terá `description` como **não obrigatório**:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image05.png">
</div>
