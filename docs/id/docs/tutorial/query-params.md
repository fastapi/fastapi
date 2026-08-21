# Parameter Query { #query-parameters }

Ketika Anda mendeklarasikan parameter fungsi lain yang bukan bagian dari parameter path, parameter tersebut secara otomatis diinterpretasikan sebagai parameter "query".

{* ../../docs_src/query_params/tutorial001_py310.py hl[9] *}

Query adalah sekumpulan pasangan kunci-nilai (key-value) yang berada setelah tanda `?` di URL, dipisahkan oleh karakter `&`.

Sebagai contoh, pada URL:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

...parameter query-nya adalah:

* `skip`: dengan nilai `0`
* `limit`: dengan nilai `10`

Karena parameter tersebut adalah bagian dari URL, mereka "secara alami" berupa string.

Namun saat Anda mendeklarasikannya dengan tipe Python (pada contoh di atas, sebagai `int`), mereka dikonversi ke tipe tersebut dan divalidasi.

Semua proses yang berlaku pada parameter path juga berlaku pada parameter query:

* Dukungan editor kode (tentu saja)
* <dfn title="mengonversi string yang berasal dari HTTP request menjadi data Python">"parsing"</dfn> data
* Validasi data
* Dokumentasi otomatis

## Nilai Default { #defaults }

Karena parameter query bukan bagian tetap dari path, mereka bisa bersifat opsional dan dapat memiliki nilai default.

Pada contoh di atas, mereka memiliki nilai default `skip=0` dan `limit=10`.

Jadi, mengakses URL:

```
http://127.0.0.1:8000/items/
```

akan sama dengan mengakses:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

Tetapi jika Anda mengakses, misalnya:

```
http://127.0.0.1:8000/items/?skip=20
```

Nilai parameter di dalam fungsi Anda akan menjadi:

* `skip=20`: karena Anda mengaturnya di URL
* `limit=10`: karena itu adalah nilai default

## Parameter Opsional { #optional-parameters }

Dengan cara yang sama, Anda dapat mendeklarasikan parameter query opsional dengan menetapkan nilai default-nya ke `None`:

{* ../../docs_src/query_params/tutorial002_py310.py hl[7] *}

Dalam kasus ini, parameter fungsi `q` akan bersifat opsional, dan bernilai `None` secara default.

/// tip | Tips

Perhatikan juga bahwa **FastAPI** cukup cerdas untuk mengenali bahwa parameter path `item_id` adalah parameter path dan `q` bukan, sehingga `q` adalah parameter query.

///

## Konversi Tipe Parameter Query { #query-parameter-type-conversion }

Anda juga dapat mendeklarasikan tipe `bool`, dan mereka akan dikonversi:

{* ../../docs_src/query_params/tutorial003_py310.py hl[7] *}

Dalam kasus ini, jika Anda mengakses:

```
http://127.0.0.1:8000/items/foo?short=1
```

atau

```
http://127.0.0.1:8000/items/foo?short=True
```

atau

```
http://127.0.0.1:8000/items/foo?short=true
```

atau

```
http://127.0.0.1:8000/items/foo?short=on
```

atau

```
http://127.0.0.1:8000/items/foo?short=yes
```

atau variasi huruf lainnya (huruf besar, huruf kapital di awal, dll), fungsi Anda akan melihat parameter `short` bernilai `bool` `True`. Jika tidak, bernilai `False`.

## Beberapa Parameter Path dan Query { #multiple-path-and-query-parameters }

Anda dapat mendeklarasikan beberapa parameter path dan parameter query secara bersamaan, **FastAPI** tahu mana yang merupakan parameter path dan mana yang merupakan parameter query.

Dan Anda tidak perlu mendeklarasikannya dalam urutan tertentu.

Mereka akan dikenali berdasarkan nama:

{* ../../docs_src/query_params/tutorial004_py310.py hl[6,8] *}

## Parameter Query Wajib { #required-query-parameters }

Ketika Anda mendeklarasikan nilai default untuk parameter non-path (sejauh ini kita baru melihat parameter query), maka parameter tersebut tidak wajib diisi.

Jika Anda tidak ingin menambahkan nilai tertentu tetapi hanya ingin menjadikannya opsional, tetapkan nilai default-nya sebagai `None`.

Namun ketika Anda ingin membuat parameter query menjadi wajib, Anda cukup tidak mendeklarasikan nilai default apa pun:

{* ../../docs_src/query_params/tutorial005_py310.py hl[6:7] *}

Di sini parameter query `needy` adalah parameter query wajib dengan tipe `str`.

Jika Anda membuka di browser URL seperti:

```
http://127.0.0.1:8000/items/foo-item
```

...tanpa menambahkan parameter wajib `needy`, Anda akan melihat pesan galat seperti:

```JSON
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "query",
        "needy"
      ],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

Karena `needy` adalah parameter wajib, Anda perlu mengaturnya di URL:

```
http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
```

...ini akan berfungsi:

```JSON
{
    "item_id": "foo-item",
    "needy": "sooooneedy"
}
```

Dan tentu saja, Anda dapat mendefinisikan beberapa parameter sebagai wajib, beberapa memiliki nilai default, dan beberapa sepenuhnya opsional:

{* ../../docs_src/query_params/tutorial006_py310.py hl[8] *}

Dalam kasus ini, ada 3 parameter query:

* `needy`, bertipe `str` yang wajib diisi.
* `skip`, bertipe `int` dengan nilai default `0`.
* `limit`, bertipe `int` yang opsional.

/// tip | Tips

Anda juga dapat menggunakan `Enum` dengan cara yang sama seperti pada [Parameter Path](path-params.md#predefined-values).

///
