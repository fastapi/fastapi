# Debugging { #debugging }

Visual Studio Code veya PyCharm gibi editörünüzde debugger'ı bağlayabilirsiniz.

## `uvicorn`'ı Çağırma { #call-uvicorn }

FastAPI uygulamanızda `uvicorn`'ı import edip doğrudan çalıştırın:

{* ../../docs_src/debugging/tutorial001_py310.py hl[1,15] *}

### `__name__ == "__main__"` Hakkında { #about-name-main }

`__name__ == "__main__"` ifadesinin temel amacı, dosyanız şu şekilde çağrıldığında çalışacak:

<div class="termy">

```console
$ python myapp.py
```

</div>

ancak başka bir dosya onu import ettiğinde çalışmayacak bir kod bölümüne sahip olmaktır, örneğin:

```Python
from myapp import app
```

#### Daha fazla detay { #more-details }

Dosyanızın adının `myapp.py` olduğunu varsayalım.

Şu şekilde çalıştırırsanız:

<div class="termy">

```console
$ python myapp.py
```

</div>

Python tarafından otomatik oluşturulan, dosyanızın içindeki `__name__` adlı dahili değişkenin değeri `"__main__"` string'i olur.

Dolayısıyla şu bölüm:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

çalışır.

---

Ancak modülü (dosyayı) import ederseniz bu gerçekleşmez.

Yani örneğin `importer.py` adında başka bir dosyanız var ve içinde şunlar bulunuyorsa:

```Python
from myapp import app

# Some more code
```

bu durumda `myapp.py` içindeki otomatik oluşturulan `__name__` değişkeni `"__main__"` değerine sahip olmaz.

Bu yüzden şu satır:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

çalıştırılmaz.

/// info | Bilgi

Daha fazla bilgi için <a href="https://docs.python.org/3/library/__main__.html" class="external-link" target="_blank">resmi Python dokümantasyonuna</a> bakın.

///

## Kodunuzu Debugger ile Çalıştırma { #run-your-code-with-your-debugger }

Uvicorn server'ını doğrudan kodunuzdan çalıştırdığınız için, Python programınızı (FastAPI uygulamanızı) debugger'dan doğrudan başlatabilirsiniz.

---

Örneğin Visual Studio Code'da şunları yapabilirsiniz:

* "Debug" paneline gidin.
* "Add configuration..." seçin.
* "Python" seçin
* "`Python: Current File (Integrated Terminal)`" seçeneğiyle debugger'ı çalıştırın.

Böylece server, **FastAPI** kodunuzla başlar; breakpoint'lerinizde durur vb.

Aşağıdaki gibi görünebilir:

<img src="/img/tutorial/debugging/image01.png">

---

PyCharm kullanıyorsanız şunları yapabilirsiniz:

* "Run" menüsünü açın.
* "Debug..." seçeneğini seçin.
* Bir context menü açılır.
* Debug edilecek dosyayı seçin (bu örnekte `main.py`).

Böylece server, **FastAPI** kodunuzla başlar; breakpoint'lerinizde durur vb.

Aşağıdaki gibi görünebilir:

<img src="/img/tutorial/debugging/image02.png">
