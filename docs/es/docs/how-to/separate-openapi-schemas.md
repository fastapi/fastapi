# Separación de Esquemas OpenAPI para Entrada y Salida o No { #separate-openapi-schemas-for-input-and-output-or-not }

Desde que se lanzó **Pydantic v2**, el OpenAPI generado es un poco más exacto y **correcto** que antes. 😎

De hecho, en algunos casos, incluso tendrá **dos JSON Schemas** en OpenAPI para el mismo modelo Pydantic, para entrada y salida, dependiendo de si tienen **valores por defecto**.

Veamos cómo funciona eso y cómo cambiarlo si necesitas hacerlo.

## Modelos Pydantic para Entrada y Salida { #pydantic-models-for-input-and-output }

Digamos que tienes un modelo Pydantic con valores por defecto, como este:

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:7] hl[7] *}

### Modelo para Entrada { #model-for-input }

Si usas este modelo como entrada, como aquí:

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:15] hl[14] *}

...entonces el campo `description` **no será requerido**. Porque tiene un valor por defecto de `None`.

### Modelo de Entrada en la Documentación { #input-model-in-docs }

Puedes confirmar eso en la documentación, el campo `description` no tiene un **asterisco rojo**, no está marcado como requerido:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image01.png">
</div>

### Modelo para Salida { #model-for-output }

Pero si usas el mismo modelo como salida, como aquí:

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py hl[19] *}

...entonces, porque `description` tiene un valor por defecto, si **no devuelves nada** para ese campo, aún tendrá ese **valor por defecto**.

### Modelo para Datos de Response de Salida { #model-for-output-response-data }

Si interactúas con la documentación y revisas el response, aunque el código no agregó nada en uno de los campos `description`, el response JSON contiene el valor por defecto (`null`):

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image02.png">
</div>

Esto significa que **siempre tendrá un valor**, solo que a veces el valor podría ser `None` (o `null` en JSON).

Eso significa que, los clientes que usan tu API no tienen que revisar si el valor existe o no, pueden **asumir que el campo siempre estará allí**, pero solo que en algunos casos tendrá el valor por defecto de `None`.

La forma de describir esto en OpenAPI es marcar ese campo como **requerido**, porque siempre estará allí.

Debido a eso, el JSON Schema para un modelo puede ser diferente dependiendo de si se usa para **entrada o salida**:

* para **entrada** el `description` **no será requerido**
* para **salida** será **requerido** (y posiblemente `None`, o en términos de JSON, `null`)

### Modelo para Salida en la Documentación { #model-for-output-in-docs }

También puedes revisar el modelo de salida en la documentación, **ambos** `name` y `description` están marcados como **requeridos** con un **asterisco rojo**:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image03.png">
</div>

### Modelo para Entrada y Salida en la Documentación { #model-for-input-and-output-in-docs }

Y si revisas todos los esquemas disponibles (JSON Schemas) en OpenAPI, verás que hay dos, uno `Item-Input` y uno `Item-Output`.

Para `Item-Input`, `description` **no es requerido**, no tiene un asterisco rojo.

Pero para `Item-Output`, `description` **es requerido**, tiene un asterisco rojo.

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image04.png">
</div>

Con esta funcionalidad de **Pydantic v2**, la documentación de tu API es más **precisa**, y si tienes clientes y SDKs autogenerados, también serán más precisos, con una mejor **experiencia para desarrolladores** y consistencia. 🎉

## No Separar Esquemas { #do-not-separate-schemas }

Ahora, hay algunos casos donde podrías querer tener el **mismo esquema para entrada y salida**.

Probablemente el caso principal para esto es si ya tienes algún código cliente/SDKs autogenerado y no quieres actualizar todo el código cliente/SDKs autogenerado aún, probablemente querrás hacerlo en algún momento, pero tal vez no ahora.

En ese caso, puedes desactivar esta funcionalidad en **FastAPI**, con el parámetro `separate_input_output_schemas=False`.

/// note | Nota

El soporte para `separate_input_output_schemas` fue agregado en FastAPI `0.102.0`. 🤓

///

{* ../../docs_src/separate_openapi_schemas/tutorial002_py310.py hl[10] *}

### Mismo Esquema para Modelos de Entrada y Salida en la Documentación { #same-schema-for-input-and-output-models-in-docs }

Y ahora habrá un único esquema para entrada y salida para el modelo, solo `Item`, y tendrá `description` como **no requerido**:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image05.png">
</div>
