<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, performa tinggi, mudah di pelajari, cepat dalam penulisan kode, siap untuk produksi</em>
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

**Dokumentasi**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Sumber Kode**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI adalah framework web modern, cepat (kinerja tinggi), untuk membangun API dengan Python 3.8+ berdasarkan standar Python tipe.

Fitur Utama:

* **Cepat**: performa sangat tinggi, setara dengan **NodeJS** dan **Go** (terimakasih untuk Starlette dan Pydantic). [Salah satu framework Python tercepat yang tersedia.](#performa).
* **Cepat dalam penulisan kode**: Meningkatkan kecepatan pengembangan fitur sekitar 200% hingga 300%. *
* **Sedikit Bug**: Mengurangi sekitar 40% dari kesalahan yang disebabkan oleh manusia (pengembang). *
* **Intuitif**: Dukungan editor yang sangat baik. <abbr title="juga di kenal sebagai auto-complete, autocompletion, IntelliSense">Completion</abbr> dimanapun. Waktu debugging yang lebih sedikit.
* **Mudah**: Dirancang agar mudah digunakan dan dipelajari. Waktu membaca dokumen lebih sedikit.
* **Singkat**: Meminimalkan duplikasi kode. Beberapa fitur dari setiap deklarasi parameter. Lebih sedikit bug.
* **Tangguh**: Dapatkan kode siap produksi. Dengan dokumentasi interaktif otomatis.
* **Berdasarkan standar**: Berdasarkan (dan sepenuhnya kompatibel dengan) standar untuk API <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (Sebelumnya dikenal sebagai Swagger) dan <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* estimasi berdasarkan pengujian pada tim pengembangan internal, membangun aplikasi produksi.</small>

## Sponsor

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

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">Sponsor lainnya</a>

## Pendapat

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

"_If anyone is looking to build a production Python API, I would highly recommend **FastAPI**. It is **beautifully designed**, **simple to use** and **highly scalable**, it has become a **key component** in our API first development strategy and is driving many automations and services such as our Virtual TAC Engineer._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, FastAPI untuk antarmuka baris perintah (CLI)

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Jika kamu membangun sebuah <abbr title="Command Line Interface">CLI</abbr> aplikasi yang digunakan di terminal sebagai pengganti web API, Lihatlah <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** adalah saudara kecil FastAPI. Dan ini dimaksudkan menjadi **FastAPI untuk CLI**. ⌨️ 🚀

## Persyaratan

Python 3.8+

FastAPI berdiri di atas bahu para raksasa:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> untuk bagian web.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> untuk bagian data.

## Instalasi

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Kamu juga akan memerlukan server ASGI, untuk produksi seperti <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> atau <a href="https://github.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

## Contoh

### Buatlah

* Buat file `main.py` dengan:

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
<summary>atau gunakan <code>async def</code>...</summary>

Jika kodemu menggunakan `async` / `await`, gunakan `async def`:

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

**Note**:

Jika kamu tidak tahu, periksa bagian _"In a hurry?"_ tentang <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` dan `await` di dokumentasi/a>.

</details>

### Jalankan

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
<summary>Tentang perintah <code>uvicorn main:app --reload</code>...</summary>

Perintah `uvicorn main:app` merujuk kepada:

* `main`: file `main.py` (Python "module").
* `app`: objek yang dibuat di dalam `main.py` dengan baris `app = FastAPI()`.
* `--reload`: membuat server restart setelah perubahan kode. Lakukan ini hanya untuk pengembangan.

</details>

### Periksa

Buka browser-mu di <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Kamu akan melihat respons JSON sebagai:

```JSON
{"item_id": 5, "q": "somequery"}
```

Kamu sudah membuat sebuah API yang:

* Menerima _requests_ HTTP pada _paths_ `/` dan `/items/{item_id}`.
* Kedua _paths_ menggunakan <em>operasi</em> `GET` (juga dikenal sebagai _metode_ HTTP).
* _path_ `/items/{item_id}` memiliki _path parameter_ `item_id` yang seharusnya berupa `int`.
* _path_ `/items/{item_id}` memiliki parameter _query opsional_ `q` bertipe `str`.

### Dokumentasi API interaktif

Sekarang buka <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Kamu akan melihat dokumentasi API interaktif otomatis (disediakan oleh <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Dokumentasi API alternatif

Dan sekarang, buka <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Kamu akan melihat dokumentasi otomatis alternatif (disediakan oleh <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Contoh pembaruan

Sekarang modifikasi file `main.py` untuk menerima body dari _requests_ `PUT`.

Deklarasikan body menggunakan tipe Python standar, berkat Pydantic.

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

Server seharusnya akan me-reload secara otomatis (karena Kamu menambahkan `--reload` pada perintah `uvicorn` di atas).

### Pembaruan Dokumentasi API interaktif

Sekarang buka <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* Dokumentasi API interaktif akan diperbarui secara otomatis, termasuk body baru:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Klik tombol "Try it out", itu memungkinkan kamu mengisi parameter dan berinteraksi langsung dengan API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Kemudian klik tombol "Execute", antarmuka pengguna akan berinteraksi dengan API mu, mengirimkan parameter, mendapatkan hasil, dan menampilkannya di layar:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Pembaruan Dokumentasi API alternatif

Dan sekarang, buka <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* Dokumentasi alternatif juga akan mencerminkan parameter pencarian dan body yang baru:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Rekap

Secara ringkas, Kamu mendeklarasikan **sekali** tipe parameter, body, dll. sebagai parameter fungsi.

Kamu melakukannya dengan tipe standar Python modern.

Kamu tidak perlu mempelajari sintaks baru, metode atau kelas dari suatu perpustakaan tertentu, dll.

Hanya standar **Python 3.8+**.

Untuk Contoh, untuk tipe data `int`:

```Python
item_id: int
```

atau untuk model `Item` yang lebih kompleks:

```Python
item: Item
```

...dan dengan satu deklarasi tersebut kamu mendapatkan:

* Dukungan editor, termasuk:
    * <abbr title="juga di kenal sebagai auto-complete, autocompletion, IntelliSense">Completion</abbr>.
    * Pengecekan tipe.
* Validasi data:
    * Otomatis dan jelas ketika data tidak valid.
    * Validasi bahkan untuk objek JSON yang bersarang secara mendalam.
* <abbr title="juga di kenal sebagai: serialization, parsing, marshalling">Konversi</abbr> data input: datang dari jaringan ke Python data dan tipe. Membaca dari:
    * JSON.
    * Path parameters.
    * Query parameters.
    * Cookies.
    * Headers.
    * Forms.
    * Files.
* <abbr title="juga di kenal sebagai: serialization, parsing, marshalling">Konversi</abbr> data output: mengonversi dari data dan tipe Python ke data jaringan (sebagai JSON):
    * Konversi Python tipe (`str`, `int`, `float`, `bool`, `list`, dll).
    * `datetime` objek.
    * `UUID` objek.
    * Database model.
    * ...dan banyak lagi.
* Dokumentasi API interaktif otomatis, termasuk 2 antarmuka pengguna alternatif:
    * Swagger UI.
    * ReDoc.

---

Kembali ke contoh kode sebelumnya, **FastAPI** akan:

* Validasi bahwa ada `item_id` dalam jalur untuk _requests_ `GET` dan `PUT`.
* Validasi bahwa `item_id` ber-tipe `int` untuk `GET` dan `PUT` _requests_.
    * Jika bukan, klien akan melihat _error_ yang berguna dan jelas.
* Periksa apakah ada parameter query opsional bernama `q` (seperti pada `http://127.0.0.1:8000/items/foo?q=somequery`) untuk `GET` _requests_.
    * Karena parameter `q` dideklarasikan dengan `= None`, itu bersifat opsional.
    * Tanpa `None`, itu akan menjadi wajib  (seperti yang terjadi pada _body_ dalam kasus `PUT`).
* Untuk `PUT` _requests_ ke `/items/{item_id}`, Membaca _body_ sebagai JSON:
    * Periksa bahwa memiliki atribut yang wajib `name` yang seharusnya berupa `str`.
    * Periksa bahwa memiliki atribut yang wajib `price` yang harus berupa `float`.
    * Periksa bahwa memiliki atribut opsional `is_offer`, yang seharusnya berupa `bool`, jika ada.
    * Semua ini juga akan berfungsi untuk objek JSON yang bersarang secara mendalam.
* Konversi dari dan ke JSON otomatis.
* Dokumentasikan semuanya dengan OpenAPI, yang dapat digunakan oleh:
    * Sistem dokumentasi interaktif.
    * Sistem generasi kode klien otomatis, untuk banyak bahasa pemrograman.
* Tersedia 2 antarmuka web dokumentasi interaktif secara langsung.

---

Kita baru saja menyentuh permukaan, tetapi kamu sudah mendapatkan gambaran bagaimana semuanya berfungsi.

Coba ubah baris dengan:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...dari:

```Python
        ... "item_name": item.name ...
```

...menjadi:

```Python
        ... "item_price": item.price ...
```

...dan lihat bagaimana editor kamu akan menyelesaikan otomatis atribut-atribut tersebut dan mengetahui tipe mereka:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Untuk contoh yang lebih lengkap termasuk lebih banyak fitur, lihat <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - Panduan Pengguna</a>.

**Peringatan Spoiler**: tutorial - panduan pengguna termasuk:

* Deklarasi **parameter** dari tempat lain seperti: **headers**, **cookies**, **form fields**, dan **files**.
* Cara mengatur **konstrain validasi** seperti `maximum_length` atau `regex.
* Sangat kuat dan mudah di gunakan **<abbr title="also known as components, resources, providers, services, injectables">Dependency Injection</abbr>** sistem.
* Keamanan dan otentikasi, termasuk dukungan untuk **OAuth2** dengan token **JWT** dan otentikasi **HTTP Basic**.
* Teknik yang lebih advanced (namun sama mudahnya) untuk mendeklarasikan **model JSON yang bersarang secara mendalam** (berkat Pydantic).
* **GraphQL** intergrasi dengan <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> dan perpustakaan lainnya.
* Banyak fitur tambahan (berkat Starlette) seperti:
    * **WebSockets**
    * pengujian yang sangat mudah berdasarkan HTTPX dan `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...dll.

## Performa

Benchmarks independen dari TechEmpower menunjukkan aplikasi **FastAPI** yang berjalan di bawah Uvicorn sebagai <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">salah satu _framework_ Python tercepat yang tersedia</a>, hanya di bawah Starlette dan Uvicorn sendiri (digunakan secara internal oleh FastAPI) (*)

Untuk memahaminya lebih lanjut, lihat bagian <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Dependensi Opsional

Digunakan oleh Pydantic:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - untuk validasi email.
* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - untuk manajemen pengaturan.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - untuk jenis tambahan yang akan digunakan dengan Pydantic.

Digunakan oleh Starlette:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - Diperlukan jika kamu ingin menggunakan `TestClient`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Diperlukan jika kamu ingin menggunakan konfigurasi templat default.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Diperlukan jika kamu ingin mendukung _form_ <abbr title="mengonversi string yang berasal dari permintaan HTTP menjadi data Python">"parsing"</abbr>, dengan `request.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Diperlukan untuk `SessionMiddleware`.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Diperlukan untuk Starlette's `SchemaGenerator` (kamu mungkin tidak memerlukannya dengan FastAPI).
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Diperlukan jika kamu ingin menggunakan `UJSONResponse`.

Digunakan oleh FastAPI / Starlette:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - Untuk server yang memuat dan melayani aplikasi kamu.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Diperlukan jika kamu ingin menggunakan `ORJSONResponse`.


Kamu dapat menginstal semuanya dengan `pip install "fastapi[all]"`.

## Lisensi

Proyek ini dilisensikan di bawah ketentuan lisensi MIT.
