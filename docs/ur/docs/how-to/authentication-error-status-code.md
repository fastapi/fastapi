# پرانے 403 Authentication Error Status Codes استعمال کریں { #use-old-403-authentication-error-status-codes }

FastAPI ورژن `0.122.0` سے پہلے، جب integrated security utilities authentication ناکام ہونے پر client کو error واپس کرتی تھیں، تو وہ HTTP status code `403 Forbidden` استعمال کرتی تھیں۔

FastAPI ورژن `0.122.0` سے شروع کرتے ہوئے، وہ زیادہ مناسب HTTP status code `401 Unauthorized` استعمال کرتی ہیں، اور HTTP specifications کی پیروی کرتے ہوئے response میں ایک معقول `WWW-Authenticate` header واپس کرتی ہیں، [RFC 7235](https://datatracker.ietf.org/doc/html/rfc7235#section-3.1)، [RFC 9110](https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized)۔

لیکن اگر کسی وجہ سے آپ کے clients پرانے رویے پر منحصر ہیں، تو آپ اپنی security classes میں `make_not_authenticated_error` method کو override کر کے واپس پرانے رویے پر جا سکتے ہیں۔

مثال کے طور پر، آپ `HTTPBearer` کی ایک subclass بنا سکتے ہیں جو default `401 Unauthorized` error کی بجائے `403 Forbidden` error واپس کرے:

{* ../../docs_src/authentication_error_status_code/tutorial001_an_py310.py hl[9:13] *}

/// tip | مشورہ

نوٹ کریں کہ function exception instance واپس کرتا ہے، اسے raise نہیں کرتا۔ Raise کرنا باقی اندرونی کوڈ میں ہوتا ہے۔

///
