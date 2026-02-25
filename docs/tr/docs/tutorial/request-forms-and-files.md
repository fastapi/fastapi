# Request Forms ve Files { #request-forms-and-files }

`File` ve `Form` kullanarak aynı anda hem dosyaları hem de form alanlarını tanımlayabilirsiniz.

/// info | Bilgi

Yüklenen dosyaları ve/veya form verisini almak için önce <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a> paketini kurun.

Bir [virtual environment](../virtual-environments.md){.internal-link target=_blank} oluşturduğunuzdan, onu aktive ettiğinizden ve ardından paketi kurduğunuzdan emin olun, örneğin:

```console
$ pip install python-multipart
```

///

## `File` ve `Form` Import Edin { #import-file-and-form }

{* ../../docs_src/request_forms_and_files/tutorial001_an_py310.py hl[3] *}

## `File` ve `Form` Parametrelerini Tanımlayın { #define-file-and-form-parameters }

Dosya ve form parametrelerini, `Body` veya `Query` için yaptığınız şekilde oluşturun:

{* ../../docs_src/request_forms_and_files/tutorial001_an_py310.py hl[10:12] *}

Dosyalar ve form alanları form data olarak upload edilir ve siz de dosyaları ve form alanlarını alırsınız.

Ayrıca bazı dosyaları `bytes` olarak, bazılarını da `UploadFile` olarak tanımlayabilirsiniz.

/// warning | Uyarı

Bir *path operation* içinde birden fazla `File` ve `Form` parametresi tanımlayabilirsiniz; ancak request'in body'si `application/json` yerine `multipart/form-data` ile encode edileceği için, JSON olarak almayı beklediğiniz `Body` alanlarını aynı anda tanımlayamazsınız.

Bu **FastAPI** kısıtı değildir; HTTP protokolünün bir parçasıdır.

///

## Özet { #recap }

Aynı request içinde hem veri hem de dosya almanız gerektiğinde `File` ve `Form`'u birlikte kullanın.
