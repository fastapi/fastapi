# WSGI شامل کرنا - Flask, Django, اور دیگر { #including-wsgi-flask-django-others }

آپ WSGI ایپلیکیشنز کو mount کر سکتے ہیں جیسا کہ آپ نے [Sub Applications - Mounts](sub-applications.md) اور [Proxy کے پیچھے](behind-a-proxy.md) میں دیکھا۔

اس کے لیے، آپ `WSGIMiddleware` استعمال کر سکتے ہیں اور اسے اپنی WSGI ایپلیکیشن، مثلاً Flask، Django وغیرہ کو wrap کرنے کے لیے استعمال کر سکتے ہیں۔

## `WSGIMiddleware` استعمال کرنا { #using-wsgimiddleware }

/// info | معلومات

اس کے لیے `a2wsgi` انسٹال کرنا ضروری ہے، مثال کے طور پر `pip install a2wsgi` سے۔

///

آپ کو `a2wsgi` سے `WSGIMiddleware` import کرنا ہوگا۔

پھر WSGI (مثلاً Flask) ایپ کو middleware کے ساتھ wrap کریں۔

اور پھر اسے ایک path کے نیچے mount کریں۔

{* ../../docs_src/wsgi/tutorial001_py310.py hl[1,3,23] *}

/// note | نوٹ

پہلے، `fastapi.middleware.wsgi` سے `WSGIMiddleware` استعمال کرنے کی سفارش کی جاتی تھی، لیکن اب یہ deprecated ہے۔

اس کی بجائے `a2wsgi` پیکیج استعمال کرنے کی تجویز دی جاتی ہے۔ استعمال کا طریقہ وہی رہتا ہے۔

بس یقینی بنائیں کہ `a2wsgi` پیکیج انسٹال ہے اور `WSGIMiddleware` کو `a2wsgi` سے درست طریقے سے import کریں۔

///

## چیک کریں { #check-it }

اب، `/v1/` path کے نیچے ہر request Flask ایپلیکیشن کے ذریعے ہینڈل ہوگی۔

اور باقی **FastAPI** کے ذریعے ہینڈل ہوں گی۔

اگر آپ اسے چلائیں اور [http://localhost:8000/v1/](http://localhost:8000/v1/) پر جائیں تو آپ کو Flask کا response نظر آئے گا:

```txt
Hello, World from Flask!
```

اور اگر آپ [http://localhost:8000/v2](http://localhost:8000/v2) پر جائیں تو آپ کو FastAPI کا response نظر آئے گا:

```JSON
{
    "message": "Hello World"
}
```
