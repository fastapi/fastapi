# Fitur

## Fitur FastAPI

**FastAPI** memberi Anda hal-hal berikut:

### Berdasarkan standar terbuka

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> untuk pembuatan API, termasuk deklarasi <abbr title="juga dikenal sebagai: endpoint atau route">path</abbr> <abbr title="juga dikenal sebagai Metode HTTP, seperti POST, GET, PUT, DELETE">operasi</abbr>, parameter, request body, keamanan, dll.
* Dokumentasi model data otomatis dengan <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> (karena OpenAPI sendiri didasarkan pada JSON Schema).
* Dirancang berdasarkan standar-standar ini setelah studi yang cermat, bukan sebagai lapisan tambahan yang dibuat belakangan.
* Hal ini juga memungkinkan penggunaan **pembuatan kode klien** secara otomatis dalam berbagai bahasa pemrograman.

### Dokumentasi Otomatis

Antarmuka pengguna web untuk dokumentasi dan eksplorasi API yang interaktif. Karena framework ini didasarkan pada OpenAPI, tersedia berbagai pilihan, dengan 2 di antaranya sudah disertakan secara bawaan.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>, dengan eksplorasi interaktif, Anda bisa langsung memanggil dan menguji API dari peramban.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Dokumentasi API alternatif dengan <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a>.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Hanya Python Modern

Semuanya didasarkan pada deklarasi **tipe Python** standar (berkat Pydantic). Tidak ada sintaks baru yang perlu dipelajari. Cukup Python modern standar.

Jika Anda membutuhkan penyegaran 2 menit tentang cara menggunakan tipe Python (bahkan jika Anda tidak menggunakan FastAPI), periksa tutorial singkat: [Python Types](python-types.md){.internal-link target=_blank}.

Anda cukup menulis Python standar dengan tipe:

```Python
from datetime import date

from pydantic import BaseModel

# Mendeklarasikan variabel sebagai string (str)
# dan mendapatkan dukungan editor di dalam fungsi tersebut
def main(user_id: str):
    return user_id


# Sebuah model Pydantic
class User(BaseModel):
    id: int
    name: str
    joined: date
```

Fungsi tersebut kemudian bisa digunakan seperti berikut:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

/// info

`**second_user_data` berarti:

Ambil pasangan kunci dan nilai dari Kamus (Dicts) `second_user_data` secara langsung sebagai argumen kunci-nilai, setara dengan: `User(id=4, name="Mary", joined="2018-11-30")`.

///

### Bantuan Editor

Seluruh framework dirancang agar mudah dan intuitif untuk digunakan, semua keputusan telah diuji pada berbagai editor bahkan sebelum pengembangan dimulai, demi memastikan pengalaman pengembangan terbaik.

Dalam survei pengembang Python, jelas bahwa <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank"> salah satu fitur yang paling banyak digunakan adalah "pelengkapan otomatis" (autocompletion)</a>.

Seluruh framework **FastAPI** dirancang untuk memenuhi kebutuhan tersebut. Pelengkapan otomatis berfungsi di mana pun.

Anda akan jarang perlu kembali ke dokumentasi.

Berikut adalah contoh bagaimana editor Anda dapat membantu Anda:

* Di <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* Di <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

Anda akan mendapatkan pelengkapan otomatis dalam kode yang mungkin sebelumnya Anda anggap mustahil. Contohnya, kunci `price` di dalam body JSON (yang bisa saja bersarang) yang berasal dari sebuah request.

Tidak ada lagi kesalahan penulisan nama kunci, bolak-balik antara dokumentasi, atau scroll naik-turun untuk mencari apakah Anda pada akhirnya menggunakan `username` atau `user_name`.


### Ringkas

Framework ini memiliki pengaturan **bawaan** yang masuk akal untuk segala hal, dengan konfigurasi opsional di setiap bagian. Semua parameter bisa disesuaikan dengan cermat untuk memenuhi kebutuhan Anda dan mendefinisikan API yang Anda inginkan.

Namun secara bawaan, semuanya **berjalan begitu saja**.


### Validasi

* Validasi untuk sebagian besar (atau semua?) **tipe data** Python, termasuk:
    * Objek JSON (`dict`).
    * Array JSON (`list`) yang mendefinisikan tipe item.
    * String (`str`) field, yang mendefinisikan panjang minimal dan maksimal.
    * Angka (`int`, `float`) dengan nilai minimal dan maksimal, dan lain-lain.

* Validasi untuk tipe yang lebih kompleks, seperti:
    * URL.
    * Email.
    * UUID.
    * ...dan lainnya.

Semua validasi ditangani oleh **Pydantic** yang sudah mapan dan tangguh.

### Keamanan dan Otentikasi

Keamanan dan otentikasi terintegrasi, tanpa kompromi dengan basis data atau model data apa pun.

Semua skema keamanan yang didefinisikan dalam OpenAPI dapat didukung, termasuk:

* HTTP Basic.
* **OAuth2** (juga dengan **JWT tokens**). Anda bisa melihat tutorial disini [OAuth2 with JWT](tutorial/security/oauth2-jwt.md){.internal-link target=_blank}.
* Kunci API di:
    * Headers.
    * Query parameters.
    * Cookies, dll.

Ditambah semua fitur keamanan dari Starlette (termasuk **session cookies**).

Semua fitur ini dibangun sebagai alat dan komponen yang dapat digunakan kembali, mudah diintegrasikan dengan sistem Anda, penyimpanan data, basis data relasional, dan NoSQL, dll.


### Injeksi Ketergantungan (Dependency Injection)

FastAPI menyertakan sistem <abbr title='juga dikenal sebagai "komponen", "resource", "service", "provider"'><strong>Injeksi Ketergantungan</strong></abbr> yang sangat mudah digunakan namun sangat kuat.

* Bahkan ketergantungan dapat memiliki ketergantungan yang lain, menciptakan hierarki atau **"grafik" ketergantungan**.
* Semua **ditangani secara otomatis** oleh framework.
* Semua ketergantungan dapat meminta data dari request dan **menambah batasan operasi path** serta dokumentasi otomatis.
* **Validasi otomatis** bahkan untuk **parameter path operation** yang didefinisikan dalam ketergantungan.
* Dukungan untuk sistem otentikasi pengguna yang kompleks, **koneksi basis data**, dll.
* **Tidak ada kompromi** dengan basis data, frontend, dll., tetapi integrasi yang mudah dengan semuanya.


### "Plug-in" Tak Terbatas

Atau dengan kata lain, tidak perlu "plug-in", cukup impor dan gunakan kode yang Anda butuhkan.

Setiap integrasi dirancang agar sangat mudah digunakan (dengan ketergantungan) sehingga Anda dapat membuat "plug-in" untuk aplikasi Anda hanya dalam 2 baris kode menggunakan struktur dan sintaks yang sama dengan yang digunakan untuk **path operations** Anda.


### Teruji

* 100% <abbr title="Jumlah kode yang diuji secara otomatis">cakupan pengujian</abbr>.
* 100% basis kode dengan <abbr title="Anotasi tipe Python, agar editor dan alat eksternal dapat memberikan dukungan yang lebih baik">anotasi tipe</abbr>.
* Digunakan dalam aplikasi produksi.


## Fitur Starlette

**FastAPI** sepenuhnya kompatibel dengan (dan berbasis pada) <a href="https://www.starlette.io/" class="external-link" target="_blank"><strong>Starlette</strong></a>. Jadi, kode Starlette tambahan apa pun yang Anda miliki juga akan berfungsi.

`FastAPI` sebenarnya adalah sub-kelas dari `Starlette`. Jadi, jika Anda sudah tahu atau menggunakan Starlette, sebagian besar fungsionalitasnya akan bekerja dengan cara yang sama.

Dengan **FastAPI**, Anda mendapatkan semua fitur **Starlette** (karena FastAPI hanyalah Starlette yang lebih canggih):

* Performa yang sangat mengesankan. Ini adalah <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">salah satu framework Python tercepat yang tersedia, setara dengan **NodeJS** dan **Go**</a>.
* Dukungan **WebSocket**.
* Tugas latar belakang dalam proses..
* Event startup dan shutdown.
* Klien pengujian yang dibangun di atas HTTPX.
* **CORS**, GZip, Static Files, Streaming responses.
* Dukungan **Sesi and Cookie**.
* 100% cakupan pengujian.
* 100% basis kode dengan anotasi tipe.


## Fitur Pydantic

**FastAPI** sepenuhnya kompatibel dengan (dan berbasis pada) <a href="https://docs.pydantic.dev/" class="external-link" target="_blank"><strong>Pydantic</strong></a>. Jadi, kode Pydantic tambahan apa pun yang Anda miliki juga akan berfungsi.

Termasuk pustaka eksternal yang juga berbasis Pydantic, seperti <abbr title="Object-Relational Mapper">ORM</abbr>, <abbr title="Object-Document Mapper">ODM</abbr> untuk basis data.

Ini juga berarti bahwa dalam banyak kasus, Anda dapat meneruskan objek yang Anda dapatkan dari request **langsung ke basis data**, karena semuanya divalidasi secara otomatis.

Hal yang sama berlaku sebaliknya, dalam banyak kasus Anda dapat langsung meneruskan objek yang Anda dapatkan dari basis data **langsung ke klien**.

Dengan **FastAPI**, Anda mendapatkan semua fitur **Pydantic** (karena FastAPI berbasis pada Pydantic untuk semua penanganan data):

* **Tidak membingungkan**:
    * Tidak ada bahasa mikro definisi skema baru yang perlu dipelajari.
    * Jika Anda tahu tipe Python, Anda tahu cara menggunakan Pydantic.
* Berfungsi dengan baik dengan **<abbr title="Integrated Development Environment, mirip dengan editor kode">IDE</abbr>/<abbr title="program yang memeriksa kesalahan kode">linter</abbr>/brain**:
    * Karena struktur data Pydantic hanyalah instans dari kelas yang Anda definisikan; pelengkapan otomatis, linting, mypy, dan intuisi Anda akan berfungsi dengan baik dengan data yang telah divalidasi.
* Validasi **struktur kompleks**:
    * Penggunaan model Pydantic hierarkis, `List` and `Dict` dari `typing` Python, dll.
    * Dan validator memungkinkan skema data kompleks didefinisikan, diperiksa, dan didokumentasikan dengan jelas dan mudah sebagai JSON Schema.
    * Anda dapat memiliki objek **JSON yang bersarang** dalam dan semuanya tervalidasi serta teranotasi.
* **Dapat diperluas**:
    * Pydantic memungkinkan tipe data kustom didefinisikan atau Anda dapat memperluas validasi dengan metode pada model yang dihiasi dengan decorator validator.
* 100% cakupan pengujian.
