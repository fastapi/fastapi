# Alternatif, Inspirasi dan Perbandingan

Apa yang menginspirasi **FastAPI**, bagaimana bila dibandingkan dengan alternatif lain dan apa yang dapat kita pelajari dari sana.

## Pengantar

**FastAPI** tidak akan ada tanpa pekerjaan sebelumnya dari orang lain.

Ada banyak alat yang dibuat sebelumnya dan telah membantu menginspirasi pembuatannya.

Saya telah menghindari pembuatan kerangka kerja baru selama beberapa tahun. Pertama saya mencoba menyelesaikan semua fitur yang dicakup oleh **FastAPI** menggunakan banyak kerangka kerja, plug-in, dan alat yang berbeda.

Tetapi pada titik tertentu, tidak ada pilihan lain selain membuat sesuatu yang menyediakan semua fitur ini, mengambil ide terbaik dari alat sebelumnya, dan menggabungkannya dengan cara terbaik, menggunakan fitur bahasa yang bahkan tidak tersedia sebelumnya (Python 3.6+ petunjuk tipe).

## Alat Sebelumnya

### <a href="https://www.djangoproject.com/" class="external-link" target="_blank">Django</a>

Django adalah kerangka kerja Python paling populer dan dipercaya secara luas. Digunakan untuk membangun sistem seperti Instagram.

Django relatif erat digabungkan dengan database relasional (seperti MySQL atau PostgreSQL), jadi, memiliki database NoSQL (seperti Couchbase, MongoDB, Cassandra, dll) sebagai mesin penyimpanan utama tidaklah mudah.

Django dibuat untuk menghasilkan HTML di backend, bukan untuk membuat API yang digunakan oleh frontend modern (seperti React, Vue.js, dan Angular) atau oleh sistem lain (seperti <abbr title="Internet of Things">IoT</abbr > perangkat) berkomunikasi dengannya.

### <a href="https://www.django-rest-framework.org/" class="external-link" target="_blank">Django REST Framework</a>

Kerangka kerja Django REST dibuat untuk menjadi alat yang fleksibel untuk membangun API Web menggunakan Django di bawahnya, untuk meningkatkan kemampuan API-nya.

Ini digunakan oleh banyak perusahaan termasuk Mozilla, Red Hat dan Eventbrite.

Ini adalah salah satu contoh pertama **dokumentasi API otomatis**, dan ini secara khusus merupakan salah satu ide pertama yang mengilhami "pencarian" **FastAPI**.

!!! note
     Kerangka Django REST dibuat oleh Tom Christie. Pembuat Starlette dan Uvicorn yang sama, yang menjadi dasar **FastAPI**.

!!! check "**FastAPI** terinspirasi untuk"
     Memiliki antarmuka pengguna web dokumentasi API otomatis.

### <a href="https://flask.palletsprojects.com" class="external-link" target="_blank">Flask</a>

Flask adalah "microframework", tidak termasuk integrasi database, atau banyak hal yang ada secara default di Django.

Kesederhanaan dan fleksibilitas ini memungkinkan melakukan hal-hal seperti menggunakan database NoSQL sebagai sistem penyimpanan data utama.

Karena sangat sederhana, relatif intuitif untuk dipelajari, meskipun dokumentasinya agak teknis di beberapa titik.

Hal ini juga biasa digunakan untuk aplikasi lain yang tidak perlu database, manajemen pengguna, atau salah satu dari banyak fitur yang telah ada di Django. Meskipun banyak dari fitur ini dapat ditambahkan dengan plug-in.

Pemisahan bagian-bagian ini, dan menjadi "kerangka mikro" yang dapat diperluas untuk mencakup apa yang dibutuhkan adalah fitur utama yang ingin saya pertahankan.

Mengingat kesederhanaan Flask, sepertinya cocok untuk membangun API. Hal berikutnya yang ditemukan adalah "Django REST Framework" untuk Flask.

!!! check "**FastAPI** terinspirasi untuk"
     Menjadi kerangka mikro. Memudahkan dalam memadupadankan alat dan bagian yang dibutuhkan.

    Memiliki sistem perutean yang sederhana dan mudah digunakan.


### <a href="https://requests.readthedocs.io" class="external-link" target="_blank">Requests</a>

**FastAPI** sebenarnya bukan alternatif dari **Requests**. Lingkup mereka sangat berbeda.

Sebenarnya sudah biasa bila menggunakan Requests *di dalam* aplikasi FastAPI.

Tapi tetap saja, FastAPI mendapat cukup banyak inspirasi dari Requests.

**Requests** adalah pustaka untuk *berinteraksi* dengan API (sebagai klien), sedangkan **FastAPI** adalah pustaka untuk *membangun* API (sebagai server).

Mereka, kurang lebih, di ujung yang berlawanan, tetapi saling melengkapi.

Requests memiliki desain yang sangat sederhana dan intuitif, sangat mudah digunakan, dengan standar yang masuk akal. Tetapi pada saat yang sama, sangat kuat dan dapat disesuaikan.

Itu sebabnya, seperti yang dikatakan di situs web resmi:

> Requests adalah salah satu paket Python yang paling banyak diunduh sepanjang masa

Cara Anda menggunakannya sangat sederhana. Misalnya, untuk melakukan permintaan `GET`, Anda akan menulis:

```Python
response = requests.get("http://example.com/some/url")
```

Pada sisi FastAPI *operasi jalur* bisa terlihat seperti:

```Python hl_lines="1"
@app.get("/some/url")
def read_url():
    return {"message": "Hello World"}
```

Lihat persamaan pada `requests.get(...)` dan `@app.get(...)`.

!!! check "**FastAPI terinspirasi** untuk"
     * Memiliki API yang sederhana dan intuitif.
     * Gunakan nama metode HTTP (operasi) secara langsung, dengan cara yang lugas dan intuitif.
     * Memiliki default yang masuk akal, tetapi kustomisasi yang kuat.


### <a href="https://swagger.io/" class="external-link" target="_blank">Swagger</a> / <a href="https://github.com/OAI/OpenAPI-Specification/" class="external-link" target="_blank">OpenAPI</a>

Fitur utama yang saya inginkan dari Django REST Framework adalah dokumentasi API otomatis.

Kemudian saya menemukan bahwa ada standar untuk mendokumentasikan API, menggunakan JSON (atau YAML, ekstensi JSON) yang disebut Swagger.

Dan ada antarmuka pengguna web untuk API Swagger yang sudah dibuat. Jadi, dengan menghasilkan dokumentasi Swagger untuk API akan memungkinkan penggunaan antarmuka web ini secara otomatis.

Pada titik tertentu, Swagger diberikan kepada Linux Foundation, dan namanya dirubah menjadi OpenAPI.

Itu sebabnya ketika berbicara tentang versi 2.0, biasanya dikatakan "Swagger", dan untuk versi 3+ disebut "OpenAPI".

!!! check "**FastAPI** terinspirasi untuk"
    Mengadopsi dan menggunakan standar terbuka untuk spesifikasi API, bukan skema khusus.

    Dan mengintegrasikan antarmuka pengguna berbasis standar:

    * <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>
    * <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>

    Keduanya dipilih karena cukup populer dan stabil, tetapi anda dapat melakukan pencarian cepat, Anda dapat menemukan lusinan antarmuka pengguna alternatif tambahan untuk OpenAPI (yang dapat Anda gunakan dengan **FastAPI**).

### Flask REST frameworks

Ada beberapa kerangka kerja Flask REST, tetapi setelah menginvestasikan waktu dan bekerja untuk menyelidikinya, saya menemukan bahwa banyak yang dihentikan atau ditinggalkan, dengan beberapa masalah yang membuat mereka tidak layak.

### <a href="https://marshmallow.readthedocs.io/en/3.0/" class="external-link" target="_blank">Marshmallow</a>

Salah satu fitur utama yang dibutuhkan oleh sistem API adalah data "<abbr title="juga disebut menyusun, konversi">serialisasi</abbr>" yang mengambil data dari kode (Python) dan mengubahnya menjadi sesuatu yang dapat dikirim melalui jaringan. Misalnya, mengubah objek yang berisi data dari database menjadi objek JSON. Mengubah objek `datetime` menjadi string, dll.

Fitur besar lainnya yang dibutuhkan oleh API adalah validasi data, memastikan bahwa data tersebut valid, dengan parameter tertentu. Misalnya, bahwa beberapa bidang adalah `int`, dan bukan string acak. Ini sangat berguna untuk data yang masuk.

Tanpa sistem validasi data, Anda harus melakukan semua pemeriksaan secara manual, dalam kode.

Fitur-fitur inilah yang disediakan oleh Marshmallow. Ini adalah pustaka yang hebat, dan saya telah sering menggunakannya sebelumnya.

Tapi dibuat sebelum ada petunjuk tipe Python. Jadi, untuk mendefinisikan setiap <abbr title="definisi bagaimana data harus dibentuk">skema</abbr> Anda perlu menggunakan utilitas dan kelas khusus yang disediakan oleh Marshmallow.

!!! check "**FastAPI** terinspirasi untuk"
    Menggunakan kode untuk mendefinisikan "skema" yang menyediakan tipe data dan validasi, secara otomatis.

### <a href="https://webargs.readthedocs.io/en/latest/" class="external-link" target="_blank">Webargs</a>

Fitur besar lainnya yang dibutuhkan oleh API adalah <abbr title="membaca and mengubah ke data Python">menguraikan</abbr> data dari permintaan yang masuk.

Webargs adalah alat yang dibuat untuk bekerja di atas beberapa kerangka kerja, termasuk Flask.

Menggunakan Marshmallow untuk melakukan validasi data. Dan Webargs dibuat oleh pengembang yang sama.

Ini adalah alat yang hebat dan saya juga sering menggunakannya, sebelum memiliki **FastAPI**.

!!! info
    Webargs dibuat oleh pengembang yang sama dengan Marshmallow.

!!! check "**FastAPI** terinspirasi untuk"
    Validasi otomatis untuk data permintaan yang masuk.

### <a href="https://apispec.readthedocs.io/en/stable/" class="external-link" target="_blank">APISpec</a>

Marshmallow dan Webargs menyediakan validasi, parsing, dan serialisasi sebagai plug-in.

Tapi belum ada dokumentasi. Kemudian dibuatlah APISpec.

APISpec adalah plug-in untuk banyak kerangka kerja (dan ada juga plug-in untuk Starlette).

Cara kerjanya adalah dengan annda menulis definisi skema menggunakan format YAML di dalam docstring dari setiap fungsi yang menangani rute.

Dan akan menghasilkan skema OpenAPI.

Begitu cara kerjanya pada Flask, Starlette, Responder, dan yang lainnya.

Tapi, kita memiliki masalah lagi dengan sintaksis-mikro, di dalam string Python (Yaml besar).

Editor tidak bisa membantu banyak dengan itu. Dan jika kita mengubah parameter atau skema Marshmallow dan lupa merubah docstring YAML, skema yang dihasilkan akan menjadi usang.

!!! info
    APISpec di buat oleh developer yang sama dengan Marshmallow.


!!! check "Menginspirasi **FastAPI** untuk"
    Mendukung standar terbuka untuk API, OpenAPI.

### <a href="https://flask-apispec.readthedocs.io/en/latest/" class="external-link" target="_blank">Flask-apispec</a>

Flask-apispec adalah plug-in Flask, yang menyatukan Webargs, Marshmallow, dan APISpec.

Flask-apispec menggunakan informasi dari Webargs dan Marshmallow untuk menghasilkan skema OpenAPI secara otomatis, menggunakan APISpec.

Flask-apispec adalah alat yang hebat, sangat di bawah nilai. Seharusnya jauh lebih populer daripada banyak plug-in Flask di luar sana. Mungkin karena dokumentasinya terlalu ringkas dan abstrak.

Flask-apispec menyelesaikan masalah dimana kita harus menulis YAML (sintaksis yang lain) didalam docstring Python.

Kombinasi Flask, Flask-apispec dengan Marshmallow dan Webargs ini adalah kommbinasi backend favorit saya sampai membuat **FastAPI**.

Penggunaannya mengarah pada pembuatan beberapa generator `Flask full-stack`. Ini adalah kombinasi utama dimana saya (dan beberapa tim external) gunakan hingga sekarang:

* <a href="https://github.com/tiangolo/full-stack" class="external-link" target="_blank">https://github.com/tiangolo/full-stack</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchbase</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchdb" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchdb</a>

Dan generator full-stack yang sama ini adalah dasar dari [**FastAPI** Project Generators](project-generation.md){.internal-link target=_blank}.

!!! info
    Flask-apispec dibuat oleh pengembang Marshmallow yang sama.

!!! check "Menginspirasi **FastAPI** untuk"
    Menghasilkan skema OpenAPI secara otomatis, dari kode yang sama yang mendefinisikan serialisasi dan validasi.

### <a href="https://nestjs.com/" class="external-link" target="_blank">NestJS</a> (and <a href="https://angular.io/" class="external-link" target="_blank">Angular</a>)

NestJS bahkan bukan Python, NestJS adalah kerangka kerja JavaScript NodeJS (TypeScript) yang terinspirasi oleh Angular.

NestJS mencapai sesuatu yang agak mirip dengan apa yang dapat dilakukan dengan Flask-apispec.

NestJS memiliki sistem injeksi ketergantungan yang terintegrasi, terinspirasi oleh Angular dua. NestJS membutuhkan pre-registering "injectables" (seperti semua sistem injeksi ketergantungan lain yang saya tahu), jadi, dapat menambah verbositas dan pengulangan kode.

Karena parameter dijelaskan dengan tipe TypeScript (mirip dengan petunjuk tipe Python), dukungan editor cukup baik.

Tetapi karena data TypeScript tidak disimpan setelah dikompilasi ke JavaScript, itu tidak dapat bergantung pada jenis untuk mendefinisikan validasi, serialisasi, dan dokumentasi pada saat yang bersamaan. Karena ini dan beberapa keputusan desain, untuk mendapatkan validasi, serialisasi, dan pembuatan skema otomatis, diperlukan penambahan dekorator di banyak tempat. Dan menjadikannya sangat bertele-tele.

NestJS tidak dapat menangani model bersarang dengan baik. Jadi, apabila badan JSON dalam permintaan adalah objek JSON yang memiliki bidang dalam yang pada gilirannya adalah objek JSON bersarang, maka tidak dapat didokumentasikan dan divalidasi dengan benar.

!!! check "**FastAPI** terinspirasi untuk"
    Menggunakan tipe Python untuk mendapatkan dukungan editor.

    Memiliki sistem injeksi ketergantungan yang kuat. Menemukan cara untuk meminimalkan pengulangan kode.

### <a href="https://sanic.readthedocs.io/en/latest/" class="external-link" target="_blank">Sanic</a>

Sanic adalah salah satu kerangka kerja Python pertama yang sangat cepat berdasarkan `asyncio`. Sanic dibuat sangat mirip dengan Flask.

!!! note "Detail Teknis"
    Sanic menggunakan <a href="https://github.com/MagicStack/uvloop" class="external-link" target="_blank">`uvloop`</a> alih-alih loop `asyncio` default Python. Itulah yang membuatnya begitu cepat.

    Hal ini yang mengilhami Uvicorn dan Starlette, yang saat ini lebih cepat dari Sanic dalam benchmark terbuka.

!!! check "Menginspirasi **FastAPI** untuk"
    Temukan cara untuk memiliki kinerja yang gila.
    
    Itulah alasan mengapa **FastAPI** didasarkan pada Starlette, karena ini adalah kerangka kerja tercepat yang tersedia (diuji oleh benchmark pihak ketiga).

### <a href="https://falconframework.org/" class="external-link" target="_blank">Falcon</a>

Falcon adalah kerangka kerja Python berkinerja tinggi lainnya, dirancang agar minimal, dan berfungsi sebagai dasar kerangka kerja lain seperti Hug.

Falcon menggunakan standar sebelumnya untuk kerangka kerja web Python (WSGI) yang sinkron, sehingga tidak dapat menangani WebSockets dan kasus penggunaan lainnya. Namun demikian, Falcon juga memiliki kinerja yang sangat baik.

Falcon dirancang untuk memiliki fungsi yang menerima dua parameter, satu "permintaan" dan satu "tanggapan". Kemudian Anda "membaca" bagian dari permintaan, dan "menulis" bagian ke respons. Karena desain ini, tidak mungkin untuk mendeklarasikan parameter dan badan permintaan dengan petunjuk tipe Python standar sebagai parameter fungsi.

Jadi, validasi data, serialisasi, dan dokumentasi, harus dilakukan secara kode, bukan otomatis. Atau hal tersebut harus diimplementasikan sebagai kerangka kerja di atas Falcon, seperti Hug. Perbedaan yang sama ini terjadi pada kerangka kerja lain yang terinspirasi oleh desain Falcon, yang memiliki satu objek permintaan dan satu objek respons sebagai parameter.

!!! check "Menginspirasi **FastAPI** untuk"
    Temukan cara untuk mendapatkan performa hebat.

    Bersamaan dengan Hug (karena Hug didasarkan pada Falcon) menginspirasi **FastAPI** untuk mendeklarasikan parameter `response` dalam fungsi.

    Meskipun pada FastAPI itu adalah hal yang opsional, dan digunakan terutama untuk mengatur header, cookie, dan kode status alternatif.

### <a href="https://moltenframework.com/" class="external-link" target="_blank">Molten</a>

Saya menemukan Molten pada tahap pertama pembuatan **FastAPI**. Dan Molten memiliki ide yang sangat mirip:

* Berdasarkan petunjuk tipe Python.
* Validasi dan dokumentasi dari tipe ini.
* Sistem Injeksi Ketergantungan.

Molten tidak menggunakan validasi data, serialisasi, dan dokumentasi pustaka pihak ketiga seperti Pydantic, ia memiliki pustaka sendiri. Jadi, definisi tipe data ini tidak akan dapat digunakan kembali dengan mudah.

Molten membutuhkan sedikit lebih banyak konfigurasi verbose. Dan karena didasarkan pada WSGI (bukan ASGI), Molten tidak dirancang untuk memanfaatkan kinerja tinggi yang disediakan oleh alat seperti Uvicorn, Starlette, dan Sanic.

Sistem injeksi dependensi memerlukan pra-pendaftaran dependensi dan dependensi diselesaikan berdasarkan tipe yang dideklarasikan. Jadi, tidak mungkin mendeklarasikan lebih dari satu "komponen" yang menyediakan tipe tertentu.

Rute dideklarasikan di satu tempat, menggunakan fungsi yang dideklarasikan di tempat lain (daripada menggunakan dekorator yang dapat ditempatkan tepat di atas fungsi yang menangani titik akhir). Ini lebih mirip dengan bagaimana cara kerja Django dibandingkan dengan Flask (dan Starlette) melakukannya. Hal ini memisahkan hal-hal yang relatif erat digabungkan.

!!! check "Menginspiriasi **FastAPI** untuk"
    Menentukan validasi tambahan untuk tipe data yang menggunakan nilai "default" dari atribut model. Hal ini meningkatkan dukungan editor, dan sebelumnya tidak tersedia di Pydantic.

    Hal ini yang sebenarnya mengilhami pembaruan Pydantic, agar dapat mendukung gaya deklarasi validasi yang sama (semua fungsi ini sekarang sudah tersedia di Pydantic).

### <a href="https://www.hug.rest/" class="external-link" target="_blank">Hug</a>

Hug adalah salah satu kerangka kerja pertama yang mengimplementasikan deklarasi tipe parameter API menggunakan petunjuk tipe Python. Ini adalah ide bagus yang menginspirasi alat lain untuk melakukan hal yang sama.

Hug menggunakan tipe khusus dalam deklarasinya alih-alih tipe Python standar, tetapi hal itu masih merupakan langkah maju yang besar.

Hal itu juga merupakan salah satu kerangka kerja pertama yang menghasilkan skema khusus yang mendeklarasikan seluruh API di JSON.

Hug tidak didasarkan pada standar seperti OpenAPI dan JSON Schema. Jadi tidak mudah untuk mengintegrasikannya dengan alat lain, seperti UI Swagger. Tapi sekali lagi, itu adalah ide yang sangat inovatif.

Hug memiliki fitur yang menarik dan tidak biasa: menggunakan kerangka kerja yang sama, memungkinkan untuk membuat API dan juga CLI.

Karena didasarkan pada standar sebelumnya untuk kerangka kerja web Python sinkron (WSGI), ia tidak dapat menangani Websockets dan hal-hal lain, meskipun masih memiliki kinerja tinggi juga.

!!! info
    Hug was created by Timothy Crosley, the same creator of <a href="https://github.com/timothycrosley/isort" class="external-link" target="_blank">`isort`</a>, a great tool to automatically sort imports in Python files.

!!! check "Ideas inspired in **FastAPI**"
    Hug inspired parts of APIStar, and was one of the tools I found most promising, alongside APIStar.

    Hug helped inspiring **FastAPI** to use Python type hints to declare parameters, and to generate a schema defining the API automatically.

    Hug inspired **FastAPI** to declare a `response` parameter in functions to set headers and cookies.

### <a href="https://github.com/encode/apistar" class="external-link" target="_blank">APIStar</a> (<= 0.5)

Right before deciding to build **FastAPI** I found **APIStar** server. It had almost everything I was looking for and had a great design.

It was one of the first implementations of a framework using Python type hints to declare parameters and requests that I ever saw (before NestJS and Molten). I found it more or less at the same time as Hug. But APIStar used the OpenAPI standard.

It had automatic data validation, data serialization and OpenAPI schema generation based on the same type hints in several places.

Body schema definitions didn't use the same Python type hints like Pydantic, it was a bit more similar to Marshmallow, so, editor support wouldn't be as good, but still, APIStar was the best available option.

It had the best performance benchmarks at the time (only surpassed by Starlette).

At first, it didn't have an automatic API documentation web UI, but I knew I could add Swagger UI to it.

It had a dependency injection system. It required pre-registration of components, as other tools discussed above. But still, it was a great feature.

I was never able to use it in a full project, as it didn't have security integration, so, I couldn't replace all the features I was having with the full-stack generators based on Flask-apispec. I had in my backlog of projects to create a pull request adding that functionality.

But then, the project's focus shifted.

It was no longer an API web framework, as the creator needed to focus on Starlette.

Now APIStar is a set of tools to validate OpenAPI specifications, not a web framework.

!!! info
    APIStar was created by Tom Christie. The same guy that created:

    * Django REST Framework
    * Starlette (in which **FastAPI** is based)
    * Uvicorn (used by Starlette and **FastAPI**)

!!! check "Inspired **FastAPI** to"
    Exist.

    The idea of declaring multiple things (data validation, serialization and documentation) with the same Python types, that at the same time provided great editor support, was something I considered a brilliant idea.
    
    And after searching for a long time for a similar framework and testing many different alternatives, APIStar was the best option available.

    Then APIStar stopped to exist as a server and Starlette was created, and was a new better foundation for such a system. That was the final inspiration to build **FastAPI**.

    I consider **FastAPI** a "spiritual successor" to APIStar, while improving and increasing the features, typing system, and other parts, based on the learnings from all these previous tools.

## Used by **FastAPI**

### <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a>

Pydantic is a library to define data validation, serialization and documentation (using JSON Schema) based on Python type hints.

That makes it extremely intuitive.

It is comparable to Marshmallow. Although it's faster than Marshmallow in benchmarks. And as it is based on the same Python type hints, the editor support is great.

!!! check "**FastAPI** uses it to"
    Handle all the data validation, data serialization and automatic model documentation (based on JSON Schema).

    **FastAPI** then takes that JSON Schema data and puts it in OpenAPI, apart from all the other things it does.

### <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a>

Starlette is a lightweight <abbr title="The new standard for building asynchronous Python web">ASGI</abbr> framework/toolkit, which is ideal for building high-performance asyncio services.

It is very simple and intuitive. It's designed to be easily extensible, and have modular components.

It has:

* Seriously impressive performance.
* WebSocket support.
* GraphQL support.
* In-process background tasks.
* Startup and shutdown events.
* Test client built on requests.
* CORS, GZip, Static Files, Streaming responses.
* Session and Cookie support.
* 100% test coverage.
* 100% type annotated codebase.
* Zero hard dependencies.

Starlette is currently the fastest Python framework tested. Only surpassed by Uvicorn, which is not a framework, but a server.

Starlette provides all the basic web microframework functionality.

But it doesn't provide automatic data validation, serialization or documentation.

That's one of the main things that **FastAPI** adds on top, all based on Python type hints (using Pydantic). That, plus the dependency injection system, security utilities, OpenAPI schema generation, etc.

!!! note "Technical Details"
    ASGI is a new "standard" being developed by Django core team members. It is still not a "Python standard" (a PEP), although they are in the process of doing that.

    Nevertheless, it is already being used as a "standard" by several tools. This greatly improves interoperability, as you could switch Uvicorn for any other ASGI server (like Daphne or Hypercorn), or you could add ASGI compatible tools, like `python-socketio`.

!!! check "**FastAPI** uses it to"
    Handle all the core web parts. Adding features on top.

    The class `FastAPI` itself inherits directly from the class `Starlette`.
    
    So, anything that you can do with Starlette, you can do it directly with **FastAPI**, as it is basically Starlette on steroids.

### <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>

Uvicorn is a lightning-fast ASGI server, built on uvloop and httptools.

It is not a web framework, but a server. For example, it doesn't provide tools for routing by paths. That's something that a framework like Starlette (or **FastAPI**) would provide on top.

It is the recommended server for Starlette and **FastAPI**.

!!! check "**FastAPI** recommends it as"
    The main web server to run **FastAPI** applications.

    You can combine it with Gunicorn, to have an asynchronous multi-process server.

    Check more details in the [Deployment](deployment/index.md){.internal-link target=_blank} section.

## Benchmarks and speed

To understand, compare, and see the difference between Uvicorn, Starlette and FastAPI, check the section about [Benchmarks](benchmarks.md){.internal-link target=_blank}.
