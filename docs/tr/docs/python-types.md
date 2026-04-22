# Python Tiplerine Giriş { #python-types-intro }

Python, isteğe bağlı "type hints" (diğer adıyla "type annotations") desteğine sahiptir.

Bu **"type hints"** veya annotations, bir değişkenin <dfn title="örneğin: str, int, float, bool">tip</dfn>'ini bildirmeye yarayan özel bir sözdizimidir.

Değişkenleriniz için tip bildirerek, editörler ve araçlar size daha iyi destek sağlayabilir.

Bu, Python type hints hakkında sadece **hızlı bir eğitim / bilgi tazeleme** dokümanıdır. **FastAPI** ile kullanmak için gereken minimum bilgiyi kapsar... ki aslında bu çok azdır.

**FastAPI** tamamen bu type hints üzerine kuruludur; bunlar ona birçok avantaj ve fayda sağlar.

Ancak hiç **FastAPI** kullanmasanız bile, bunlar hakkında biraz öğrenmeniz size fayda sağlayacaktır.

/// note | Not

Eğer bir Python uzmanıysanız ve type hints hakkında her şeyi zaten biliyorsanız, sonraki bölüme geçin.

///

## Motivasyon { #motivation }

Basit bir örnekle başlayalım:

{* ../../docs_src/python_types/tutorial001_py310.py *}

Bu programı çalıştırınca şu çıktıyı alırsınız:

```
John Doe
```

Fonksiyon şunları yapar:

* `first_name` ve `last_name` değerlerini alır.
* `title()` ile her birinin ilk harfini büyük harfe çevirir.
* Ortada bir boşluk olacak şekilde <dfn title="Onları tek bir bütün olarak bir araya getirir. İçerikler art arda gelir.">Birleştirir</dfn>.

{* ../../docs_src/python_types/tutorial001_py310.py hl[2] *}

### Düzenleyelim { #edit-it }

Bu çok basit bir program.

Ama şimdi bunu sıfırdan yazdığınızı hayal edin.

Bir noktada fonksiyon tanımını yazmaya başlamış olacaktınız, parametreler hazır...

Ama sonra "ilk harfi büyük harfe çeviren method"u çağırmanız gerekiyor.

`upper` mıydı? `uppercase` miydi? `first_uppercase`? `capitalize`?

Sonra eski programcı dostuyla denersiniz: editör autocomplete.

Fonksiyonun ilk parametresi olan `first_name`'i yazarsınız, sonra bir nokta (`.`) ve ardından autocomplete'i tetiklemek için `Ctrl+Space`'e basarsınız.

Ama ne yazık ki, işe yarar bir şey göremezsiniz:

<img src="/img/python-types/image01.png">

### Tipleri ekleyelim { #add-types }

Önceki sürümden tek bir satırı değiştirelim.

Fonksiyonun parametreleri olan şu parçayı:

```Python
    first_name, last_name
```

şuna çevireceğiz:

```Python
    first_name: str, last_name: str
```

Bu kadar.

Bunlar "type hints":

{* ../../docs_src/python_types/tutorial002_py310.py hl[1] *}

Bu, aşağıdaki gibi default değerler bildirmekle aynı şey değildir:

```Python
    first_name="john", last_name="doe"
```

Bu farklı bir şey.

Eşittir (`=`) değil, iki nokta (`:`) kullanıyoruz.

Ve type hints eklemek, normalde onlarsız ne oluyorsa onu değiştirmez.

Ama şimdi, type hints ile o fonksiyonu oluşturmanın ortasında olduğunuzu tekrar hayal edin.

Aynı noktada, `Ctrl+Space` ile autocomplete'i tetiklemeye çalışırsınız ve şunu görürsünüz:

<img src="/img/python-types/image02.png">

Bununla birlikte, seçenekleri görerek kaydırabilirsiniz; ta ki "tanıdık gelen" seçeneği bulana kadar:

<img src="/img/python-types/image03.png">

## Daha fazla motivasyon { #more-motivation }

Şu fonksiyona bakın, zaten type hints içeriyor:

{* ../../docs_src/python_types/tutorial003_py310.py hl[1] *}

Editör değişkenlerin tiplerini bildiği için, sadece completion değil, aynı zamanda hata kontrolleri de alırsınız:

<img src="/img/python-types/image04.png">

Artık bunu düzeltmeniz gerektiğini, `age`'i `str(age)` ile string'e çevirmeniz gerektiğini biliyorsunuz:

{* ../../docs_src/python_types/tutorial004_py310.py hl[2] *}

## Tipleri Bildirmek { #declaring-types }

Type hints bildirmek için ana yeri az önce gördünüz: fonksiyon parametreleri.

Bu, **FastAPI** ile kullanırken de onları en çok kullanacağınız yerdir.

### Basit tipler { #simple-types }

Sadece `str` değil, tüm standart Python tiplerini bildirebilirsiniz.

Örneğin şunları kullanabilirsiniz:

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005_py310.py hl[1] *}

### `typing` modülü { #typing-module }

Bazı ek kullanım durumları için standart kütüphanedeki `typing` modülünden bazı şeyleri import etmeniz gerekebilir. Örneğin bir şeyin "herhangi bir tip" olabileceğini bildirmek istediğinizde, `typing` içindeki `Any`'yi kullanabilirsiniz:

```python
from typing import Any


def some_function(data: Any):
    print(data)
```

### Generic tipler { #generic-types }

Bazı tipler, köşeli parantez içinde "type parameters" alarak iç tiplerini tanımlayabilir; örneğin "string listesi" `list[str]` olarak bildirilir.

Bu şekilde type parameter alabilen tiplere **Generic types** veya **Generics** denir.

Aynı builtin tipleri generics olarak kullanabilirsiniz (köşeli parantez ve içinde tiplerle):

* `list`
* `tuple`
* `set`
* `dict`

#### List { #list }

Örneğin, `str`'lerden oluşan bir `list` olan bir değişken tanımlayalım.

Değişkeni, aynı iki nokta (`:`) sözdizimiyle bildirin.

Tip olarak `list` yazın.

`list`, bazı iç tipleri barındıran bir tip olduğundan, bunları köşeli parantez içine yazarsınız:

{* ../../docs_src/python_types/tutorial006_py310.py hl[1] *}

/// info | Bilgi

Köşeli parantez içindeki bu iç tiplere "type parameters" denir.

Bu durumda `str`, `list`'e verilen type parameter'dır.

///

Bu şu demektir: "`items` değişkeni bir `list` ve bu listedeki her bir öğe `str`".

Bunu yaparak, editörünüz listeden öğeleri işlerken bile destek sağlayabilir:

<img src="/img/python-types/image05.png">

Tipler olmadan, bunu başarmak neredeyse imkansızdır.

`item` değişkeninin, `items` listesindeki elemanlardan biri olduğuna dikkat edin.

Ve yine de editör bunun bir `str` olduğunu bilir ve buna göre destek sağlar.

#### Tuple ve Set { #tuple-and-set }

`tuple`'ları ve `set`'leri bildirmek için de aynısını yaparsınız:

{* ../../docs_src/python_types/tutorial007_py310.py hl[1] *}

Bu şu anlama gelir:

* `items_t` değişkeni 3 öğeli bir `tuple`'dır: bir `int`, bir başka `int` ve bir `str`.
* `items_s` değişkeni bir `set`'tir ve her bir öğesi `bytes` tipindedir.

#### Dict { #dict }

Bir `dict` tanımlamak için, virgülle ayrılmış 2 type parameter verirsiniz.

İlk type parameter, `dict`'in key'leri içindir.

İkinci type parameter, `dict`'in value'ları içindir:

{* ../../docs_src/python_types/tutorial008_py310.py hl[1] *}

Bu şu anlama gelir:

* `prices` değişkeni bir `dict`'tir:
    * Bu `dict`'in key'leri `str` tipindedir (örneğin her bir öğenin adı).
    * Bu `dict`'in value'ları `float` tipindedir (örneğin her bir öğenin fiyatı).

#### Union { #union }

Bir değişkenin **birkaç tipten herhangi biri** olabileceğini bildirebilirsiniz; örneğin bir `int` veya bir `str`.

Bunu tanımlamak için, her iki tipi ayırmak üzere <dfn title='başka adıyla "bit düzeyinde veya operatörü", ancak burada o anlamı önemli değil'>dikey çizgi (`|`)</dfn> kullanırsınız.

Buna "union" denir, çünkü değişken bu iki tip kümesinin birleşimindeki herhangi bir şey olabilir.

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

Bu, `item`'ın `int` veya `str` olabileceği anlamına gelir.

#### Muhtemelen `None` { #possibly-none }

Bir değerin `str` gibi bir tipi olabileceğini ama aynı zamanda `None` da olabileceğini bildirebilirsiniz.

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

Sadece `str` yerine `str | None` kullanmak, aslında değer `None` olabilecekken her zaman `str` olduğunu varsaydığınız hataları editörün yakalamanıza yardımcı olur.

### Tip olarak sınıflar { #classes-as-types }

Bir sınıfı da bir değişkenin tipi olarak bildirebilirsiniz.

Örneğin, adı olan bir `Person` sınıfınız olsun:

{* ../../docs_src/python_types/tutorial010_py310.py hl[1:3] *}

Sonra bir değişkeni `Person` tipinde olacak şekilde bildirebilirsiniz:

{* ../../docs_src/python_types/tutorial010_py310.py hl[6] *}

Ve sonra, yine tüm editör desteğini alırsınız:

<img src="/img/python-types/image06.png">

Bunun "`one_person`, `Person` sınıfının bir **instance**'ıdır" anlamına geldiğine dikkat edin.

"`one_person`, `Person` adlı **class**'tır" anlamına gelmez.

## Pydantic modelleri { #pydantic-models }

[Pydantic](https://docs.pydantic.dev/), data validation yapmak için bir Python kütüphanesidir.

Verinin "shape"'ini attribute'lara sahip sınıflar olarak tanımlarsınız.

Ve her attribute'un bir tipi vardır.

Ardından o sınıfın bir instance'ını bazı değerlerle oluşturursunuz; bu değerleri doğrular, uygun tipe dönüştürür (gerekliyse) ve size tüm veriyi içeren bir nesne verir.

Ve bu ortaya çıkan nesne ile tüm editör desteğini alırsınız.

Resmî Pydantic dokümanlarından bir örnek:

{* ../../docs_src/python_types/tutorial011_py310.py *}

/// info | Bilgi

Daha fazlasını öğrenmek için [Pydantic'in dokümanlarına bakın](https://docs.pydantic.dev/).

///

**FastAPI** tamamen Pydantic üzerine kuruludur.

Bunların pratikte nasıl çalıştığını [Eğitim - Kullanım Kılavuzu](tutorial/index.md) içinde çok daha fazla göreceksiniz.

## Metadata Annotations ile Type Hints { #type-hints-with-metadata-annotations }

Python'da ayrıca, `Annotated` kullanarak bu type hints içine **ek <dfn title="Veri hakkında veri; bu durumda tip hakkında bilgi, örneğin bir açıklama.">üstveri</dfn>** koymayı sağlayan bir özellik de vardır.

`Annotated`'ı `typing` içinden import edebilirsiniz.

{* ../../docs_src/python_types/tutorial013_py310.py hl[1,4] *}

Python'un kendisi bu `Annotated` ile bir şey yapmaz. Editörler ve diğer araçlar için tip hâlâ `str`'dir.

Ama **FastAPI**'ye uygulamanızın nasıl davranmasını istediğinize dair ek metadata sağlamak için `Annotated` içindeki bu alanı kullanabilirsiniz.

Hatırlanması gereken önemli nokta: `Annotated`'a verdiğiniz **ilk *type parameter***, **gerçek tip**tir. Geri kalanı ise diğer araçlar için metadatadır.

Şimdilik, sadece `Annotated`'ın var olduğunu ve bunun standart Python olduğunu bilmeniz yeterli. 😎

İleride bunun ne kadar **güçlü** olabildiğini göreceksiniz.

/// tip | İpucu

Bunun **standart Python** olması, editörünüzde mümkün olan **en iyi developer experience**'ı almaya devam edeceğiniz anlamına gelir; kodu analiz etmek ve refactor etmek için kullandığınız araçlarla da, vb. ✨

Ayrıca kodunuzun pek çok başka Python aracı ve kütüphanesiyle çok uyumlu olacağı anlamına gelir. 🚀

///

## **FastAPI**'de type hints { #type-hints-in-fastapi }

**FastAPI**, birkaç şey yapmak için bu type hints'ten faydalanır.

**FastAPI** ile type hints kullanarak parametreleri bildirirsiniz ve şunları elde edersiniz:

* **Editör desteği**.
* **Tip kontrolleri**.

...ve **FastAPI** aynı bildirimleri şunlar için de kullanır:

* **Gereksinimleri tanımlamak**: request path parameters, query parameters, headers, bodies, bağımlılıklar (dependencies), vb.
* **Veriyi dönüştürmek**: request'ten gerekli tipe.
* **Veriyi doğrulamak**: her request'ten gelen veriyi:
    * Veri geçersiz olduğunda client'a dönen **otomatik hatalar** üretmek.
* OpenAPI kullanarak API'yi **dokümante etmek**:
    * bu, daha sonra otomatik etkileşimli dokümantasyon kullanıcı arayüzleri tarafından kullanılır.

Bunların hepsi kulağa soyut gelebilir. Merak etmeyin. Tüm bunları [Eğitim - Kullanım Kılavuzu](tutorial/index.md) içinde çalışırken göreceksiniz.

Önemli olan, standart Python tiplerini tek bir yerde kullanarak (daha fazla sınıf, decorator vb. eklemek yerine), **FastAPI**'nin sizin için işin büyük kısmını yapmasıdır.

/// info | Bilgi

Tüm tutorial'ı zaten bitirdiyseniz ve tipler hakkında daha fazlasını görmek için geri döndüyseniz, iyi bir kaynak: [`mypy`'nin "cheat sheet"i](https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html).

///
