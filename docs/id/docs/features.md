# Fitur

## Fitur-fitur FastAPI

**FastAPI** memberi kamu hal berikut:

### Berdasarkan standar terbuka

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> untuk pembuatan API, termasuk deklarasi <abbr title="juga di kenal: endpoints, routes">path</abbr> <abbr title="juga di kenal sebagai HTTP methods, as POST, GET, PUT, DELETE">operations</abbr>, parameters, <abbr title="isi pesan HTTP">body</abbr> requests, keamanan, dll.
* Dokumentasi model data otomatis dengan <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> (JSON Schema sebagai dasar OpenAPI itu sendiri).
* Dirancang dengan standar ini setelah analisis yang cermat. bukan hanya sebagai lapisan tambahan yang diimplementasikan setelahnya.
* Hal ini juga memungkinkan **membuat klien kode** otomatis dalam banyak bahasa.

### Dokumentasi Otomatis

Dokumentasi API interaktif dan antarmuka pengguna web untuk eksplorasi. Karena framework kerja ini mengacu pada OpenAPI, terdapat beberapa pilihan, 2 di antaranya sudah termasuk secara bawaan.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>, Dengan eksplorasi interaktif, panggil dan uji API kamu langsung dari browser.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Dokumentasi API alternatif dengan <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a>.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Hanya Python Modern

Semuanya didasarkan pada deklarasi tipe Python 3.6 standar (berkat Pydantic). Tidak ada sintaks baru yang perlu dipelajari. Hanya standar Python modern.

Jika kamu memerlukan tutorial singkat selama 2 menit tentang cara menggunakan tipe data Python (meskipun kamu tidak menggunakan FastAPI), lihat tutorial singkat ini: [Python Types](python-types.md){.internal-link target=_blank}.

Menulis Python standar dengan tipe data:

```Python
from datetime import date

from pydantic import BaseModel

# deklarasi variable dengan tipe str
# dan mendapatkan editor support di dalam function
def main(user_id: str):
    return user_id


# Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

Yang kemudian dapat digunakan seperti:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

!!! info
    `**second_user_data` berarti:

    Gunakan kunci dan nilai dict `second_user_data` secara langsung sebagai key-value, yang setara dengan: `User(id=4, name="Mary", join="2018-11-30")`

### Dukungan Editor

Semua framework dirancang agar mudah dan intuitif untuk digunakan, semua keputusan diuji pada banyak editor bahkan sebelum memulai pengembangan, untuk memastikan pengalaman pengembangan terbaik.

Dalam survei pengembang Python terakhir sudah jelas. <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">bahwa fitur yang paling banyak digunakan adalah "autocompletion"</a>.

Seluruh framework **FastAPI** didasarkan pada hal tersebut. Autocompletion bekerja dimanapun.

Kamu jarang perlu kembali ke dokumentasi.

Berikut cara editor-mu dapat membantu kamu:

* di <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* di <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

Kamu akan menyelesaikan kode yang mungkin kamu anggap mustahil sebelumnya. Misalnya, kunci `harga` di dalam badan JSON (yang bisa saja bersarang) yang berasal dari permintaan.

Tidak perlu lagi mengetik nama kunci yang salah, bolak-balik antar dokumen, atau menggulir ke atas dan ke bawah untuk mengetahui apakah kamu akhirnya menggunakan `username` atau `user_name`.

### Singkat

Memiliki **nilai bawaan** yang masuk akal untuk semua hal, dengan konfigurasi opsional di mana-mana. Semua parameter dapat disesuaikan untuk melakukan apa yang kamu butuhkan dan untuk mendefinisikan API yang kamu perlukan.

Namun, secara default, semuanya **"berfungsi dengan baik"**

### Validasi

* Validasi untuk sebagian besar (atau semua?) **tipe data** Python, termasuk:
    * JSON objek (`dict`).
    * JSON array (`list`) mendefinisikan tipe barang.
    * String (`str`), mendefinisikan panjang minimal dan maksimal.
    * Angka (`int`, `float`) dengan nilai minimal dan maksimal, dll.

* Validasi untuk tipe data yang lebih eksotik, seperti:
    * URL.
    * Email.
    * UUID.
    * ...dan lain-lain.

Semua validasi ditangani oleh **Pydantic**, sebuah alat yang sudah teruji dan kuat.

### Keamanan dan autentikasi

Keamanan dan autentikasi yang terintegrasi. Tanpa berkompromi dengan database atau model data.

Semua skema keamanan yang ditentukan di OpenAPI, termasuk:

* HTTP Basic.
* **OAuth2** (dengan **JWT tokens**). Cek tutorial di [OAuth2 dengan JWT](tutorial/security/oauth2-jwt.md){.internal-link target=_blank}.
* API keys didalam:
    * Headers.
    * Query parameters.
    * Cookies, dll.

Plus semua fitur keamanan dari Starlette (Termassuk **session cookies**).

Semuanya dibangun sebagai alat dan komponen yang dapat digunakan kembali dan mudah diintegrasikan dengan sistem-mu, penyimpanan data, database relasional dan NoSQL, dll.

### Injeksi Dependensi

FastAPI menyertakan fitur yang sangat mudah digunakan, namun sangat kuat <abbr title='juga di kenal sebagai "components", "resources", "services", "providers"'><strong>Injeksi Dependensi</strong></abbr> sistem.

* Bahkan dependensi pun bisa memiliki dependensi, sehingga menciptakan hierarki atau **"grafik" dependensi**.
* semua **otomatis ditangani** oleh framework.
* Semua dependensi dapat memerlukan data dari permintaan dan **menambah batasan operasi jalur** dan dokumentasi otomatis.
* **Validasi otomatis** bahkan untuk parameter *operasi jalur* yang ditentukan dalam dependensi.
* Dukungan untuk sistem autentikasi penggunaan yang kompleks, **koneksi database**, dll.
* **Tanpa kompromi** dengan database, frontend, dll. Namun integrasi yang mudah dengan semuanya.

### "plug-ins" Tanpa Batas

atau dengan kata lain, tidak butuh, impor dan gunakan kode yang kamu perlukan.

Integrasi apa pun dirancang agar mudah digunakan (dengan dependensi) sehingga kamu dapat membuat "plug-in" untuk aplikasi kamu dalam 2 baris kode menggunakan struktur dan sintaksis yang sama dengan yang digunakan untuk *operasi jalur* kamu.

### Uji

* 100% <abbr title="Jumlah kode yang diuji secara otomatis">cangkupan tes</abbr>.
* 100% <abbr title="Python tipe annotations, dengan ini editor dan alat eksternal kamu dapat memberi dukungan yang lebih baik">tipe annotated</abbr> basis kode.
* Digunakan dalam aplikasi produksi.

## Fitur-fitur Starlette

**FastAPI** sepenuhnya kompatibel dengan (dan berdasarkan) <a href="https://www.starlette.io/" class="external-link" target="_blank"><strong>Starlette</strong></a>. Jadi, kode tambahan Starlette apa pun yang kamu miliki, juga akan berfungsi.

`FastAPI` sebenarnya adalah sub-kelas dari `Starlette`. Jadi, jika kamu sudah mengetahui atau menggunakan Starlette, sebagian besar fungsinya akan bekerja dengan cara yang sama.

Dengan **FastAPI** kamu mendapatkan semua **Starlette**'s fitur (Karena FastAPI hanyalah Starlette yang ditingkatkan):

* Performa yang sangat mengesankan. Ini adalah <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">salah satu framework Python tercepat yang tersedia, setara dengan **NodeJS** dan **Go**</a>.
* Didukung **WebSocket**.
* Didukung **GraphQL**.
* Tugas latar belakang yang sedang dalam proses.
* Startup dan shutdown events.
* Tes klien dibuat dengan HTTPX.
* **CORS**, GZip, Static Files, Streaming responses.
* Dukungan **Session dan Cookie**.
* 100% cangkupan tes.
* 100% tipe annotated kode basis.

## Fitur-fitur Pydantic

**FastAPI** sepenuhnya kompatibel dengan (dan berdasarkan) <a href="https://pydantic-docs.helpmanual.io" class="external-link" target="_blank"><strong>Pydantic</strong></a>. Jadi,  kode tambahan Pydantic apa pun yang kamu miliki, juga akan berfungsi.

Termasuk perpustakaan eksternal juga berbasis Pydantic, seperti <abbr title="Object-Relational Mapper">ORM</abbr>s, <abbr title="Object-Document Mapper">ODM</abbr>s untuk database.

Ini juga berarti bahwa dalam banyak kasus kamu dapat meneruskan objek yang sama yang kamu dapatkan dari permintaan **langsung ke database**, karena semuanya divalidasi secara otomatis.

Hal yang sama berlaku sebaliknya, dalam banyak kasus kamu cukup meneruskan objek yang kamu dapatkan dari database **langsung ke klien**.

Dengan **FastAPI** kamu mendapatkan semua **Pydantic**'s fitur (karena FastAPI didasarkan pada Pydantic untuk semua penanganan data):

* **Tidak ada kesulitan untuk dipahami**:
    * Tidak ada bahasa baru yang perlu dipelajari.
    * Jika kamu tau Python tipe kamu tau cara menggunakan Pydantic.
* Berinteraksi dengan baik dengan **<abbr title="Integrated Development Environment, sama halnya dengan code editor">IDE</abbr>/<abbr title="sebuah program untuk cek sebuah error di code">linter</abbr>/brain**:
    * Karena struktur data pydantic hanyalah turunan dari kelas yang kamu tentukan; auto-completion, linting, mypy, dan intuisi kamu semuanya akan berfungsi dengan baik dengan data kamu yang telah divalidasi.
* Validasi **kompleks struktur**:
    * Pemanfaatan model Pydantic berhirarki, `List` dan `Dict` dari Python `typing`’s, dan sebagainya.
    * Dan validator memungkinkan skema data kompleks untuk dapat didefinisikan, diperiksa, dan didokumentasikan dengan jelas dan mudah seperti JSON Schema.
    * Kamu dapat memiliki **objek JSON** yang sangat dalam dan membuat semuanya divalidasi dan diberi anotasi.
* **Diperluas**:
    * Pydantic memungkinkan tipe data khusus ditentukan atau kamu dapat memperluas validasi dengan metode pada model yang dihiasi dengan dekorator validator.
* 100% cangkupan tes.
