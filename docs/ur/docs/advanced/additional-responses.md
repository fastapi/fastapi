# OpenAPI میں اضافی Responses { #additional-responses-in-openapi }

/// warning | انتباہ

یہ ایک کافی ایڈوانسڈ موضوع ہے۔

اگر آپ **FastAPI** کے ساتھ شروعات کر رہے ہیں تو آپ کو شاید اس کی ضرورت نہ ہو۔

///

آپ اضافی responses کا اعلان کر سکتے ہیں، اضافی status codes، media types، وضاحتوں وغیرہ کے ساتھ۔

یہ اضافی responses OpenAPI schema میں شامل کیے جائیں گے، لہذا وہ API docs میں بھی ظاہر ہوں گے۔

لیکن ان اضافی responses کے لیے آپ کو یقینی بنانا ہوگا کہ آپ براہ راست `Response` جیسے `JSONResponse` واپس کریں، اپنے status code اور مواد کے ساتھ۔

## `model` کے ساتھ اضافی Response { #additional-response-with-model }

آپ اپنے *path operation decorators* کو ایک parameter `responses` دے سکتے ہیں۔

یہ ایک `dict` وصول کرتا ہے: کلیدیں ہر response کے لیے status codes ہیں (جیسے `200`)، اور قدریں دوسری `dict` ہیں جن میں ہر ایک کی معلومات ہوتی ہیں۔

ان response `dict` میں سے ہر ایک میں `model` نامی ایک کلید ہو سکتی ہے، جس میں Pydantic model ہوتا ہے، بالکل `response_model` کی طرح۔

**FastAPI** اس model کو لے گا، اس کا JSON Schema تیار کرے گا اور اسے OpenAPI میں صحیح جگہ شامل کرے گا۔

مثال کے طور پر، status code `404` اور Pydantic model `Message` کے ساتھ ایک اور response کا اعلان کرنے کے لیے، آپ یہ لکھ سکتے ہیں:

{* ../../docs_src/additional_responses/tutorial001_py310.py hl[18,22] *}

/// note | نوٹ

ذہن میں رکھیں کہ آپ کو `JSONResponse` براہ راست واپس کرنا ہوگا۔

///

/// info | معلومات

`model` کلید OpenAPI کا حصہ نہیں ہے۔

**FastAPI** وہاں سے Pydantic model لے گا، JSON Schema تیار کرے گا، اور اسے صحیح جگہ رکھے گا۔

صحیح جگہ یہ ہے:

* کلید `content` میں، جس کی قدر ایک اور JSON object (`dict`) ہے جس میں شامل ہے:
    * media type والی ایک کلید، مثلاً `application/json`، جس کی قدر ایک اور JSON object ہے، جس میں شامل ہے:
        * ایک کلید `schema`، جس کی قدر model سے JSON Schema ہے، یہ ہے صحیح جگہ۔
            * **FastAPI** یہاں عالمی JSON Schemas کا حوالہ شامل کرتا ہے جو آپ کے OpenAPI میں کسی اور جگہ ہوتے ہیں بجائے اسے براہ راست شامل کرنے کے۔ اس طرح، دوسری ایپلیکیشنز اور clients ان JSON Schemas کو براہ راست استعمال کر سکتے ہیں، بہتر code generation ٹولز فراہم کر سکتے ہیں وغیرہ۔

///

اس *path operation* کے لیے OpenAPI میں تیار شدہ responses یہ ہوں گے:

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

Schemas کا حوالہ OpenAPI schema کے اندر کسی اور جگہ دیا گیا ہے:

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

## بنیادی response کے لیے اضافی media types { #additional-media-types-for-the-main-response }

آپ اسی `responses` parameter کو استعمال کر کے بنیادی response میں مختلف media types شامل کر سکتے ہیں۔

مثال کے طور پر، آپ `image/png` کی اضافی media type شامل کر سکتے ہیں، یہ اعلان کرتے ہوئے کہ آپ کا *path operation* ایک JSON object (media type `application/json` کے ساتھ) یا PNG تصویر واپس کر سکتا ہے:

{* ../../docs_src/additional_responses/tutorial002_py310.py hl[17:22,26] *}

/// note | نوٹ

دھیان دیں کہ آپ کو تصویر براہ راست `FileResponse` استعمال کر کے واپس کرنی ہوگی۔

///

/// info | معلومات

جب تک آپ اپنے `responses` parameter میں واضح طور پر کوئی مختلف media type بیان نہیں کرتے، FastAPI فرض کرے گا کہ response کی media type بنیادی response class جیسی ہی ہے (پہلے سے طے شدہ `application/json`)۔

لیکن اگر آپ نے `None` کو اس کی media type کے طور پر اپنی مرضی کی response class بیان کی ہے، تو FastAPI کسی بھی اضافی response کے لیے `application/json` استعمال کرے گا جس کے ساتھ ایک model منسلک ہے۔

///

## معلومات کو یکجا کرنا { #combining-information }

آپ متعدد جگہوں سے response کی معلومات کو بھی یکجا کر سکتے ہیں، بشمول `response_model`، `status_code`، اور `responses` parameters۔

آپ `response_model` کا اعلان کر سکتے ہیں، پہلے سے طے شدہ status code `200` (یا ضرورت کے مطابق کوئی اور) استعمال کرتے ہوئے، اور پھر اسی response کے لیے `responses` میں اضافی معلومات کا اعلان کر سکتے ہیں، براہ راست OpenAPI schema میں۔

**FastAPI** `responses` سے اضافی معلومات رکھے گا، اور اسے آپ کے model سے JSON Schema کے ساتھ ملا دے گا۔

مثال کے طور پر، آپ status code `404` والا response اعلان کر سکتے ہیں جو Pydantic model استعمال کرتا ہے اور اپنی مرضی کی `description` رکھتا ہے۔

اور status code `200` والا response جو آپ کا `response_model` استعمال کرتا ہے، لیکن اپنی مرضی کی `example` شامل کرتا ہے:

{* ../../docs_src/additional_responses/tutorial003_py310.py hl[20:31] *}

یہ سب یکجا ہو کر آپ کے OpenAPI میں شامل ہو جائے گا، اور API docs میں دکھایا جائے گا:

<img src="/img/tutorial/additional-responses/image01.png">

## پہلے سے طے شدہ اور اپنی مرضی کے responses کو ملانا { #combine-predefined-responses-and-custom-ones }

ہو سکتا ہے آپ چاہیں کہ کچھ پہلے سے طے شدہ responses ہوں جو بہت سے *path operations* پر لاگو ہوں، لیکن آپ انہیں ہر *path operation* کے لیے درکار اپنی مرضی کے responses کے ساتھ ملانا چاہتے ہیں۔

ان صورتوں میں، آپ Python کی `dict` کو `**dict_to_unpack` کے ساتھ "unpack" کرنے کی تکنیک استعمال کر سکتے ہیں:

```Python
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

یہاں، `new_dict` میں `old_dict` کے تمام key-value جوڑے اور نیا key-value جوڑا شامل ہوگا:

```Python
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```

آپ اس تکنیک کو اپنے *path operations* میں پہلے سے طے شدہ responses کو دوبارہ استعمال کرنے اور انہیں اضافی اپنی مرضی کے responses کے ساتھ ملانے کے لیے استعمال کر سکتے ہیں۔

مثال کے طور پر:

{* ../../docs_src/additional_responses/tutorial004_py310.py hl[11:15,24] *}

## OpenAPI responses کے بارے میں مزید معلومات { #more-information-about-openapi-responses }

یہ دیکھنے کے لیے کہ آپ responses میں بالکل کیا شامل کر سکتے ہیں، آپ OpenAPI specification میں یہ حصے دیکھ سکتے ہیں:

* [OpenAPI Responses Object](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#responses-object)، اس میں `Response Object` شامل ہے۔
* [OpenAPI Response Object](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#response-object)، آپ اپنے `responses` parameter کے اندر ہر response میں اس سے کچھ بھی براہ راست شامل کر سکتے ہیں۔ بشمول `description`، `headers`، `content` (اس کے اندر آپ مختلف media types اور JSON Schemas کا اعلان کرتے ہیں)، اور `links`۔
