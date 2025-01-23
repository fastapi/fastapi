# Berkas Statis

Anda dapat menyajikan berkas statis secara otomatis dari sebuah direktori menggunakan `StaticFiles`.

## Penggunaan `StaticFiles`

* Mengimpor `StaticFiles`.
* "Mount" representatif `StaticFiles()` di jalur spesifik.

{* ../../docs_src/static_files/tutorial001.py hl[2,6] *}

/// note | Detail Teknis

Anda dapat pula menggunakan `from starlette.staticfiles import StaticFiles`.

**FastAPI** menyediakan `starlette.staticfiles` sama seperti `fastapi.staticfiles` sebagai kemudahan pada Anda, yaitu para pengembang. Tetapi ini asli berasal langsung dari Starlette.

///

### Apa itu "Mounting"

"Mounting" dimaksud menambah aplikasi "independen" secara lengkap di jalur spesifik, kemudian menangani seluruh sub-jalur.

Hal ini berbeda dari menggunakan `APIRouter` karena aplikasi yang dimount benar-benar independen. OpenAPI dan dokumentasi dari aplikasi utama Anda tak akan menyertakan apa pun dari aplikasi yang dimount, dst.

Anda dapat mempelajari mengenai ini dalam [Panduan Pengguna Lanjutan](../advanced/index.md){.internal-link target=_blank}.

## Detail

Terhadap `"/static"` pertama mengacu pada sub-jalur yang akan menjadi tempat "sub-aplikasi" ini akan "dimount". Maka, jalur apa pun yang dimulai dengan `"/static"` akan ditangani oleh sub-jalur tersebut.

Terhadap `directory="static"` mengacu pada nama direktori yang berisi berkas statis Anda.

Terhadap `name="static"` ialah nama yang dapat digunakan secara internal oleh **FastAPI**.

Seluruh parameter ini dapat berbeda dari sekadar "`static`", sesuaikan parameter dengan keperluan dan detail spesifik akan aplikasi Anda.

## Info lanjutan

Sebagai detail dan opsi tambahan lihat <a href="https://www.starlette.io/staticfiles/" class="external-link" target="_blank">dokumentasi Starlette perihal Berkas Statis</a>.
