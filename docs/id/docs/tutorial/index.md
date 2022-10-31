# Tutorial - Pedoman Pengguna - Pengenalan

Tutorial ini menunjukan cara menggunakan ***FastAPI*** dengan semua fitur-fiturnya, tahap demi tahap.

Setiap bagian dibangun secara bertahap dari bagian sebelumnya, tetapi terstruktur untuk memisahkan banyak topik, sehingga kamu bisa secara langsung menuju ke topik spesifik untuk menyelesaikan kebutuhan API tertentu.

Ini juga dibangun untuk digunakan sebagai referensi yang akan datang.

Sehingga kamu dapat kembali lagi dan mencari apa yang kamu butuhkan dengan tepat.

## Jalankan kode

Semua blok-blok kode dapat dicopy dan digunakan langsung (Mereka semua sebenarnya adalah file python yang sudah teruji).

Untuk menjalankan setiap contoh, copy kode ke file `main.py`, dan jalankan `uvicorn` dengan:

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

**SANGAT disarankan** agar kamu menulis atau meng-copy kode, meng-editnya dan menjalankannya secara lokal.

Dengan menggunakannya di dalam editor, benar-benar memperlihatkan manfaat dari FastAPI, melihat bagaimana sedikitnya kode yang harus kamu tulis, semua pengecekan tipe, pelengkapan otomatis, dll.

---

## Install FastAPI

Langkah pertama adalah dengan meng-install FastAPI.

Untuk tutorial, kamu mungkin hendak meng-instalnya dengan semua pilihan fitur dan dependensinya:

<div class="termy">

```console
$ pip install "fastapi[all]"

---> 100%
```

</div>

...yang juga termasuk `uvicorn`, yang dapat kamu gunakan sebagai server yang menjalankan kodemu.

!!! catatan
    Kamu juga dapat meng-instalnya bagian demi bagian.

    Hal ini mungkin yang akan kamu lakukan ketika kamu hendak men-deploy aplikasimu ke tahap produksi:

    ```
    pip install fastapi
    ```

    Juga install `uvicorn` untk menjalankan server"

    ```
    pip install "uvicorn[standard]"
    ```

    Dan demikian juga untuk pilihan dependensi yang hendak kamu gunakan.

## Pedoman Pengguna Lanjutan

Tersedia juga **Pedoman Pengguna Lanjutan** yang dapat kamu baca nanti setelah **Tutorial - Pedoman Pengguna** ini.

**Pedoman Pengguna Lanjutan**, dibangun atas hal ini, menggunakan konsep yang sama, dan mengajarkan kepadamu beberapa fitur tambahan.

Tetapi kamu harus membaca terlebih dahulu **Tutorial - Pedoman Pengguna** (apa yang sedang kamu baca sekarang).

Hal ini didesain sehingga kamu dapat membangun aplikasi lengkap dengan hanya **Tutorial - Pedoman Pengguna**, dan kemudian mengembangkannya ke banyak cara yang berbeda, tergantung dari kebutuhanmu, menggunakan beberapa ide-ide tambahan dari **Pedoman Pengguna Lanjutan**.
