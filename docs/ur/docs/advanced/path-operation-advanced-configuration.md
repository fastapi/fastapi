# Path Operation ایڈوانسڈ ترتیب { #path-operation-advanced-configuration }

## OpenAPI operationId { #openapi-operationid }

/// warning | انتباہ

اگر آپ OpenAPI میں "ماہر" نہیں ہیں، تو آپ کو شاید اس کی ضرورت نہ ہو۔

///

آپ اپنے *path operation* میں `operation_id` parameter استعمال کر کے OpenAPI `operationId` مقرر کر سکتے ہیں۔

آپ کو یقینی بنانا ہوگا کہ یہ ہر operation کے لیے منفرد ہو۔

{* ../../docs_src/path_operation_advanced_configuration/tutorial001_py310.py hl[6] *}

### *path operation function* کا نام بطور operationId استعمال کرنا { #using-the-path-operation-function-name-as-the-operationid }

اگر آپ اپنے APIs کے function ناموں کو `operationId` کے طور پر استعمال کرنا چاہتے ہیں، تو آپ ان سب پر iterate کر سکتے ہیں اور ہر *path operation* کے `operation_id` کو ان کے `APIRoute.name` سے تبدیل کر سکتے ہیں۔

آپ کو یہ اپنے تمام *path operations* شامل کرنے کے بعد کرنا چاہیے۔

{* ../../docs_src/path_operation_advanced_configuration/tutorial002_py310.py hl[2, 12:21, 24] *}

/// tip | مشورہ

اگر آپ دستی طور پر `app.openapi()` کال کرتے ہیں، تو آپ کو اس سے پہلے `operationId` اپ ڈیٹ کرنے چاہئیں۔

///

/// warning | انتباہ

اگر آپ ایسا کرتے ہیں، تو آپ کو یقینی بنانا ہوگا کہ آپ کے ہر *path operation function* کا نام منفرد ہو۔

چاہے وہ مختلف modules (Python فائلوں) میں ہوں۔

///

## OpenAPI سے خارج کریں { #exclude-from-openapi }

کسی *path operation* کو تیار شدہ OpenAPI schema سے (اور اس طرح خودکار دستاویزی نظاموں سے) خارج کرنے کے لیے، parameter `include_in_schema` استعمال کریں اور اسے `False` پر مقرر کریں:

{* ../../docs_src/path_operation_advanced_configuration/tutorial003_py310.py hl[6] *}

## docstring سے ایڈوانسڈ وضاحت { #advanced-description-from-docstring }

آپ *path operation function* کے docstring سے OpenAPI کے لیے استعمال ہونے والی سطروں کو محدود کر سکتے ہیں۔

`\f` (ایک escaped "form feed" حرف) شامل کرنے سے **FastAPI** اس مقام پر OpenAPI کے لیے استعمال ہونے والی آؤٹ پٹ کو تراش دے گا۔

یہ دستاویزات میں نظر نہیں آئے گا، لیکن دوسرے ٹولز (جیسے Sphinx) باقی حصہ استعمال کر سکیں گے۔

{* ../../docs_src/path_operation_advanced_configuration/tutorial004_py310.py hl[17:27] *}

## اضافی Responses { #additional-responses }

آپ نے شاید دیکھا ہوگا کہ *path operation* کے لیے `response_model` اور `status_code` کا اعلان کیسے کیا جاتا ہے۔

یہ *path operation* کے بنیادی response کے بارے میں metadata بیان کرتا ہے۔

آپ اضافی responses بھی اعلان کر سکتے ہیں ان کے models، status codes وغیرہ کے ساتھ۔

دستاویزات میں اس بارے میں ایک مکمل باب ہے، آپ اسے [OpenAPI میں اضافی Responses](additional-responses.md) پر پڑھ سکتے ہیں۔

## OpenAPI Extra { #openapi-extra }

جب آپ اپنی ایپلیکیشن میں *path operation* کا اعلان کرتے ہیں، **FastAPI** خود بخود اس *path operation* کے بارے میں متعلقہ metadata تیار کرتا ہے تاکہ اسے OpenAPI schema میں شامل کیا جا سکے۔

/// note | تکنیکی تفصیلات

OpenAPI specification میں اسے [Operation Object](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object) کہا جاتا ہے۔

///

اس میں *path operation* کے بارے میں تمام معلومات ہوتی ہیں اور اسے خودکار دستاویزات تیار کرنے کے لیے استعمال کیا جاتا ہے۔

اس میں `tags`، `parameters`، `requestBody`، `responses` وغیرہ شامل ہیں۔

یہ *path operation* مخصوص OpenAPI schema عام طور پر **FastAPI** کی طرف سے خود بخود تیار ہوتا ہے، لیکن آپ اسے بڑھا بھی سکتے ہیں۔

/// tip | مشورہ

یہ ایک نچلی سطح کا extension point ہے۔

اگر آپ کو صرف اضافی responses کا اعلان کرنا ہے، تو اس کا ایک زیادہ آسان طریقہ [OpenAPI میں اضافی Responses](additional-responses.md) ہے۔

///

آپ `openapi_extra` parameter استعمال کر کے *path operation* کے OpenAPI schema کو بڑھا سکتے ہیں۔

### OpenAPI Extensions { #openapi-extensions }

یہ `openapi_extra` مفید ہو سکتا ہے، مثال کے طور پر، [OpenAPI Extensions](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions) کا اعلان کرنے کے لیے:

{* ../../docs_src/path_operation_advanced_configuration/tutorial005_py310.py hl[6] *}

اگر آپ خودکار API docs کھولتے ہیں، تو آپ کی extension مخصوص *path operation* کے نیچے ظاہر ہوگی۔

<img src="/img/tutorial/path-operation-advanced-configuration/image01.png">

اور اگر آپ نتیجے میں آنے والا OpenAPI دیکھتے ہیں (آپ کے API میں `/openapi.json` پر)، تو آپ اپنی extension مخصوص *path operation* کے حصے کے طور پر بھی دیکھیں گے:

```JSON hl_lines="22"
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                },
                "x-aperture-labs-portal": "blue"
            }
        }
    }
}
```

### حسب ضرورت OpenAPI *path operation* schema { #custom-openapi-path-operation-schema }

`openapi_extra` میں موجود dictionary کو *path operation* کے خود بخود تیار شدہ OpenAPI schema کے ساتھ گہرائی سے merge کیا جائے گا۔

لہذا، آپ خود بخود تیار شدہ schema میں اضافی ڈیٹا شامل کر سکتے ہیں۔

مثال کے طور پر، آپ فیصلہ کر سکتے ہیں کہ request کو اپنے کوڈ سے پڑھیں اور توثیق کریں، Pydantic کے ساتھ FastAPI کی خودکار خصوصیات استعمال کیے بغیر، لیکن آپ پھر بھی OpenAPI schema میں request کی تعریف کرنا چاہیں۔

آپ یہ `openapi_extra` کے ساتھ کر سکتے ہیں:

{* ../../docs_src/path_operation_advanced_configuration/tutorial006_py310.py hl[19:36, 39:40] *}

اس مثال میں، ہم نے کوئی Pydantic model اعلان نہیں کیا۔ دراصل، request body کو JSON کے طور پر <dfn title="converted from some plain format, like bytes, into Python objects">parse</dfn> بھی نہیں کیا گیا، اسے براہ راست `bytes` کے طور پر پڑھا گیا ہے، اور function `magic_data_reader()` اسے کسی طرح parse کرنے کا ذمہ دار ہوگا۔

بہرحال، ہم request body کے لیے متوقع schema کا اعلان کر سکتے ہیں۔

### حسب ضرورت OpenAPI content type { #custom-openapi-content-type }

اسی چال کا استعمال کرتے ہوئے، آپ Pydantic model استعمال کر کے JSON Schema بیان کر سکتے ہیں جو پھر *path operation* کے حسب ضرورت OpenAPI schema حصے میں شامل ہوتا ہے۔

اور آپ یہ اس صورت میں بھی کر سکتے ہیں جب request میں ڈیٹا کی قسم JSON نہ ہو۔

مثال کے طور پر، اس ایپلیکیشن میں ہم FastAPI کی مربوط فعالیت استعمال نہیں کرتے Pydantic models سے JSON Schema نکالنے یا JSON کے لیے خودکار توثیق کے لیے۔ دراصل، ہم request content type کو JSON کی بجائے YAML بیان کر رہے ہیں:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py310.py hl[15:20, 22] *}

بہرحال، اگرچہ ہم پہلے سے طے شدہ مربوط فعالیت استعمال نہیں کر رہے، ہم پھر بھی Pydantic model استعمال کر رہے ہیں تاکہ دستی طور پر اس ڈیٹا کے لیے JSON Schema تیار کیا جا سکے جو ہم YAML میں وصول کرنا چاہتے ہیں۔

پھر ہم request کو براہ راست استعمال کرتے ہیں، اور body کو `bytes` کے طور پر نکالتے ہیں۔ اس کا مطلب ہے کہ FastAPI request payload کو JSON کے طور پر parse کرنے کی کوشش بھی نہیں کرے گا۔

اور پھر اپنے کوڈ میں، ہم اس YAML مواد کو براہ راست parse کرتے ہیں، اور پھر ہم دوبارہ وہی Pydantic model استعمال کر کے YAML مواد کی توثیق کرتے ہیں:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py310.py hl[24:31] *}

/// tip | مشورہ

یہاں ہم وہی Pydantic model دوبارہ استعمال کر رہے ہیں۔

لیکن اسی طرح، ہم اسے کسی اور طریقے سے بھی توثیق کر سکتے تھے۔

///
