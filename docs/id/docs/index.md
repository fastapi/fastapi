
{!../../../docs/missing-translation.md!}


<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, performa tinggi, mudah dipelajari, cepat menulis kode, siap untuk produksi</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://codecov.io/gh/tiangolo/fastapi" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/tiangolo/fastapi?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

---

**Documentation**: <a href="https://fastapi.tiangolo.com/id" target="_blank">https://fastapi.tiangolo.com/id</a>

**Source Code**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI adalah web framework untuk membangun beragam API dengan menggunakan Python 3.6+ berdasarkan Python type hints yang baku.

Fitur-fitur yang tersedia antara lain:

* **Fast**: Memiliki performa yang sangat tinggi,  **NodeJS** and **Go** (terima kasih untuk Starlette dan Pydantic). [Salah satu dari framework python tercepat yang ada](#performance).

* **Fast to code**: Meningkatkan kecepatan dalam membuat fitur 200% hingga 300%*
* **Fewer bugs**: Mengurangi sekitar 40% kesalahan yang dilakukan develper. *
* **Intuitive**: Dukungan pada editor yang hebat. <abbr title="juga dikenal dengan auto-complete, autocompletion, IntelliSense">Penyelesaian Otomatis</abbr> dimanapun. Lebih sedikit waktu untuk mengidentifikasi bug.
* **Easy**: Di desain agar mudah digunakan dan dipelajari. Lebih sedikit waktu membaca dokumentasi.
* **Short**: Meminimalisir duplikasi kode. Multi fitur dari setiap deklarasi parameter. Lebih sedikt bug.
* **Robust**: Kode yang siap untuk produksi. Dilengkapi dengan dokumentasi interaktif.
* **Standards-based**: Berdasarkan pada (dan kompatibel seluruhnya dengan) standar umum APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (sebelumnya dikenal dengan Swagger) dan <a href="https://json-schema.org/" class="external-link" target="_blank">Schema JSON</a>.

<small>* perkiraan berdasarkan pada banyak tes yang dilakukan oleh tim pengembangan internal, membangun aplikasi-palikasi produksi.</small>

## Sponsors

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

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">Other sponsors</a>

## Opini-opini

"_[...] I'm using **FastAPI** a ton these days. [...] I'm actually planning to use it for all of my team's **ML services at Microsoft**. Some of them are getting integrated into the core **Windows** product and some **Office** products._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_We adopted the **FastAPI** library to spawn a **REST** server that can be queried to obtain **predictions**. [for Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** is pleased to announce the open-source release of our **crisis management** orchestration framework: **Dispatch**! [built with **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_I’m over the moon excited about **FastAPI**. It’s so fun!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Honestly, what you've built looks super solid and polished. In many ways, it's what I wanted **Hug** to be - it's really inspiring to see someone build that._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://www.hug.rest/" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_If you're looking to learn one **modern framework** for building REST APIs, check out **FastAPI** [...] It's fast, easy to use and easy to learn [...]_"

"_We've switched over to **FastAPI** for our **APIs** [...] I think you'll like it [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, FastAPI dari CLIs

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Jika kamu membangun <abbr title="Command Line Interface">CLI</abbr> sebuah aplikasi yang digunakan di terminal daripada API web, silakan lihat <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** adalah "adik" dari FastAPI. Dan memang sengaja dibuat sebagai **CLIs dari FastAPI**. ⌨️ 🚀

## Persyaratan

Python 3.6+

FastAPI berdiri diatas bahu para raksasa:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> untuk bagian web.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> untuk bagian data.

## Instalasi

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Kamu juga akan membutuhkan server ASGI untuk tahap produksi seperti <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> atau <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install uvicorn[standard]

---> 100%
```

</div>

## Contoh

### Membuat

* Buat file `main.py` dengan kode:

```Python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Or use <code>async def</code>...</summary>

If your code uses `async` / `await`, use `async def`:

```Python hl_lines="9  14"
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

**Note**:

If you don't know, check the _"In a hurry?"_ section about <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` and `await` in the docs</a>.

</details>

### Menjalankan

Jalankan server dengan:

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
<summary>About the command <code>uvicorn main:app --reload</code>...</summary>

The command `uvicorn main:app` refers to:

* `main`: the file `main.py` (the Python "module").
* `app`: the object created inside of `main.py` with the line `app = FastAPI()`.
* `--reload`: make the server restart after code changes. Only do this for development.

</details>

### Periksa

Buka browser anda pada <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Kamu akan melihat response JSON sebagai berikut:

```JSON
{"item_id": 5, "q": "somequery"}
```

Kamu telah berhasil membuat API yang memiliki kemampuan dibawah ini:

* Menerima HTTP requests pada _path_ `/` dan _path_  `/items/{item_id}`.
* Kedua _path_ menggunakan <em>operasi</em> `GET` (juga dikenal dengan  _methode_ HTTP).
* _path_  `/items/{item_id}` memiliki sebuah _parameter path_ `item_id` yang merupakan `int`.
* _path_  `/items/{item_id}` memiliki opsional `str` dengan _parameter query_ `q`.

### Dokumentasi API interaktif

Sekarang pergilah menuju  <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Kamu akan melihat dokumentasi API interaktif otomatis (disediakan oleh <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Dokumentasi API alternatif

Sekarang pergilah menuju <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Kamu akan melihat dokumentasi otomatis alternatif (yang disedeiakan oleh <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Contoh Upgrade

Sekarang ubah file `main.py` untuk menerima body dari `PUT` request.

Deklarasikan body menggunakan tipe data dari Python standar, terima kasih untuk Pydantic.

```Python hl_lines="4  9-12  25-27"
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

Server seharusnya melakukan muat ulang otomatis (sebab kamu menambahkan `--reload` kepada perintah `uvicorn` diatas).

### Upgrade dokumentasi interaktif

Sekarang pergilah menuju <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* Dokumentasi API interaktif akan secara otomatis diupdate termasuk bodi yang baru:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Klik tombol "Try it out", untuk membuatmu bisa mengisi parameter dan berinteraksi langsung dengan API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Kemudian klik tombol "Execute" dan tampilan antarmuka akan berkomunikasi langsung dengan API, dan mengirimkan parameter-parameter, dan mendapatakan hasil untuk ditampilkan pada layar:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Upgrade dokumentasi API alternatif

Sekarang pergilah menuju <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* Dokumenasti alternatif juga akan merefleksikan query parameter dan body yang baru:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Ikhtisar

Secara ringkas, kamu mendeklarasikan **satu kali** tipe-tipe parameter, body, dan lain-lain sebagai parameter fungsi.

Kamu melakukannya denga tipe-tipe dari Python modern yang standar.

Kamu tidak harus belajar syntax, metode-metode ataupun class-class baru dari librari tertentu.

Hanya **Python 3.6+** standar.

Sebagai contoh, untuk sebuah `int`:

```Python
item_id: int
```

atau untuk yang lebih kompleks mdel `Item`:

```Python
item: Item
```

...dan dengan satu deklarasi kamu akan mendapatkan:

* Dukungan editor, termasuk:
    * Penyempurnaan (_Completion_).
    * Pengecekan tipe data.
* Validasi data:
    * Error yang otomatis dan jelas ketika data tidak valid.
    * Validasi hingga pada semua obyek JSON bersarang.
* <abbr title="juga dikenal sebagai : serialization, parsing, marshalling">Merubah </abbr> data yang diinput: berasal dari jaringan ke tipe-tipe dan data python. Didapatkan dari:
    * JSON.
    * Path parameters.
    * Query parameters.
    * Cookies.
    * Headers.
    * Forms.
    * Files.
* <abbr title="also known as: serialization, parsing, marshalling">Konversi</abbr> data output: merubah tipe dan data python ke data jaringan (sebagai JSON):
    * Konversi tipe-tipe python (`str`, `int`, `float`, `bool`, `list`, dll).
    * obyek-obyek `datetime`.
    * obyek-obyek `UUID`.
    * Model-model dari database.
    * ...dan masih banyak lagi.
* Dokumentasi API interaktif otomatis, meliputi 2 alternatif tampilan antarmuka pengguna:
    * Swagger UI.
    * ReDoc.

---

Kembali lagi ke contoh kode sebelumnya **FastAPI** akan:

* Mem-validasi bahwa ada sebuah `item_id` pada path request `GET` dan `PUT`.
* Mem-validasi bahwa `item_id` merupakan tipe `int` untuk request `GET` dan `PUT`.
    * Jika hal itu tidak benar, maka klien akan melihat keterangan error yang jeals dan berguna.
* Memeriksa bahwa ada query parameter opsional dengan nama `q` (seperti pada `http://127.0.0.1:8000/items/foo?q=somequery`) untuk request `GET`.
    * Dengan dideklarasikan bahwa parameter `q = None`, maka artinya adalah opsional.
    * Tanpa `None`, maka akan menjadi diperlukan ( seperti pada body pada kasusu request dengan `PUT`).
* Untuk `PUT` request ke `/items/{item_id}`, membaca body sebagai JSON:
    * Memeriksa jika memiliki atribut `name` yang diperlukan, dimana harus merupakan `str`.
    * Periksa jika memiliki atribut `price` yang diperlukan, dimana harus merupakan `float`.
    * Periksa jika memiliki atribut opsional `is_offer`, dimana harus merupakan `bool`, jika ada.
    * Semua hal ini juga akan bekerja pada obyek-obyek JSON bersarang.
* Konversi dari dan ke JSON secara otomatis.
* Mendokumentasikan semua dengan OpenAPI, yang dapat digunakan oleh:
    * Sistem dokumentasi interaktif.
    * Sistem penghasil kode klien secara otomatis, untuk banyak bahasa.
* Menyediakan 2 dokumentasi interaktif pada tampilan web secara langsung.

---

Kita hanya melihat di permukaan, tetapi kamu telah mendapatkan gagasan tentang bagaimana itu semua berkerja.

Cobalah ubah kode pada baris dengan:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...from:

```Python
        ... "item_name": item.name ...
```

...to:

```Python
        ... "item_price": item.price ...
```

...dan lihatlah bagaimana editormu akan melakukan penyelesaian otomatis atribut-atribut dan tahu masing-masing tipenya.

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Untuk contoh yang lebih kompleks termasukfitur-fitur yang lain, lihatlah <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - Pedoman Pengguna</a>.

**Spoiler alert**: Tutorial - pedoman pengguna meliputi:

* Declaration of **parameters** from other different places as: **headers**, **cookies**, **form fields** and **files**.
* Deklarasi dari **parameter-parameter** dari tempat yang berbeda-beda seperti: **headers**, **cookies**, **form fields** dan **files**.
* Bagaimana menge-set **batasan validasi** sebagai `maximum_length` atau `regex`.
* System yang sangat tangguh dan mudah digunakan **<abbr title="juga dikenal sebagai components, resources, providers, services, injectables">Dependency Injection</abbr>** system.
* Keamanan dan otentifikasi, termasuk support untuk **OAuth2** dengan **JWT tokens** dan **HTTP Basic** auth.
* Teknik-teknik yang lebih maju (tetapi sama-sama mudah) untuk mendeklarasikan **model-model JSON bersarang** (terima kasih untuk Pydantic).
* Banyak fitur-fitur tambahan (terima kasih untuk Starlette) untuk:
    * **WebSockets**
    * **GraphQL**
    * Tes-tes yang sangat mudah berdasarkan pada `requests` dan `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...dan masih banyak lagi.

## Kinerja

Benchmark dari Independent TechEmpower memperlihatkan aplikasi-aplikasi **FastAPI** yang bekerja dibawah Uvicorn sebagai <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">salah satu dari framework-framework Python tercepat yang tersedia</a>, hanya dibawah Starlette dan Uvicorn sendiri (digunakan secara internal oleh FastAPI). (*)

Untuk lebih memahami hal tersebut, lihatlah bagian <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Dependensi Opsional

Digunakan oleh Pydantic:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - untuk JSON yang lebih cepat <abbr title="merubah string yang berasal dari permintaan HTTPke dalam data Python">"parsing"</abbr>.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - untuk validasi email.

digunakan oleh Starlette:

* <a href="https://requests.readthedocs.io" target="_blank"><code>requests</code></a> - Diperlukan jika hendak menggunakan `TestClient`.
* <a href="https://github.com/Tinche/aiofiles" target="_blank"><code>aiofiles</code></a> - Diperlukan jika hendak menggunakan `FileResponse` atau `StaticFiles`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Diperlukan jika hendak  menggunakan konfigurasi templat bawaan.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Diperlukan jika hendak mendukung <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr> form, dengan `request.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Diperlukan untuk dukungan `SessionMiddleware`.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Diperlukan untuk dukungan `SchemaGenerator` dari Starlette (kamu mungkin tidak memerlukannya dengan FastAPI).
* <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - Diperlukan untuk dukungan `GraphQLApp`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Diperlukan jika kamu hendak menggunakan `UJSONResponse`.

Digunakan oleh FastAPI / Starlette:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - untuk server yang melayani dan memuat aplikasimu.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Diperlukan jika hendak menggunakan `ORJSONResponse`.

Kamu dapat menginstall semua hal tersebut dengan `pip install fastapi[all]`.

## Lisensi

Proyek ini berlisensi dibawah ketentuan dari lisensi MIT.
