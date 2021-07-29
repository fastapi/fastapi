
{!../../../docs/missing-translation.md!}


<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, high performance, easy to learn, fast to code, ready for production</em>
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

**Dokumentasi**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Kode Sumber**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI adalah kerangka kerja web yang moderen, kencang (ber-performa tinggi), untuk membuat antar muka pemrograman aplikasi dengan Python 3.6+ berdasarkan standar petunjuk tipe Python.

Fitur utama FastAPI adalah:

* **Kencang**: Ber-performa sangat tinggi, sebanding dengan **NodeJS** dan **Go** (berkat Starlette dan Pydantic). [Salah satu kerangka kerja Python tercepat yang ada](#performance).

* **Cepat dalam proses pengkodean**: Meningkatkan proses penambahan fitur sebanyak 200% sampai 300%. *
* **Minim bug (kesalahan dan error)**: Mengurangi sekitar 40% imbas dari kesalahan manusia (pengembang perangkat lunak). *
* **Intuitif**: Di dukung oleh banyak kode editor. <abbr title="dikenal juga sebagai pelengkap otomatis, autocompletion, IntelliSense">Pelengkap</abbr> dimana-mana. Lebih sedikit waktu dalam prosess pencarian kesalahan.
* **Mudah**: Di rancang agar mudah digunakan dan dipelajari. Lebih hemat waktu dalam membaca dokumentasi.
* **Ringkas**: Meminimalisir duplikasi code. Banyak fitur dari tiap parameter yg di deklarasi. Lebih sedikit kesalahan pemrograman.
* **Kokoh**: Dapatkan kode yang siap untuk produksi. Dengan dokumentasi otomatis yang interaktif.
* **Mengikuti Standar**: Berdasarkan (dan sangat sesuai dengan) standar terbuka untuk API: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (Sebelumnya dikenal dengan Swagger) dan <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* estimasi berdasarkan pengujian oleh tim pengembang internal, membuat aplikasi untuk produksi.</small>

## Penyokong

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

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">Penyokong lainnya</a>

## Opini

"_[...] Saya banyak menggunakan **FastAPI** saat ini. [...] Saya sebenarnya berencana untuk menggunakannya dalam semua tim **Layanan ML di Microsoft**. Beberapa diantaranya sedang dalam proses integrase ke dalam inti dari produk **Windows** dan beberapa produk **Office**._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_Kami mengadopsi pustaka **FastAPI** untuk memanggil **REST** peladen yang bisa di panggil untuk mendapatkan **perkiraan**. [for Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, dan Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** dengan senang hati mengumumkan peluncuran kode sumber-terbuka dari kerangka kerja orkestrasi **manajemen krisis** kami: **Dispatch**! [built with **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_Saya sangat bersemangat tentang **FastAPI**. Sangat mengasyikkan!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> host podcast</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Sejujurnya, apa yang telah anda bangun kelihatan sangat solid dan dipoles dengan sangat hati-hati. Dalam banyak hal, ini yang saya butuhkan, sesuatu yang saya inginkan agar **Hug** bisa menjadi seperti ini - sangat menginspirasi melihat seseorang membangunnya._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong>Pencipta <a href="https://www.hug.rest/" target="_blank">Hug</a></strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_Apabila anda berencana mempelajari salah satu **Kerangka Moderen** untuk membuat REST Pemrograman Antarmuka Aplikasi, cobalah **FastAPI** [...] cepat, mudah digunakan dan mudah dipelajari [...]_"

"_Kami telah berpindah ke **FastAPI** dari **Pemrograman Antarmuka Aplikasi** kami [...] Saya rasa anda akan menyukainya [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong>Penemu <a href="https://explosion.ai" target="_blank">Explosion AI</a> - Pencipta <a href="https://spacy.io" target="_blank">spaCy</a></strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, FastAPI untuk Antarmuka Baris Perintah

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Apabila anda sedang membuat sebuah aplikasi <abbr title="Command Line Interface">Antarmuka Baris Perintah</abbr> yang akan digunakan di terminal dan bukan web API, coba <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** adalah adik dari FastAPI. Dan ditujukan untuk menjadi **FastAPI untuk Antarmuka Baris Perintah**. ⌨️ 🚀

## Persyaratan

Python 3.6+

FastAPI berdiri diatas raksasa:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> untuk bagian web.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> untuk bagian data.

## Instalasi

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Anda juga membutuhkan peladen ASGI, untuk produksi seperti <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> atau <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install uvicorn[standard]

---> 100%
```

</div>

## Contoh

### Membuat

* buat sebuah berkas `main.py` dengan:

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
<summary>Atau gunakan <code>async def</code>...</summary>

Bila kode anda menggunakan `async` / `await`, gunakan `async def`:

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

**Catatan**:

Apabila anda tidak tahu, coba lihat di bagian _"Sedang Buru - buru?"_ tentang <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` dan `await` pada dokumen</a>.

</details>

### Jalankan

Jalankan peladen dengan:

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

Perintah `uvicorn main:app` di dasarkan pada:

* `main`: berkas `main.py` ("modul" Python).
* `app`: objek yang di buat didalam `main.py` dengan baris `app = FastAPI()`.
* `--reload`: buat peladen memulai lagi bila ada perubahan kode. Lakukan ini hanya pada saat pengembangan.

</details>

### Lihat Hasilnya

Buka peramban anda ke alamat <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Anda akan mendapatkan jawaban dalam format JSON seperti dibawah:

```JSON
{"item_id": 5, "q": "somequery"}
```

Anda telah membuat sebuah Antarmuka Pemrograman Aplikasi yang berjalan:

* Menerima pemintaan HTTP pada _jalur_ `/` dan `/items/{item_id}`.
* Kedua _jalur_ menerima <em>operasi</em> `GET` (yang juga dikenal dengan _metode_ HTTP).
* _Jalur_ ini`/items/{item_id}` mempunyai _parameter jalur_ `item_id` yang berupa `int`.
* _Jalur_ ini `/items/{item_id}` mempunyai opsional _parameter query_ `str` pada `q`.

### Dokumentasi API yang interaktif

Sekarang buka halaman <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Anda akan melihat dokumentasi API otomatis yang interktif (disediakan oleh <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Dokumentasi API alternatif

Dan sekarang, buka halaman <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Anda akan melihat dokumentasi otomatis alternatif (disediakan oleh <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Contoh Peningkatan

Sekarang rubah berkas `main.py` untuk menerima data dari permintaan `PUT`.

Deklarasikan isi dari permintaan data menggunakan tipe Python standar, terima kasih Pydantic.

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

Peladen seharusnya di muat ulang otomatis (karena anda menambahkan `--reload` pada perintah `uvicorn` diatas).

### Peningkatan Dokumentasi API Interktif

Sekarang buka halaman <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* Dokumentasi API interaktif terupdate secara otomatis, termasuk penambahan data baru pada badan permintaan PUT:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Klik pada tombol "Try it out", maka anda akan diizinkan untuk mengisi parameter dan berinteraksi langsung dengan API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Kemudian klik pada tombol "Execute", antarmuka akan berkomunikasi dengan API, mengirim parameter, mengambil hasil dan menampilkannya pada layar:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Peningkatan Dokumentasi API alternatif

Dan sekarang, buka halaman <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* Dokumentasi alternatif juga akan mencerminkan query parameter dan body yang baru:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Ikhtisar

Kesimpulannya, anda mendeklarasikan tipe parameter, badan dan yang lainnya hanya **sekali**. sebagai parameter fungsi. 

Anda melakukan itu menggunakan tipe standar Python yang moderen.

Anda tidak perlu mempelajari sintaksis baru, metode atau klausa suatu pustaka secara spesifik, dan yang lainnya.

Hanya dengan **Python 3.6+**.

Sebagai contoh, untuk sebuah `int`:

```Python
item_id: int
```

atau untuk yang lebih kompleks model dari `Item`:

```Python
item: Item
```

...dan dengan sekali deklarasi, yang anda dapatkan:

* Dukungan kode editor, termasuk:
    * Pelengkap.
    * Pemeriksaan tipe.
* validasi data:
    * Data di validasi secara otomatis dan informasi kesalahan yang jelas bila data tidak valid.
    * Bahkan validasi untuk objek JSON yang sangat bersarang.
* <abbr title="juga dikenal dengan: serialisasi, penguraian, penyusunan">Konversi</abbr> data yang di masukkan: berasal dari jaringan ke data dan tipe Python. Dibaca dari:
    * JSON.
    * Parameter jalur.
    * Parameter query.
    * Cookie.
    * Header.
    * Form.
    * Berkas.
* <abbr title="juga dikenal dengan: serialisasi, penguraian, penyusunan">Konversi</abbr> dari data keluaran: merubah dari data dan tipe Python ke data jaringan (sebagai JSON):
    * Konversi tipe Python (`str`, `int`, `float`, `bool`, `list`, dll.).
    * obyek `datetime`.
    * obyek `UUID`.
    * Model Basis data.
    * ...dan banyak lagi.
* Interaktif dokumentasi API otomatis, termasuk 2 antarmuka alternatif:
    * Swagger UI.
    * ReDoc.

---

Kembali ke contoh kode sebelumnya, **FastAPI** akan:

* Memvalidasi apakah `item_id` ada pada jalur untuk permintaan dengan method `GET` dan `PUT`.
* Memvalidasi apakah `item_id` ber tipe `int` untuk permintaan `GET` dan `PUT`.
    * Apabila tidak, klien akan mendapatkan pesan kesalahan yang jelas, dan sangat berguna.
* Memeriksa apakah ada query parameter yang opsional bernama `q` (seperti pada `http://127.0.0.1:8000/items/foo?q=somequery`) untuk permintaan `GET`.
    * Karena parameter `q` di deklarasikan dengan `= None`, artinya parameter ini opsional.
    * Tanpa `None` maka akan menjadi required (Wajib ada)  seperti contoh pada body dengan request `PUT`.
* Untuk permintaan `PUT` ke `/items/{item_id}`, Membaca badan dari permintaan sebagai JSON:
    * Memeriksa apakah terdapat atribut wajib `name` dalam bentuk `str`. 
    * Memeriksa apakah terdapat atribut wajib `price` dalam bentuk `float`.
    * Memeriksa apakah terdapat atribut opsional `is_offer`, dalam bentuk `bool`, bila ada.
    * Semua ini juga berlaku untuk obyek JSON sangat bersarang.
* Konversi dari dan ke JSON secara otomatis.
* Mendokumentasikan semuanya dengan OpenAPI, yang dapat digunakan oleh:
    * Sistem dokumentasi interaktif.
    * Sistem pembuatan kode klien otomatis, untuk banyak bahasa.
* Menyediakan 2 antarmuka web dokumentasi interaktif secara langsung.

---

Kami baru saja menggores permukaannya, tetapi Anda sudah mendapatkan ide tentang cara kerjanya.

Coba ubah baris dengan:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...dari:

```Python
        ... "item_name": item.name ...
```

...ke:

```Python
        ... "item_price": item.price ...
```

...dan lihat bagaimana editor Anda akan melengkapi atribut secara otomatis dan mengetahui jenisnya:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Untuk contoh yang lebih lengkap termasuk lebih banyak fitur, lihat <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - Panduan Pengguna</a>.

**Peringatan spoiler**: tutorial - panduan pengguna termasuk:

* Deklarasi **parameter** dari tempat lain yang berbeda seperti: **headers**, **cookies**, **form field** dan **files**..
* Cara menetapkan **batasan validasi** dengan `maximum_length` atau `regex`.
* Sangat kuat dan mudah digunakan pada **<abbr title="juga dikenal sebagai komponen, sumber daya, penyedia, layanan, injeksi">Injeksi Ketergantungan</abbr>** sistem.
* Keamanan dan autentikasi, termasuk dukungan untuk **OAuth2** dengan **token JWT** dan **HTTP Basic** auth.
* Teknik yang lebih canggih (tetapi sama mudahnya) untuk mendeklarasikan **model JSON bersarang dalam** (terima kasih kepada Pydantic).
* Banyak fitur tambahan (terima kasih kepada Starlette) sebagai:
    * **WebSockets**
    * **GraphQL**
    * tes yang sangat mudah berdasarkan `requests` dan `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...dan banyak lagi.

## Kinerja

Tolok ukur TechEmpower Independen menunjukkan aplikasi **FastAPI** yang berjalan di bawah Uvicorn sebagai <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l= zijzen-7" class="external-link" target="_blank">salah satu kerangka kerja Python tercepat yang tersedia</a>, hanya di bawah Starlette dan Uvicorn sendiri (digunakan secara internal oleh FastAPI). (*)

Untuk mengerti selebihnya, lihat bagian <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Tolak Ukur</a>.

## Dpendensi Optional

Digunakan oleh Pydantic:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - untuk JSON yang lebih cepat <abbr title="mengonversi string yang berasal dari permintaan HTTP menjadi data Python">"dalam penguraian"</abbr>.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - untuk validasi email.

Digunakan oleh Starlette:

* <a href="https://requests.readthedocs.io" target="_blank"><code>requests</code></a> - Diperlukan bila anda ingin menggunakan `TestClient`.
* <a href="https://github.com/Tinche/aiofiles" target="_blank"><code>aiofiles</code></a> - Diperlukan bila anda menggunakan `FileResponse` atau `StaticFiles`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Diperlukan jika Anda ingin menggunakan konfigurasi template default
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Diperlukan jika Anda ingin mendukung <abbr title="mengonversi string yang berasal dari permintaan HTTP menjadi data Python">"penguraian"</abbr> formulir, dengan `request.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Diperlukan untuk dukungan `SessionMiddleware`.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Diperlukan untuk dukungan `SchemaGenerator` Starlette (anda mungkin tidak memerlukannya dengan FastAPI).
* <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - Diperlukan untuk dukungan `GraphQLApp`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Diperlukan bila anda menggunakan `UJSONResponse`.

Digunakan oleh FastAPI / Starlette:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - untuk peladen yang memuat dan melyano aplikasi anda.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Diperlukan bila anda akan menggunakan `ORJSONResponse`.

Anda dapat menginstall semuanya dengan `pip install fastapi[all]`.

## Lisensi

Proyek ini dilisensikan di bawah persyaratan lisensi MIT.
