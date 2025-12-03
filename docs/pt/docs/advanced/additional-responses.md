# Retornos Adicionais no OpenAPI { #additional-responses-in-openapi }

/// warning | Atenção

Este é um tema bem avançado.

Se você está começando com o **FastAPI**, provavelmente você não precisa disso.

///

Você pode declarar retornos adicionais, com códigos de status adicionais, media types, descrições, etc.

Essas respostas adicionais serão incluídas no esquema do OpenAPI, e também aparecerão na documentação da API.

Porém para as respostas adicionais, você deve garantir que está retornando um `Response` como por exemplo o `JSONResponse` diretamente, junto com o código de status e o conteúdo.

## Retorno Adicional com `model` { #additional-response-with-model }

Você pode fornecer o parâmetro `responses` aos seus *decoradores de caminho*.

Este parâmetro recebe um `dict`, as chaves são os códigos de status para cada retorno, como por exemplo `200`, e os valores são um outro `dict` com a informação de cada um deles.

Cada um desses `dict` de retorno pode ter uma chave `model`, contendo um modelo do Pydantic, assim como o `response_model`.

O **FastAPI** pegará este modelo, gerará o esquema JSON dele e incluirá no local correto do OpenAPI.

Por exemplo, para declarar um outro retorno com o status code `404` e um modelo do Pydantic chamado `Message`, você pode escrever:

{* ../../docs_src/additional_responses/tutorial001.py hl[18,22] *}

/// note | Nota

Lembre-se que você deve retornar o `JSONResponse` diretamente.

///

/// info | Informação

A chave `model` não é parte do OpenAPI.

O **FastAPI** pegará o modelo do Pydantic, gerará o `JSON Schema`, e adicionará no local correto.

O local correto é:

* Na chave `content`, que tem como valor um outro objeto JSON (`dict`) que contém:
    * Uma chave com o media type, como por exemplo `application/json`, que contém como valor um outro objeto JSON, contendo::
        * Uma chave `schema`, que contém como valor o JSON Schema do modelo, sendo este o local correto.
            * O **FastAPI** adiciona aqui a referência dos esquemas JSON globais que estão localizados em outro lugar, ao invés de incluí-lo diretamente. Deste modo, outras aplicações e clientes podem utilizar estes esquemas JSON diretamente, fornecer melhores ferramentas de geração de código, etc.

///

O retorno gerado no OpenAPI para esta *operação de rota* será:

```JSON hl_lines="3-12"
{
    "responses": {
        "404": {
            "description": "Additional Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Message"
                    }
                }
            }
        },
        "200": {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Item"
                    }
                }
            }
        },
        "422": {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/HTTPValidationError"
                    }
                }
            }
        }
    }
}
```

Os esquemas são referenciados em outro local dentro do esquema OpenAPI:

```JSON hl_lines="4-16"
{
    "components": {
        "schemas": {
            "Message": {
                "title": "Message",
                "required": [
                    "message"
                ],
                "type": "object",
                "properties": {
                    "message": {
                        "title": "Message",
                        "type": "string"
                    }
                }
            },
            "Item": {
                "title": "Item",
                "required": [
                    "id",
                    "value"
                ],
                "type": "object",
                "properties": {
                    "id": {
                        "title": "Id",
                        "type": "string"
                    },
                    "value": {
                        "title": "Value",
                        "type": "string"
                    }
                }
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": [
                    "loc",
                    "msg",
                    "type"
                ],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "msg": {
                        "title": "Message",
                        "type": "string"
                    },
                    "type": {
                        "title": "Error Type",
                        "type": "string"
                    }
                }
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/ValidationError"
                        }
                    }
                }
            }
        }
    }
}
```

## Media types adicionais para o retorno principal { #additional-media-types-for-the-main-response }

Você pode utilizar o mesmo parâmetro `responses` para adicionar diferentes media types para o mesmo retorno principal.

Por exemplo, você pode adicionar um media type adicional de `image/png`, declarando que a sua *operação de rota* pode retornar um objeto JSON (com o media type `application/json`) ou uma imagem PNG:

{* ../../docs_src/additional_responses/tutorial002.py hl[19:24,28] *}

/// note | Nota

Note que você deve retornar a imagem utilizando um `FileResponse` diretamente.

///

/// info | Informação

A menos que você especifique um media type diferente explicitamente em seu parâmetro `responses`, o FastAPI assumirá que o retorno possui o mesmo media type contido na classe principal de retorno (padrão `application/json`).

Porém se você especificou uma classe de retorno com o valor `None` como media type, o FastAPI utilizará `application/json` para qualquer retorno adicional que possui um modelo associado.

///

## Combinando informações { #combining-information }

Você também pode combinar informações de diferentes lugares, incluindo os parâmetros `response_model`, `status_code`, e `responses`.

Você pode declarar um `response_model`, utilizando o código de status padrão `200` (ou um customizado caso você precise), e depois adicionar informações adicionais para esse mesmo retorno em `responses`, diretamente no esquema OpenAPI.

O **FastAPI** manterá as informações adicionais do `responses`, e combinará com o esquema JSON do seu modelo.

Por exemplo, você pode declarar um retorno com o código de status `404` que utiliza um modelo do Pydantic que possui um `description` customizado.

E um retorno com o código de status `200` que utiliza o seu `response_model`, porém inclui um `example` customizado:

{* ../../docs_src/additional_responses/tutorial003.py hl[20:31] *}

Isso será combinado e incluído em seu OpenAPI, e disponibilizado na documentação da sua API:

<img src="/img/tutorial/additional-responses/image01.png">

## Combinar retornos predefinidos e personalizados { #combine-predefined-responses-and-custom-ones }

Você pode querer possuir alguns retornos predefinidos que são aplicados para diversas *operações de rota*, porém você deseja combinar com retornos personalizados que são necessários para cada *operação de rota*.

Para estes casos, você pode utilizar a técnica do Python de "desempacotamento" de um `dict` utilizando `**dict_to_unpack`:

```Python
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

Aqui, o `new_dict` terá todos os pares de chave-valor do `old_dict` mais o novo par de chave-valor:

```Python
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```

Você pode utilizar essa técnica para reutilizar alguns retornos predefinidos nas suas *operações de rota* e combiná-las com personalizações adicionais.

Por exemplo:

{* ../../docs_src/additional_responses/tutorial004.py hl[13:17,26] *}

## Mais informações sobre retornos OpenAPI { #more-information-about-openapi-responses }

Para verificar exatamente o que você pode incluir nos retornos, você pode conferir estas seções na especificação do OpenAPI:

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#responses-object" class="external-link" target="_blank">Objeto de Retorno OpenAPI</a>, inclui o `Response Object`.
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#response-object" class="external-link" target="_blank">Objeto de Retorno OpenAPI</a>, você pode incluir qualquer coisa dele diretamente em cada retorno dentro do seu parâmetro `responses`. Incluindo `description`, `headers`, `content` (dentro dele que você declara diferentes media types e esquemas JSON), e `links`.
