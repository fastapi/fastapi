# حسب ضرورت Response Classes - File، HTML، Redirect، Streaming، وغیرہ

کئی حسب ضرورت response classes دستیاب ہیں جنہیں آپ ایک instance بنا کر اپنی *path operations* سے براہ راست واپس کر سکتے ہیں۔

اس کے بارے میں مزید پڑھیں [FastAPI دستاویزات میں حسب ضرورت Response - HTML، Stream، File، اور دیگر](https://fastapi.tiangolo.com/advanced/custom-response/)۔

آپ انہیں براہ راست `fastapi.responses` سے import کر سکتے ہیں:

```python
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    ORJSONResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
    StreamingResponse,
    UJSONResponse,
)
```

## FastAPI Responses

کچھ حسب ضرورت FastAPI response classes تھیں جو JSON کی کارکردگی کو بہتر بنانے کے لیے بنائی گئی تھیں۔

تاہم، اب یہ deprecated ہو چکی ہیں کیونکہ اب آپ [Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/) استعمال کر کے بہتر کارکردگی حاصل کر سکتے ہیں۔

اس طرح، Pydantic ڈیٹا کو Rust کی طرف JSON bytes میں serialize کرے گا، جو ان حسب ضرورت JSON responses سے بہتر کارکردگی فراہم کرے گا۔

اس کے بارے میں مزید پڑھیں [حسب ضرورت Response - HTML، Stream، File، اور دیگر - `orjson` یا Response Model](https://fastapi.tiangolo.com/advanced/custom-response/#orjson-or-response-model)۔

::: fastapi.responses.UJSONResponse
    options:
        members:
            - charset
            - status_code
            - media_type
            - body
            - background
            - raw_headers
            - render
            - init_headers
            - headers
            - set_cookie
            - delete_cookie

::: fastapi.responses.ORJSONResponse
    options:
        members:
            - charset
            - status_code
            - media_type
            - body
            - background
            - raw_headers
            - render
            - init_headers
            - headers
            - set_cookie
            - delete_cookie

## Starlette Responses

آپ ان سب کے بارے میں مزید پڑھ سکتے ہیں [FastAPI دستاویزات میں حسب ضرورت Response](https://fastapi.tiangolo.com/advanced/custom-response/) اور [Starlette دستاویزات میں Responses](https://starlette.dev/responses/)۔

::: fastapi.responses.FileResponse
    options:
        members:
            - chunk_size
            - charset
            - status_code
            - media_type
            - body
            - background
            - raw_headers
            - render
            - init_headers
            - headers
            - set_cookie
            - delete_cookie

::: fastapi.responses.HTMLResponse
    options:
        members:
            - charset
            - status_code
            - media_type
            - body
            - background
            - raw_headers
            - render
            - init_headers
            - headers
            - set_cookie
            - delete_cookie

::: fastapi.responses.JSONResponse
    options:
        members:
            - charset
            - status_code
            - media_type
            - body
            - background
            - raw_headers
            - render
            - init_headers
            - headers
            - set_cookie
            - delete_cookie

::: fastapi.responses.PlainTextResponse
    options:
        members:
            - charset
            - status_code
            - media_type
            - body
            - background
            - raw_headers
            - render
            - init_headers
            - headers
            - set_cookie
            - delete_cookie

::: fastapi.responses.RedirectResponse
    options:
        members:
            - charset
            - status_code
            - media_type
            - body
            - background
            - raw_headers
            - render
            - init_headers
            - headers
            - set_cookie
            - delete_cookie

::: fastapi.responses.Response
    options:
        members:
            - charset
            - status_code
            - media_type
            - body
            - background
            - raw_headers
            - render
            - init_headers
            - headers
            - set_cookie
            - delete_cookie

::: fastapi.responses.StreamingResponse
    options:
        members:
            - body_iterator
            - charset
            - status_code
            - media_type
            - body
            - background
            - raw_headers
            - render
            - init_headers
            - headers
            - set_cookie
            - delete_cookie
