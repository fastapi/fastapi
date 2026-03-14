# Status Codes

آپ `status` module کو `fastapi` سے import کر سکتے ہیں:

```python
from fastapi import status
```

`status` براہ راست Starlette کی طرف سے فراہم کیا گیا ہے۔

اس میں نامزد constants (variables) کا ایک گروپ ہے جن کی قدریں integer status codes ہیں۔

مثال کے طور پر:

* 200: `status.HTTP_200_OK`
* 403: `status.HTTP_403_FORBIDDEN`
* وغیرہ۔

یہ آپ کی app میں HTTP (اور WebSocket) status codes تک فوری رسائی کے لیے آسان ہو سکتا ہے، نام کے لیے autocompletion استعمال کرتے ہوئے بغیر integer status codes یاد رکھنے کی ضرورت کے۔

اس کے بارے میں مزید پڑھیں [FastAPI دستاویزات میں Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)۔

## مثال

```python
from fastapi import FastAPI, status

app = FastAPI()


@app.get("/items/", status_code=status.HTTP_418_IM_A_TEAPOT)
def read_items():
    return [{"name": "Plumbus"}, {"name": "Portal Gun"}]
```

::: fastapi.status
