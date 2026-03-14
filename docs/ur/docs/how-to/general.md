# عمومی - طریقہ کار - ترکیبیں { #general-how-to-recipes }

یہاں عمومی یا اکثر پوچھے جانے والے سوالات کے لیے دستاویزات میں دیگر مقامات کی طرف کئی اشارے ہیں۔

## ڈیٹا فلٹر کریں - Security { #filter-data-security }

اس بات کو یقینی بنانے کے لیے کہ آپ ضرورت سے زیادہ ڈیٹا واپس نہ کریں، [Tutorial - Response Model - Return Type](../tutorial/response-model.md) کی دستاویزات پڑھیں۔

## Response کی کارکردگی بہتر بنائیں - Response Model - Return Type { #optimize-response-performance-response-model-return-type }

JSON ڈیٹا واپس کرتے وقت کارکردگی بہتر بنانے کے لیے، return type یا response model استعمال کریں، اس طرح Pydantic بغیر Python سے گزرے Rust کی طرف سے JSON میں serialization سنبھالے گا۔ مزید معلومات کے لیے [Tutorial - Response Model - Return Type](../tutorial/response-model.md) کی دستاویزات پڑھیں۔

## دستاویزات کے Tags - OpenAPI { #documentation-tags-openapi }

اپنی *path operations* میں tags شامل کرنے اور انہیں docs UI میں گروپ کرنے کے لیے، [Tutorial - Path Operation Configurations - Tags](../tutorial/path-operation-configuration.md#tags) کی دستاویزات پڑھیں۔

## دستاویزات کا خلاصہ اور تفصیل - OpenAPI { #documentation-summary-and-description-openapi }

اپنی *path operations* میں summary اور description شامل کرنے اور انہیں docs UI میں دکھانے کے لیے، [Tutorial - Path Operation Configurations - Summary and Description](../tutorial/path-operation-configuration.md#summary-and-description) کی دستاویزات پڑھیں۔

## دستاویزات Response description - OpenAPI { #documentation-response-description-openapi }

Response کی تفصیل جو docs UI میں دکھائی جاتی ہے اس کی وضاحت کرنے کے لیے، [Tutorial - Path Operation Configurations - Response description](../tutorial/path-operation-configuration.md#response-description) کی دستاویزات پڑھیں۔

## دستاویزات میں *Path Operation* کو Deprecate کریں - OpenAPI { #documentation-deprecate-a-path-operation-openapi }

کسی *path operation* کو deprecate کرنے اور اسے docs UI میں دکھانے کے لیے، [Tutorial - Path Operation Configurations - Deprecation](../tutorial/path-operation-configuration.md#deprecate-a-path-operation) کی دستاویزات پڑھیں۔

## کسی بھی ڈیٹا کو JSON-compatible میں تبدیل کریں { #convert-any-data-to-json-compatible }

کسی بھی ڈیٹا کو JSON-compatible میں تبدیل کرنے کے لیے، [Tutorial - JSON Compatible Encoder](../tutorial/encoder.md) کی دستاویزات پڑھیں۔

## OpenAPI Metadata - Docs { #openapi-metadata-docs }

اپنے OpenAPI schema میں metadata شامل کرنے کے لیے، بشمول license، version، contact وغیرہ، [Tutorial - Metadata and Docs URLs](../tutorial/metadata.md) کی دستاویزات پڑھیں۔

## OpenAPI Custom URL { #openapi-custom-url }

OpenAPI URL کو اپنی مرضی کے مطابق بنانے (یا ہٹانے) کے لیے، [Tutorial - Metadata and Docs URLs](../tutorial/metadata.md#openapi-url) کی دستاویزات پڑھیں۔

## OpenAPI Docs URLs { #openapi-docs-urls }

خود کار طریقے سے تیار کردہ docs user interfaces کے لیے استعمال ہونے والے URLs کو اپ ڈیٹ کرنے کے لیے، [Tutorial - Metadata and Docs URLs](../tutorial/metadata.md#docs-urls) کی دستاویزات پڑھیں۔
