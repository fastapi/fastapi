# Request को सीधे इस्तेमाल करना { #using-the-request-directly }

अब तक, आप request के जिन हिस्सों की ज़रूरत है, उन्हें उनके types के साथ declare करते रहे हैं।

Data लेना:

* path से parameters के रूप में।
* Headers।
* Cookies।
* आदि।

और ऐसा करके, **FastAPI** उस data को validate कर रहा है, उसे convert कर रहा है और आपकी API के लिए documentation अपने-आप generate कर रहा है।

लेकिन ऐसी स्थितियाँ होती हैं जहाँ आपको `Request` object को सीधे access करने की ज़रूरत हो सकती है।

## `Request` object के बारे में विवरण { #details-about-the-request-object }

क्योंकि **FastAPI** असल में नीचे से **Starlette** है, जिसके ऊपर कई tools की एक layer है, इसलिए जब ज़रूरत हो, आप Starlette के [`Request`](https://www.starlette.dev/requests/) object को सीधे इस्तेमाल कर सकते हैं।

इसका मतलब यह भी होगा कि अगर आप `Request` object से सीधे data लेते हैं (उदाहरण के लिए, body पढ़ते हैं), तो FastAPI उसे validate, convert या document नहीं करेगा (OpenAPI के साथ, automatic API user interface के लिए)।

हालाँकि कोई भी अन्य parameter जो सामान्य रूप से declare किया गया हो (उदाहरण के लिए, Pydantic model के साथ body), वह फिर भी validate, convert, annotate आदि होगा।

लेकिन कुछ विशिष्ट मामले हैं जहाँ `Request` object लेना उपयोगी होता है।

## `Request` object को सीधे इस्तेमाल करें { #use-the-request-object-directly }

मान लीजिए कि आप अपनी *path operation function* के अंदर client का IP address/host लेना चाहते हैं।

इसके लिए आपको request को सीधे access करना होगा।

{* ../../docs_src/using_request_directly/tutorial001_py310.py hl[1,7:8] *}

`Request` type वाले *path operation function* parameter को declare करके, **FastAPI** जान जाएगा कि उस parameter में `Request` pass करना है।

/// tip | सुझाव

ध्यान दें कि इस मामले में, हम request parameter के साथ एक path parameter declare कर रहे हैं।

इसलिए, path parameter extract किया जाएगा, validate किया जाएगा, specified type में convert किया जाएगा और OpenAPI के साथ annotate किया जाएगा।

इसी तरह, आप किसी भी अन्य parameter को सामान्य रूप से declare कर सकते हैं, और साथ ही `Request` भी प्राप्त कर सकते हैं।

///

## `Request` documentation { #request-documentation }

आप [`Request` object के बारे में official Starlette documentation site](https://www.starlette.dev/requests/) पर और विवरण पढ़ सकते हैं।

/// note | तकनीकी विवरण

आप `from starlette.requests import Request` भी इस्तेमाल कर सकते हैं।

**FastAPI** इसे सीधे सिर्फ आपकी, developer की, सुविधा के लिए प्रदान करता है। लेकिन यह सीधे Starlette से आता है।

///
