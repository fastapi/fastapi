# Kode Status Respons { #response-status-code }

Sama seperti Anda dapat menentukan model respons, Anda juga dapat mendeklarasikan kode status HTTP yang digunakan untuk respons dengan parameter `status_code` di salah satu *operasi path*:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* dll.

{* ../../docs_src/response_status_code/tutorial001_py310.py hl[6] *}

/// note | Catatan

Perhatikan bahwa `status_code` adalah parameter dari metode "decorator" (`get`, `post`, dll), bukan dari *fungsi operasi path* Anda seperti parameter dan body.

///

Parameter `status_code` menerima angka kode status HTTP.

/// note | Catatan

`status_code` juga dapat menerima `IntEnum`, seperti [`http.HTTPStatus`](https://docs.python.org/3/library/http.html#http.HTTPStatus) milik Python.

///

Ini akan:

* Mengembalikan kode status tersebut di dalam respons.
* Mendokumentasikannya di dalam skema OpenAPI (dan antarmuka pengguna):

<img src="/img/tutorial/response-status-code/image01.png">

/// note | Catatan

Beberapa kode respons (lihat bagian berikutnya) menunjukkan bahwa respons tidak memiliki body.

FastAPI mengetahui hal ini, dan akan menghasilkan dokumen OpenAPI yang menyatakan bahwa tidak ada body respons.

///

## Tentang kode status HTTP { #about-http-status-codes }

/// note | Catatan

Jika Anda sudah mengetahui apa itu kode status HTTP, lewati ke bagian berikutnya.

///

Dalam HTTP, Anda mengirimkan kode status berupa 3 digit angka sebagai bagian dari respons.

Kode status ini memiliki nama terkait untuk membantu mengenalinya, tetapi bagian terpentingnya adalah angkanya.

Singkatnya:

* `100 - 199` untuk "Informasi". Anda jarang menggunakannya secara langsung. Respons dengan kode status ini tidak boleh memiliki body.
* **`200 - 299`** untuk respons "Sukses". Ini adalah kode yang paling sering Anda gunakan.
    * `200` adalah kode status default, yang berarti semuanya "OK".
    * Contoh lainnya adalah `201`, "Created". Ini biasanya digunakan setelah membuat data baru di database.
    * Kasus khusus adalah `204`, "No Content". Respons ini digunakan ketika tidak ada konten yang dikembalikan ke klien, sehingga respons tidak boleh memiliki body.
* **`300 - 399`** untuk "Pengalihan" (Redirection). Respons dengan kode status ini bisa memiliki body atau tidak, kecuali `304`, "Not Modified", yang tidak boleh memiliki body.
* **`400 - 499`** untuk respons "Kesalahan Klien" (Client error). Ini adalah jenis kedua yang paling sering Anda gunakan.
    * Contohnya adalah `404`, untuk respons "Not Found".
    * Untuk kesalahan umum dari klien, Anda bisa menggunakan `400`.
* `500 - 599` untuk kesalahan server. Anda hampir tidak pernah menggunakannya secara langsung. Ketika terjadi masalah pada kode aplikasi atau server Anda, kode status ini akan otomatis dikembalikan.

/// tip | Tips

Untuk mengetahui lebih banyak tentang setiap kode status dan kegunaannya, periksa [dokumentasi <abbr title="Mozilla Developer Network">MDN</abbr> tentang kode status HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status).

///

## Pintasan untuk mengingat nama kode { #shortcut-to-remember-the-names }

Mari kita lihat contoh sebelumnya lagi:

{* ../../docs_src/response_status_code/tutorial001_py310.py hl[6] *}

`201` adalah kode status untuk "Created".

Namun Anda tidak perlu menghafal arti dari setiap kode ini.

Anda dapat menggunakan variabel praktis dari `fastapi.status`.

{* ../../docs_src/response_status_code/tutorial002_py310.py hl[1,6] *}

Variabel ini hanya berupa pintasan yang menyimpan angka yang sama, sehingga Anda dapat menggunakan fitur autocomplete editor untuk menemukannya:

<img src="/img/tutorial/response-status-code/image02.png">

/// note | Detail Teknis

Anda juga dapat menggunakan `from starlette import status`.

**FastAPI** menyediakan `starlette.status` yang sama sebagai `fastapi.status` untuk kenyamanan Anda sebagai developer. Namun ini berasal langsung dari Starlette.

///

## Mengubah nilai default { #changing-the-default }

Nantinya, di [Panduan Pengguna Lanjutan](../advanced/response-change-status-code.md), Anda akan melihat cara mengembalikan kode status yang berbeda dari nilai default yang Anda deklarasikan di sini.
