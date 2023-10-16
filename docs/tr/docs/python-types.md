# Python Veri Tiplerine Giriş

Python isteğe bağlı olarak "tip belirteçlerini" ('tür ek açıklamaları' olarak da adlandırılır) destekler.

 **"Tip belirteçleri"** (veya ek açıklamalar) bir değişkenin <abbr title="örneğin: str, int, float, bool">tipinin</abbr> belirtilmesine olanak sağlayan özel bir sözdizimidir.

Değişkenleriniz için tip bildirerek, editörler ve araçlar size daha iyi bir kullanım deneyimi sağlayabilir.

Bu sayfa Python tip belirteçleriyle ilgili **hızlı bir başlangıç rehberi/bilgi tazeleyici** görevindedir. İçeriği ise FastAPI ile kullanılacak minimum gereksinimleri kapsar, ki bu dağın görünen yüzü.

**FastAPI**'nin tamamı bu tip belirteçlere dayanır ve bunlar birçok avantaj ve fayda sağlar.

Ancak hiç **FastAPI** kullanmasanız bile, bu konu hakkında biraz bilgi edinmeniz yararınıza olacaktır.

!!! not
    Eğer bir Python uzmanıysanız ve tip ipuçları hakkında her şeyi zaten biliyorsanız, bir sonraki bölüme geçebilirsiniz.

## Motivasyon

Basit bir örnek ile başlayalım:

```Python
{!../../../docs_src/python_types/tutorial001.py!}
```

Bu program çağrıldığında <abbr title="Output">çıktısı</abbr> aşağıdaki gibi olur:

```
John Doe
```

Fonksiyon sırayla şunları yapar:

* `first_name` ve `last_name` değerlerini alır.
* `title()` ile her birinin ilk harfini büyük harfe dönüştürür.
* Değişkenleri, aralarında bir boşluk bırakarak <abbr title="Onları bir bütün olarak sırayla birleştirir.">birleştirir</abbr>.

```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial001.py!}
```

### Düzenleme

Bu program son derece basitti.

Şimdi, bu programı sıfırdan yazmaya başladığınızı düşünün. İlk adım, fonksiyonun tanımına başlamak ve gerekli parametreleri hazırlamaktır. Ancak metin içerisindeki ilk harfi büyük harfe dönüştüren metodu hatırlamanız gerekecek.

 `upper` mıydı? Yoksa  `uppercase`' mi? `first_uppercase`? Ya da `capitalize`?

Ardından, programcıların en iyi dostu olan otomatik tamamlamayı kullanarak işinizi kolaylaştırdınız.

`first_name`, ardından bir nokta ('.') yazıp otomatik tamamlamayı tetiklemek için 'Ctrl+Space' tuşlarına bastınız.

Ancak, ne yazık ki, yararlı hiçbir şey elde edemediniz:

<img src="/img/python-types/image01.png">

### Tipleri Ekle

Önceki sürümden sadece bir satırı değiştirelim.

Tam olarak bu parçayı, işlevin parametrelerini şu şekilde değiştireceğiz:

```Python
    first_name, last_name
```

ve bu hale getirmiş olacağız:

```Python
    first_name: str, last_name: str
```

İşte bu kadar!

"Tip belirteçlerini" aşağıdaki gibi uygulayabilirsiniz:

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial002.py!}
```

Parametrelere varsayılan değer atamak ile aynı şey değildir:

```Python
    first_name="john", last_name="doe"
```

Dolayısıyla bu iki kullanımın tamamen birbirinden farklı.

Dikkat edin; iki nokta üst üste (`:`) kullanıyoruz , eşittir (`=`) DEĞİL.

Ayrıca tip ipuçları eklemek kodun çıktısını değiştirmez.

Şimdi programı tekrar en baştan yazdığınızı hayal edin.

Aynı noktada, `Ctrl+Space` ile otomatik tamamlamayı tetiklediniz ve şunu görüyorsunuz:

<img src="/img/python-types/image02.png">

Aradığınızı bulana kadar seçenekleri kaydırabilirsiniz:

<img src="/img/python-types/image03.png">

## Daha Fazla Motivasyon

Tür belirteçlerine sahip bir fonksiyonu inceleyelim:

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial003.py!}
```

Editör, değişkenlerin tiplerini bildiğinden dolayı yalnızca otomatik tamamlamayı değil, hata kontrollerini de sağlar:

<img src="/img/python-types/image04.png">

Artık `age` değişkenini `str(age)` olarak kullanmanız gerektiğini biliyorsunuz:

```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial004.py!}
```

## Tip Tanımlama

Az önce tip belirteçlerinin en çok kullanıldığı ana yeri gördünüz.

**FastAPI** ile çalışırken tip belirteçlerini en çok kullanacağımız yer yine fonksiyonlardır.

### Basit Tipler

Elbette sadece `str` değil, tüm standart Python tipleri kullanabilirsiniz.

Örneğin şunları da kullanabilirsiniz:

* `int`
* `float`
* `bool`
* `bytes`

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial005.py!}
```

### Tip Parametreleri ile Generic Tipler

"dict", "list", "set" ve "tuple" gibi başka değerler içerebilen bazı veri yapıları vardır. Ve dahili değerler de kendi türlerine sahip olabilirler.

Dahili tipleri olan bu tiplere "**generic**"(jenerik) tipler denir. Ve bunları iç tipleriyle bile bildirmek mümkündür.

Bu tipleri ve dahili tpileri bildirmek için standart Python küyüphanesi "typing"i kullanabilirsiniz. Bu tür tip belirteçlerini desteklemek için özel olarak mevcuttur.

#### Python'ın Yeni Versiyonları İçin

Yazım kullanan `sözdizimi`, Python 3.6'dan Python 3.9, Python 3.10 vb. dahil olmak üzere en son sürümlere kadar tüm sürümlerle **uyumludur**.

Python geliştikçe, **yeni sürümler** bu `belirteç` (tip eki) açıklamaları için gelişmiş destekle birlikte gelir ve çoğu durumda tür ek açıklamalarını bildirmek için yazım modülünü içe aktarmanıza ve kullanmanıza bile gerek kalmaz.

Projeniz için Python'un daha yeni bir sürümünü seçebilir ve böylece ekstra basitleştirilmiş özelliklerden yararlanabilirsiniz.

Tüm dokümanlarda Python'un her sürümüyle uyumlu örnekler bulabilirsiniz (eğer bir farklılık oluştuysa).

Örneğin "**Python 3.6+**" Python 3.6 veya üzeri (3.7, 3.8, 3.9, 3.10, vb. dahil) ile uyumlu olduğu anlamına gelir. Ve "**Python 3.9+**" Python 3.9 veya üzeri (3.10 vb. dahil) ile uyumlu olduğu anlamına gelir.

**Python'un en son sürümlerini** kullanayorsanız, en son sürüm için oluşturulan örnekleri kullanın. Bunlar **en iyi ve en basit sözdizimine** sahip olacaktır, örneğin, "**Python 3.10+**".

#### `List` (Liste)

Örneğin `str` değerlerden oluşan bir `list` tanımlayalım.

=== "Python 3.9+"

    Declare the variable, with the same colon (`:`) syntax.

    As the type, put `list`.

    As the list is a type that contains some internal types, you put them in square brackets:

    ```Python hl_lines="1"
    {!> ../../../docs_src/python_types/tutorial006_py39.py!}
    ```

=== "Python 3.6+"

    From `typing`, import `List` (büyük harf olan `L` ile):

    ``` Python hl_lines="1"
    {!> ../../../docs_src/python_types/tutorial006.py!}
    ```

    Değişkenin tipini yine iki nokta üstüste (`:`) ile belirleyin ve tip olarak `List` kullanın.

    Liste, bazı dahili tipleri içeren bir tür olduğundan, bunları köşeli parantez içine alırsınız:

    ```Python hl_lines="4"
    {!> ../../../docs_src/python_types/tutorial006.py!}

!!! ipucu
    Köşeli parantez içindeki bu dahili tiplere "tip parametreleri" denir.

    Bu durumda `str`, `List`e iletilen tür parametresidir (veya Python 3.9+ için `list`)

Bunun anlamı şudur: "`items` değişkeni bir `list`tir ve bu listedeki öğelerin her biri bir `str`dir".

!!! tip
    Python 3.9 veya daha üstünü kullanıyorsanız, `List`i `typing`den import etmek zorunda değilsiniz, bunun yerine aynı normal `list` türünü kullanabilirsiniz.

Bunu yaparak, editörünüz listedeki öğeleri işlerken bile destek sağlayabilir:

<img src="/img/python-types/image05.png">

Tipler olmadan bunu başarmak neredeyse imkansızdır.

Değişken öğenin `list` öğelerindeki `items`dan biri olduğuna dikkat edin.

Yine de editör bunun bir `str` olduğunu biliyor ve bunun için destek sağlıyor.

#### `Tuple` ve `Set`

`Tuple` ve `set`lerin tiplerini bildirmek için de aynısını yapıyoruz:

=== "Python 3.9+"

    ```Python hl_lines="1"
    {!> ../../../docs_src/python_types/tutorial007_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial007.py!}
    ```

Bu şu anlama geliyor:

* `items_t` değişkeni sırasıyla `int`, `int`, ve `str` tiplerinden oluşan bir `tuple` türündedir .
* `items_s` ise her öğesi `bytes` türünde olan bir `set` örneğidir.

#### `Dict`

Bir `dict` tanımlamak için virgülle ayrılmış iki parametre verebilirsiniz.

İlk tip parametresi `dict` değerinin `key` değeri içindir.

İkinci parametre ise `dict` değerinin `value` değeri içindir:

=== "Python 3.9+"

    ```Python hl_lines="1"
    {!> ../../../docs_src/python_types/tutorial008_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial008.py!}
    ```

Bu şu anlama gelir:

*  `prices` değişkeni `dict` tipindedir:
    *  `dict` değişkeninin `key` değeri  `str` tipindedir (herbir item'ın "name" değeri).
    *  `dict` değişkeninin `value` değeri `float` tipindedir (lherbir item'ın "price" değeri).

#### Union

Bir değişkenin `int` veya `str` gibi **çeşitli türlerden** herhangi biri olabileceğini bildirebilirsiniz.

Python 3.6 ve üzeri sürümlerde (Python 3.10 dahil) `typing`den `Union` türünü kullanabilir ve kabul edilecek olası türleri köşeli parantezlerin içine koyabilirsiniz.

Python 3.10'da olası türleri dikey bir <abbr title='"bitsel veya operatör" olarak da adlandırılır, ancak bu anlam burada geçerli değildir'>çubukla (`|`)</abbr> (|) ayırabileceğiniz yeni bir **sözdizimi** de var.

=== "Python 3.10+"

    ```Python hl_lines="1"
    {!> ../../../docs_src/python_types/tutorial008b_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial008b.py!}
    ```

Her iki durumda da bu, `item`in bir `int` veya `str` olabileceği anlamına gelir.

#### `None` Kullanımı

Bir değerin `str` gibi bir türe sahip olabileceğini, ancak `None` da olabileceğini bildirebilirsiniz.

Python 3.6 ve üzeri sürümlerde (Python 3.10 dahil) `typing` modülünden `Optional`ı içe aktarıp kullanarak bildirebilirsiniz.

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial009.py!}
```

Sadece `str` yerine `Optional[str]` kullanmak, düzenleyicinin bir değerin aslında `None` da olabileceğini ve gelen değerin `str` olmadığı durumlarda hataları tespit etmenize yardımcı olmasını sağlar.

`Optional[Something]` aslında `Union[Something, None]` için bir kısayoldur, eşdeğerdirler.

Bu aynı zamanda Python 3.10'da `Something | None` kullanabileceğiniz anlamına gelir:

=== "Python 3.10+"

    ```Python hl_lines="1"
    {!> ../../../docs_src/python_types/tutorial009_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial009.py!}
    ```

=== "Python 3.6+ alternative"

    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial009b.py!}
    ```

#### `Union` veya `Optional` Kullanımı

Eğer 3.10'un altında bir Python sürümü kullanıyorsanız, işte size benim çok **öznel** bakış açımdan bir ipucu:

* 🚨 `Optional[SomeType]` kullanmaktan kaçının
* Bunun yerine ✨ **use `Union[SomeType, None]`** ✨kullanın.

Her ikisi de eşdeğerdir ve altta aynıdır, ancak `Optional` yerine `Union`ı öneririm çünkü "**optional**" kelimesi değerin isteğe bağlı olduğunu ima ediyor gibi görünür ve aslında isteğe bağlı olmasa ve hala gerekli olsa bile "`None` olabilir" anlamına gelir.

Bence(Tiangolo için) `Union[SomeType, None]` ne anlama geldiği konusunda daha açık.

Bu sadece kelimeler ve isimlerle ilgili. Ancak bu kelimeler sizin ve ekip arkadaşlarınızın kod hakkındaki düşüncelerini etkileyebilir.

Örnek olarak bu fonksiyonu ele alalım:

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial009c.py!}
```

The parameter `name` is defined as `Optional[str]`, but it is **not optional**, you cannot call the function without the parameter:
Parametre `adı` `Optional[str]` olarak tanımlanmıştır, ancak **isteğe bağlı değildir**, parametre olmadan işlevi çağıramazsınız:

```Python
say_hi()  # Olamaz, bu hata fırlatıyor! 😱
```

Burada `name` parametresi **hala zorunludur** (*isteğe bağlı* değildir) çünkü varsayılan bir değeri yoktur. Yine de, `name` değer olarak `None` kabul eder:

```Python
say_hi(name=None)  # Bu çalışıyor ve None geçerli 🎉
```

İyi haber şu ki, Python 3.10'a geçtiğinizde bu konuda endişelenmenize gerek kalmayacak, çünkü türlerin birliklerini tanımlamak için sadece `|` kullanabileceksiniz:

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial009c_py310.py!}
```

Ve artık `Optional` ve `Union` hakkında endişelenmenize gerek kalmayacak. 😎

#### Generic Tipler

Köşeli parantez içinde tip parametreleri alan bu tiplere **Generic tipler** veya **Generics** adı verilir:

=== "Python 3.10+"

    Aynı yerleşik türleri jenerik olarak kullanabilirsiniz (köşeli parantez ve içindeki türlerle):

    * `list`
    * `tuple`
    * `set`
    * `dict`

    Ve Python 3.6'da olduğu gibi, `typing` modülünden:

    * `Union`
    * `Optional` (Python 3.6'de olduğu gibi aynısı)
    * ...ve diğerleri.

    In Python 3.10, as an alternative to using the generics `Union` and `Optional`, you can use the <abbr title='also called "bitwise or operator", but that meaning is not relevant here'>vertical bar (`|`)</abbr> to declare unions of types, that's a lot better and simpler.
    Python 3.10'da, `Union` ve `Optional` jeneriklerini kullanmaya alternatif olarak, türlerin birliklerini bildirmek için <abbr title='"bitsel veya operatör" olarak da adlandırılır, ancak bu anlam burada geçerli değildir'>dikey çubuğu (`|`)</abbr> kullanabilirsiniz, bu çok daha iyi ve basittir.

=== "Python 3.9+"

    Aynı yerleşik türleri jenerik olarak kullanabilirsiniz (köşeli parantez ve içindeki türlerle):

    * `list`
    * `tuple`
    * `set`
    * `dict`

    Ve Python 3.6'da olduğu gibi, `typing` modülünden:

    * `Union`
    * `Optional`
    * ...ve diğerleri.

=== "Python 3.6+"

    * `List`
    * `Tuple`
    * `Set`
    * `Dict`
    * `Union`
    * `Optional`
    * ...ve diğerleri.

### Tür(Type) Olarak Sınıflar(Classes)

Bir sınıfı bir değişkenin türü olarak da bildirebilirsiniz.

Diyelim ki adı olan bir `Person` sınıfınız var:

```Python hl_lines="1-3"
{!../../../docs_src/python_types/tutorial010.py!}
```

Ardından, `Person` türünde bir değişken bildirebilirsiniz:

```Python hl_lines="6"
{!../../../docs_src/python_types/tutorial010.py!}
```

Ve sonra, yine, tüm editör desteğini alırsınız:

<img src="/img/python-types/image06.png">

Bunun "`one_person`, `Person` sınıfının bir **örneğidir**" anlamına geldiğine dikkat edin.

Bu, "`one_person`, `Person` adlı **sınıftır**" anlamına gelmez.

## Pydantic Modelleri

<a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> veri doğrulaması yapmak için bir Python kütüphanesidir.

Verilerin "biçimini" niteliklere sahip sınıflar olarak düzenlersiniz.

Ve her niteliğin bir türü vardır.

Sınıfın bazı değerlerle bir örneğini oluşturursunuz ve değerleri doğrular, bunları uygun türe dönüştürür ve size tüm verileri içeren bir nesne verir.

Ve ortaya çıkan nesne üzerindeki bütün editör desteğini alırsınız.

Resmi Pydantic dokümanlarından alınmıştır:

=== "Python 3.10+"

    ```Python
    {!> ../../../docs_src/python_types/tutorial011_py310.py!}
    ```

=== "Python 3.9+"

    ```Python
    {!> ../../../docs_src/python_types/tutorial011_py39.py!}
    ```

=== "Python 3.6+"

    ```Python
    {!> ../../../docs_src/python_types/tutorial011.py!}
    ```

!!! info
    Daha fazla şey öğrenmek için <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic'i takip edin</a>.

**FastAPI** tamamen Pydantic'e dayanmaktadır.

Daha fazlasini görmek için [Tutorial - User Guide](tutorial/index.md){.internal-link target=_blank}.

!!! tip
    Pydantic, varsayılan değer olmadan `Optional` veya `Union[Something, None]` kullandığınızda özel bir davranışa sahiptir, `Required`, `Optional` alanları hakkında Pydantic dokümanlarında daha fazla bilgi edinebilirsiniz: <a href="https://pydantic-docs.helpmanual.io/usage/models/#required-optional-fields" class="external-link" target="_blank">Required Optional Fields</a>.

## Meta Veri Ek Açıklamaları ile Tip İpuçları

Python ayrıca `Annotated` kullanarak bu tür ipuçlarına **ek meta veriler** koymaya izin veren bir özelliğe sahiptir.

=== "Python 3.9+"

    Python 3.9'da `Annotated` standart kütüphanenin bir parçasıdır, bu nedenle `typing`den içe aktarabilirsiniz.

    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial013_py39.py!}
    ```

=== "Python 3.6+"

    Python 3.9'un altındaki sürümlerde, `Annotated`ı `typing_extensions`tan içe aktarmalısınız.

    **FastAPI** ile birlikte yüklü gelecektir.

    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial013.py!}
    ```

Python'un kendi başına `Annotated` ile hiçbir şey yapmaz. Ve editörler ve diğer araçlar için tür olarak hala birer `str`dir.

Ancak **FastAPI**'ye uygulamanızın nasıl davranmasını istediğinize ilişkin ek meta veriler sağlamak için `Annotated`daki bu alanı kullanabilirsiniz.

Hatırlanması gereken önemli şey, `Annotated`a ilettiğiniz **ilk tür *parametresinin*** **gerçek tür** olduğudur. Geri kalanı, diğer araçlar için sadece meta verilerdir.

Şimdilik, `Annotated`ın var olduğunu ve standart Python olduğunu bilmeniz yeterlidir. 😎

Daha sonra bunun ne kadar **güçlü** olabileceğini göreceksiniz.

!!! tip
    Bunun **standart Python** olması, editörünüzde, kodunuzu analiz etmek ve yeniden düzenlemek için kullandığınız araçlarla vb. mümkün olan **en iyi geliştirici deneyimini** elde edeceğiniz anlamına gelir. ✨

    Ayrıca kodunuz diğer birçok Python aracı ve kütüphanesi ile uyum içinde çalışacaktır. 🚀


##  **FastAPI** Tip Belirteçleri

**FastAPI** birkaç şey yapmak için bu tür tip belirteçlerinden faydalanır.

**FastAPI** ile parametre tiplerini bildirirsiniz ve şunları elde edersiniz:

* **Editor desteği**.
* **Tip kontrolü**.

...ve **FastAPI** aynı belirteçleri şunlar için de kullanıyor:

* **Gereksinimleri tanımlama**:  request path parameters, query parameters, headers, bodies, dependencies, ve benzeri gereksinimlerden
* **Verileri çevirme**: Gönderilen veri tipinden istenilen veri tipine çevirme.
* **Verileri doğrulama**: Her gönderilen verinin:
    * doğrulanması ve geçersiz olduğunda **otomatik hata** oluşturma.
* OpenAPI kullanarak apinizi **Belgeleyin** :
    * bu daha sonra otomatik etkileşimli dokümantasyon kullanıcı arayüzü tarafından kullanılır.

Bütün bunlar kulağa soyut gelebilir. Merak etme. Tüm bunları çalışırken göreceksiniz. [Tutorial - User Guide](tutorial/index.md){.internal-link target=_blank}.

Önemli olan, standart Python türlerini tek bir yerde kullanarak (daha fazla sınıf, dekoratör vb. eklemek yerine), **FastAPI**'nin bizim için işi yapmasını sağlamak.

!!! info
   Tüm öğreticiyi zaten okuduysanız ve türler hakkında daha fazla bilgi için geri döndüyseniz, iyi bir kaynak:<a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank"> the "cheat sheet" from `mypy`</a>.
