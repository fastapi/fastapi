# FastAPI

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI, framework performa tinggi, mudah dipelajari, cepat untuk coding, siap untuk pengembangan</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage">
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

**Kode Sumber**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI adalah *framework* *web* moderen, cepat (performa-tinggi) untuk membangun API dengan Python berdasarkan tipe petunjuk Python.

Fitur utama FastAPI:

* **Cepat**: Performa sangat tinggi, setara **NodeJS** dan **Go** (berkat Starlette dan Pydantic). [Salah satu *framework* Python tercepat yang ada](#performa).
* **Cepat untuk coding**: Meningkatkan kecepatan pengembangan fitur dari 200% sampai 300%. *
* **Sedikit bug**: Mengurangi hingga 40% kesalahan dari manusia (pemrogram). *
* **Intuitif**: Dukungan editor hebat. <abbr title="juga dikenal otomatis-lengkap, pelengkapan otomatis, kecerdasan">Penyelesaian</abbr> di mana pun. Lebih sedikit *debugging*.
* **Mudah**: Dibuat mudah digunakan dan dipelajari. Sedikit waktu membaca dokumentasi.
* **Ringkas**: Mengurasi duplikasi kode. Beragam fitur dari setiap deklarasi parameter. Lebih sedikit *bug*.
* **Handal**: Dapatkan kode siap-digunakan. Dengan dokumentasi otomatis interaktif.
* **Standar-resmi**: Berdasarkan (kompatibel dengan ) standar umum untuk API: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (sebelumnya disebut Swagger) dan <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>*  estimasi berdasarkan pengujian tim internal pengembangan applikasi siap pakai.</small>

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

## Opini

"_[...] Saya banyak menggunakan **FastAPI** sekarang ini. [...] Saya berencana menggunakannya di semua tim servis ML Microsoft. Beberapa dari mereka sudah mengintegrasikan dengan produk inti *Windows** dan sebagian produk **Office**._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_Kami adopsi library **FastAPI** untuk membuat server **REST** yang melakukan kueri untuk menghasilkan **prediksi**. [untuk Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** dengan bangga mengumumkan rilis open-source orkestrasi framework **manajemen krisis** : **Dispatch**! [dibuat dengan **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_Saya sangat senang dengan **FastAPI**. Sangat menyenangkan!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://x.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Jujur, apa yang anda buat sangat solid dan berkualitas. Ini adalah yang saya inginkan di **Hug** - sangat menginspirasi melihat seseorang membuat ini._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://github.com/hugapi/hug" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_Jika anda ingin mempelajari **framework moderen** untuk membangun REST API, coba **FastAPI** [...] cepat, mudah digunakan dan dipelajari [...]_"

"_Kami sudah pindah ke **FastAPI** untuk **API** kami [...] Saya pikir kamu juga akan suka [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://x.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---
"_Jika anda ingin membuat API Python siap pakai, saya merekomendasikan **FastAPI**. FastAPI **didesain indah**, **mudah digunakan** dan **sangat scalable**, FastAPI adalah **komponen kunci** di strategi pengembangan API pertama kami dan mengatur banyak otomatisasi dan service seperti TAC Engineer kami._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, CLI FastAPI

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Jika anda mengembangkan app <abbr title="Command Line Interface">CLI</abbr> yang digunakan di terminal bukan sebagai API web, kunjungi <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** adalah saudara kecil FastAPI. Dan ditujukan sebagai **CLI FastAPI**. ⌨️ 🚀

## Prayarat

FastAPI berdiri di pundak raksasa:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> untuk bagian web.
* <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> untuk bagian data.

## Instalasi

Buat dan aktifkan <a href="https://fastapi.tiangolo.com/virtual-environments/" class="external-link" target="_blank">virtual environment</a> kemudian *install* FastAPI:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**Catatan**: Pastikan anda menulis `"fastapi[standard]"` dengan tanda petik untuk memastikan bisa digunakan di semua *terminal*.

## Contoh

### Buat app

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
<summary>Atau gunakan <code>async def</code>...</summary>

Jika kode anda menggunakan `async` / `await`, gunakan `async def`:

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

**Catatan**:

Jika anda tidak paham, kunjungi _"Panduan cepat"_ bagian <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` dan `await` di dokumentasi</a>.

</details>

### Jalankan

Jalankan *server* dengan:

<div class="termy">

```console
$ fastapi dev main.py

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>Mengenai perintah <code>fastapi dev main.py</code>...</summary>

Perintah `fastapi dev` membaca file `main.py`, memeriksa app **FastAPI** di dalamnya, dan menjalan server dengan <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a>.

Secara otomatis, `fastapi dev` akan mengaktifkan *auto-reload* untuk pengembangan lokal.

Informasi lebih lanjut kunjungi <a href="https://fastapi.tiangolo.com/fastapi-cli/" target="_blank">Dokumen FastAPI CLI</a>.

</details>

### Periksa

Buka *browser* di <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Anda akan melihat respon JSON berikut:

```JSON
{"item_id": 5, "q": "somequery"}
```

Anda telah membuat API:

* Menerima permintaan HTTP di _path_ `/` dan `/items/{item_id}`.
* Kedua _paths_ menerima <em>operasi</em> `GET` (juga disebut _metode_ HTTP).
* _path_ `/items/{item_id}` memiliki _parameter path_ `item_id` yang harus berjenis `int`.
* _path_ `/items/{item_id}` memiliki _query parameter_ `q` berjenis `str`.

### Dokumentasi API interaktif

Sekarang kunjungi <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Anda akan melihat dokumentasi API interaktif otomatis (dibuat oleh <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Dokumentasi API alternatif

Kemudian kunjungi <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Anda akan melihat dokumentasi alternatif otomatis (dibuat oleh <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Contoh upgrade

Sekarang ubah `main.py` untuk menerima struktur permintaan `PUT`.

Deklarasikan struktur menggunakan tipe standar Python, berkat Pydantic.

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

Server `fastapi dev` akan otomatis memuat kembali.

### Upgrade dokumentasi API interaktif

Kunjungi <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* Dokumentasi API interaktif akan otomatis diperbarui, termasuk kode yang baru:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Klik tombol "Try it out", anda dapat mengisi parameter dan langsung berinteraksi dengan API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Kemudian klik tombol "Execute", tampilan pengguna akan berkomunikasi dengan API, mengirim parameter, mendapatkan dan menampilkan hasil ke layar:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Upgrade dokumentasi API alternatif

Kunjungi <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* Dokumentasi alternatif akan menampilkan parameter *query* dan struktur *request*:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Ringkasan

Singkatnya, anda mendeklarasikan **sekali** jenis parameter, struktur, dll. sebagai parameter fungsi.

Anda melakukannya dengan tipe standar moderen Python.

Anda tidak perlu belajar sintaksis, metode, *classs* baru dari *library* tertentu, dll.

Cukup **Python** standar.

Sebagai contoh untuk `int`:

```Python
item_id: int
```

atau untuk model lebih rumit `Item`:

```Python
item: Item
```

...dengan sekali deklarasi anda mendapatkan:

* Dukungan editor, termasuk:
    * Pelengkapan kode.
    * Pengecekan tipe.
* Validasi data:
    * Kesalahan otomatis dan jelas ketika data tidak sesuai.
    * Validasi hingga untuk object JSON bercabang mendalam.
* <abbr title="juga disebut: serialization, parsing, marshalling">Konversi</abbr> input data: berasal dari jaringan ke data dan tipe Python. Membaca dari:
    * JSON.
    * Parameter path.
    * Parameter query.
    * Cookie.
    * Header.
    * Form.
    * File.
* <abbr title="juga disebut: serialization, parsing, marshalling">Konversi</abbr> output data: konversi data Python ke tipe jaringan data (seperti JSON):
    * Konversi tipe Python (`str`, `int`, `float`, `bool`, `list`, dll).
    * Objek `datetime`.
    * Objek `UUID`.
    * Model database.
    * ...dan banyak lagi.
* Dokumentasi interaktif otomatis, termasuk 2 alternatif tampilan pengguna:
    * Swagger UI.
    * ReDoc.

---

Kembali ke kode contoh sebelumnya, **FastAPI** akan:

* Validasi apakah terdapat `item_id` di *path* untuk permintaan `GET` dan `PUT` requests.
* Validasi apakah `item_id` berjenit `int` untuk permintaan `GET` dan `PUT`.
    * Jika tidak, klien akan melihat pesan kesalahan jelas.
* Periksa jika ada parameter *query* opsional bernama `q` (seperti `http://127.0.0.1:8000/items/foo?q=somequery`) untuk permintaan `GET`.
    * Karena parameter `q` dideklarasikan dengan `= None`, maka bersifat opsional.
    * Tanpa `None` maka akan menjadi wajib ada (seperti struktur di kondisi dengan `PUT`).
* Untuk permintaan `PUT` `/items/{item_id}`, membaca struktur sebagai JSON:
    * Memeriksa terdapat atribut wajib `name` harus berjenis `str`.
    * Memeriksa terdapat atribut wajib`price` harus berjenis `float`.
    * Memeriksa atribut opsional `is_offer`, harus berjenis `bool`, jika ada.
    * Semua ini juga sama untuk objek json yang bersarang mendalam.
* Konversi dari dan ke JSON secara otomatis.
* Dokumentasi segalanya dengan OpenAPI, dengan menggunakan:
    * Sistem dokumentasi interaktif.
    * Sistem otomatis penghasil kode, untuk banyak bahasa.
* Menyediakan 2 tampilan dokumentasi web interaktif dengan langsung.

---

Kita baru menyentuh permukaannya saja, tetapi anda sudah mulai paham gambaran besar cara kerjanya.

Coba ubah baris:

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

...anda akan melihat kode editor secara otomatis melengkapi atributnya dan tahu tipe nya:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Untuk contoh lengkap termasuk fitur lainnya, kunjungi <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - Panduan Pengguna</a>.

**Peringatan spoiler**: tutorial - panduan pengguna termasuk:

* Deklarasi **parameter** dari tempat berbeda seperti: **header**, **cookie**, **form field** and **file**.
* Bagaimana mengatur **batasan validasi** seperti `maximum_length`atau `regex`.
* Sistem **<abbr title="also known as components, resources, providers, services, injectables">Dependency Injection</abbr>** yang hebat dan mudah digunakan.
* Keamanan dan autentikasi, termasuk dukungan ke **OAuth2** dengan **JWT token** dan autentikasi **HTTP Basic**.
* Teknik lebih aju (tetapi mudah dipakai untuk deklarasi **model JSON bersarang ke dalam** (berkat Pydantic).
* Integrasi **GraphQL** dengan <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> dan library lainnya.
* Fitur lainnya (berkat Starlette) seperti:
    * **WebSocket**
    * Test yang sangat mudah berdasarkan HTTPX dan `pytest`
    * **CORS**
    * **Cookie Session**
    * ...dan lainnya.

## Performa

Tolok ukur Independent TechEmpower mendapati aplikasi **FastAPI** berjalan menggunakan Uvicorn sebagai <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">salah satu framework Python tercepat yang ada</a>, hanya di bawah Starlette dan Uvicorn itu sendiri (digunakan di internal FastAPI). (*)

Penjelasan lebih lanjut, lihat bagian <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Tolok ukur</a>.

## Dependensi

FastAPI bergantung pada Pydantic dan Starlette.

### Dependensi `standar`

Ketika anda meng-*install* FastAPI dengan `pip install "fastapi[standard]"`, maka FastAPI akan menggunakan sekumpulan dependensi opsional `standar`:

Digunakan oleh Pydantic:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> - untuk validasi email.

Digunakan oleh Starlette:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - Dibutuhkan jika anda menggunakan `TestClient`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Dibutuhkan jika anda menggunakan konfigurasi template bawaan.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - Dibutuhkan jika anda menggunakan form dukungan <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>, dengan `request.form()`.

Digunakan oleh FastAPI / Starlette:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - untuk server yang memuat dan melayani aplikasi anda. Termasuk `uvicorn[standard]`, yang memasukan sejumlah dependensi (misal `uvloop`) untuk needed melayani dengan performa tinggi.
* `fastapi-cli` - untuk menyediakan perintah `fastapi`.

### Tanpda dependensi `standard`

Jika anda tidak ingin menambahkan dependensi opsional `standard`, anda dapat menggunakan `pip install fastapi` daripada `pip install "fastapi[standard]"`.

### Dependensi Opsional Tambahan

Ada beberapa dependensi opsional yang bisa anda install.

Dependensi opsional tambahan Pydantic:

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - untuk manajemen setting.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - untuk tipe tambahan yang digunakan dengan Pydantic.

Dependensi tambahan opsional FastAPI:

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Diperlukan jika anda akan menggunakan`ORJSONResponse`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Diperlukan jika anda akan menggunakan `UJSONResponse`.

## Lisensi

Project terlisensi dengan lisensi MIT.
