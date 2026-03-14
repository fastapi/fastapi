# Base64 کے طور پر Bytes کے ساتھ JSON { #json-with-bytes-as-base64 }

اگر آپ کی ایپ کو JSON ڈیٹا وصول اور بھیجنا ہے، لیکن اس میں binary ڈیٹا بھی شامل کرنا ہے، تو آپ اسے base64 کے طور پر encode کر سکتے ہیں۔

## Base64 بمقابلہ فائلیں { #base64-vs-files }

پہلے غور کریں کہ کیا آپ binary ڈیٹا اپ لوڈ کرنے کے لیے [Request Files](../tutorial/request-files.md) اور binary ڈیٹا بھیجنے کے لیے [Custom Response - FileResponse](./custom-response.md#fileresponse--fileresponse-) استعمال کر سکتے ہیں، JSON میں encode کرنے کی بجائے۔

JSON صرف UTF-8 encoded strings رکھ سکتا ہے، اس لیے اس میں خام bytes نہیں ہو سکتے۔

Base64 binary ڈیٹا کو strings میں encode کر سکتا ہے، لیکن ایسا کرنے کے لیے اسے اصل binary ڈیٹا سے زیادہ characters استعمال کرنے ہوتے ہیں، اس لیے یہ عام طور پر عام فائلوں سے کم موثر ہوتا ہے۔

Base64 صرف اسی وقت استعمال کریں جب آپ کو یقینی طور پر JSON میں binary ڈیٹا شامل کرنا ہو، اور آپ اس کے لیے فائلیں استعمال نہیں کر سکتے۔

## Pydantic `bytes` { #pydantic-bytes }

آپ `bytes` fields کے ساتھ Pydantic model بیان کر سکتے ہیں، اور پھر model config میں `val_json_bytes` استعمال کر کے بتا سکتے ہیں کہ input JSON ڈیٹا کو *validate* کرنے کے لیے base64 استعمال کرے، اس validation کے حصے کے طور پر یہ base64 string کو bytes میں decode کرے گا۔

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:9,29:35] hl[9] *}

اگر آپ `/docs` چیک کریں، تو وہ دکھائیں گے کہ `data` field base64 encoded bytes کی توقع رکھتا ہے:

<div class="screenshot">
<img src="/img/tutorial/json-base64-bytes/image01.png">
</div>

آپ اس طرح request بھیج سکتے ہیں:

```json
{
    "description": "Some data",
    "data": "aGVsbG8="
}
```

/// tip | مشورہ

`aGVsbG8=` `hello` کی base64 encoding ہے۔

///

اور پھر Pydantic base64 string decode کرے گا اور آپ کو model کے `data` field میں اصل bytes دے گا۔

آپ کو اس طرح response ملے گا:

```json
{
  "description": "Some data",
  "content": "hello"
}
```

## آؤٹ پٹ ڈیٹا کے لیے Pydantic `bytes` { #pydantic-bytes-for-output-data }

آپ آؤٹ پٹ ڈیٹا کے لیے بھی model config میں `ser_json_bytes` کے ساتھ `bytes` fields استعمال کر سکتے ہیں، اور JSON response بناتے وقت Pydantic bytes کو base64 کے طور پر *serialize* کرے گا۔

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,12:16,29,38:41] hl[16] *}

## ان پٹ اور آؤٹ پٹ ڈیٹا دونوں کے لیے Pydantic `bytes` { #pydantic-bytes-for-input-and-output-data }

اور یقیناً، آپ JSON ڈیٹا وصول اور بھیجتے وقت `val_json_bytes` سے input (*validate*) اور `ser_json_bytes` سے output (*serialize*) دونوں ہینڈل کرنے کے لیے base64 استعمال کرنے کے لیے ترتیب شدہ وہی model استعمال کر سکتے ہیں۔

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,19:26,29,44:46] hl[23:26] *}
