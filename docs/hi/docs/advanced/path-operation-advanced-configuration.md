# Path Operation की उन्नत Configuration { #path-operation-advanced-configuration }

## OpenAPI operationId { #openapi-operationid }

/// warning | चेतावनी

अगर आप OpenAPI में "expert" नहीं हैं, तो शायद आपको इसकी ज़रूरत नहीं है।

///

आप अपने *path operation* में उपयोग किए जाने वाले OpenAPI `operationId` को parameter `operation_id` के साथ सेट कर सकते हैं।

आपको यह सुनिश्चित करना होगा कि यह प्रत्येक operation के लिए unique हो।

{* ../../docs_src/path_operation_advanced_configuration/tutorial001_py310.py hl[6] *}

### *path operation function* के नाम को operationId के रूप में उपयोग करना { #using-the-path-operation-function-name-as-the-operationid }

अगर आप अपने APIs के function नामों को `operationId`s के रूप में उपयोग करना चाहते हैं, तो आप `FastAPI` को एक custom `generate_unique_id_function` पास कर सकते हैं।

यह function प्रत्येक `APIRoute` प्राप्त करता है और उस path operation के लिए उपयोग करने वाला `operationId` return करता है।

{* ../../docs_src/path_operation_advanced_configuration/tutorial002_py310.py hl[2,5:6,9] *}

/// warning | चेतावनी

अगर आप ऐसा करते हैं, तो आपको यह सुनिश्चित करना होगा कि आपके प्रत्येक *path operation functions* का नाम unique हो।

भले ही वे अलग-अलग modules (Python files) में हों।

///

## OpenAPI से बाहर रखना { #exclude-from-openapi }

किसी *path operation* को generated OpenAPI schema से बाहर रखने के लिए (और इस प्रकार, automatic documentation systems से भी), parameter `include_in_schema` का उपयोग करें और इसे `False` पर सेट करें:

{* ../../docs_src/path_operation_advanced_configuration/tutorial003_py310.py hl[6] *}

## Docstring से उन्नत description { #advanced-description-from-docstring }

आप OpenAPI के लिए किसी *path operation function* की docstring से उपयोग की जाने वाली lines को सीमित कर सकते हैं।

एक `\f` (एक escaped "form feed" character) जोड़ने से **FastAPI** इस बिंदु पर OpenAPI के लिए उपयोग किए जाने वाले output को truncate कर देता है।

यह documentation में नहीं दिखेगा, लेकिन अन्य tools (जैसे Sphinx) बाकी हिस्से का उपयोग कर सकेंगे।

{* ../../docs_src/path_operation_advanced_configuration/tutorial004_py310.py hl[17:27] *}

## अतिरिक्त Responses { #additional-responses }

आपने शायद देखा होगा कि किसी *path operation* के लिए `response_model` और `status_code` कैसे declare किए जाते हैं।

यह किसी *path operation* के मुख्य response के बारे में metadata define करता है।

आप उनके models, status codes आदि के साथ अतिरिक्त responses भी declare कर सकते हैं।

इसके बारे में documentation में यहाँ एक पूरा chapter है, आप इसे [OpenAPI में अतिरिक्त Responses](additional-responses.md) पर पढ़ सकते हैं।

## OpenAPI Extra { #openapi-extra }

जब आप अपने application में कोई *path operation* declare करते हैं, तो **FastAPI** उस *path operation* के बारे में relevant metadata को automatically generate करता है, जिसे OpenAPI schema में शामिल किया जाता है।

/// note | तकनीकी विवरण

OpenAPI specification में इसे [Operation Object](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object) कहा जाता है।

///

इसमें *path operation* के बारे में सारी जानकारी होती है और इसका उपयोग automatic documentation generate करने के लिए किया जाता है।

इसमें `tags`, `parameters`, `requestBody`, `responses` आदि शामिल होते हैं।

यह *path operation*-specific OpenAPI schema सामान्यतः **FastAPI** द्वारा automatically generate किया जाता है, लेकिन आप इसे extend भी कर सकते हैं।

/// tip | सुझाव

यह एक low level extension point है।

अगर आपको केवल अतिरिक्त responses declare करने की ज़रूरत है, तो ऐसा करने का एक अधिक सुविधाजनक तरीका [OpenAPI में अतिरिक्त Responses](additional-responses.md) के साथ है।

///

आप parameter `openapi_extra` का उपयोग करके किसी *path operation* के लिए OpenAPI schema को extend कर सकते हैं।

### OpenAPI Extensions { #openapi-extensions }

यह `openapi_extra` उपयोगी हो सकता है, उदाहरण के लिए, [OpenAPI Extensions](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions) declare करने के लिए:

{* ../../docs_src/path_operation_advanced_configuration/tutorial005_py310.py hl[6] *}

अगर आप automatic API docs खोलते हैं, तो आपका extension specific *path operation* के नीचे दिखाई देगा।

<img src="/img/tutorial/path-operation-advanced-configuration/image01.png">

और अगर आप resulting OpenAPI (आपकी API में `/openapi.json` पर) देखते हैं, तो आपको अपना extension specific *path operation* के हिस्से के रूप में भी दिखाई देगा:

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

### Custom OpenAPI *path operation* schema { #custom-openapi-path-operation-schema }

`openapi_extra` में मौजूद dictionary को *path operation* के लिए automatically generated OpenAPI schema के साथ deeply merge किया जाएगा।

तो, आप automatically generated schema में अतिरिक्त data जोड़ सकते हैं।

उदाहरण के लिए, आप FastAPI की Pydantic के साथ automatic features का उपयोग किए बिना, अपने code से request को read और validate करने का निर्णय ले सकते हैं, लेकिन फिर भी आप OpenAPI schema में request को define करना चाह सकते हैं।

आप यह `openapi_extra` के साथ कर सकते हैं:

{* ../../docs_src/path_operation_advanced_configuration/tutorial006_py310.py hl[19:36, 39:40] *}

इस उदाहरण में, हमने कोई Pydantic model declare नहीं किया। वास्तव में, request body को JSON के रूप में <dfn title="किसी plain format, जैसे bytes, से Python objects में बदला गया">parsed</dfn> भी नहीं किया गया है, इसे सीधे `bytes` के रूप में read किया गया है, और function `magic_data_reader()` किसी तरीके से इसे parse करने का ज़िम्मेदार होगा।

फिर भी, हम request body के लिए expected schema declare कर सकते हैं।

### Custom OpenAPI content type { #custom-openapi-content-type }

इसी trick का उपयोग करके, आप JSON Schema define करने के लिए Pydantic model का उपयोग कर सकते हैं, जिसे फिर *path operation* के लिए custom OpenAPI schema section में शामिल किया जाता है।

और आप ऐसा तब भी कर सकते हैं जब request में data type JSON न हो।

उदाहरण के लिए, इस application में हम Pydantic models से JSON Schema निकालने के लिए FastAPI की integrated functionality या JSON के लिए automatic validation का उपयोग नहीं करते हैं। वास्तव में, हम request content type को JSON नहीं, बल्कि YAML के रूप में declare कर रहे हैं:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py310.py hl[15:20, 22] *}

फिर भी, हालांकि हम default integrated functionality का उपयोग नहीं कर रहे हैं, हम अभी भी उस data के लिए JSON Schema manually generate करने के लिए Pydantic model का उपयोग कर रहे हैं जिसे हम YAML में receive करना चाहते हैं।

फिर हम request को सीधे उपयोग करते हैं, और body को `bytes` के रूप में extract करते हैं। इसका मतलब है कि FastAPI request payload को JSON के रूप में parse करने की कोशिश भी नहीं करेगा।

और फिर अपने code में, हम उस YAML content को सीधे parse करते हैं, और फिर हम YAML content को validate करने के लिए फिर से उसी Pydantic model का उपयोग कर रहे हैं:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py310.py hl[24:31] *}

/// tip | सुझाव

यहाँ हम उसी Pydantic model को reuse करते हैं।

लेकिन इसी तरह, हम इसे किसी और तरीके से भी validate कर सकते थे।

///
