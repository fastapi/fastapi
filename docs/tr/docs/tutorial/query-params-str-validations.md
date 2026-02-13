# Query Parametreleri ve String Doğrulamaları { #query-parameters-and-string-validations }

**FastAPI**, parametreleriniz için ek bilgi ve doğrulamalar (validation) tanımlamanıza izin verir.

Örnek olarak şu uygulamayı ele alalım:

{* ../../docs_src/query_params_str_validations/tutorial001_py310.py hl[7] *}

Query parametresi `q`, `str | None` tipindedir. Yani tipi `str`’dir ama `None` da olabilir. Nitekim varsayılan değer `None` olduğu için FastAPI bunun zorunlu olmadığını anlar.

/// note | Not

FastAPI, `q`’nun zorunlu olmadığını `= None` varsayılan değerinden anlar.

`str | None` kullanmak, editörünüzün daha iyi destek vermesini ve hataları yakalamasını sağlar.

///

## Ek Doğrulama { #additional-validation }

`q` opsiyonel olsa bile, verildiği durumda **uzunluğunun 50 karakteri geçmemesini** zorlayacağız.

### `Query` ve `Annotated` import edin { #import-query-and-annotated }

Bunu yapmak için önce şunları import edin:

* `fastapi` içinden `Query`
* `typing` içinden `Annotated`

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[1,3] *}

/// info | Bilgi

FastAPI, 0.95.0 sürümünde `Annotated` desteğini ekledi (ve önermeye başladı).

Daha eski bir sürüm kullanıyorsanız `Annotated` kullanmaya çalışırken hata alırsınız.

`Annotated` kullanmadan önce FastAPI sürümünü en az 0.95.1’e yükseltmek için [FastAPI sürümünü yükseltin](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank}.

///

## `q` parametresinin tipinde `Annotated` kullanın { #use-annotated-in-the-type-for-the-q-parameter }

[Python Types Intro](../python-types.md#type-hints-with-metadata-annotations){.internal-link target=_blank} içinde `Annotated` ile parametrelerinize metadata ekleyebileceğinizi söylemiştim, hatırlıyor musunuz?

Şimdi bunu FastAPI ile kullanmanın zamanı. 🚀

Şu tip anotasyonuna sahiptik:

```Python
q: str | None = None
```

Şimdi bunu `Annotated` ile saracağız; şöyle olacak:

```Python
q: Annotated[str | None] = None
```

Bu iki sürüm de aynı anlama gelir: `q`, `str` veya `None` olabilen bir parametredir ve varsayılan olarak `None`’dır.

Şimdi işin eğlenceli kısmına geçelim. 🎉

## `q` parametresindeki `Annotated` içine `Query` ekleyin { #add-query-to-annotated-in-the-q-parameter }

Artık ek bilgi (bu durumda ek doğrulama) koyabildiğimiz bir `Annotated`’ımız olduğuna göre, `Annotated` içine `Query` ekleyin ve `max_length` parametresini `50` olarak ayarlayın:

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[9] *}

Varsayılan değerin hâlâ `None` olduğuna dikkat edin; yani parametre hâlâ opsiyonel.

Ama şimdi `Annotated` içinde `Query(max_length=50)` kullanarak FastAPI’ye bu değer için **ek doğrulama** istediğimizi söylüyoruz: en fazla 50 karakter. 😎

/// tip | İpucu

Burada `Query()` kullanıyoruz çünkü bu bir **query parametresi**. İleride `Path()`, `Body()`, `Header()` ve `Cookie()` gibi, `Query()` ile aynı argümanları kabul eden diğerlerini de göreceğiz.

///

FastAPI artık şunları yapacak:

* Verinin uzunluğunun en fazla 50 karakter olduğundan emin olacak şekilde **doğrulayacak**
* Veri geçerli değilse client için **net bir hata** gösterecek
* Parametreyi OpenAPI şemasındaki *path operation* içinde **dokümante edecek** (dolayısıyla **otomatik dokümantasyon arayüzünde** görünecek)

## Alternatif (eski): Varsayılan değer olarak `Query` { #alternative-old-query-as-the-default-value }

FastAPI’nin önceki sürümlerinde ( <dfn title="2023-03’ten önce">0.95.0</dfn> öncesi) `Query`’yi `Annotated` içine koymak yerine, parametrenizin varsayılan değeri olarak kullanmanız gerekiyordu. Etrafta bu şekilde yazılmış kod görme ihtimaliniz yüksek; bu yüzden açıklayalım.

/// tip | İpucu

Yeni kodlarda ve mümkün olduğunda, yukarıda anlatıldığı gibi `Annotated` kullanın. Birden fazla avantajı vardır (aşağıda anlatılıyor) ve dezavantajı yoktur. 🍰

///

Fonksiyon parametresinin varsayılan değeri olarak `Query()` kullanıp `max_length` parametresini 50 yapmak şöyle olurdu:

{* ../../docs_src/query_params_str_validations/tutorial002_py310.py hl[7] *}

Bu senaryoda (`Annotated` kullanmadığımız için) fonksiyondaki `None` varsayılan değerini `Query()` ile değiştirmemiz gerekiyor. Bu durumda varsayılan değeri `Query(default=None)` ile vermeliyiz; bu, (en azından FastAPI açısından) aynı varsayılan değeri tanımlama amacına hizmet eder.

Yani:

```Python
q: str | None = Query(default=None)
```

...parametreyi `None` varsayılan değeriyle opsiyonel yapar; şununla aynı:


```Python
q: str | None = None
```

Ancak `Query` sürümü bunun bir query parametresi olduğunu açıkça belirtir.

Sonrasında `Query`’ye daha fazla parametre geçebiliriz. Bu örnekte string’ler için geçerli olan `max_length`:

```Python
q: str | None = Query(default=None, max_length=50)
```

Bu, veriyi doğrular, veri geçerli değilse net bir hata gösterir ve parametreyi OpenAPI şemasındaki *path operation* içinde dokümante eder.

### Varsayılan değer olarak `Query` veya `Annotated` içinde `Query` { #query-as-the-default-value-or-in-annotated }

`Annotated` içinde `Query` kullanırken `Query` için `default` parametresini kullanamayacağınızı unutmayın.

Bunun yerine fonksiyon parametresinin gerçek varsayılan değerini kullanın. Aksi halde tutarsız olur.

Örneğin şu kullanım izinli değildir:

```Python
q: Annotated[str, Query(default="rick")] = "morty"
```

...çünkü varsayılan değerin `"rick"` mi `"morty"` mi olması gerektiği belli değildir.

Bu nedenle (tercihen) şöyle kullanırsınız:

```Python
q: Annotated[str, Query()] = "rick"
```

...veya eski kod tabanlarında şuna rastlarsınız:

```Python
q: str = Query(default="rick")
```

### `Annotated`’ın avantajları { #advantages-of-annotated }

Fonksiyon parametrelerindeki varsayılan değer stiline göre **`Annotated` kullanmanız önerilir**; birden fazla nedenle **daha iyidir**. 🤓

**Fonksiyon parametresinin** **varsayılan** değeri, **gerçek varsayılan** değerdir; bu genel olarak Python açısından daha sezgiseldir. 😌

Aynı fonksiyonu FastAPI olmadan **başka yerlerde** de **çağırabilirsiniz** ve **beklendiği gibi çalışır**. Eğer **zorunlu** bir parametre varsa (varsayılan değer yoksa) editörünüz hata ile bunu belirtir; ayrıca gerekli parametreyi vermeden çalıştırırsanız **Python** da şikayet eder.

`Annotated` kullanmayıp bunun yerine **(eski) varsayılan değer stilini** kullanırsanız, o fonksiyonu FastAPI olmadan **başka yerlerde** çağırdığınızda doğru çalışması için argümanları geçmeniz gerektiğini **hatırlamak** zorunda kalırsınız; yoksa değerler beklediğinizden farklı olur (ör. `QueryInfo` veya benzeri). Üstelik editörünüz de şikayet etmez ve Python da fonksiyonu çalıştırırken şikayet etmez; ancak içerideki operasyonlar hata verince ortaya çıkar.

`Annotated` birden fazla metadata anotasyonu alabildiği için, artık aynı fonksiyonu <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">Typer</a> gibi başka araçlarla da kullanabilirsiniz. 🚀

## Daha fazla doğrulama ekleyin { #add-more-validations }

`min_length` parametresini de ekleyebilirsiniz:

{* ../../docs_src/query_params_str_validations/tutorial003_an_py310.py hl[10] *}

## Regular expression ekleyin { #add-regular-expressions }

Parametrenin eşleşmesi gereken bir `pattern` <dfn title="String'ler için arama deseni tanımlayan karakter dizisi">düzenli ifade</dfn> tanımlayabilirsiniz:

{* ../../docs_src/query_params_str_validations/tutorial004_an_py310.py hl[11] *}

Bu özel regular expression pattern’i, gelen parametre değerinin şunları sağladığını kontrol eder:

* `^`: Aşağıdaki karakterlerle başlar; öncesinde karakter yoktur.
* `fixedquery`: Tam olarak `fixedquery` değerine sahiptir.
* `$`: Orada biter; `fixedquery` sonrasında başka karakter yoktur.

Bu **"regular expression"** konuları gözünüzü korkutuyorsa sorun değil. Birçok kişi için zor bir konudur. Regular expression’lara ihtiyaç duymadan da pek çok şey yapabilirsiniz.

Artık ihtiyaç duyduğunuzda **FastAPI** içinde kullanabileceğinizi biliyorsunuz.

## Varsayılan değerler { #default-values }

Elbette `None` dışında varsayılan değerler de kullanabilirsiniz.

Örneğin `q` query parametresi için `min_length` değerini `3` yapmak ve varsayılan değer olarak `"fixedquery"` vermek istediğinizi düşünelim:

{* ../../docs_src/query_params_str_validations/tutorial005_an_py310.py hl[9] *}

/// note | Not

`None` dahil herhangi bir tipte varsayılan değere sahip olmak, parametreyi opsiyonel (zorunlu değil) yapar.

///

## Zorunlu parametreler { #required-parameters }

Daha fazla doğrulama veya metadata tanımlamamız gerekmiyorsa, `q` query parametresini yalnızca varsayılan değer tanımlamayarak zorunlu yapabiliriz:

```Python
q: str
```

şunun yerine:

```Python
q: str | None = None
```

Acak biz artık `Query` ile tanımlıyoruz; örneğin şöyle:

```Python
q: Annotated[str | None, Query(min_length=3)] = None
```

Dolayısıyla `Query` kullanırken bir değeri zorunlu yapmak istediğinizde, varsayılan değer tanımlamamanız yeterlidir:

{* ../../docs_src/query_params_str_validations/tutorial006_an_py310.py hl[9] *}

### Zorunlu ama `None` olabilir { #required-can-be-none }

Bir parametrenin `None` kabul edebileceğini söyleyip yine de zorunlu olmasını sağlayabilirsiniz. Bu, client’ların değer göndermesini zorunlu kılar; değer `None` olsa bile.

Bunu yapmak için `None`’ı geçerli bir tip olarak tanımlayın ama varsayılan değer vermeyin:

{* ../../docs_src/query_params_str_validations/tutorial006c_an_py310.py hl[9] *}

## Query parametresi listesi / birden fazla değer { #query-parameter-list-multiple-values }

Bir query parametresini `Query` ile açıkça tanımladığınızda, bir değer listesi alacak şekilde (başka bir deyişle, birden fazla değer alacak şekilde) de tanımlayabilirsiniz.

Örneğin URL’de `q` query parametresinin birden fazla kez görünebilmesini istiyorsanız şöyle yazabilirsiniz:

{* ../../docs_src/query_params_str_validations/tutorial011_an_py310.py hl[9] *}

Sonra şu URL ile:

```
http://localhost:8000/items/?q=foo&q=bar
```

*path operation function* içinde, *function parameter* olan `q` parametresinde, birden fazla `q` *query parameters* değerini (`foo` ve `bar`) bir Python `list`’i olarak alırsınız.

Dolayısıyla bu URL’ye response şöyle olur:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

/// tip | İpucu

Yukarıdaki örnekte olduğu gibi tipi `list` olan bir query parametresi tanımlamak için `Query`’yi açıkça kullanmanız gerekir; aksi halde request body olarak yorumlanır.

///

Etkileşimli API dokümanları da buna göre güncellenir ve birden fazla değere izin verir:

<img src="/img/tutorial/query-params-str-validations/image02.png">

### Varsayılanlarla query parametresi listesi / birden fazla değer { #query-parameter-list-multiple-values-with-defaults }

Hiç değer verilmezse varsayılan bir `list` de tanımlayabilirsiniz:

{* ../../docs_src/query_params_str_validations/tutorial012_an_py310.py hl[9] *}

Şu adrese giderseniz:

```
http://localhost:8000/items/
```

`q`’nun varsayılanı `["foo", "bar"]` olur ve response şöyle olur:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### Sadece `list` kullanmak { #using-just-list }

`list[str]` yerine doğrudan `list` de kullanabilirsiniz:

{* ../../docs_src/query_params_str_validations/tutorial013_an_py310.py hl[9] *}

/// note | Not

Bu durumda FastAPI, listenin içeriğini kontrol etmez.

Örneğin `list[int]`, listenin içeriğinin integer olduğunu kontrol eder (ve dokümante eder). Ancak tek başına `list` bunu yapmaz.

///

## Daha fazla metadata tanımlayın { #declare-more-metadata }

Parametre hakkında daha fazla bilgi ekleyebilirsiniz.

Bu bilgiler oluşturulan OpenAPI’a dahil edilir ve dokümantasyon arayüzleri ile harici araçlar tarafından kullanılır.

/// note | Not

Farklı araçların OpenAPI desteği farklı seviyelerde olabilir.

Bazıları tanımladığınız ek bilgilerin hepsini göstermeyebilir; ancak çoğu durumda eksik özellik geliştirme planındadır.

///

Bir `title` ekleyebilirsiniz:

{* ../../docs_src/query_params_str_validations/tutorial007_an_py310.py hl[10] *}

Ve bir `description`:

{* ../../docs_src/query_params_str_validations/tutorial008_an_py310.py hl[14] *}

## Alias parametreleri { #alias-parameters }

Parametrenin adının `item-query` olmasını istediğinizi düşünün.

Örneğin:

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

Ancak `item-query` geçerli bir Python değişken adı değildir.

En yakın seçenek `item_query` olur.

Ama sizin hâlâ tam olarak `item-query` olmasına ihtiyacınız var...

O zaman bir `alias` tanımlayabilirsiniz; bu alias, parametre değerini bulmak için kullanılacaktır:

{* ../../docs_src/query_params_str_validations/tutorial009_an_py310.py hl[9] *}

## Parametreleri deprecated yapmak { #deprecating-parameters }

Diyelim ki artık bu parametreyi istemiyorsunuz.

Bazı client’lar hâlâ kullandığı için bir süre tutmanız gerekiyor, ama dokümanların bunu açıkça <dfn title="kullanımdan kalkmış, kullanmamanız önerilir">deprecated</dfn> olarak göstermesini istiyorsunuz.

O zaman `Query`’ye `deprecated=True` parametresini geçin:

{* ../../docs_src/query_params_str_validations/tutorial010_an_py310.py hl[19] *}

Dokümanlarda şöyle görünür:

<img src="/img/tutorial/query-params-str-validations/image01.png">

## Parametreleri OpenAPI’dan hariç tutun { #exclude-parameters-from-openapi }

Oluşturulan OpenAPI şemasından (dolayısıyla otomatik dokümantasyon sistemlerinden) bir query parametresini hariç tutmak için `Query`’nin `include_in_schema` parametresini `False` yapın:

{* ../../docs_src/query_params_str_validations/tutorial014_an_py310.py hl[10] *}

## Özel Doğrulama { #custom-validation }

Yukarıdaki parametrelerle yapılamayan bazı **özel doğrulama** ihtiyaçlarınız olabilir.

Bu durumlarda, normal doğrulamadan sonra (ör. değerin `str` olduğunun doğrulanmasından sonra) uygulanacak bir **custom validator function** kullanabilirsiniz.

Bunu, `Annotated` içinde <a href="https://docs.pydantic.dev/latest/concepts/validators/#field-after-validator" class="external-link" target="_blank">Pydantic’in `AfterValidator`</a>’ını kullanarak yapabilirsiniz.

/// tip | İpucu

Pydantic’te <a href="https://docs.pydantic.dev/latest/concepts/validators/#field-before-validator" class="external-link" target="_blank">`BeforeValidator`</a> ve başka validator’lar da vardır. 🤓

///

Örneğin bu custom validator, bir item ID’sinin <abbr title="International Standard Book Number - Uluslararası Standart Kitap Numarası">ISBN</abbr> kitap numarası için `isbn-` ile veya <abbr title="Internet Movie Database - İnternet Film Veritabanı: filmler hakkında bilgi içeren bir web sitesi">IMDB</abbr> film URL ID’si için `imdb-` ile başladığını kontrol eder:

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py hl[5,16:19,24] *}

/// info | Bilgi

Bu özellik Pydantic 2 ve üzeri sürümlerde mevcuttur. 😎

///

/// tip | İpucu

Veritabanı veya başka bir API gibi herhangi bir **harici bileşen** ile iletişim gerektiren bir doğrulama yapmanız gerekiyorsa, bunun yerine **FastAPI Dependencies** kullanmalısınız; onları ileride öğreneceksiniz.

Bu custom validator’lar, request’te sağlanan **yalnızca** **aynı veri** ile kontrol edilebilen şeyler içindir.

///

### O Kodu Anlamak { #understand-that-code }

Önemli nokta, **`Annotated` içinde bir fonksiyonla birlikte `AfterValidator` kullanmak**. İsterseniz bu kısmı atlayabilirsiniz. 🤸

---

Ama bu örnek kodun detaylarını merak ediyorsanız, birkaç ek bilgi:

#### `value.startswith()` ile String { #string-with-value-startswith }

Fark ettiniz mi? `value.startswith()` ile bir string, tuple alabilir ve tuple içindeki her değeri kontrol eder:

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[16:19] hl[17] *}

#### Rastgele Bir Item { #a-random-item }

`data.items()` ile, her dictionary öğesi için key ve value içeren tuple’lardan oluşan bir <dfn title="for döngüsüyle üzerinde gezinebileceğimiz bir şey; list, set vb.">yinelemeli nesne</dfn> elde ederiz.

Bu yinelemeli nesneyi `list(data.items())` ile düzgün bir `list`’e çeviririz.

Ardından `random.choice()` ile list’ten **rastgele bir değer** alırız; yani `(id, name)` içeren bir tuple elde ederiz. Şuna benzer: `("imdb-tt0371724", "The Hitchhiker's Guide to the Galaxy")`.

Sonra tuple içindeki bu **iki değeri** `id` ve `name` değişkenlerine **atarız**.

Böylece kullanıcı bir item ID’si vermemiş olsa bile yine de rastgele bir öneri alır.

...bütün bunları **tek bir basit satırda** yapıyoruz. 🤯 Python’u sevmemek elde mi? 🐍

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[22:30] hl[29] *}

## Özet { #recap }

Parametreleriniz için ek doğrulamalar ve metadata tanımlayabilirsiniz.

Genel doğrulamalar ve metadata:

* `alias`
* `title`
* `description`
* `deprecated`

String’lere özel doğrulamalar:

* `min_length`
* `max_length`
* `pattern`

`AfterValidator` ile custom doğrulamalar.

Bu örneklerde `str` değerleri için doğrulamanın nasıl tanımlanacağını gördünüz.

Sayılar gibi diğer tipler için doğrulamaları nasıl tanımlayacağınızı öğrenmek için sonraki bölümlere geçin.
