# Parameter Path

"parameter" atau "variabel" path didefinisikan dengan sintaksis Python format string:

{* ../../docs_src/path_params/tutorial001.py hl[6:7] *}

Nilai parameter path `item_id` akan dikirim ke fungsi sebagai argument `item_id`:

Jika anda menjalankan contoh berikut dan kunjungi <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>, anda akan melihat respon:

```JSON
{"item_id":"foo"}
```

## Parameter path dengan tipe data

Tipe data parameter path bisa didefinisikan di dalam fungsi, menggunakan anotasi tipe data standar Python:

{* ../../docs_src/path_params/tutorial002.py hl[7] *}

Dalam hal ini `item_id` didefinisikan sebagai `int`.

/// check | Periksa

Penyunting kode anda bisa membantu periksa di dalam fungsi seperti pemeriksaan kesalahan, kelengkapan kode, dll.

///

## <abbr title="juga disebut: serialization, parsing, marshalling">Konversi</abbr> data

Jika contoh berikut dijalankan dan diakses browser melalui <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a>, anda akan melihat respon:

```JSON
{"item_id":3}
```

/// check | Periksa

Perhatikan nilai fungsi yang diterima (dan dihasilkan) adalah `3`, sebagai `int` di Python, dan bukan string `"3"`.

Sehingga dengan deklarasi tipe data **FastAPI** memberikan request otomatis <abbr title="konversi string dari request HTTP menjadi data Python">"parsing"</abbr>.

///

## Validasi Data

Tetapi jika di browser anda akses <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>, anda akan melihat pesan kesalahan HTTP:

```JSON
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "item_id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "foo"
    }
  ]
}
```

Karena parameter path `item_id` bernilai `"foo"` yang bukan tipe data `int`.

Kesalahan yang sama akan muncul jika menggunakan `float` daripada `int`, seperti di: <a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2</a>

/// check | Periksa

Dengan deklarasi tipe data Python, **FastAPI** melakukan validasi data.

Perhatikan kesalahan tersebut juga menjelaskan validasi apa yang tidak sesuai.

Validasi ini sangat membantu ketika mengembangkan dan men-*debug* kode yang berhubungan dengan API anda.

///

## Dokumentasi

Ketika anda membuka browser di <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>, anda melihat dokumentasi API interaktif otomatis berikut:

<img src="/img/tutorial/path-params/image01.png">

/// check | Periksa

Dengan deklarasi tipe data Python yang sama, **FastAPI** membuat dokumentasi interaktif otomatis (terintegrasi Swagger UI).

Perhatikan parameter path dideklarasikan sebagai integer.

///

## Keuntungan basis-standar, dokumentasi alternatif

Karena skema yang dibuat berasal dari standar <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md" class="external-link" target="_blank">OpenAPI</a>, maka banyak alat lain yang kompatibel.

Sehingga **FastAPI** menyediakan dokumentasi alternatif (menggunakan ReDoc), yang bisa diakses di <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>:

<img src="/img/tutorial/path-params/image02.png">

Cara yang sama untuk menggunakan tools kompatibel lainnya. Termasuk alat membuat kode otomatis untuk banyak bahasa.

## Pydantic

Semua validasi data dikerjakan di belakang layar oleh <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>, sehingga anda mendapatkan banyak kemudahan. Anda juga tahu proses ini akan ditangani dengan baik.

Anda bisa mendeklarasikan tipe data dengan `str`, `float`, `bool` dan banyak tipe data kompleks lainnya.

Beberapa tipe di atas akan dibahas pada bab berikutnya tutorial ini.

## Urutan berpengaruh

Ketika membuat  *operasi path*, anda bisa menghadapi kondisi dimana *path* nya sudah tetap.

Seperti `/users/me`, untuk mendapatkan data user yang sedang aktif.

Kemudian anda bisa memiliki path `/users/{user_id}` untuk mendapatkan data user tertentu melalui user ID.

karena *operasi path* dievaluasi melalui urutan, anda harus memastikan path untuk `/users/me` dideklarasikan sebelum `/user/{user_id}`:

{* ../../docs_src/path_params/tutorial003.py hl[6,11] *}

Sebaliknya, path `/users/{user_id}` juga akan sesuai dengan `/users/me`, "menganggap" menerima parameter `user_id` dengan nilai `"me"`.

Serupa, anda juga tidak bisa mendefinisikan operasi path:

{* ../../docs_src/path_params/tutorial003b.py hl[6,11] *}

Path pertama akan selalu digunakan karena path sesuai dengan yang pertama.

## Nilai terdefinisi

Jika ada *operasi path* yang menerima *parameter path*, tetapi anda ingin nilai valid *parameter path* sudah terdefinisi, anda bisa menggunakan standar Python <abbr title="Enumeration">`Enum`</abbr>.

### Membuat class `Enum`

Import `Enum` dan buat *sub-class* warisan dari `str` dan `Enum`.

Dengan warisan dari `str` dokumen API mengetahui nilai nya harus berjenis `string` supaya bisa digunakan dengan benar.

Kemudian buat atribut *class* dengan nilai tetap *string* yang benar:

{* ../../docs_src/path_params/tutorial005.py hl[1,6:9] *}

/// info

<a href="https://docs.python.org/3/library/enum.html" class="external-link" target="_blank">Enumerasi (atau enum) tersedia di Python</a> sejak versi 3.4.

///

/// tip | Tips

"AlxexNet", "ResNet", dan "LeNet" adalah nama <abbr title="Secara teknis, arsitektur model Deep Learning">model</abbr> *Machine Learning*.

///

### Mendeklarasikan *parameter path*

Kemudian buat *parameter path* dengan tipe anotasi menggunakan *class* enum dari (`ModelName`)

{* ../../docs_src/path_params/tutorial005.py hl[16] *}

### Periksa dokumentasi

Karena nilai yang tersedia untuk *parameter path* telah terdefinisi, dokumen interatik bisa memunculkan:

<img src="/img/tutorial/path-params/image03.png">

### Bekerja dengan *enumarasi* Python

Nilai *parameter path* akan menjadi *anggota enumerasi*.

#### Membandingkan *anggota enumerasi*

Anda bisa membandingkan parameter *path* dengan *anggota enumerasi* di enum `ModelName` yang anda buat:

{* ../../docs_src/path_params/tutorial005.py hl[17] *}

#### Mendapatkan *nilai enumerasi*

Anda bisa mendapatkan nilai (`str` dalam kasus ini) menggunakan `model_name.value`, atau secara umum `anggota_enum_anda.value`:

{* ../../docs_src/path_params/tutorial005.py hl[20] *}

/// tip | Tips

Anda bisa mengakses nilai `"lenet"` dnegan `ModelName.lenet.value`.

///

#### Menghasilkan *anggota enumerasi*

Anda bisa menghasilkan *anggota enumerasi* dari *operasi path* bahkan di body JSON bersarang (contoh `dict`).

They will be converted to their corresponding values (strings in this case) before returning them to the client:

{* ../../docs_src/path_params/tutorial005.py hl[18,21,23] *}

Klien akan mendapatkan respon JSON seperti berikut:

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## Parameter path berisi path

Misalkan terdapat *operasi path* dengan path `/files/{file_path}`.

Tetapi anda memerlukan `file_path` itu berisi *path*, seperti like `home/johndoe/myfile.txt`.

Sehingga URL untuk file tersebut akan seperti: `/files/home/johndoe/myfile.txt`.

### Dukungan OpenAPI

OpenAPI tidak bisa mendeklarasikan *parameter path* berisi *path* di dalamnya, karena menyebabkan kondisi yang sulit di*test* dan didefinisikan.

Tetapi, di **FastAPI** anda tetap bisa melakukannya dengan menggunakan *tools* internal dari Starlette.

Dan dokumentasi tetap berfungsi walaupun tidak menambahkan keterangan bahwa parameter harus berisi *path*.

### Konverter path

Melalui Starlette anda bisa mendeklarasikan *parameter path* berisi *path* dengan URL seperti:

```
/files/{file_path:path}
```

Dikondisi ini nama parameter adalah `file_path` dan bagian terakhir `:path` menginformasikan parameter harus sesuai dengan setiap *path*.

Sehingga anda bisa menggunakan:

{* ../../docs_src/path_params/tutorial004.py hl[6] *}

/// tip | Tips

Anda mungkin perlu parameter berisi `/home/johndoe/myfile.txt` di awali garis belakang (`/`).

Di kondisi ini, URL nya menjadi: `/files//home/johndoe/myfile.txt`, dengan dua garis belakang (`//`) di antara `files` dan `home`.

///

## Ringkasan

Di **FastAPI** dengan menggunakan deklarasi tipe Python standar, pendek, intuitif, anda mendapatkan:

* Dukungan editor: pemeriksaan kesalahan, autocompletion, dll.
* "<abbr title="konversi string dari request HTTP menjadi data Python">Parsing</abbr>" data.
* Validasi data.
* Annotasi API dan dokumentasi otomatis.

Semua itu anda hanya perlu mendeklarasikan sekali saja.

Ini adalah salah satu keunggulan **FastAPI** dibandingkan dengan *framework* lainnya (selain dari performa Python *native*c)
