# First Steps

File FastAPI yang paling sederhana bisa berupa seperti dibawah ini:

```Python
{!../../../docs_src/first_steps/tutorial001.py!}
```

Salin kode diatas ke dalam file `main.py`.

Jalankan server:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>:     Started reloader process [28720]
<span style="color: green;">INFO</span>:     Started server process [28722]
<span style="color: green;">INFO</span>:     Waiting for application startup.
<span style="color: green;">INFO</span>:     Application startup complete.
```

</div>

!!! catatan
    Perintah `uvicorn main:app` merujuk kepada:

    * `main`: file `main.py` ("module" Python).
    * `app`: object yang terbentuk didalam file `main.py` pada baris `app = FastAPI()`.
    * `--reload`: membuat server restart setelah terjadinya perubahan kode. Hanya digunakan pada saat development.

Pada output yang muncul, terdapat baris yang memiliki hal seperti:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Baris tersebut menunjukan URL dimana aplikasimu dijalankan pada mesin lokalmu.

### Periksalah

Buka browsermu pada <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Kamu akan melihat respon JSON sebagai berikut:

```JSON
{"message": "Hello World"}
```

### Dokument API Interactive

Dan sekarang, pergilah menuju <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Kamu akan melihat dokumentasi API interaktif otomatis tersebut (disediakan oleh <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Dokumen API Alternative

Dan sekarang, pergilah ke <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Kamu akan melihat dokumentasi API interaktif otomatis tersebut (disediakan oleh <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI

**FastAPI** menghasilkan "skema" dengan semua API menggunakan **OpenAPI** standard untuk mendefinisikan API.

#### "Skema"

Sebuah "skema" adalah definisi atau deskripsi dari sesuatu. Bukanlah kode yang mengimplementasikannya, tetapi hanyalah sebuah deskripsi abstrak.

#### "Skema" API

Pada kasus ini, <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> adalah sebuah spesifikasi yang menentukan bagaimana cara untuk mendefinisikan sebuah "skema" dari API mu.

Definisi skema ini meliputi path (jalur) dari API, parameter-parameter yang diambil, dan lain-lain.

#### "Skema" Data

Istilah "skema" bisa juga merujuk kepada bentuk dari suatu data, seperti konten JSON.

Pada kasus tersebut, artinya adalah atribut-atribut JSON, dan tipe-tipe data yang mereka miliki, dan lain-lain.

#### OpenAPI dan Skema JSON

OpenAPI mendefinisikan sebuah skema API untuk API mu. Dan skema tersebut meliputi definisi-definisi (atau skema-skema) dari data yang terkirim dan diterima oleh API mu menggunakan **JSON Schema**, merupakan standar dari skema-skema data JSON.

#### Periksa `openapi.json`

Jika kamu penasaran tentang bagaimana skema OpenAPI mentah terlihat, FastAPI secara otomatis akan menghasilkan sebuah JSON (skema) dengan deskripsi dari semua API mu.

Kamu dapat melihatnya secara langsung di <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a>.

Di situ akan terlihat sebuah JSON yang diawali dengan sesuatu seperti:

```JSON
{
    "openapi": "3.0.2",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {



...
```

#### Untuk apa OpenAPI

Skema OpenAPI adalah hal yang menjadi kekuatan bagi dua sistem dokumentasi interaktif.


Dan terdapat puluhan alternatif, semuanya berbasis pada OpenAPI. Kamu dapat dengan mudah menambahkan yang manapun dari alternatif-alternatif tersebut ke dalam aplikasimu yang dibangun menggunakan **FastAPI**.

Kamu juga dapat menggunakannya untuk menghasilkan kode secara otomatis, untuk klien-klien yang berkomunikasi dengan API mu. Sebagai contoh, frontend, mobile atau aplikasi-aplikasi IoT.

## Ikhtisiar, tahap demi tahap

### Tahap 1: import `FastAPI`

```Python hl_lines="1"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`FastAPI` adalah kelas Python yang menyediakan semua fungsionalitas untuk API mu.

!!! catatan "Detail Teknis"
    `FastAPI` adalah sebuah kelas yang mewarisi secara langsung dari `Starlette`.

    Kamu dapat menggunakan semua fungsionalitas <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> melalui `FastAPI` juga.

### Tahap 2: membuat "instance" `FastAPI`

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Di sini variable `app` akan menjadi "instance" dari kelas `FastAPI`,

Hal ini akan menjadi poin utama dari interaksi untuk membuat semua API mu.

`app` ini adalah hal yang sama dengan yang dirujuk oleh `uvicorn` di dalam perintah:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Jika kamu membuat aplikasimu seperti:

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial002.py!}
```

dan menaruhnya di dalam file `main.py`, maka kamu akan memanggil `uvicorn` seperti:

<div class="termy">

```console
$ uvicorn main:my_awesome_api --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### Tahap 3: membuat *operasi path*

#### Path

"Path" disini mengacu kepada bagian akhir dari URL yang diawali dengan `/`.

Jadi pada URL seperti:

```
https://example.com/items/foo
```

...akan menjadi:

```
/items/foo
```

!!! informasi
    sebuah "path" juga secara umum dipanggil "endpoint" atau "route".

Ketika membangun API, "path" adalah jalan utama untuk memisahkan "perhatian/fokus" dan "sumber daya".

#### Operasi

"Operasi" disini merujuk kepada salah satu dari metode-metode HTTP.

Salah satu dari:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...dan yang lebih eksotik lagi:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

Pada protokol HTTP, kamu dapat mengkomunikasikan ke setiap "path" menggunakan satu (atau lebih) dari metode-metode tersebut.

---

Ketika membangun API, kamu biasanya menggunakan metode-metode HTTP tertentu ini untuk melakukan sebuah aksi tertentu.

Biasanya kamu akan menggunakan:

* `POST`: untuk membuat data.
* `GET`: untuk membaca data.
* `PUT`: untuk meng-update data.
* `DELETE`: untuk meng-hapus data.

Jadi, di dalam OpenAPI, setiap dari metode-metode HTTP tersebut dipanggil dengan sebutan "operasi".

Kita akan memanggil mereka dengan sebutan "**operasi-operasi**" juga.

#### Mendefinisikan sebuah *dekorator operasi path*

```Python hl_lines="6"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`@app.get("/")` memberitahukan **FastAPI** bahwa fungsi yang langsung berada dibawahnya bertugas menangani request yang menuju:

* path `/`
* menggunakan <abbr title="an HTTP GET method"><code>get</code> operasi</abbr>

!!! info "`@decorator` Informasi"
    Bahwa syntax `@sesuatu` pada Python disebut sebuah "dekorator",

    Kamu meletakannya diatas sebuah fungsi. Seperti topi dekoratif yang menarik (Saya kira dari sana istilah ini berasal).

    Sebuah "dekorator" mengambil fungsi dibawahnya dan melakukan sesuatu dengannya.

    Pada kasus kita, dekorator ini memberitahukan **FastAPI** bahwa fungsi dibawahnya berhubungan dengan **path** `/` dengan sebuah **operasi** `get`.

    Itu adalah "**dekorator operasi path**".

Kamu juga bisa menggunakan operasi-operasi lainnya.

* `@app.post()`
* `@app.put()`
* `@app.delete()`

Dan juga yang eksotik:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

!!! tip
    Kamu bebas untuk menggunakan setiap operasi (Metode HTTP) seperti yang kamu inginkan.

    **FastAPI** tidak memaksakan arti tertentu.

    Informasi di sini disajikan sebagai petunjuk, bukan sebuah keharusan.

    Sebagai contoh, ketika menggunakan GraphQL kamu biasanya melakukan semua aksi menggunakan hanya operasi `POST`.

### Tahap 4: mendefinisikan **fungsi operasi path**

Ini adalah "**fungsi operasi path**" kita:

* **path**: adalah `/`.
* **operation**: adalah `get`.
* **function**: adalah fungsi yang terletak dibawah "dekorator" (dibawah `@app.get("/")`).

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Ini adalah fungsi Python.

Ini akan dipanggil oleh **FastAPI** kapanpun ia menerima request ke URL "`/`" dari operasi `GET`.

Pada kasus ini, ini adahal fungsi `async`.

---

Kamu juga dapat mendefinisikannya sebagai fungsi normal selain `async def`:

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial003.py!}
```

!!! catatan
    Jika kamu tidak tahu perbedaannya, periksalah [Async: *"In a hurry?"*](../async.md#in-a-hurry){.internal-link target=_blank}.

### Tahap 5: mengembalikan konten

```Python hl_lines="8"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Kamu dapat mengembalikan sebuah `dict`, `list`, nilai tunggal sebagai `str`, `int`, dan lain-lain.

Kamu juga dapat mengembalikan model-model Pydantic (kamu akan melihatnya lagi nanti).

Terdapat banyak sekali obyek dan model yang dapat secara otomatis di-ubah ke dalam JSON (termasuk ORM's, dan lain-lain). Cabalah menggunakan salah satu favoritmu, akan sangat mungkin bahwa mereka sudah mendukungnya.

## Ikhtisar

* Import `FastAPI`.
* Buat sebuah instance `app`.
* Tulis sebuah **dekorasi path operasi** (seperti `@app.get("/")`).
* Tulis sebuah **fungsi path operasi** (seperti `def root(): ...` diatas).
* Jalankan server development (seperti `uvicorn main:app --reload`).
