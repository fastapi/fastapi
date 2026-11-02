# Base64 के रूप में Bytes वाला JSON { #json-with-bytes-as-base64 }

अगर आपके app को JSON data receive और send करना है, लेकिन आपको उसमें binary data शामिल करना है, तो आप उसे base64 के रूप में encode कर सकते हैं।

## Base64 बनाम Files { #base64-vs-files }

पहले यह विचार करें कि क्या आप binary data upload करने के लिए [Request Files](../tutorial/request-files.md) और binary data भेजने के लिए [कस्टम Response - FileResponse](./custom-response.md#fileresponse) का उपयोग कर सकते हैं, बजाय इसके कि उसे JSON में encode किया जाए।

JSON में केवल UTF-8 encoded strings हो सकती हैं, इसलिए उसमें raw bytes नहीं हो सकते।

Base64 binary data को strings में encode कर सकता है, लेकिन ऐसा करने के लिए उसे मूल binary data की तुलना में अधिक characters का उपयोग करना पड़ता है, इसलिए यह सामान्य files की तुलना में आमतौर पर कम efficient होगा।

Base64 का उपयोग केवल तभी करें जब आपको निश्चित रूप से JSON में binary data शामिल करना हो, और आप उसके लिए files का उपयोग नहीं कर सकते।

## Pydantic `bytes` { #pydantic-bytes }

आप `bytes` fields वाला एक Pydantic model declare कर सकते हैं, और फिर model config में `val_json_bytes` का उपयोग करके उसे बता सकते हैं कि input JSON data को *validate* करने के लिए base64 का उपयोग करे; उस validation के हिस्से के रूप में यह base64 string को bytes में decode करेगा।

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:9,29:35] hl[9] *}

अगर आप `/docs` देखें, तो वे दिखाएँगे कि field `data` base64 encoded bytes की अपेक्षा करता है:

<div class="screenshot">
<img src="/img/tutorial/json-base64-bytes/image01.png">
</div>

आप इस तरह का request भेज सकते हैं:

```json
{
    "description": "Some data",
    "data": "aGVsbG8="
}
```

/// tip | सुझाव

`aGVsbG8=` `hello` की base64 encoding है।

///

और फिर Pydantic base64 string को decode करेगा और आपको model के `data` field में मूल bytes देगा।

आपको इस तरह का response मिलेगा:

```json
{
  "description": "Some data",
  "content": "hello"
}
```

## Output Data के लिए Pydantic `bytes` { #pydantic-bytes-for-output-data }

आप output data के लिए model config में `ser_json_bytes` के साथ `bytes` fields का भी उपयोग कर सकते हैं, और JSON response generate करते समय Pydantic bytes को base64 के रूप में *serialize* करेगा।

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,12:16,29,38:41] hl[16] *}

## Input और Output Data के लिए Pydantic `bytes` { #pydantic-bytes-for-input-and-output-data }

और बेशक, JSON data receive और send करते समय आप उसी model को base64 उपयोग करने के लिए configure कर सकते हैं, ताकि input (*validate*) को `val_json_bytes` के साथ और output (*serialize*) को `ser_json_bytes` के साथ handle किया जा सके।

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,19:26,29,44:46] hl[23:26] *}
