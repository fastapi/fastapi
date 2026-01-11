# Python Tiplerine Giriş { #python-types-intro }

Python, isteğe bağlı "type hints" (diğer adıyla "type annotations") desteğine sahiptir.

Bu **"type hints"** veya annotations, bir değişkenin <abbr title="for example: str, int, float, bool">type</abbr>'ını bildirmeye olanak sağlayan özel bir sözdizimidir.

Değişkenleriniz için type bildirerek, editörler ve araçlar size daha iyi destek sağlayabilir.

Bu, Python type hints hakkında sadece **hızlı bir eğitim / bilgi tazeleme** yazısıdır. **FastAPI** ile kullanmak için gerekli olan minimum kısmı kapsar... ki bu aslında çok azdır.

**FastAPI** tamamen bu type hints'lere dayanır; bunlar ona pek çok avantaj ve fayda sağlar.

Ama **FastAPI**'yi hiç kullanmasanız bile, bunlar hakkında biraz öğrenmek size fayda sağlar.

/// note | Not

Python uzmanıysanız ve type hints ile ilgili her şeyi zaten biliyorsanız, sonraki bölüme geçin.

///

## Motivasyon { #motivation }

Basit bir örnekle başlayalım:

{* ../../docs_src/python_types/tutorial001_py39.py *}

Bu programı çağırmak şunu çıktılar:

```
John Doe
```

Fonksiyon şunları yapar:

* Bir `first_name` ve `last_name` alır.
* Her birinin ilk harfini `title()` ile büyük harfe çevirir.
* Ortada bir boşluk olacak şekilde <abbr title="Puts them together, as one. With the contents of one after the other.">Concatenates</abbr> eder.

{* ../../docs_src/python_types/tutorial001_py39.py hl[2] *}

### Düzenleyelim { #edit-it }

Bu çok basit bir program.

Ama şimdi bunu sıfırdan yazdığınızı hayal edin.

Bir noktada fonksiyonun tanımına başlamış olurdunuz, parametreleriniz hazırdı...

Ama sonra "ilk harfi büyük harfe çeviren o method"u çağırmanız gerekir.

`upper` mıydı? `uppercase` miydi? `first_uppercase`? `capitalize`?

Sonra, programcının eski dostu editör otomatik tamamlama ile denersiniz.

Fonksiyonun ilk parametresi olan `first_name`'i yazarsınız, sonra bir nokta (`.`) koyarsınız ve ardından tamamlamayı tetiklemek için `Ctrl+Space`'e basarsınız.

Ama maalesef, işe yarar hiçbir şey gelmez:

<img src="/img/python-types/image01.png">

### Tipleri ekleyin { #add-types }

Önceki sürümden tek bir satırı değiştirelim.

Fonksiyonun parametreleri olan tam şu parçayı:

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

Bu, şu şekilde varsayılan değerler bildirmekle aynı şey değildir:

```Python
    first_name="john", last_name="doe"
```

Bu farklı bir şey.

Eşittir (`=`) değil, iki nokta üst üste (`:`) kullanıyoruz.

Ve type hints eklemek normalde, onlarsız ne olacaktıysa olan şeyi değiştirmez.

Ama şimdi, type hints varken o fonksiyonu oluşturmanın ortasında olduğunuzu hayal edin.

Aynı noktada `Ctrl+Space` ile otomatik tamamlamayı tetiklemeyi denersiniz ve şunu görürsünüz:

<img src="/img/python-types/image02.png">

Bununla, seçenekleri görerek aşağı kaydırabilir, "tanıdık gelen" seçeneği bulana kadar ilerleyebilirsiniz:

<img src="/img/python-types/image03.png">

## Daha fazla motivasyon { #more-motivation }

Bu fonksiyona bakın, zaten type hints'e sahip:

{* ../../docs_src/python_types/tutorial003_py39.py hl[1] *}

Editör değişkenlerin tiplerini bildiği için, sadece tamamlama değil, hata kontrolleri de alırsınız:

<img src="/img/python-types/image04.png">

Artık bunu düzeltmeniz gerektiğini biliyorsunuz; `age`'i `str(age)` ile string'e çevirin:

{* ../../docs_src/python_types/tutorial004_py39.py hl[2] *}

## Tipleri bildirmek { #declaring-types }

Type hints bildirmek için ana yeri, fonksiyon parametreleri olarak, az önce gördünüz.

Bu, **FastAPI** ile de onları kullanacağınız ana yerdir.

### Basit tipler { #simple-types }

Sadece `str` değil, tüm standart Python tiplerini bildirebilirsiniz.

Örneğin şunları kullanabilirsiniz:

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005_py39.py hl[1] *}

### Tip parametreleri ile Generic tipler { #generic-types-with-type-parameters }

`dict`, `list`, `set` ve `tuple` gibi, başka değerleri içerebilen bazı veri yapıları vardır. Ve iç değerlerin de kendi tipi olabilir.

İç tipleri olan bu tiplere "**generic**" tipler denir. Ve bunları, iç tipleriyle beraber bile bildirmek mümkündür.

Bu tipleri ve iç tipleri bildirmek için standart Python modülü `typing`'i kullanabilirsiniz. Bu modül özellikle bu type hints'leri desteklemek için vardır.

#### Python'un daha yeni sürümleri { #newer-versions-of-python }

`typing` kullanarak yapılan sözdizimi, Python 3.6'dan en yeni sürümlere kadar (Python 3.9, Python 3.10, vb. dahil) tüm sürümlerle **uyumludur**.

Python geliştikçe, **daha yeni sürümler** bu type annotations için daha iyi destekle gelir ve çoğu durumda type annotations bildirmek için `typing` modülünü import edip kullanmanıza bile gerek kalmaz.

Projeniz için Python'un daha yeni bir sürümünü seçebiliyorsanız, bu ek sadelikten faydalanabilirsiniz.

Tüm dokümanlarda Python'un her sürümüyle uyumlu örnekler vardır (fark olduğunda).

Örneğin "**Python 3.6+**" Python 3.6 veya üstüyle (3.7, 3.8, 3.9, 3.10, vb. dahil) uyumlu demektir. Ve "**Python 3.9+**" Python 3.9 veya üstüyle (3.10, vb. dahil) uyumlu demektir.

Python'un **en son sürümlerini** kullanabiliyorsanız, en son sürüme ait örnekleri kullanın; bunlar **en iyi ve en basit sözdizimine** sahip olacaktır, örneğin "**Python 3.10+**".

#### List { #list }

Örneğin, `str` değerlerinden oluşan bir `list` olan bir değişken tanımlayalım.

Değişkeni, aynı iki nokta üst üste (`:`) sözdizimi ile bildirin.

Tip olarak `list` yazın.

`list`, bazı iç tipleri barındıran bir tip olduğundan, bunları köşeli parantez içine alırsınız:

{* ../../docs_src/python_types/tutorial006_py39.py hl[1] *}

/// info | Bilgi

Köşeli parantez içindeki bu iç tiplere "type parameters" denir.

Bu durumda, `str`, `list`'e aktarılan type parameter'dır.

///

Bu şu anlama gelir: "`items` değişkeni bir `list`tir ve bu listedeki her bir öğe bir `str`dir".

Bunu yaparak, editörünüz listedeki öğeleri işlerken bile destek sağlayabilir:

<img src="/img/python-types/image05.png">

Tipler olmadan, bunu başarmak neredeyse imkansızdır.

`item` değişkeninin `items` listesindeki öğelerden biri olduğuna dikkat edin.

Ve yine de editör bunun bir `str` olduğunu bilir ve bunun için destek sağlar.

#### Tuple ve Set { #tuple-and-set }

`tuple`'ları ve `set`'leri bildirmek için de aynısını yaparsınız:

{* ../../docs_src/python_types/tutorial007_py39.py hl[1] *}

Bu şu anlama gelir:

* `items_t` değişkeni 3 öğeli bir `tuple`'dır: bir `int`, bir başka `int` ve bir `str`.
* `items_s` değişkeni bir `set`'tir ve her bir öğesi `bytes` tipindedir.

#### Dict { #dict }

Bir `dict` tanımlamak için, virgülle ayrılmış 2 type parameter geçersiniz.

İlk type parameter, `dict`'in key'leri içindir.

İkinci type parameter, `dict`'in value'ları içindir:

{* ../../docs_src/python_types/tutorial008_py39.py hl[1] *}

Bu şu anlama gelir:

* `prices` değişkeni bir `dict`'tir:
    * Bu `dict`'in key'leri `str` tipindedir (diyelim ki her item'ın adı).
    * Bu `dict`'in value'ları `float` tipindedir (diyelim ki her item'ın fiyatı).

#### Union { #union }

Bir değişkenin **birden fazla tipten** herhangi biri olabileceğini bildirebilirsiniz, örneğin bir `int` veya bir `str`.

Python 3.6 ve üstünde (Python 3.10 dahil) `typing`'den `Union` tipini kullanabilir ve köşeli parantez içine kabul edilecek olası tipleri koyabilirsiniz.

Python 3.10'da ayrıca, olası tipleri <abbr title='also called "bitwise or operator", but that meaning is not relevant here'>vertical bar (`|`)</abbr> ile ayırabileceğiniz **yeni bir sözdizimi** de vardır.

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

Her iki durumda da bu, `item`'ın bir `int` veya bir `str` olabileceği anlamına gelir.

#### `None` olma ihtimali { #possibly-none }

Bir değerin `str` gibi bir tipe sahip olabileceğini ama aynı zamanda `None` da olabileceğini bildirebilirsiniz.

Python 3.6 ve üstünde (Python 3.10 dahil) bunu, `typing` modülünden `Optional` import edip kullanarak bildirebilirsiniz.

```Python hl_lines="1  4"
{!../../docs_src/python_types/tutorial009_py39.py!}
```

Sadece `str` yerine `Optional[str]` kullanmak, bir değerin her zaman `str` olduğunu varsayabileceğiniz ama aslında `None` da olabileceği durumlarda editörün hataları tespit etmenize yardımcı olmasını sağlar.

`Optional[Something]` aslında `Union[Something, None]` için bir kısayoldur, eşdeğerdirler.

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

Python sürümünüz 3.10'un altındaysa, benim oldukça **öznel** bakış açıma göre bir ipucu:

* 🚨 `Optional[SomeType]` kullanmaktan kaçının
* Bunun yerine ✨ **`Union[SomeType, None]` kullanın** ✨.

İkisi de eşdeğerdir ve altta aynı şeydir, ama `Optional` yerine `Union` önermemin nedeni şu: "**optional**" kelimesi, değerin isteğe bağlı olduğunu ima ediyor gibi görünebilir; oysa aslında anlamı " `None` olabilir"dir, optional olmasa ve hâlâ gerekli olsa bile.

Bence `Union[SomeType, None]` ne demek istediğini daha açık biçimde ifade eder.

Bu sadece kelimeler ve isimlerle ilgili. Ama bu kelimeler, sizin ve takım arkadaşlarınızın kod hakkında nasıl düşündüğünü etkileyebilir.

Örnek olarak şu fonksiyonu ele alalım:

{* ../../docs_src/python_types/tutorial009c_py39.py hl[1,4] *}

`name` parametresi `Optional[str]` olarak tanımlanmış, ama **optional değil**, parametre olmadan fonksiyonu çağırmazsınız:

```Python
say_hi()  # Oh, no, this throws an error! 😱
```

`name` parametresi hâlâ **gerekli** ( *optional* değil) çünkü varsayılan değeri yok. Yine de `name`, değer olarak `None` kabul eder:

```Python
say_hi(name=None)  # This works, None is valid 🎉
```

İyi haber şu ki, Python 3.10'a geçtiğinizde bununla uğraşmanıza gerek kalmayacak, çünkü tip union'larını tanımlamak için basitçe `|` kullanabileceksiniz:

{* ../../docs_src/python_types/tutorial009c_py310.py hl[1,4] *}

Ve artık `Optional` ve `Union` gibi isimlerle uğraşmanıza gerek kalmayacak. 😎

#### Generic tipler { #generic-types }

Köşeli parantez içinde type parameter alan bu tiplere **Generic types** veya **Generics** denir, örneğin:

//// tab | Python 3.10+

Generic olarak aynı builtin tipleri (köşeli parantez ve içinde tiplerle) kullanabilirsiniz:

* `list`
* `tuple`
* `set`
* `dict`

Ve önceki Python sürümlerinde olduğu gibi, `typing` modülünden:

* `Union`
* `Optional`
* ...and others.

Python 3.10'da, generic olan `Union` ve `Optional` kullanmaya alternatif olarak, <abbr title='also called "bitwise or operator", but that meaning is not relevant here'>vertical bar (`|`)</abbr> ile tip union'ları bildirebilirsiniz; bu çok daha iyi ve daha basittir.

////

//// tab | Python 3.9+

Generic olarak aynı builtin tipleri (köşeli parantez ve içinde tiplerle) kullanabilirsiniz:

* `list`
* `tuple`
* `set`
* `dict`

Ve `typing` modülündeki generics'ler:

* `Union`
* `Optional`
* ...and others.

////

### Tip olarak sınıflar { #classes-as-types }

Bir sınıfı da bir değişkenin tipi olarak bildirebilirsiniz.

Diyelim ki bir adı olan `Person` sınıfınız var:

{* ../../docs_src/python_types/tutorial010_py39.py hl[1:3] *}

Sonra bir değişkeni `Person` tipinde olacak şekilde bildirebilirsiniz:

{* ../../docs_src/python_types/tutorial010_py39.py hl[6] *}

Ve sonra, yine tüm editör desteğini alırsınız:

<img src="/img/python-types/image06.png">

Bunun "`one_person`, `Person` sınıfının bir **instance**'ıdır" anlamına geldiğine dikkat edin.

"`one_person`, `Person` adlı **class**'tır" anlamına gelmez.

## Pydantic modelleri { #pydantic-models }

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>, veri doğrulaması yapmak için bir Python kütüphanesidir.

Verinin "shape"'ini (şeklini) attribute'lara sahip sınıflar olarak bildirirsiniz.

Ve her attribute'un bir tipi vardır.

Sonra bu sınıfın bir instance'ını bazı değerlerle oluşturursunuz; bu değerleri doğrular, (gerekiyorsa) uygun tipe dönüştürür ve size tüm verileri içeren bir nesne verir.

Ve ortaya çıkan o nesne ile tüm editör desteğini alırsınız.

Resmi Pydantic dokümanlarından bir örnek:

{* ../../docs_src/python_types/tutorial011_py310.py *}

/// info | Bilgi

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic hakkında daha fazlasını öğrenmek için dokümanlarına göz atın</a>.

///

**FastAPI** tamamen Pydantic'e dayanır.

Bunların hepsini pratikte çok daha fazla [Tutorial - User Guide](tutorial/index.md){.internal-link target=_blank} içinde göreceksiniz.

/// tip | İpucu

Pydantic, varsayılan değer olmadan `Optional` veya `Union[Something, None]` kullandığınızda özel bir davranışa sahiptir; bununla ilgili daha fazlasını Pydantic dokümanlarında <a href="https://docs.pydantic.dev/2.3/usage/models/#required-fields" class="external-link" target="_blank">Required Optional fields</a> bölümünde okuyabilirsiniz.

///

## Metadata Annotations ile Type Hints { #type-hints-with-metadata-annotations }

Python ayrıca `Annotated` kullanarak bu type hints'lerin içine **ek <abbr title="Data about the data, in this case, information about the type, e.g. a description.">metadata</abbr>** koymaya izin veren bir özelliğe de sahiptir.

Python 3.9'dan beri `Annotated`, standart kütüphanenin bir parçasıdır, dolayısıyla onu `typing`'den import edebilirsiniz.

{* ../../docs_src/python_types/tutorial013_py39.py hl[1,4] *}

Python'un kendisi bu `Annotated` ile bir şey yapmaz. Ve editörler ile diğer araçlar için tip hâlâ `str`'dir.

Ama `Annotated` içindeki bu alanı, uygulamanızın nasıl davranmasını istediğinize dair **FastAPI**'ye ek metadata sağlamak için kullanabilirsiniz.

Hatırlanması gereken önemli şey şu: `Annotated`'a verdiğiniz **ilk *type parameter***, **asıl tip**tir. Geri kalanı ise diğer araçlar için metadata'dır.

Şimdilik sadece `Annotated`'ın var olduğunu ve bunun standart Python olduğunu bilmeniz yeterli. 😎

İleride ne kadar **güçlü** olabileceğini göreceksiniz.

/// tip | İpucu

Bunun **standart Python** olması, editörünüzde hâlâ mümkün olan **en iyi geliştirici deneyimini** alacağınız anlamına gelir; kodunuzu analiz etmek ve refactor etmek için kullandığınız araçlarla vb. ✨

Ayrıca kodunuzun, diğer birçok Python aracı ve kütüphanesiyle çok uyumlu olacağı anlamına da gelir. 🚀

///

## **FastAPI**'de type hints { #type-hints-in-fastapi }

**FastAPI**, birkaç şey yapmak için bu type hints'lerden faydalanır.

**FastAPI** ile type hints kullanarak parametreleri bildirirsiniz ve şunları elde edersiniz:

* **Editör desteği**.
* **Tip kontrolleri**.

...ve **FastAPI** aynı bildirimleri şunlar için de kullanır:

* **Gereksinimleri tanımlamak**: request path parameters, query parameters, headers, bodies, dependencies, vb.'den.
* **Veriyi dönüştürmek**: request'ten gereken tipe.
* **Veriyi doğrulamak**: her request'ten gelen veriyi:
    * Veri geçersiz olduğunda client'a döndürülen **otomatik hatalar** üretmek.
* OpenAPI kullanarak API'yi **belgelemek**:
    * bunun daha sonra otomatik etkileşimli dokümantasyon kullanıcı arayüzleri tarafından kullanılması.

Bunların hepsi soyut gelebilir. Merak etmeyin. Bunların hepsini çalışırken [Tutorial - User Guide](tutorial/index.md){.internal-link target=_blank} içinde göreceksiniz.

Önemli olan, standart Python tiplerini tek bir yerde kullanarak (daha fazla sınıf, decorator vb. eklemek yerine), **FastAPI**'nin sizin için işin büyük kısmını yapacak olmasıdır.

/// info | Bilgi

Tüm tutorial'ı zaten baştan sona geçtiyseniz ve tipler hakkında daha fazlasını görmek için geri döndüyseniz, iyi bir kaynak: <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">`mypy`'nin "cheat sheet"i</a>.

///
