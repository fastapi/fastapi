# Sorgu Parametreleri ve String Doğrulamaları

**FastAPI**, parametreler için ek bilgi ve doğrulama tanımlamalarına olanak sağlar.

Örneğin, aşağıdaki uygulamada:

=== "Python 3.10+"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial001_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial001.py!}
    ```

 `q` sorgu parametresi, `Union[str, None]` (Python 3.10'da `str | None`) tipinden olduğundan dolayı `str` ve ayrıca `None` da olabilir ve hatta varsayılan değer olarak `None` aldığından dolayı FastAPI bu parametrenin zorunlu olmadığını anlayacaktır.

!!! note "Not"
    FastAPI, `= None` varsayılan değerinden dolayı `q` parametresinin zorunlu olmadığını anlayacaktır.

    `Union[str, None]` ifadesinin içindeki `Union` tipi sayesinde editör daha iyi bir desteğe sahip olacak ve hataları tespit edebilecektir.

## Ek Doğrulama

Bu senaryoda, `q` parametresi zorunlu olmasına rağmen tanımlandığında **uzunluğunun 50 karakteri geçmemesi** gerektiğini zorunlu kılacağız.

### `Query` ve `Annotated` İfadelerini İçeri Aktaralım

Bunu sağlamak adına aşağıdaki ifadeleri içeri aktaralım:

* `fastapi` paketinden `Query`
* `typing` (Python 3.9 veya daha alt versiyonlarda `typing_extensions`) paketinden `Annotated`

=== "Python 3.10+"

    Python 3.9 veya daha üst versiyonlarda `Annotated` standart kütüphaneye dahil olduğundan dolayı direkt olarak `typing` paketinden içeri aktarılabilir.

    ```Python hl_lines="1  3"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_an_py310.py!}
    ```

=== "Python 3.8+"

    Python 3.9 veya daha alt versiyonlarda `Annotated`, `typing_extensions` paketinden içeri aktarılmalıdır.

    Halihazırda FastAPI'ya dahili bir şekilde kurulur.

    ```Python hl_lines="3-4"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_an.py!}
    ```

!!! info "Bilgi"
    FastAPI, 0.95.0 versiyonu ile birlikte `Annotated` ifadesini desteklemeye (ve önermeye) başladı.

    Daha eski bir sürüme sahipseniz `Annotated` ifadesini kullanırken hata alacaksınızdır.

    `Annotated` ifadesini kullanmadan önce [FastAPI versiyon güncellemesini](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank} en az 0.95.1 sürümüne getirdiğinizden emin olunuz.

## `Annotated` İfadesini `q` Parametresinde Kullanalım

Hatırlarsanız `Annotated` ifadesinin, parametrelere üstveri eklemede kullanılabileceğini [Python Veri Tiplerine Giriş](../python-types.md#type-hints-with-metadata-annotations){.internal-link target=_blank} bağlantısında bahsetmiştik.

Hadi şimdi bunu FastAPI ile kullanalım. 🚀

Buna benzer bir tip belirtecine sahiptik:

=== "Python 3.10+"

    ```Python
    q: str | None = None
    ```

=== "Python 3.8+"

    ```Python
    q: Union[str, None] = None
    ```

Bu ifade `Annotated` ile sarmalandıktan sonra şöyle gözükecektir:

=== "Python 3.10+"

    ```Python
    q: Annotated[str | None] = None
    ```

=== "Python 3.8+"

    ```Python
    q: Annotated[Union[str, None]] = None
    ```

İki versiyon da `q` parametresinin `str` ya da `None` tipinden olabileceğini ve varsayılan olarak `None` olduğunu belirtir.

Hadi eğlenceli kısma geçelim. 🎉

## `q` Parametresindeki `Annotated` İfadesine `Query` Ekleyelim

İçine daha fazla üstveri ekleyebileceğimiz `Annotated` ifadesine sahip olduğumuzdan dolayı içine `Query` ifadesini ekleyip `max_length` değerini 50 olarak tanımlayalım:

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_an_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_an.py!}
    ```

Dikkatinizi çekerim ki, varsayılan değer `None` olduğundan dolayı parametremiz hala isteğe bağlıdır.

Fakat şimdi, `Annotated` ifadesinin içine `Query(max_length=50)` ilave ederek bu değerin sorgu parametrelerinden elde edilmesi (varsayılan olarak zaten böyle çalışır 🤷) ve **ek doğrulamaya** sahip olması gerektiğini (bunu yapıyor olmamızın yegâne sebebidir) bildiriyoruz. 😎

Bundan sonra FastAPI:

* Maksimum uzunluğun 50 karakter olmasını göz önünde bulundurarak veriyi **doğrulayacak**
* Veri geçersiz olduğu durumda istemciye **belirgin bir hata** gösterecek
* OpenAPI şema *yol operasyonunda* parametreyi **dokümante** edecek (böylece **otomatik dokümantasyon arayüzünde** yer alacak)

## Varsayılan Değer Olarak (Eski) Alternatif `Query`

FastAPI'ın önceki versiyonları, (<abbr title="2023-03'den önce">0.95.0</abbr>'den önce) `Query`'nin `Annotated` ifadesinin içine konulması yerine fonksiyonda parametrenin varsayılan değeri olmasını zorunlu kılıyordu. Bu tür kullanım içeren kod ile karşılaşma ihtimaliniz yüksek olduğundan dolayı sizleri bu konuda bilgilendirmek isteriz.

!!! tip "İpucu"
    Yeni yazacağınız programlarda ve mümkün olan her zaman `Annotated` ifadesini (yukarıda açıklandığı şekilde) kullanmaya özen gösteriniz. Bu kullanımın (aşağıda açıklandığı gibi) birden fazla avantajı olmasına karşılık hiçbir dezavantajı bulunmamaktadır. 🍰

`max_length` parametresini 50 değerine atayarak `Query()` ifadesini, fonksiyonda varsayılan parametre değeri olarak aşağıdaki gibi tanımlamanız gerekirdi:

=== "Python 3.10+"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial002.py!}
    ```

(`Annotated` kullanmadığımız) Bu durumda, `Query()` ifadeli fonksiyon parametresindeki `None` varsayılan değerini `Query(default=None)` ifadesi ile değiştirmemiz gerekiyor. Tanımlanan yeni ifade, varsayılan değer atamak için eski ifade ile (en azından FastAPI için) aynı amaca hizmet eder.

Böylece:

```Python
q: Union[str, None] = Query(default=None)
```

...ifadesi, parametreyi, `None` varsayılan değeri ile isteğe bağlı bir hale çevirir, aşağıdaki ifadede de olduğu gibi:

```Python
q: Union[str, None] = None
```

Python 3.10 ve daha üst versiyonlarda:

```Python
q: str | None = Query(default=None)
```

...ifadesi parametreyi, `None` varsayılan değeri ile isteğe bağlı bir hale çevirir, aşağıdaki ifadede de olduğu gibi:

```Python
q: str | None = None
```

Fakat bu kullanım parametreyi, açıkça sorgu parametresi olarak tanımlar.

!!! info "Bilgi"
    Unutmamak gerekir ki, `None` ifadesini varsayılan değer olarak kullanıp parametreyi **zorunlu olmayan** bir hale getirerek:

    ```Python
    = None
    ```

    ya da:

    ```Python
    = Query(default=None)
    ```

    ifadeleri, bir parametreyi isteğe bağlı bir hale çeviren en önemli kısımlardır.

    `Union[str, None]` ifadeli kısım, editörün daha iyi bir destek sağlamasına olanak sağlar fakat FastAPI'ya parametrenin zorunlu olmadığını belirtmez.

Böylece `Query` ifadesine daha fazla parametre gönderebilir bir hale geliriz. Bu durumda, string değerlere etki eden `max_length` ifadesini örnek verebiliriz:

```Python
q: Union[str, None] = Query(default=None, max_length=50)
```

Bu ifade veriyi doğrulayacak, veri geçersiz olduğunda belirgin bir hata gösterecek ve OpenAPI şema *yol operasyonundaki* parameteyi dokümante edecek.

### Varsayılan Değer Olarak `Query` veya `Annotated` İfadesinin İçinde

Unutmamanız gerekir ki, `Annotated` ifadesinin içinde `Query` kullanırken `Query` için `default` parametresini kullanamazsınız.

Tutarsızlık olmaması adına fonksiyon parametresinin asıl varsayılan değerini kullanabilirsiniz.

Mesela, böyle bir kullanım:

```Python
q: Annotated[str, Query(default="rick")] = "morty"
```

...varsayılan değerin, `"rick"` ya da `"morty"` değerlerinden hangisi olduğu belli olmadığından dolayı mümkün değildir.

Bu yüzden, (tercihen) böyle kullanmalısınız:

```Python
q: Annotated[str, Query()] = "rick"
```

...veya eski kodlarda şununla karşılaşabilirsiniz:

```Python
q: str = Query(default="rick")
```

### `Annotated` İfadesinin Avantajları

Fonksiyon parametrelerindeki varsayılan değerler yerine **`Annotated` kullanımı tavsiye edilir** ve bu kullanım birçok sebepten ötürü **daha iyidir**. 🤓

**Fonksiyon parametresindeki** **varsayılan** değer Python dili ile daha sezgisel çalışan **asıl varsayılan** değerdir. 😌

Aynı fonksiyon, FastAPI olmadan da **farklı yerlerde** **çağırılabilir** ve **beklenildiği gibi çalışır**. Eğer ortada **zorunlu** (varsayılan değeri olmayan) bir parametre varsa **editörünüz** sizi bir hata ile bilgilendirecektir, aynı şekilde, fonksiyonu, zorunlu parametre olmadan çalıştırırsanız **Python** huysuzlanacaktır.

`Annotated` ifadesini kullanmayıp yerine **(eski) varsayılan değer tarzını** tercih ederseniz ve eğer fonksiyonu FastAPI olmadan **farklı bir yerde** çağırırsanız fonksiyonun doğru bir şekilde çalışması adına parametreleri doğru bir şekilde şekilde geçmeyi **unutmamalısınız**. Aksi takdirde değerler beklediğinizden farklı bir şekilde tanımlanacaktır (örneğin `QueryInfo` ya da `str` olmayan benzer bir değer). Ayrıca, bu durumda fonksiyon içindeki işlemler hata vermediği sürece editörünüz ve Python, fonksiyon çalışırken huysuzlanmayacaktır.

`Annotated` ifadesi birden fazla üstveri alabileceği için aynı fonksiyonu <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">Typer</a> gibi araçlar ile de kullanabilirsiniz. 🚀

## Daha Fazla Doğrulama Ekleyelim

`min_length` parametresini de kullanabiliriz:

=== "Python 3.10+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial003_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial003_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial003_an.py!}
    ```

=== "Python 3.10+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial003_py310.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial003.py!}
    ```

## Regular Expression Ekleyelim

Parametrenin eşleşeceği bir <abbr title="Regular expression, regex ya da regexp stringler için arama patterni tanımlayan bir karakter dizisidir.">regular expression</abbr> `patterni` tanımlayabilirsiniz:

=== "Python 3.10+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="12"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_an.py!}
    ```

=== "Python 3.10+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_py310.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial004.py!}
    ```

Bu regular expression patterni, alınan parametre değerinin aşağıdaki durumlara uyumluluğunu kontrol eder:

* `^`: kendinden önce herhangi bir karakter bulundurmaz ve ardından gelen karakterler ile başlar.
* `fixedquery`: `fixedquery` ile aynı değerdedir.
* `$`: burada biter ve `fixedquery` değerinin ardından herhangi bir karakter gelmez.

Bütün bu **"regular expressionlar"** ile kafanız karıştı ise endişelenmeyin. Çoğu insan için bu konu epeyce zordur. Regular expressionlara ihtiyaç duymadan da hala bir çok şey yapabilirsiniz.

Fakat ne zaman onlara ihtiyacınız olursa **FastAPI** ile halihazırda kullanılabilir olduklarını aklınızda bulundurmanızda fayda vardır.

### Pydantic v1 Versiyonunda `pattern` Yerine `regex`

Pydantic versiyon 2 ve FastAPI 0.100.0 versiyonlarından önce bu parametre, `pattern` yerine `regex` diye yazılıyordu fakat artık kullanılmıyor.

Bu kullanımı içeren kodlar ile hala karşılaşabilirsiniz:

=== "Python 3.10+ Pydantic v1"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_an_py310_regex.py!}
    ```

Fakat, artık kullanılmadığını ve yeni `pattern` parametresine güncellenmesi gerektiğini aklınızda bulundurmalısınız. 🤓

## Varsayılan Değerler

Elbette, `None` dışında farklı varsayılan değerler de kullanabilirsiniz.

Farz edelim ki, `q` sorgu parametresinin `min_length` değerinin `3` ve varsayılan değerinin `"fixedquery"` olması gerekiyor:

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial005_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial005_an.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial005.py!}
    ```

!!! note "Not"
    `None` ifadesi dahil herhangi bir tipten varsayılan bir değere sahip olmak, parametreyi isteğe bağlı (zorunlu olmayan) bir hale getirir.

## Zorunlu Hale Getirelim

Daha fazla doğrulama veya üstveri eklemeye ihtiyacımız olmadığı zamanlarda `q` sorgu parametresini aşağıdaki gibi varsayılan bir değer tanımlamayarak zorunlu hale getirebiliriz:

```Python
q: str
```

şunun yerine:

```Python
q: Union[str, None] = None
```

Şimdi ise `Query` ifadesi ile tanımlıyoruz, şu şekilde:

=== "Annotated"

    ```Python
    q: Annotated[Union[str, None], Query(min_length=3)] = None
    ```

=== "Annotated'sız"

    ```Python
    q: Union[str, None] = Query(default=None, min_length=3)
    ```

Yani, `Query` ifadesini kullanırken bir değeri zorunlu kılmak istiyorsanız varsayılan bir değer tanımlamamanız yeterli olacaktır:

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial006_an.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial006.py!}
    ```

    !!! tip "İpucu"
        Dikkatinizi çekerim ki, burada `Query()` ifadesi, fonksiyon parametresinin varsayılan değeri olarak tanımlanmış olmasına rağmen `default=None` ifadesini `Query()`'ya geçmedik.

        Yine de, `Annotated`'lı versiyonu kullanmak muhtemelen daha iyi olacaktır. 😉

### <abbr title="Ellipsis">Üç Nokta</abbr> (`...`) ile Zorunlu Kılmak

Bir değeri açıkça zorunlu kılmak için alternatif bir yol daha vardır. Bunu yapmak için varsayılan değeri `...` yapabilirsiniz:

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006b_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial006b_an.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial006b.py!}
    ```

!!! info "Bilgi"
    Eğer daha önce `...` ile karşılaşmadıysanız bu ifade <a href="https://docs.python.org/3/library/constants.html#Ellipsis" class="external-link" target="_blank">Python'ın bir parçasıdır ve "Ellipsis" (üç nokta) olarak adlandırılır</a>.

    Bu ifade, Pydantic ve FastAPI tarafından bir değeri açıkça zorunlu kılmak için kullanılır.

Bu kullanım, **FastAPI**'ın parametreyi zorunlu olarak tanımasına olanak sağlayacaktır.

### `None` ile Zorunlu Kılmak

Bir parametreyi, `None` değerini alıyor olmasına rağmen zorunlu bir hale getirebilirsiniz. Bu kullanım, istemcileri, değer `None` olsa bile bir değer göndermeye mecbur kılar.

Bunu yapmak için `None` değerini geçerli hale getirip varsayılan değeri `...` yapabilirsiniz:

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c_an.py!}
    ```

=== "Python 3.10+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c_py310.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c.py!}
    ```

!!! tip "İpucu"
    FastAPI'daki tüm veri doğrulamaya ve serializationa güç veren Pydantic'in, `Optional` veya `Union[Something, None]` ifadeleri varsayılan değer olmadan kullanıldığında ortaya çıkan ve <a href="https://pydantic-docs.helpmanual.io/usage/models/#required-optional-fields" class="external-link" target="_blank">Zorunlu İsteğe Bağlı alanlar</a> bağlantısında daha fazla bilgisini bulabileceğiniz özel bir davranışı vardır.

!!! tip "İpucu"
    Unutmayınız ki, çoğu durumda, bir değer zorunlu ise varsayılan bir değere ihtiyaç kalmaz, yani `...` ifadesini kullanmanıza pek de gerek yoktur.

## Sorgu Parametre Listesi / Birden Fazla Değer

`Query` ifadesini kullanarak açıkça bir sorgu parametresi tanımlarken parametrenin bir değerler listesi, diğer bir deyişle birden fazla değer almasını da sağlayabilirsiniz.

Örneğin, bağlantıda birden fazla kez bulunabilecek `q` adında bir sorgu parametresi tanımlamak adına şu kullanımı tercih edebilirsiniz:

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_an.py!}
    ```

=== "Python 3.10+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_py310.py!}
    ```

=== "Python 3.9+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_py39.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011.py!}
    ```

Sonrasında, böyle bir bağlantı ile:

```
http://localhost:8000/items/?q=foo&q=bar
```

`q` *sorgu parametresinin* birden fazla değerini (`foo` ve `bar`) *yol operasyon fonksiyonu* içerisinde olan `q` *fonksiyon parametresinde* Python `list` dahilinde alabilirsiniz.

Sonuç olarak, bu bağlantı için şuna benzer bir yanıt alırsınız:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

!!! tip "İpucu"
    `list` tipinde bir sorgu parametresi tanımlamak adına açıkça `Query` ifadesini kullanmalısınız. Aksi takdirde parametre, istek gövdesi olarak yorumlanacaktır.

Etkileşimli API dokümantasyonu da birden fazla değere izin verebilmek adına bu doğrultuda güncellenecektir:

<img src="/img/tutorial/query-params-str-validations/image02.png">

### Sorgu Parametre Listesi / Varsayılan Değerler ile Birden Fazla Değer

Ayrıca, veri iletilmediği durumlar için varsayılan bir değerler `list`'i de tanımlayabilirsiniz:

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial012_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial012_an.py!}
    ```

=== "Python 3.9+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial012_py39.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial012.py!}
    ```

Şu bağlantıyı ziyaret ederseniz:

```
http://localhost:8000/items/
```

`q` için varsayılan değer `["foo", "bar"]` olacak ve aldığınız yanıt şu olacaktır:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### `list` Kullanımı

Üstelik, `List[str]` (ya da Python 3.9 ve daha üst versiyonlarda `list[str]`) yerine direkt olarak `list` kullanabilirsiniz.:

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial013_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial013_an.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial013.py!}
    ```

!!! note "Not"
    Unutmamak gerekir ki, bu durumda FastAPI, listenin içeriğini denetlemeyecektir.

    Örneğin, `List[int]` ifadesi, listenin içeriğinin integerlardan oluşması gerektiğini denetler (ve dokümante eder). Fakat, yalnız başına `list` bunu yapmaz.

## Daha Fazla Üstveri Tanımlayalım

Parametre ile ilgili fazladan bilgi tanımı yapabilirsiniz.

Yaptığınız bilgi tanımı, oluşturulmuş olan OpenAPI dokümantasyonuna dahil edilir ve dokümantasyon kullanıcı arayüzleri ve harici araçlar tarafından kullanılır.

!!! note "Not"
    Unutmamanız gerekir ki, farklı araçların farklı düzeylerde OpenAPI desteği bulunur.

    Bazıları tanımlanmış ek bilgileri göstermeyebilir fakat çoğu durumda bu eksik olan özellik geliştirme için halihazırda planlıdır.

`title` ekleyebilirsiniz:

=== "Python 3.10+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial007_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial007_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial007_an.py!}
    ```

=== "Python 3.10+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial007_py310.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial007.py!}
    ```

`description` da dahil edebilirsiniz:

=== "Python 3.10+"

    ```Python hl_lines="14"
    {!> ../../../docs_src/query_params_str_validations/tutorial008_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="14"
    {!> ../../../docs_src/query_params_str_validations/tutorial008_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="15"
    {!> ../../../docs_src/query_params_str_validations/tutorial008_an.py!}
    ```

=== "Python 3.10+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial008_py310.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="13"
    {!> ../../../docs_src/query_params_str_validations/tutorial008.py!}
    ```

## Parametreler İçin Takma Ad

Diyelim ki parametrenin `item-query` olmasını istiyorsunuz.

Aynı şuradaki gibi:

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

Fakat, `item-query` ifadesinin geçerli bir Python değişken ismi olmadığını fark ettiniz.

Buna en benzer ifade `item_query` olacaktır.

Fakat, yine de ifadenin harfiyen `item-query` olmasını istiyorsunuz...

Bunun için parametre değerini bulmak adına kullanılacak olan bir `alias` tanımlayabilirsiniz:

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial009_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial009_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial009_an.py!}
    ```

=== "Python 3.10+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial009_py310.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial009.py!}
    ```

## Parametreleri Kullanımdan Kaldırmak

Farz edelim ki bir parametreden artık hoşnut değilsiniz.

Fakat, parametreyi kullanan istemciler olduğundan dolayı onu kaldıramıyorsunuz ama dokümantasyonun, parametrenin <abbr title="obsolete, kullanımı tavsiye edilmeyen">kullanımdan kaldırıldığını</abbr> açıkça belirtmesini istiyorsunuz.

Bunun için `Query` ifadesine `deprecated=True` parametresini geçebilirsiniz:

=== "Python 3.10+"

    ```Python hl_lines="19"
    {!> ../../../docs_src/query_params_str_validations/tutorial010_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="19"
    {!> ../../../docs_src/query_params_str_validations/tutorial010_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="20"
    {!> ../../../docs_src/query_params_str_validations/tutorial010_an.py!}
    ```

=== "Python 3.10+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="16"
    {!> ../../../docs_src/query_params_str_validations/tutorial010_py310.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="18"
    {!> ../../../docs_src/query_params_str_validations/tutorial010.py!}
    ```

Dokümantasyon şu şekilde görünecektir:

<img src="/img/tutorial/query-params-str-validations/image01.png">

## OpenAPI'e Dahil Etmemek

Bir sorgu parametresini, oluşturulan OpenAPI şemasının (ve dolayısıyla otomatik dokümantasyon sisteminin) haricinde tutmak için `Query` ifadesinin `include_in_schema` parametresini `False` değerine atayabilirsiniz:

=== "Python 3.10+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial014_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial014_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial014_an.py!}
    ```

=== "Python 3.10+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial014_py310.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial014.py!}
    ```

## Özet

Parametreleriniz için ek doğrulama ve üstveriler tanımlayabilirsiniz.

Jenerik doğrulama ve üstveriler:

* `alias`
* `title`
* `description`
* `deprecated`

Stringlere özgü doğrulamalar:

* `min_length`
* `max_length`
* `pattern`

Gösterilen örneklerde `str` için doğrulamaların nasıl tanımlanacağı işlenmiştir.

Sayılar gibi diğer tipler için doğrulamaların nasıl tanımlandığını görmek adına sonraki bölümlere göz atabilirsiniz.
