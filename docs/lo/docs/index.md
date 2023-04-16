
{!../../../docs/missing-translation.md!}


<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>ເຄື່ອງມື FastAPI , ປະສິດທິພາບສູງ, ຮຽນງ່າຍ, ສ້າງໄດ້ໄວ, ພ້ອມສຳລັບ production</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/tiangolo/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/tiangolo/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**ເອກະສານ**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Source Code**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI ແມ່ນທັນສະໄໝ, ໄວ (ປະສິດທິພາບສູງ), ເຄື່ອງມືເວັບສຳລັບພັດທະນາ APIs ດ້ວຍພາສາ Python ເວີຊັ່ນ 3.7 ຂຶ້ນໄປ ອີງຕາມມາດຕະຖານຂອງ Python type hints.

ຄຸນສົມບັດຫຼັກປະກອບມີ:

* **ໄວ**: ປະສິດທິພາບສູງຫຼາຍ, on par with **NodeJS** and **Go** (thanks to Starlette and Pydantic). [One of the fastest Python frameworks available](#performance).
* **ສ້າງໄດ້ໄວ**: ເພີ່ມຄວາມໄວໃນການພັດທະນາຄຸນສົມບັດປະມັນ 200% ເຖິງ 300%. *
* **ບັນຫາໜ້ອຍ**: ຫຼຸດຜ່ອນປະມານ 40% ຂອງຄົນ (ຜູ້ພັດທະນາ) ທີອາດກໍໃຫ້ເກີດຄວາມຜິດພາດ. *
* **ໃຊ້ງານງ່າຍ**: ມີ editor ທີຄັກ. <abbr title="also known as auto-complete, autocompletion, IntelliSense">ຊ່ອຍຕື່ມຄໍາ</abbr> ທຸກບ່ອນ. ການຫາຂໍ້ຜິດພາດໃຊ້ເວລາໜ້ອຍລົງ.
* **ງ່າຍ**: ຖືກອອກແບບມາໃຫ້ໃຊ້ງານ ແລະ ຮຽນຮູ້ງ່າຍ. ໃຊ້ເວລາໜ້ອຍໃນການອ່ານເອກະສານ.
* **ສັ້ນ**: ຫຼຸດຜ່ອນການຊໍ້າກັນຂອງໂຄດ. ຄຸນສົມບັດຫຼາຍຈາກການປະກາດແຕ່ລະພາລາມີເຕີ. ຂໍ້ຜິດພາດໜ້ອຍ.
* **ແຂງແກ່ນ**: ຮັບໂຄດທີພ້ອມສຳລັບວຽກ production. ພ້ອມເອກະສານແບບໂຕ້ຕອບໂດຍອັດຕະໂນມັດ.
* **ຕາມມາດຕະຖານ**: ອີງໃສ່ (ແລະເຂົ້າກັນໄດ້ຢ່າງເຕັມສ່ວນກັບ) ມາດຕະຖານທີເປີດສໍາລັບ APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (ໃນເມືອກ່ອນເອີ້ນວ່າ Swagger) ແລະ <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* ຄາດຄະເນໂດຍອີງໃສ່ການທົດສອບໃນທີມພັດທະນາພາຍໃນ, ສ້າງ production application</small>

## ຜູ້ສະໜັບສະໜູນ

<!-- sponsors -->

{% if sponsors %}
{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">ຜູ້ສະໜັບສະໜຸນອື່ນໆ</a>

## ຄວາມຄິດເຫັນ

"_[...] ຂ້ອຍໃຊ້ **FastAPI** ຫຼາຍໃນທຸກມື້ນີ້. [...] ຂ້ອຍກຳລັງມີແຜນຈະໃຊ້ກັບທີມ  **ML services ທັງໝົດທີ Microsoft**. ບາງສ່ວນແມ່ນໄດ້ໃຊ້ເຂົ້າກັບ core ຂອງຜະລິດຕະພັນ **Windows** ແລະ ຜະລິດຕະພັນ **Office**._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_ພວກເຮົາໄດ້ຮອງຮັບ **FastAPI** library ເພື່ອສ້າງເຊີເວີ **REST**  ທີສາມາດ query ເພື່ອຮັບ **ການຄາດເດົາ**ໄດ້. [ສຳລັບ Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, ແລະ Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** ຍິນດີທີຈະປະກາດ open-source ໂຄ່ງການ **ການຄຸ້ມຄອງວິກິດການ** ຂອງພວກເຮົາ: **ດ່ວນ**! [ສ້າງດ້ວຍ **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_ຂ້ອຍຕື່ນເຕັ້ນຫຼາຍກັບ **FastAPI**. ມັນມ່ວນຫຼາຍ!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> ນັກຈັດ podcast</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_ເວົ້າຕາມຄວາມເປັນຈິງ, ສິ່ງທີເຈົ້າສ້າງແມ່ນມີຄວາມເຂັ້ມແຂງ ແລະ ສ່ວນງາມຫຼາຍ. ໃນຫຼາຍໆດ້ານ, ມັນເປັນສິ່ງທີຂ້ອຍຕ້ອງການ ຢາກໃຫ້ **Hug** ເປັນ - ມັນເປັນແຮງບັນດານໃຈແທ້ໆ ທີ່ໄດ້ເຫັນໃຜບາງຄົນສ້າງມັນຂຶ້ນມາ._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong>ຜູ້ສ້າງ <a href="https://www.hug.rest/" target="_blank">Hug</a></strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_ຖ້າທ່ານຕ້ອງການຮຽນຮູ້ **ເຄື່ອງມືສະໄໝໃໝ່** ສຳລັບການສ້າງ REST API, ລອງເບິ່ງ **FastAPI** [...] ມັນໄວ, ໃຊ້ງານງ່າຍ ແລະ ຮຽນຮູ້ງ່າຍ [...]_"

"_ພວກເຮົາໄດ້ປ່ຽນມາໃຊ້ **FastAPI** ສຳລັບ **APIs** ຂອງພວກເຮົາ [...] ຂ້ອຍຄິດວ່າເຈົ້າຈະມັກມັນ [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> ຜູ້ກໍ່ຕັ້ງ - <a href="https://spacy.io" target="_blank">spaCy</a> ຜູ້ສ້າງ </strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"_ຖ້າໃຜກຳລັງຫາການສ້າງ Python API ທີໃຊ້ງານແທ້, ຂ້ອຍຂໍແນະນຳ **FastAPI** ເປັນຢ່າງສູງ. ມັນ **ຖືກອອກແບບມາຢ່າງດີ**, **ງ່າຍໃນການໃຊ້ງານ** ແລະ **ງ່າຍໃນການຂະຫຍາຍ**, ມັນໄດ້ເປັນ **ຕົວເລືອກຫຼັກ** ໃນການພັດທະນາ API ຂອງພວກເຮົາ ແລະ ມັນກຳລັງຂັບເຄື່ອນລະບົບອັດຕະໂນມັດ ແລະ ບໍລິການຕ່າງໆເຊັ່ນ: Virtual TAC Engineer ຂອງພວກເຮົາ._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, FastAPI ຂອງ CLIs

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

ຖ້າທ່ານກຳລັງສ້າງ <abbr title="Command Line Interface">CLI</abbr> app ເພື່ອໄປໃຊ້ໃນ terminal ແທນທີຈະໃຊ້ web API, ກວດເບິ່ງ<a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** ແມ່ນນ້ອງສາວຂອງ FastAPI . ແລະ ມັນມີຈຸດປະສົງທີຈະເປັນ **FastAPI ສຳລັບ CLIs**. ⌨️ 🚀

## ຄວາມຕ້ອງການ

Python 3.7+

FastAPI ຢືນຢູ່ເທິງບ່າຂອງຍັກໃຫຍ່:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> ສຳລັບພາກສ່ວນຂອງເວັບ.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> ສຳລັບພາກສ່ວນຂອງຂໍ້ມູນ.

## ການຕິດຕັ້ງ

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

ທ່ານຈະຕ້ອງມີເຊີເວີ ASGI ສຳລັບ production ຕົວຢ່າງ <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> ຫຼື <a href="https://github.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

## ຕົວຢ່າງ

### ສ້າງມັນ

* ສ້າງຟາຍໃໝ່ `main.py` ດ້ວຍ:

```Python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>ຫຼື ໃຊ້ <code>async def</code>...</summary>

ຖ້າເຈົ້າຂຽນໂຄດດ້ວຍ `async` / `await`, ໃຊ້ `async def`:

```Python hl_lines="9  14"
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

**ໝາຍເຫດ**:

ຖ້າເຈົ້າບໍ່ຮູ້, ກວດໃນຫົວຂໍ້ _"ຟ້າວຫວາ?"_  ກ່ຽວກັບ <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` ແລະ `await` ໃນເອກະສານ</a>.

</details>

### ແລ່ນມັນ

ແລ່ນເຊີເວີດ້ວຍ:

<div class="termy">

```console
$ uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>ກ່ຽວກັບຄຳສັ່ງ <code>uvicorn main:app --reload</code>...</summary>

ຄຳສັ່ງ `uvicorn main:app` ໝາຍເຖິງ:

* `main`: ຟາຍ `main.py` (the Python "module").
* `app`: object ຖືກສ້າງໃນຟາຍ `main.py` ໃນແຖວ `app = FastAPI()`.
* `--reload`: ເຮັດໃຫ້ server ແລ່ນໃໝ່ ຫຼັງຈາກໂຄດມີການປ່ຽນແປງ. ໃຊ້ສະເພາະຕອນພັດທະນາ.

</details>

### ກວດມັນ

ເປີດບາວເຊີຂອງທ່ານທີ່ <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

ທ່ານຈະເຫັນຂໍ້ຄວາມ JSON ແຈ້ງກັບ ດັ່ງນີ້:

```JSON
{"item_id": 5, "q": "somequery"}
```

ທ່ານໄດ້ສ້າງ API ທີ:

* ຮັບ HTTP requests ໃນ the _paths_ `/` ແລະ `/items/{item_id}`.
* ທັງສອງ _paths_ ຮັບ `GET` <em>operations</em> (ເອີ້ນກັນວ່າ HTTP _methods_).
* _path_ `/items/{item_id}` ມີ a _path parameter_ `item_id` ທີຄວນເປັນ `int`.
* _path_ `/items/{item_id}` ມີຕົວເລືອກ `str` _query parameter_ `q`.

### ເອກະສານ API ແບບຕອບໂຕ້

ຕອນນີ້ໃຫ້ໄປທີ <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

ທ່ານຈະເຫັນ ເອກະສານ API ແບບໂຕ້ຕອບໂດຍອັດຕະໂນມັດ (ໃຫ້ບໍລິການໂດຍ <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### ເອກະສານ API ແບບໃກ້ຄຽງ

ຕອນນີ້, ໄປທີ <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

ທ່ານຈະເຫັນ ເອກະສານ API ແບບໃກ້ຄຽງໂດຍອັດຕະໂນມັດ  (ໃຫ້ບໍລິການໂດຍ <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## ຕົວຢ່າງຂອງການອັບເກດ

ຕອນນີ້ແກ້ໄຂຟາຍ `main.py` ເພື່ອຮັບ body ຈາກ `PUT` request.

ປະກາດ body ໂດຍໃຊ້ Python types ມາດຕະຖານ, ຂອບໃຈ Pydantic.

```Python hl_lines="4  9-12  25-27"
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

ເຊີເວີຄວນຈະໂຫຼດໃໝ່ໂດຍອັດຕະໂນມັດ (ເພາະວ່າທ່ານໄດ້ເພີ່ມ `--reload` ໃນຊຸດຄຳສັ່ງຂອງ `uvicorn` ດ້ານເທິງ).

### ອັບເກດເອກະສານ API ແບບຕອບໂຕ້

ຕອນນີ້ໄປທີ <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* ເອກະສານ API ແບບຕອບໂຕ້ຈະອັບເດດໂດຍອັດຕະໂນມັດ, ລວມທັງ body ໃໝ່:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* ຄິກໃສ່ປຸ່ມ "Try it out", ມັນອະນຸຍາດໃຫ້ເຈົ້າໃສ່ parameters ແລະ ຕອບໂຕ້ໂດຍກົງກັບ API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* ຈາກນັ້ນຄິກໃສ່ປຸ່ມ "Execute" , ໜ້າໂຕ້ຕອຍຜູ້ໃຊ້ ຈະສື່ສານກັບ API ຂອງທ່ານ, ສົ່ງ parameters, ຮັບ ຜົນລັບ ແລະ ສະແດງເທິງໜ້າຈໍ:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### ອັບເກດເອກະສານ API ແບບໃກ້ຄຽງ

ຕອນນີ້, ໄປທີ <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* ເອກະສານ API ແບບໃກ້ຄຽງ ຈະສະທ້ອນ query parameter ໃໝ່ ແລະ body:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### ສະຫຼຸບ

ສະຫຼຸບ, ທ່ານປະກາດ **ເທື່ອດຽວ** ປະເພດຂອງ parameter , body, ແລະ ອື່ນໆ. ເປັນ parameters ຂອງ function.

ທ່ານເຮັດໄດ້ຍ້ອນມາດຕະຖານປະເພດຂອງພາສາ Python ສະໄໝໃໝ່.

ທ່ານບໍ່ຈຳເປັນຕ້ອງຮຽນ syntax ໃໝ່, method ຫຼື class ຂອງ library ສະເພາະ, ແລະ ອື່ນໆ.

ພຽງແຕ່ມາດຕະຖານຂອງພາສາ  **Python ເວີຊັ່ນ 3.7 ຂຶ້ນໄປ**.

ຕົວຢ່າງ, ສຳລັບປະເພດ `int`:

```Python
item_id: int
```

ຫຼື ສຳລັບ model `Item` ທີຊັບຊ້ອນ :

```Python
item: Item
```

...ແລະ ຍ້ອນການປະກາດພຽງເທື່ອດຽວທ່ານຈະໄດ້ຮັບ:

* ສະໜັບສະໜູນ Editor, ລວມກັບ:
    * ການຕື່ມຄຳອັດຕະໂນມັດ.
    * ກວດປະເພດ.
* ການກວດສອບຂໍ້ມູນ:
    * ສະແດງບັນຫາທີຊັດເຈນຖ້າຂໍ້ມູນບໍ່ຖືກຕ້ອງໂດຍອັດຕະໂນມັດ.
    * ກວດສອບຮອດ JSON object ໃນຊັ້ນທີເລິກໆ.
* <abbr title="ທີຮູ້ຈັກກັນ ຕົວຢ່າງ: serialization, parsing, marshalling">ການປ່ຽນຂໍ້ມູນ</abbr> ຂອງຂໍ້ມູນທີປ້ອນເຂົ້າມາ: ມາຈາກ network ໄປຫາຂໍ້ມູນ ແລະ ປະເພດ ຂອງພາສາ Python. ອ່ານຈາກ:
    * JSON.
    * Path parameters.
    * Query parameters.
    * Cookies.
    * Headers.
    * Forms.
    * Files.
* <abbr title="ທີຮູ້ຈັກກັນ ຕົວຢ່າງ: serialization, parsing, marshalling">ການປ່ຽນຂໍ້ມູນ</abbr> ຂອງຂໍ້ມູນທີສົ່ງອອກ: ແປງ ຂໍ້ມູນ ແລະ ປະເພດຂອງພາສາ Python ໄປຫາ ຂໍ້ມູນ network  (ໃນຮູບແບບ JSON):
    * ແປງປະເພດຂອງພາສາ Python (`str`, `int`, `float`, `bool`, `list`, ແລະ ອື່ນໆ).
    * `datetime` objects.
    * `UUID` objects.
    * Database models.
    * ...ແລະ ອື່ນໆ ອີກຫຼາຍ.
* ເອກະສານ API ແບບຕອບໂຕ້ອັດຕະໂນມັດ, ປະກອບມີ 2 ແບບ:
    * Swagger UI.
    * ReDoc.

---

ກັບຄືນໄປຫາໂຄດຕົວຢ່າງທີ່ຜ່ານມາ, **FastAPI** ຈະ:

* ກວດສອບວ່າ `item_id` ຢູ່ໃນ path ສຳລັບ `GET` ແລະ `PUT` requests.
* ກວດສອບວ່າມີ `item_id` ເປັນປະເພດ `int` ສຳລັບ `GET` ແລະ `PUT` requests.
    * ຖ້າບໍ່ມີ, ຜູ້ໃຊ້ຈະເຫັນຂໍ້ຜິດພາດທີເປັນປະໂຫຍດ ແລະ ຊັດເຈນ.
* ກວດສອບວ່າມີ query parameter ທີມີ ຫຼື ບໍ່ມີກະໄດ້ ຊື່ວ່າ `q` (as in `http://127.0.0.1:8000/items/foo?q=somequery`) ສຳລັບ `GET` requests.
    * ເນື່ອງຈາກ `q` parameter ຖືກປະກາດດ້ວຍ `= None`,ໝາຍຄວາມວ່າມັນຈະມີ ຫຼື ບໍ່ມີກະໄດ້.
    * ຖ້າບໍ່ມີ `None` ມັນຈະເປັນທີຕ້ອງການ (ຄືກັນກັບໃນ body ໃນຕົວຢ່າງກັບ `PUT`).
* ສຳລັບ `PUT` requests ໄປຫາ `/items/{item_id}`, ອ່ານ body ເປັນ JSON:
    * ກວດວ່າມັນມີ attribute ທີຕ້ອງການ `name` ເປັນປະເພດ `str`.
    * ກວດວ່າມັນມີ attribute ທີຕ້ອງການ `price` ເປັນປະເພດ `float`.
    * ກວດວ່າມັນມີ attribute ທີມີກະໄດ້ `is_offer`, ຄວນເປັນປະເພດ  `bool`, ຖ້າປະກົດ.
    * ທັງໝົດນີ້ແມ່ນເຮັດວຽກໄດ້ກັບ JSON objects ທີເລິກໆ ແລະ ຊັບຊ້ອນ.
* ແປງ ຈາກ ແລະ ໄປຫາ JSON ໂດຍອັດຕະໂນມັດ.
* ເອກະສານທຸກຢ່າງດ້ວຍ OpenAPI, ທີສາມາດໃຊ້ໂດຍ:
    * ລະບົບເອກະສານແບບໂຕ້ຕອບ.
    * ລະບົບສ້າງໂຄດໂດຍອັດຕະໂນມັດໃຫ້ຜຸ້ໃຊ້, ສຳລັບຫຼາຍພາສາ.
* ສະໜອງ 2 ຮູບແບບເອກະສານແບບຕອບໂຕ້ຜ່ານ web interfaces ໂດຍກົງ.

---

ພວກເຮົາພຽງແຕ່ໄດ້ລອງໜ້ອຍດຽວ, ແຕ່ທ່ານໄດ້ຮັບແນວຄິດວ່າວິທີການເຮັດວຽກມັນເປັນແນວໃດແລ້ວ.

ລອງປ່ຽນແຖວນີ້ກັບ:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...ຈາກ:

```Python
        ... "item_name": item.name ...
```

...ເປັນ:

```Python
        ... "item_price": item.price ...
```

...ແລະ ເບິ່ງວ່າ editor ຂອງທ່ານຈະ auto-complete attribute ແລະ ຮູ້ຈັກປະເພດຂອງພວກມັນໄດ້ແນວໃດ:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

ສຳລັບຕົວຢ່າງທີສົມບູນພ້ອມກັບ feature ເພີ່ມເຕີມ, ເບິ່ງ <a href="https://fastapi.tiangolo.com/tutorial/">ບົດຮຽນ - ຄູ່ມືຜູ້ໃຊ້</a>.

**ບອກກ່ອນ**: ບົດຮຽນ - ຄູ່ມືຜູ້ໃຊ້ປະກອບມີ:

* ການປະກາດ **parameters** ຈາກຄົນລະບ່ອນເຊັ່ນ: **headers**, **cookies**, **form fields** ແລະ **files**.
* ວິທີການຕັ້ງຄ່າ **validation constraints** ເປັນ `maximum_length` ຫຼື `regex`.
* ລະບົບ **<abbr title="ດັ່ງທີຮູ້ກັນໃນ components, resources, providers, services, injectables">Dependency Injection</abbr>** ທີມີປະສິດທິພາບສູງ ແລະ ໃຊ້ງານງ່າຍ .
* ຄວາມປອດໄພ ແລະ ການຢັ້ງຢືນຕົວຕົນ, ລວມໄປເຖິງການສະໜັບສະໜູນຈາກ **OAuth2** ກັບ **JWT tokens** ແລະ **HTTP Basic** auth.
* ເຕັກນິກຂັ້ນສູງຕື່ມ (ແຕ່ງ່າຍຄືກັນ) ສຳລັບການປະກາດ **JSON models ທີຊັບຊ້ອນ** (ຂອບໃຈ Pydantic).
* ຕໍ່ກັບ **GraphQL**  ດ້ວຍ <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> ແລະ library ອື່ນ.
* ຄຸນສົມບັດພິເສດອີກຫຼາກຫຼາຍ (ຂອບໃຈ Starlette) ດັ່ງນີ້:
    * **WebSockets**
    * ການທົດສອບທີງ່າຍຫຼາຍໂດຍໃຊ້ HTTPX ແລະ `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...ແລະ ອື່ນໆ.

## ປະສິດທິພາບ

ຕົວຊີ້ວັດອິດສະຫຼະ TechEmpower ສະແດງໃຫ້ເຫັນວ່າ **FastAPI** application ແລ່ນພາຍໃຕ້ Uvicorn ໃນຮູບແບບຂອງ
 <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">ໜຶ່ງໃນເຄື່ອງມື Python ທີໄວທີສຸດທີມີຢູ່</a>, ເປັນຮອງແຕ່ Starlette ແລະ Uvicorn ຂອງພວກເຂົາ (ໃຊ້ພາຍໃນໂດຍ FastAPI). (*)

ເພື່ອທຳຄວາມເຂົ້າໃຈກັບມັນຫຼາຍຂຶ້ນ, ເບິ່ງຫົວຂໍ້ <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">ເກນວັດມາດຕະຖານ</a>.

## ທາງເລືອກ Dependencies

ໃຊ້ໂດຍ Pydantic:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - for faster JSON <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - for email validation.

ໃຊ້ໂດຍ Starlette:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - Required if you want to use the `TestClient`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Required if you want to use the default template configuration.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Required if you want to support form <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>, with `request.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Required for `SessionMiddleware` support.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Required for Starlette's `SchemaGenerator` support (you probably don't need it with FastAPI).
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Required if you want to use `UJSONResponse`.

ໃຊ້ໂດຍ FastAPI / Starlette:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - for the server that loads and serves your application.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Required if you want to use `ORJSONResponse`.

ທ່ານສາມາດຕິດຕັ້ງທັງໝົດດ້ວຍການໃຊ້ຊຸດຄຳສັ່ງນີ້ `pip install "fastapi[all]"`.

## ລາຍເຊັນ

ໂຄ່ງການນີ້ຢູ່ມີລາຍເຊັນພາຍໃຕ້ເງື່ອນໄຂຂອງລາຍເຊັນ MIT.
