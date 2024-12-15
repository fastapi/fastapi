# Langkah Pertama

File FastAPI yang paling sederhana bisa seperti berikut:

{* ../../docs_src/first_steps/tutorial001.py *}

Salin file tersebut ke `main.py`.

Jalankan di server:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:single">main.py</u>
<font color="#3465A4">INFO    </font> Using path <font color="#3465A4">main.py</font>
<font color="#3465A4">INFO    </font> Resolved absolute path <font color="#75507B">/home/user/code/awesomeapp/</font><font color="#AD7FA8">main.py</font>
<font color="#3465A4">INFO    </font> Searching for package file structure from directories with <font color="#3465A4">__init__.py</font> files
<font color="#3465A4">INFO    </font> Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

 ╭─ <font color="#8AE234"><b>Python module file</b></font> ─╮
 │                      │
 │  🐍 main.py          │
 │                      │
 ╰──────────────────────╯

<font color="#3465A4">INFO    </font> Importing module <font color="#4E9A06">main</font>
<font color="#3465A4">INFO    </font> Found importable FastAPI app

 ╭─ <font color="#8AE234"><b>Importable FastAPI app</b></font> ─╮
 │                          │
 │  <span style="background-color:#272822"><font color="#FF4689">from</font></span><span style="background-color:#272822"><font color="#F8F8F2"> main </font></span><span style="background-color:#272822"><font color="#FF4689">import</font></span><span style="background-color:#272822"><font color="#F8F8F2"> app</font></span><span style="background-color:#272822">  </span>  │
 │                          │
 ╰──────────────────────────╯

<font color="#3465A4">INFO    </font> Using import string <font color="#8AE234"><b>main:app</b></font>

 <span style="background-color:#C4A000"><font color="#2E3436">╭────────── FastAPI CLI - Development mode ───────────╮</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  Serving at: http://127.0.0.1:8000                  │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  API docs: http://127.0.0.1:8000/docs               │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  Running in development mode, for production use:   │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  </font></span><span style="background-color:#C4A000"><font color="#555753"><b>fastapi run</b></font></span><span style="background-color:#C4A000"><font color="#2E3436">                                        │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">╰─────────────────────────────────────────────────────╯</font></span>

<font color="#4E9A06">INFO</font>:     Will watch for changes in these directories: [&apos;/home/user/code/awesomeapp&apos;]
<font color="#4E9A06">INFO</font>:     Uvicorn running on <b>http://127.0.0.1:8000</b> (Press CTRL+C to quit)
<font color="#4E9A06">INFO</font>:     Started reloader process [<font color="#34E2E2"><b>2265862</b></font>] using <font color="#34E2E2"><b>WatchFiles</b></font>
<font color="#4E9A06">INFO</font>:     Started server process [<font color="#06989A">2265873</font>]
<font color="#4E9A06">INFO</font>:     Waiting for application startup.
<font color="#4E9A06">INFO</font>:     Application startup complete.
```

</div>

Di output, terdapat sebaris pesan:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Baris tersebut menunjukan URL dimana app aktif di komputer anda.


### Mencoba aplikasi

Buka browser di <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Anda akan melihat response JSON sebagai berikut:

```JSON
{"message": "Hello World"}
```

### Dokumen API interaktif

Sekarang kunjungi <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Anda akan melihat dokumentasi API interaktif otomatis (dibuat oleh <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Dokumen API alternatif

Dan sekarang, kunjungi <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Anda akan melihat dokumentasi alternatif otomatis (dibuat oleh <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI

**FastAPI** membuat sebuah "schema" dimana semua API anda menggunakan standar **OpenAPI** untuk mendefinisikan API.

#### "Schema"

"schema" adalah suatu definisi atau deskripsi dari sesuatu. Bukan kode yang mengimplementasi definisi tersebut. Ini hanyalah sebuah deskripsi abstrak.

#### "schema" API

Dalam hal ini, <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> adalah spesifikasi yang menunjukan bagaimana untuk mendefinisikan sebuah skema di API anda.

Definisi skema ini termasuk jalur API anda, parameter yang bisa diterima, dll.

#### "schema" Data

Istilah "schema" bisa juga merujuk ke struktur data, seperti konten JSON.

Dalam kondisi ini, ini berarti attribut JSON dan tipe data yang dimiliki, dll.

#### Schema OpenAPI and JSON

"schema" OpenAPI mendefinisikan skema API dari API yang anda buat. Skema tersebut termasuk definisi (atau "schema") dari data yang dikirim atau diterima oleh API dari **JSON Schema**, skema data standar JSON.

#### Lihat `openapi.json`

Jika anda penasaran bagaimana skema OpenAPI polos seperti apa, FastAPI secara otomatis membuat JSON (schema) dengan deksripsi API anda.

anda bisa melihatnya di: <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a>.

Anda akan melihat JSON yang dimulai seperti:

```JSON
{
    "openapi": "3.1.0",
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

#### Kegunaan OpenAPI

Skema OpenAPI adalah tulang punggung dua sistem dokumentasi API interaktif yang ada di FastAPI.

Ada banyak alternatif sistem dokumentasi lainnya yang semuanya berdasarkan OpenAPI. Anda bisa menambahkannya ke aplikasi **FastAPI** anda.

Anda juga bisa menggunakan OpenAPI untuk membuat kode secara otomatis, untuk klien yang menggunakan API anda. Sebagai contoh, frontend, aplikasi mobile atau IoT.

## Ringkasan, secara bertahap

### Langkah 1: impor `FastAPI`

{* ../../docs_src/first_steps/tutorial001.py hl[1] *}

`FastAPI` adalah class Python yang menyediakan semua fungsionalitas API anda.

/// note | Detail Teknis

`FastAPI` adalah class turunan langsung dari `Starlette`.

Anda bisa menggunakan semua fungsionalitas <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> dengan `FastAPI` juga.

///

### Langkah 2: buat "instance" dari `FastAPI`

{* ../../docs_src/first_steps/tutorial001.py hl[3] *}

Di sini variabel `app` akan menjadi sebuah "instance" dari class `FastAPI`.

Ini akan menjadi gerbang utama untuk membuat semua API anda.

### Langkah 3: Buat *operasi path*

#### Path

"Path" atau jalur di sini merujuk ke bagian URL terakhir dimulai dari `/` pertama.

Sehingga, URL seperti:

```
https://example.com/items/foo
```

...path-nya adalah:

```
/items/foo
```

/// info

"path" juga biasa disebut "endpoint" atau "route".

///

ketika membuat API, "path" adalah jalan utama untuk memisahkan "concern" dan "resources".

#### Operasi

"Operasi" di sini merujuk ke salah satu dari metode HTTP berikut.

Salah satu dari:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...dan operasi lainnya yang unik:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

Dalam protokol HTTP, anda bisa berkomunikasi ke setiap path menggunakan satu (atau lebih) metode di atas.

---

Ketika membuat API, anda umumnya menggunakan metode HTTP tertentu untuk proses tertentu.

Umumnya menggunakan:

* `POST`: untuk membuat data.
* `GET`: untuk membaca data.
* `PUT`: untuk memperbarui data.
* `DELETE`: untuk menghapus data.

Sehingga, di OpanAPI, setiap metode HTTP ini disebut sebuah "operasi".

Kita akan menyebut mereka juga "**operasi**".

#### Mendefinisikan *dekorator operasi path*

{* ../../docs_src/first_steps/tutorial001.py hl[6] *}

`@app.get("/")` memberitahu **FastAPI** bahwa fungsi di bawahnya mengurusi request yang menuju ke:

* path `/`
* menggunakan <abbr title="an HTTP GET method">operasi <code>get</code></abbr>

/// info | `@decorator` Info

Sintaksis `@sesuatu` di Python disebut "dekorator".

Dekorator ditempatkan di atas fungsi. Seperti sebuah topi cantik (Saya pikir istilah ini berasal dari situ).

"dekorator" memanggil dan bekerja dengan fungsi yang ada di bawahnya

Pada kondisi ini, dekorator ini memberi tahu **FastAPI** bahwa fungsi di bawah nya berhubungan dengan **path** `/` dengan **operasi** `get`.

Sehingga disebut **dekorator operasi path**.

///

Operasi lainnya yang bisa digunakan:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

Dan operasi unik lainnya:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip | Tips

Jika anda bisa menggunakan operasi apa saja (metode HTTP).

**FastAPI** tidak mengharuskan anda menggunakan operasi tertentu.

Informasi di sini hanyalah sebagai panduan, bukan keharusan.

Sebagai contoh, ketika menggunakan GraphQL, semua operasi umumnya hanya menggunakan `POST`.

///

### Langkah 4: mendefinisikan **fungsi operasi path**

Ini "**fungsi operasi path**" kita:

* **path**: adalah `/`.
* **operasi**: adalah `get`.
* **fungsi**: adalah fungsi yang ada di bawah dekorator (di bawah `@app.get("/")`).

{* ../../docs_src/first_steps/tutorial001.py hl[7] *}

Ini adalah fungsi Python.

Fungsi ini dipanggil **FastAPI** setiap kali menerima request ke URL "`/`" dengan operasi `GET`.

Di kondisi ini, ini adalah sebuah fungsi `async`.

---

Anda bisa mendefinisikan fungsi ini sebagai fungsi normal daripada `async def`:

{* ../../docs_src/first_steps/tutorial003.py hl[7] *}

/// note | Catatan

Jika anda tidak tahu perbedaannya, kunjungi [Async: *"Panduan cepat"*](../async.md#in-a-hurry){.internal-link target=_blank}.

///

### Langkah 5: hasilkan konten

{* ../../docs_src/first_steps/tutorial001.py hl[8] *}

Anda bisa menghasilkan `dict`, `list`, nilai singular seperti `str`, `int`, dll.

Anda juga bisa menghasilkan model Pydantic (anda akan belajar mengenai ini nanti).

Ada banyak objek dan model yang secara otomatis dikonversi ke JSON (termasuk ORM, dll). Anda bisa menggunakan yang anda suka, kemungkinan sudah didukung.

## Ringkasan

* Impor `FastAPI`.
* Buat sebuah instance `app`.
* Tulis  **dekorator operasi path** menggunakan dekorator seperti `@app.get("/")`.
* Definisikan **fungsi operasi path**; sebagai contoh, `def root(): ...`.
* Jalankan server development dengan perintah `fastapi dev`.
