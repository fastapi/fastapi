# Python Tiplerine Giriş { #python-types-intro }

Python, isteğe bağlı "type hints" (diğer adıyla "type annotations") desteğine sahiptir.

Bu **"type hints"** veya annotations, bir değişkenin <abbr title="örneğin: str, int, float, bool">type</abbr>'ını bildirmeye yarayan özel bir sözdizimidir.

Değişkenleriniz için type bildirerek, editörler ve araçlar size daha iyi destek sağlayabilir.

Bu, Python type hints hakkında sadece **hızlı bir eğitim / bilgi tazeleme** dokümanıdır. **FastAPI** ile kullanmak için gereken minimum bilgiyi kapsar... ki aslında bu çok azdır.

**FastAPI** tamamen bu type hints üzerine kuruludur; bunlar ona birçok avantaj ve fayda sağlar.

Ancak hiç **FastAPI** kullanmasanız bile, bunlar hakkında biraz öğrenmeniz size fayda sağlayacaktır.

/// note | Not

Eğer bir Python uzmanıysanız ve type hints hakkında her şeyi zaten biliyorsanız, sonraki bölüme geçin.

///

## Motivasyon { #motivation }

Basit bir örnekle başlayalım:

{* ../../docs_src/python_types/tutorial001_py39.py *}

Bu programı çalıştırınca şu çıktıyı alırsınız:

```
John Doe
```

Fonksiyon şunları yapar:

* `first_name` ve `last_name` değerlerini alır.
* `title()` ile her birinin ilk harfini büyük harfe çevirir.
* Ortada bir boşluk olacak şekilde <abbr title="Hepsini, tek bir bütün olacak şekilde bir araya koyar. İçerikler ardışık şekilde yer alır.">Concatenates</abbr> eder.

{* ../../docs_src/python_types/tutorial001_py39.py hl[2] *}

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

{* ../../docs_src/python_types/tutorial002_py39.py hl[1] *}

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

{* ../../docs_src/python_types/tutorial003_py39.py hl[1] *}

Editör değişkenlerin tiplerini bildiği için, sadece completion değil, aynı zamanda hata kontrolleri de alırsınız:

<img src="/img/python-types/image04.png">

Artık bunu düzeltmeniz gerektiğini, `age`'i `str(age)` ile string'e çevirmeniz gerektiğini biliyorsunuz:

{* ../../docs_src/python_types/tutorial004_py39.py hl[2] *}

## Tipleri bildirmek { #declaring-types }

Type hints bildirmek için ana yeri az önce gördünüz: fonksiyon parametreleri.

Bu, **FastAPI** ile kullanırken de onları en çok kullanacağınız yerdir.

### Basit tipler { #simple-types }

Sadece `str` değil, tüm standart Python tiplerini bildirebilirsiniz.

Örneğin şunları kullanabilirsiniz:

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005_py39.py hl[1] *}

### Tip parametreleri ile Generic tipler { #generic-types-with-type-parameters }

`dict`, `list`, `set` ve `tuple` gibi, başka değerler içerebilen bazı veri yapıları vardır. Ve iç değerlerin kendi tipi de olabilir.

İç tipleri olan bu tiplere "**generic**" tipler denir. Ve bunları, iç tipleriyle birlikte bildirmek mümkündür.

Bu tipleri ve iç tipleri bildirmek için standart Python modülü `typing`'i kullanabilirsiniz. Bu modül, özellikle bu type hints desteği için vardır.

#### Python'un daha yeni sürümleri { #newer-versions-of-python }

`typing` kullanan sözdizimi, Python 3.6'dan en yeni sürümlere kadar (Python 3.9, Python 3.10, vb. dahil) tüm sürümlerle **uyumludur**.

Python geliştikçe, **daha yeni sürümler** bu type annotations için daha iyi destekle gelir ve çoğu durumda type annotations bildirmek için `typing` modülünü import edip kullanmanız bile gerekmez.

Projeniz için daha yeni bir Python sürümü seçebiliyorsanız, bu ek sadelikten yararlanabilirsiniz.

Tüm dokümanlarda her Python sürümüyle uyumlu örnekler vardır (fark olduğunda).

Örneğin "**Python 3.6+**", Python 3.6 veya üstüyle (3.7, 3.8, 3.9, 3.10, vb. dahil) uyumludur. "**Python 3.9+**" ise Python 3.9 veya üstüyle (3.10 vb. dahil) uyumludur.

Eğer **Python'un en güncel sürümlerini** kullanabiliyorsanız, en güncel sürüme ait örnekleri kullanın; bunlar **en iyi ve en basit sözdizimine** sahip olur, örneğin "**Python 3.10+**".

#### List { #list }

Örneğin, `str`'lerden oluşan bir `list` olan bir değişken tanımlayalım.

Değişkeni, aynı iki nokta (`:`) sözdizimiyle bildirin.

Type olarak `list` yazın.

`list`, bazı iç tipleri barındıran bir tip olduğundan, bunları köşeli parantez içine yazarsınız:

{* ../../docs_src/python_types/tutorial006_py39.py hl[1] *}

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

{* ../../docs_src/python_types/tutorial007_py39.py hl[1] *}

Bu şu anlama gelir:

* `items_t` değişkeni 3 öğeli bir `tuple`'dır: bir `int`, bir başka `int` ve bir `str`.
* `items_s` değişkeni bir `set`'tir ve her bir öğesi `bytes` tipindedir.

#### Dict { #dict }

Bir `dict` tanımlamak için, virgülle ayrılmış 2 type parameter verirsiniz.

İlk type parameter, `dict`'in key'leri içindir.

İkinci type parameter, `dict`'in value'ları içindir:

{* ../../docs_src/python_types/tutorial008_py39.py hl[1] *}

Bu şu anlama gelir:

* `prices` değişkeni bir `dict`'tir:
    * Bu `dict`'in key'leri `str` tipindedir (örneğin her bir öğenin adı).
    * Bu `dict`'in value'ları `float` tipindedir (örneğin her bir öğenin fiyatı).

#### Union { #union }

Bir değişkenin **birkaç tipten herhangi biri** olabileceğini bildirebilirsiniz; örneğin bir `int` veya bir `str`.

Python 3.6 ve üzeri sürümlerde (Python 3.10 dahil), `typing` içinden `Union` tipini kullanabilir ve köşeli parantez içine kabul edilecek olası tipleri yazabilirsiniz.

Python 3.10'da ayrıca, olası tipleri <abbr title='also called "bitwise or operator", but that meaning is not relevant here'>vertical bar (`|`)</abbr> ile ayırabildiğiniz **yeni bir sözdizimi** de vardır.

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial008b_py39.py!}
```

////

Her iki durumda da bu, `item`'ın `int` veya `str` olabileceği anlamına gelir.

#### Muhtemelen `None` { #possibly-none }

Bir değerin `str` gibi bir tipi olabileceğini ama aynı zamanda `None` da olabileceğini bildirebilirsiniz.

Python 3.6 ve üzeri sürümlerde (Python 3.10 dahil), `typing` modülünden `Optional` import edip kullanarak bunu bildirebilirsiniz.

```Python hl_lines="1  4"
{!../../docs_src/python_types/tutorial009_py39.py!}
```

Sadece `str` yerine `Optional[str]` kullanmak, aslında değer `None` olabilecekken her zaman `str` olduğunu varsaydığınız hataları editörün yakalamanıza yardımcı olmasını sağlar.

`Optional[Something]`, aslında `Union[Something, None]` için bir kısayoldur; eşdeğerdirler.

Bu aynı zamanda Python 3.10'da `Something | None` kullanabileceğiniz anlamına gelir:

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial009_py39.py!}
```

////

//// tab | Python 3.9+ alternatif

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial009b_py39.py!}
```

////

#### `Union` veya `Optional` kullanmak { #using-union-or-optional }

Python sürümünüz 3.10'un altındaysa, benim oldukça **öznel** bakış açıma göre küçük bir ipucu:

* 🚨 `Optional[SomeType]` kullanmaktan kaçının
* Bunun yerine ✨ **`Union[SomeType, None]` kullanın** ✨.

İkisi eşdeğerdir ve altta aynı şeydir; ama ben `Optional` yerine `Union` önermeyi tercih ederim. Çünkü "**optional**" kelimesi değerin optional olduğunu ima ediyor gibi durur; ama gerçekte anlamı "değer `None` olabilir"dir. Değer optional olmasa ve hâlâ required olsa bile.

Bence `Union[SomeType, None]` ne anlama geldiğini daha açık şekilde ifade ediyor.

Bu, tamamen kelimeler ve isimlendirmelerle ilgili. Ancak bu kelimeler, sizin ve ekip arkadaşlarınızın kod hakkında nasıl düşündüğünü etkileyebilir.

Örnek olarak şu fonksiyonu ele alalım:

{* ../../docs_src/python_types/tutorial009c_py39.py hl[1,4] *}

`name` parametresi `Optional[str]` olarak tanımlanmış, ama **optional değil**; parametre olmadan fonksiyonu çağıramazsınız:

```Python
say_hi()  # Oh, no, this throws an error! 😱
```

`name` parametresi **hâlâ required**'dır (*optional* değildir) çünkü bir default değeri yoktur. Yine de `name`, değer olarak `None` kabul eder:

```Python
say_hi(name=None)  # This works, None is valid 🎉
```

İyi haber şu ki, Python 3.10'a geçtiğinizde bununla uğraşmanız gerekmeyecek; çünkü tiplerin union'larını tanımlamak için doğrudan `|` kullanabileceksiniz:

{* ../../docs_src/python_types/tutorial009c_py310.py hl[1,4] *}

Ve böylece `Optional` ve `Union` gibi isimlerle de uğraşmanız gerekmeyecek. 😎

#### Generic tipler { #generic-types }

Köşeli parantez içinde type parameter alan bu tiplere **Generic types** veya **Generics** denir, örneğin:

//// tab | Python 3.10+

Aynı builtin tipleri generics olarak kullanabilirsiniz (köşeli parantez ve içindeki tiplerle):

* `list`
* `tuple`
* `set`
* `dict`

Ve önceki Python sürümlerinde olduğu gibi `typing` modülünden:

* `Union`
* `Optional`
* ...and others.

Python 3.10'da, `Union` ve `Optional` generics'lerini kullanmaya alternatif olarak, tip union'larını bildirmek için <abbr title='also called "bitwise or operator", but that meaning is not relevant here'>vertical bar (`|`)</abbr> kullanabilirsiniz; bu çok daha iyi ve daha basittir.

////

//// tab | Python 3.9+

Aynı builtin tipleri generics olarak kullanabilirsiniz (köşeli parantez ve içindeki tiplerle):

* `list`
* `tuple`
* `set`
* `dict`

Ve `typing` modülünden gelen generics:

* `Union`
* `Optional`
* ...and others.

////

### Tip olarak sınıflar { #classes-as-types }

Bir sınıfı da bir değişkenin tipi olarak bildirebilirsiniz.

Örneğin, adı olan bir `Person` sınıfınız olsun:

{* ../../docs_src/python_types/tutorial010_py39.py hl[1:3] *}

Sonra bir değişkeni `Person` tipinde olacak şekilde bildirebilirsiniz:

{* ../../docs_src/python_types/tutorial010_py39.py hl[6] *}

Ve sonra, yine tüm editör desteğini alırsınız:

<img src="/img/python-types/image06.png">

Bunun "`one_person`, `Person` sınıfının bir **instance**'ıdır" anlamına geldiğine dikkat edin.

"`one_person`, `Person` adlı **class**'tır" anlamına gelmez.

## Pydantic modelleri { #pydantic-models }

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>, data validation yapmak için bir Python kütüphanesidir.

Verinin "shape"'ini attribute'lara sahip sınıflar olarak tanımlarsınız.

Ve her attribute'un bir tipi vardır.

Ardından o sınıfın bir instance'ını bazı değerlerle oluşturursunuz; bu değerleri doğrular, uygun tipe dönüştürür (gerekliyse) ve size tüm veriyi içeren bir nesne verir.

Ve bu ortaya çıkan nesne ile tüm editör desteğini alırsınız.

Resmî Pydantic dokümanlarından bir örnek:

{* ../../docs_src/python_types/tutorial011_py310.py *}

/// info | Bilgi

Daha fazlasını öğrenmek için <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic'in dokümanlarına bakın</a>.

///

**FastAPI** tamamen Pydantic üzerine kuruludur.

Bunların pratikte nasıl çalıştığını [Tutorial - User Guide](tutorial/index.md){.internal-link target=_blank} içinde çok daha fazla göreceksiniz.

/// tip | İpucu

Pydantic, default value olmadan `Optional` veya `Union[Something, None]` kullandığınızda özel bir davranışa sahiptir; bununla ilgili daha fazla bilgiyi Pydantic dokümanlarında <a href="https://docs.pydantic.dev/2.3/usage/models/#required-fields" class="external-link" target="_blank">Required Optional fields</a> bölümünde okuyabilirsiniz.

///

## Metadata Annotations ile Type Hints { #type-hints-with-metadata-annotations }

Python'da ayrıca, `Annotated` kullanarak bu type hints içine **ek <abbr title="Veri hakkında veri; bu durumda type hakkında bilgi, örneğin bir açıklama.">metadata</abbr>** koymayı sağlayan bir özellik de vardır.

Python 3.9'dan itibaren `Annotated`, standart kütüphanenin bir parçasıdır; bu yüzden `typing` içinden import edebilirsiniz.

{* ../../docs_src/python_types/tutorial013_py39.py hl[1,4] *}

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

* **Gereksinimleri tanımlamak**: request path parameters, query parameters, headers, bodies, dependencies, vb.
* **Veriyi dönüştürmek**: request'ten gerekli tipe.
* **Veriyi doğrulamak**: her request'ten gelen veriyi:
    * Veri geçersiz olduğunda client'a dönen **otomatik hatalar** üretmek.
* OpenAPI kullanarak API'yi **dokümante etmek**:
    * bu, daha sonra otomatik etkileşimli dokümantasyon kullanıcı arayüzleri tarafından kullanılır.

Bunların hepsi kulağa soyut gelebilir. Merak etmeyin. Tüm bunları [Tutorial - User Guide](tutorial/index.md){.internal-link target=_blank} içinde çalışırken göreceksiniz.

Önemli olan, standart Python tiplerini tek bir yerde kullanarak (daha fazla sınıf, decorator vb. eklemek yerine), **FastAPI**'nin sizin için işin büyük kısmını yapmasıdır.

/// info | Bilgi

Tüm tutorial'ı zaten bitirdiyseniz ve tipler hakkında daha fazlasını görmek için geri döndüyseniz, iyi bir kaynak: <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">`mypy`'nin "cheat sheet"i</a>.

///
