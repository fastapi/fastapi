# WSGI शामिल करना - Flask, Django, अन्य { #including-wsgi-flask-django-others }

आप WSGI applications को mount कर सकते हैं, जैसा आपने [Sub Applications - Mounts](sub-applications.md), [Proxy के पीछे](behind-a-proxy.md) में देखा।

इसके लिए, आप `WSGIMiddleware` का उपयोग कर सकते हैं और इसे अपनी WSGI application को wrap करने के लिए इस्तेमाल कर सकते हैं, उदाहरण के लिए, Flask, Django, आदि।

## `WSGIMiddleware` का उपयोग करना { #using-wsgimiddleware }

/// note | नोट

इसके लिए `a2wsgi` install करना required है, उदाहरण के लिए `pip install a2wsgi` के साथ।

///

आपको `a2wsgi` से `WSGIMiddleware` import करना होगा।

फिर WSGI (जैसे Flask) app को middleware के साथ wrap करें।

और फिर उसे किसी path के अंतर्गत mount करें।

{* ../../docs_src/wsgi/tutorial001_py310.py hl[1,3,23] *}

/// note | नोट

पहले, `fastapi.middleware.wsgi` से `WSGIMiddleware` का उपयोग करने की सलाह दी जाती थी, लेकिन अब यह deprecated है।

इसके बजाय `a2wsgi` package का उपयोग करने की सलाह दी जाती है। उपयोग वही रहता है।

बस यह सुनिश्चित करें कि आपके पास `a2wsgi` package install है और आप `a2wsgi` से `WSGIMiddleware` को सही ढंग से import करते हैं।

///

## इसे जाँचें { #check-it }

अब, path `/v1/` के अंतर्गत हर request को Flask application द्वारा handle किया जाएगा।

और बाकी को **FastAPI** द्वारा handle किया जाएगा।

यदि आप इसे run करते हैं और [http://localhost:8000/v1/](http://localhost:8000/v1/) पर जाते हैं, तो आपको Flask से response दिखाई देगा:

```txt
Hello, World from Flask!
```

और यदि आप [http://localhost:8000/v2](http://localhost:8000/v2) पर जाते हैं, तो आपको FastAPI से response दिखाई देगा:

```JSON
{
    "message": "Hello World"
}
```
