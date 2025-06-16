# İstek Gövdesi

API'a, bir istemciden (mesela tarayıcıdan) veri göndermek istenilen durumlarda veri, **istek gövdesi** olarak gönderilir.

**İstek** gövdesi API'a istemci tarafından gönderilen veriyi temsil eder. **Yanıt** gövdesi ise API'ın istemciye ilettiği veriden meydana gelir.

API'lar genellikle her zaman bir **yanıt** gövdesi iletmek zorundadır. Fakat, istemcilerin **istek** gövdesi gönderme gibi bir zorunluluğu yoktur.

Bütün güç ve avantajlarından faydalınılarak <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> modelleri, **istek** gövdeleri oluşturmak için kullanılır.

/// info | Bilgi

Veri göndermek için `POST` (en yaygın), `PUT`, `DELETE` veya `PATCH` kullanılır.

Bir gövde göndermek için `GET` isteği kullanılmasının, spesifikasyonlar üzerinde beklenmedik etkilere sahip olmasına rağmen, bu olay, özellikle fazlasıyla karmaşık veya olağandışı durumlar için FastAPI tarafından desteklenir.

Bahsedilen durumun uygulanması tavsiye edilmediğinden dolayı `GET` isteği kullanılırken Swagger UI destekli interaktif doküman, gövde için ek alan göstermeyecektir. Ayrıca aradaki proxyler de bunu desteklemeyebilir.

///

## Pydantic'in `BaseModel`'ini Projeye Dahil Edelim

Öncelikle, `BaseModel` sınıfını `pydantic` paketinden projemize dahil edelim:

{* ../../docs_src/body/tutorial001_py310.py hl[2] *}

## Veri Modelimizi Oluşturalım

Sonra, `BaseModel` sınıfını miras alacak bir veri modeli sınıfı tanımlayalım.

Özellikler için standart Python tipleri kullanmayı ihmal etmeyelim:

{* ../../docs_src/body/tutorial001_py310.py hl[5:9] *}

Sorgu parametrelerinde olduğu gibi, bir model özelliği, varsayılan değere sahipse o özellik zorunlu değildir, eğer sahip değilse zorunludur. Özellikler, `None` kullanılarak  isteğe bağlı hale getirilebilirler.

Örneğin üstteki model, alttaki gibi bir JSON "`object`"'i (diğer bir adla Python `dict`'i) tanımlar:

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...`description` ve `tax` alanları (`None` varsayılan değeri sayesinde) isteğe bağlı olduklarından dolayı alttaki JSON "`object`"'i de geçerli sayılabilirdi:

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## Parametre Olarak Tanımlayalım

Gövdeyi, bir *yol operasyonu* olarak eklemek için yol ve sorgu parametrelerinde yaptığımız gibi tanımlayabiliriz:

{* ../../docs_src/body/tutorial001_py310.py hl[16] *}

...sonrasında yarattığımız `Item` modelini gövde tipi olarak tanımlayalım.

## Sonuçlar

Yalnızca bu Python tip tanımlaması ile **FastAPI**:

* İstek gövdesini JSON olarak yorumlar.
* Karşılık gelen tipleri (eğer gerekiyorsa) dönüştürür.
* Veriyi doğrular.
    * Veri geçersiz ise hatalı verinin ne ve nerede olduğunu belirten güzel ve anlaşılır bir hata döndürür.
* `item` parametresi içerisine alınan veriyi aktarır.
    * Gövdeyi, fonksiyon içerisinde `Item` tipli olarak tanımladığımızdan ötürü her özellik ve özellik tipi için tüm editör desteğine de (kod tamamlama, vb.) sahip olmuş oluruz.
* Modelimiz için <a href="https://json-schema.org" class="external-link" target="_blank">JSON şema</a> tanımları oluşturur ve ek olarak bu tanımları projemizde herhangi bir yerde kullanabilmemize olanak sağlar.
* Bu şemalar, meydana gelen OpenAPI şemasının bir parçası olur ve otomatik dokümantasyon <abbr title="User Interface">UI'ları</abbr> tarafından da kullanılır.

## Otomatik Dokümantasyon

Modellerimizin JSON şemaları, interaktif API dokümanında gösterilmek üzere OpenAPI tarafından oluşturulan şemanın bir parçası olur:

<img src="/img/tutorial/body/image01.png">

Ve ayrıca bu şemalar, onlara ihtiyaç duyan her *yol operasyonu* içindeki API dokümanında kullanılır:

<img src="/img/tutorial/body/image02.png">

## Editör Desteği

Editörünüz ve fonksiyonunuz içerisindeki her alanda tip ipuçları ve kod tamamlama desteği alırsınız (bu destek, Pydantic modeli yerine `dict` alsaydınız gerçekleşmezdi).:

<img src="/img/tutorial/body/image03.png">

Yanlış tip operasyonları için de ayrıca hata uyarıları alırsınız:

<img src="/img/tutorial/body/image04.png">

Bu durum, şansın aksine tüm framework bu tasarım üstüne kurulu olduğundan dolayı meydana gelmektedir.

Ve ayrıca, tüm editörlerle çalışıyor olmasından emin olmak adına bu durum, herhangi bir devreye alımdan önce tasarım aşamasında en ince ayrıntısına kadar test edilmiştir.

Hatta, bu durumu desteklemesi amacıyla, Pydantic kütüphanesinin kendi içerisinde bile bazı değişiklikler yapılmıştır.

En son ekran görüntüleri, <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>'da çekilmiştir.

Halbuki, aynı editör desteğini, <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> veya çoğu diğer Python editörleri ile de elde edebilirsiniz:

<img src="/img/tutorial/body/image05.png">

/// tip | İpucu

Eğer, editörünüz olarak <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> uygulamasını kullanıyorsanız <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Pydantic PyCharm Plugin</a> eklentisinden de faydalanabilirsiniz.

Bu eklenti, aşağıdaki özellikler ile birlikte Pydantic modelleri için editör desteğini güçlendirir:

* oto-tamamlama
* tip uyarıları
* düzenleme
* arama
* inceleme

///

## Modeli Kullanalım

Fonksiyon içerisinde direkt olarak modelin tüm özelliklerine erişebilirsiniz:

{* ../../docs_src/body/tutorial002_py310.py *}

## İstek Gövdesi + Yol Parametreleri

Yol parametrelerini ve istek gövdesini aynı anda tanımlayabilirsiniz.

**FastAPI**, yol parametreleri ile eşleşen fonksiyon parametrelerinin **yol kısmından elde edileceklerinin** ve Pydantic modelleri olarak tanımlanan fonksiyon parametrelerinin **istek gövdesinden elde edileceklerinin** bilincindedir.

{* ../../docs_src/body/tutorial003_py310.py hl[15:16] *}

## İstek Gövdesi + Yol ve Sorgu Parametreleri

Ayrıca, **gövde**, **yol** ve **sorgu** parametrelerinin hepsini aynı anda tanımlayabilirsiniz.

**FastAPI** her birini ayırt edecek ve veriyi doğru yerden elde edecektir.

{* ../../docs_src/body/tutorial004_py310.py hl[16] *}

Fonksiyon parametreleri şu şekilde ayırt edilecektir:

* Eğer parametre, **yol** kısmında da tanımlıysa yol parametresi olarak değerlendirilecektir.
* Eğer parametre, **tekil tipten** (`int`, `float`, `str`, `bool`, vb. gibi) ise **sorgu** parametresi olarak yorumlanacaktır.
* Eğer parametre, bir **Pydantic modeli** ise istek **gövdesi** olarak yorumlanacaktır.

/// note | Not

FastAPI, `q` değerinin zorunlu olmadığını `= None` varsayılan değerini aldığı için fark edecektir.

`Union[str, None]` kısmındaki `Union` anahtar kelimesi FastAPI tarafından kullanılmamasına rağmen kullandığınız editörün size daha iyi destek vermesini ve hataları belirlemesini sağlayacaktır.

## Pydantic Olmadan

Eğer Pydantic modellerini kullanmak istemiyorsanız **Body** parametresinden faydalanabilirsiniz. Ayrıntılı bilgi için [Body - Çoklu Parametreler: Gövde içinde tekil değerler](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank} sayfasını ziyaret edebilirsiniz.
