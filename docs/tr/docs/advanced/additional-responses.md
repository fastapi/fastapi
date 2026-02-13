# OpenAPI'de Ek Response'lar { #additional-responses-in-openapi }

/// warning | Uyarı

Bu konu oldukça ileri seviye bir konudur.

**FastAPI**'ye yeni başlıyorsanız buna ihtiyaç duymayabilirsiniz.

///

Ek status code'lar, media type'lar, açıklamalar vb. ile ek response'lar tanımlayabilirsiniz.

Bu ek response'lar OpenAPI şemasına dahil edilir; dolayısıyla API dokümanlarında da görünürler.

Ancak bu ek response'lar için, status code'unuzu ve içeriğinizi vererek `JSONResponse` gibi bir `Response`'u doğrudan döndürdüğünüzden emin olmanız gerekir.

## `model` ile Ek Response { #additional-response-with-model }

*Path operation decorator*'larınıza `responses` adlı bir parametre geçebilirsiniz.

Bu parametre bir `dict` alır: anahtarlar her response için status code'lardır (`200` gibi), değerler ise her birine ait bilgileri içeren başka `dict`'lerdir.

Bu response `dict`'lerinin her birinde, `response_model`'e benzer şekilde bir Pydantic model içeren `model` anahtarı olabilir.

**FastAPI** bu modeli alır, JSON Schema'sını üretir ve OpenAPI'de doğru yere ekler.

Örneğin, `404` status code'u ve `Message` Pydantic model'i ile başka bir response tanımlamak için şunu yazabilirsiniz:

{* ../../docs_src/additional_responses/tutorial001_py310.py hl[18,22] *}

/// note | Not

`JSONResponse`'u doğrudan döndürmeniz gerektiğini unutmayın.

///

/// info | Bilgi

`model` anahtarı OpenAPI'nin bir parçası değildir.

**FastAPI** buradaki Pydantic model'i alır, JSON Schema'yı üretir ve doğru yere yerleştirir.

Doğru yer şurasıdır:

* Değeri başka bir JSON nesnesi (`dict`) olan `content` anahtarının içinde:
    * Media type anahtarı (örn. `application/json`) bulunur; bunun değeri başka bir JSON nesnesidir ve onun içinde:
        * Değeri model'den gelen JSON Schema olan `schema` anahtarı vardır; doğru yer burasıdır.
            * **FastAPI** bunu doğrudan gömmek yerine OpenAPI'deki başka bir yerde bulunan global JSON Schema'lara bir referans ekler. Böylece diğer uygulamalar ve client'lar bu JSON Schema'ları doğrudan kullanabilir, daha iyi code generation araçları sağlayabilir, vb.

///

Bu *path operation* için OpenAPI'de üretilen response'lar şöyle olur:

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

Schema'lar OpenAPI şemasının içinde başka bir yere referanslanır:

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

## Ana Response İçin Ek Media Type'lar { #additional-media-types-for-the-main-response }

Aynı `responses` parametresini, aynı ana response için farklı media type'lar eklemek amacıyla da kullanabilirsiniz.

Örneğin, `image/png` için ek bir media type ekleyerek, *path operation*'ınızın bir JSON nesnesi (media type `application/json`) ya da bir PNG görseli döndürebildiğini belirtebilirsiniz:

{* ../../docs_src/additional_responses/tutorial002_py310.py hl[17:22,26] *}

/// note | Not

Görseli `FileResponse` kullanarak doğrudan döndürmeniz gerektiğine dikkat edin.

///

/// info | Bilgi

`responses` parametrenizde açıkça farklı bir media type belirtmediğiniz sürece FastAPI, response'un ana response class'ı ile aynı media type'a sahip olduğunu varsayar (varsayılan `application/json`).

Ancak media type'ı `None` olan özel bir response class belirttiyseniz, FastAPI ilişkili bir model'i olan tüm ek response'lar için `application/json` kullanır.

///

## Bilgileri Birleştirme { #combining-information }

`response_model`, `status_code` ve `responses` parametreleri dahil olmak üzere, response bilgilerini birden fazla yerden birleştirebilirsiniz.

Varsayılan `200` status code'unu (ya da gerekiyorsa özel bir tane) kullanarak bir `response_model` tanımlayabilir, ardından aynı response için ek bilgileri `responses` içinde, doğrudan OpenAPI şemasına ekleyebilirsiniz.

**FastAPI**, `responses` içindeki ek bilgileri korur ve model'inizin JSON Schema'sı ile birleştirir.

Örneğin, Pydantic model kullanan ve özel bir `description` içeren `404` status code'lu bir response tanımlayabilirsiniz.

Ayrıca `response_model`'inizi kullanan, ancak özel bir `example` içeren `200` status code'lu bir response da tanımlayabilirsiniz:

{* ../../docs_src/additional_responses/tutorial003_py310.py hl[20:31] *}

Bunların hepsi OpenAPI'nize birleştirilerek dahil edilir ve API dokümanlarında gösterilir:

<img src="/img/tutorial/additional-responses/image01.png">

## Ön Tanımlı Response'ları Özel Olanlarla Birleştirme { #combine-predefined-responses-and-custom-ones }

Birçok *path operation* için geçerli olacak bazı ön tanımlı response'larınız olabilir; ancak bunları her *path operation*'ın ihtiyaç duyduğu özel response'larla birleştirmek isteyebilirsiniz.

Bu durumlarda, Python'daki bir `dict`'i `**dict_to_unpack` ile "unpacking" tekniğini kullanabilirsiniz:

```Python
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

Burada `new_dict`, `old_dict` içindeki tüm key-value çiftlerini ve buna ek olarak yeni key-value çiftini içerir:

```Python
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```

Bu tekniği, *path operation*'larınızda bazı ön tanımlı response'ları yeniden kullanmak ve bunları ek özel response'larla birleştirmek için kullanabilirsiniz.

Örneğin:

{* ../../docs_src/additional_responses/tutorial004_py310.py hl[11:15,24] *}

## OpenAPI Response'ları Hakkında Daha Fazla Bilgi { #more-information-about-openapi-responses }

Response'ların içine tam olarak neleri dahil edebileceğinizi görmek için OpenAPI spesifikasyonundaki şu bölümlere bakabilirsiniz:

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#responses-object" class="external-link" target="_blank">OpenAPI Responses Object</a>, `Response Object`'i içerir.
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#response-object" class="external-link" target="_blank">OpenAPI Response Object</a>, buradaki her şeyi `responses` parametreniz içinde, her bir response'un içine doğrudan ekleyebilirsiniz. Buna `description`, `headers`, `content` (bunun içinde farklı media type'lar ve JSON Schema'lar tanımlarsınız) ve `links` dahildir.
