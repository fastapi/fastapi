# Ortam Değişkenleri { #environment-variables }

/// tip | İpucu

"Ortam değişkenleri"nin ne olduğunu ve nasıl kullanılacağını zaten biliyorsanız, bu bölümü atlayabilirsiniz.

///

Ortam değişkeni (genelde "**env var**" olarak da anılır), Python kodunun **dışında**, **işletim sistemi** seviyesinde bulunan ve Python kodunuz (veya diğer programlar) tarafından okunabilen bir değişkendir.

Ortam değişkenleri; uygulama **ayarları**nı yönetmek, Python’un **kurulumu**nun bir parçası olarak konfigürasyon yapmak vb. durumlarda işe yarar.

## Env Var Oluşturma ve Kullanma { #create-and-use-env-vars }

Python’a ihtiyaç duymadan, **shell (terminal)** içinde ortam değişkenleri **oluşturabilir** ve kullanabilirsiniz:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// You could create an env var MY_NAME with
$ export MY_NAME="Wade Wilson"

// Then you could use it with other programs, like
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Create an env var MY_NAME
$ $Env:MY_NAME = "Wade Wilson"

// Use it with other programs, like
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## Python’da env var Okuma { #read-env-vars-in-python }

Ortam değişkenlerini Python’un **dışında** (terminalde veya başka bir yöntemle) oluşturup daha sonra **Python’da okuyabilirsiniz**.

Örneğin `main.py` adında bir dosyanız şöyle olabilir:

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip | İpucu

<a href="https://docs.python.org/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> fonksiyonunun ikinci argümanı, bulunamadığında döndürülecek varsayılan (default) değerdir.

Verilmezse varsayılan olarak `None` olur; burada varsayılan değer olarak `"World"` verdik.

///

Sonrasında bu Python programını çalıştırabilirsiniz:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Here we don't set the env var yet
$ python main.py

// As we didn't set the env var, we get the default value

Hello World from Python

// But if we create an environment variable first
$ export MY_NAME="Wade Wilson"

// And then call the program again
$ python main.py

// Now it can read the environment variable

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Here we don't set the env var yet
$ python main.py

// As we didn't set the env var, we get the default value

Hello World from Python

// But if we create an environment variable first
$ $Env:MY_NAME = "Wade Wilson"

// And then call the program again
$ python main.py

// Now it can read the environment variable

Hello Wade Wilson from Python
```

</div>

////

Ortam değişkenleri kodun dışında ayarlanabildiği, ama kod tarafından okunabildiği ve dosyalarla birlikte saklanmasının (ör. `git`’e commit edilmesinin) gerekmediği için, konfigürasyon veya **ayarlar** için sıkça kullanılır.

Ayrıca, bir ortam değişkenini yalnızca **belirli bir program çalıştırımı** için oluşturabilirsiniz; bu değişken sadece o program tarafından, sadece o çalıştırma süresince kullanılabilir.

Bunu yapmak için, program komutunun hemen öncesinde ve aynı satırda tanımlayın:

<div class="termy">

```console
// Create an env var MY_NAME in line for this program call
$ MY_NAME="Wade Wilson" python main.py

// Now it can read the environment variable

Hello Wade Wilson from Python

// The env var no longer exists afterwards
$ python main.py

Hello World from Python
```

</div>

/// tip | İpucu

Bu konuyla ilgili daha fazlasını <a href="https://12factor.net/config" class="external-link" target="_blank">Twelve-Factor Uygulaması: Config</a> bölümünde okuyabilirsiniz.

///

## Tipler ve Doğrulama { #types-and-validation }

Bu ortam değişkenleri yalnızca **metin string**’lerini taşıyabilir. Çünkü Python’un dışındadırlar ve diğer programlarla, sistemin geri kalanıyla (hatta Linux, Windows, macOS gibi farklı işletim sistemleriyle) uyumlu olmak zorundadırlar.

Bu, Python’da bir ortam değişkeninden okunan **her değerin `str` olacağı** anlamına gelir. Farklı bir tipe dönüştürme veya doğrulama işlemleri kod içinde yapılmalıdır.

Uygulama **ayarları**nı yönetmek için ortam değişkenlerini kullanmayı, [İleri Seviye Kullanıcı Rehberi - Ayarlar ve Ortam Değişkenleri](./advanced/settings.md){.internal-link target=_blank} bölümünde daha detaylı öğreneceksiniz.

## `PATH` Ortam Değişkeni { #path-environment-variable }

İşletim sistemlerinin (Linux, macOS, Windows) çalıştırılacak programları bulmak için kullandığı **özel** bir ortam değişkeni vardır: **`PATH`**.

`PATH` değişkeninin değeri uzun bir string’dir; Linux ve macOS’te dizinler iki nokta üst üste `:` ile, Windows’ta ise noktalı virgül `;` ile ayrılır.

Örneğin `PATH` ortam değişkeni şöyle görünebilir:

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

Bu, sistemin şu dizinlerde program araması gerektiği anlamına gelir:

* `/usr/local/bin`
* `/usr/bin`
* `/bin`
* `/usr/sbin`
* `/sbin`

////

//// tab | Windows

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32
```

Bu, sistemin şu dizinlerde program araması gerektiği anlamına gelir:

* `C:\Program Files\Python312\Scripts`
* `C:\Program Files\Python312`
* `C:\Windows\System32`

////

Terminalde bir **komut** yazdığınızda, işletim sistemi `PATH` ortam değişkeninde listelenen **bu dizinlerin her birinde** programı **arar**.

Örneğin terminalde `python` yazdığınızda, işletim sistemi bu listedeki **ilk dizinde** `python` adlı bir program arar.

Bulursa **onu kullanır**. Bulamazsa **diğer dizinlerde** aramaya devam eder.

### Python Kurulumu ve `PATH`’in Güncellenmesi { #installing-python-and-updating-the-path }

Python’u kurarken, `PATH` ortam değişkenini güncellemek isteyip istemediğiniz sorulabilir.

//// tab | Linux, macOS

Diyelim ki Python’u kurdunuz ve `/opt/custompython/bin` dizinine yüklendi.

`PATH` ortam değişkenini güncellemeyi seçerseniz, kurulum aracı `/opt/custompython/bin` yolunu `PATH` ortam değişkenine ekler.

Şöyle görünebilir:

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

Böylece terminalde `python` yazdığınızda, sistem `/opt/custompython/bin` (son dizin) içindeki Python programını bulur ve onu kullanır.

////

//// tab | Windows

Diyelim ki Python’u kurdunuz ve `C:\opt\custompython\bin` dizinine yüklendi.

`PATH` ortam değişkenini güncellemeyi seçerseniz, kurulum aracı `C:\opt\custompython\bin` yolunu `PATH` ortam değişkenine ekler.

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

Böylece terminalde `python` yazdığınızda, sistem `C:\opt\custompython\bin` (son dizin) içindeki Python programını bulur ve onu kullanır.

////

Yani şunu yazarsanız:

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

Sistem `python` programını `/opt/custompython/bin` içinde **bulur** ve çalıştırır.

Bu, kabaca şunu yazmaya denktir:

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

Sistem `python` programını `C:\opt\custompython\bin\python` içinde **bulur** ve çalıştırır.

Bu, kabaca şunu yazmaya denktir:

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

Bu bilgiler, [Virtual Environments](virtual-environments.md){.internal-link target=_blank} konusunu öğrenirken işinize yarayacak.

## Sonuç { #conclusion }

Buraya kadar **ortam değişkenleri**nin ne olduğuna ve Python’da nasıl kullanılacağına dair temel bir fikir edinmiş olmalısınız.

Ayrıca <a href="https://en.wikipedia.org/wiki/Environment_variable" class="external-link" target="_blank">Ortam Değişkeni için Wikipedia</a> sayfasından daha fazlasını da okuyabilirsiniz.

Çoğu zaman ortam değişkenlerinin hemen nasıl işe yarayacağı ilk bakışta çok net olmayabilir. Ancak geliştirme yaparken birçok farklı senaryoda tekrar tekrar karşınıza çıkarlar; bu yüzden bunları bilmek faydalıdır.

Örneğin bir sonraki bölümde, [Virtual Environments](virtual-environments.md) konusunda bu bilgilere ihtiyaç duyacaksınız.
