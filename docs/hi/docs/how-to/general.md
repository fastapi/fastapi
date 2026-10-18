# सामान्य - How To - Recipes { #general-how-to-recipes }

सामान्य या अक्सर पूछे जाने वाले प्रश्नों के लिए, docs में अन्य जगहों के कई pointers यहाँ दिए गए हैं।

## Data फ़िल्टर करें - सुरक्षा { #filter-data-security }

यह सुनिश्चित करने के लिए कि आप जितना data लौटाना चाहिए उससे अधिक न लौटाएँ, [Tutorial - Response Model - Return Type](../tutorial/response-model.md) के docs पढ़ें।

## Response Performance को optimize करें - Response Model - Return Type { #optimize-response-performance-response-model-return-type }

JSON data लौटाते समय performance को optimize करने के लिए, return type या response model का उपयोग करें, इस तरह Pydantic JSON में serialization को Rust side पर संभालेगा, Python से गुज़रे बिना। अधिक पढ़ें [Tutorial - Response Model - Return Type](../tutorial/response-model.md) के docs में।

## Documentation Tags - OpenAPI { #documentation-tags-openapi }

अपने *path operations* में tags जोड़ने और उन्हें docs UI में group करने के लिए, [Tutorial - Path Operation Configurations - Tags](../tutorial/path-operation-configuration.md#tags) के docs पढ़ें।

## Documentation Summary और Description - OpenAPI { #documentation-summary-and-description-openapi }

अपने *path operations* में summary और description जोड़ने, और उन्हें docs UI में दिखाने के लिए, [Tutorial - Path Operation Configurations - Summary and Description](../tutorial/path-operation-configuration.md#summary-and-description) के docs पढ़ें।

## Documentation Response description - OpenAPI { #documentation-response-description-openapi }

response का description define करने के लिए, जो docs UI में दिखाया जाता है, [Tutorial - Path Operation Configurations - Response description](../tutorial/path-operation-configuration.md#response-description) के docs पढ़ें।

## Documentation में *Path Operation* को Deprecate करें - OpenAPI { #documentation-deprecate-a-path-operation-openapi }

किसी *path operation* को deprecate करने और उसे docs UI में दिखाने के लिए, [Tutorial - Path Operation Configurations - Deprecation](../tutorial/path-operation-configuration.md#deprecate-a-path-operation) के docs पढ़ें।

## किसी भी Data को JSON-compatible में convert करें { #convert-any-data-to-json-compatible }

किसी भी data को JSON-compatible में convert करने के लिए, [Tutorial - JSON Compatible Encoder](../tutorial/encoder.md) के docs पढ़ें।

## OpenAPI Metadata - Docs { #openapi-metadata-docs }

अपने OpenAPI schema में metadata जोड़ने के लिए, जिसमें license, version, contact, आदि शामिल हैं, [Tutorial - Metadata and Docs URLs](../tutorial/metadata.md) के docs पढ़ें।

## OpenAPI Custom URL { #openapi-custom-url }

OpenAPI URL को customize करने (या हटाने) के लिए, [Tutorial - Metadata and Docs URLs](../tutorial/metadata.md#openapi-url) के docs पढ़ें।

## OpenAPI Docs URLs { #openapi-docs-urls }

अपने-आप generate किए गए docs user interfaces के लिए उपयोग किए जाने वाले URLs को update करने के लिए, [Tutorial - Metadata and Docs URLs](../tutorial/metadata.md#docs-urls) के docs पढ़ें।
