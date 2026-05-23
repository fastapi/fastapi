# Response Model - Dönüş Tipi { #response-model-return-type }

*Path operation function* **dönüş tipini** (return type) type annotation ile belirtip response için kullanılacak tipi tanımlayabilirsiniz.

Fonksiyon **parametreleri** için input data’da kullandığınız **type annotations** yaklaşımının aynısını burada da kullanabilirsiniz; Pydantic model’leri, list’ler, dict’ler, integer, boolean gibi skaler değerler vb.

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

FastAPI bu dönüş tipini şunlar için kullanır:

* Dönen veriyi **doğrulamak** (validate).
    * Veri geçersizse (ör. bir field eksikse), bu *sizin* uygulama kodunuzun bozuk olduğu, olması gerekeni döndürmediği anlamına gelir; bu yüzden yanlış veri döndürmek yerine server error döner. Böylece siz ve client’larınız, beklenen veri ve veri şeklinin geleceğinden emin olabilirsiniz.
* OpenAPI’deki *path operation* içine response için bir **JSON Schema** eklemek.
    * Bu, **otomatik dokümantasyon** tarafından kullanılır.
    * Ayrıca otomatik client code generation araçları tarafından da kullanılır.
* Dönen veriyi Pydantic kullanarak JSON’a **serileştirmek**; Pydantic **Rust** ile yazıldığı için **çok daha hızlıdır**.

Ama en önemlisi:

* Çıktı verisini, dönüş tipinde tanımlı olana göre **sınırlar ve filtreler**.
    * Bu, özellikle **güvenlik** açısından önemlidir; aşağıda daha fazlasını göreceğiz.

## `response_model` Parametresi { #response-model-parameter }

Bazı durumlarda, tam olarak dönüş tipinin söylediği gibi olmayan bir veriyi döndürmeniz gerekebilir ya da isteyebilirsiniz.

Örneğin, **bir dict** veya bir veritabanı objesi döndürmek isteyip, ama **onu bir Pydantic model olarak declare etmek** isteyebilirsiniz. Böylece Pydantic model, döndürdüğünüz obje (ör. dict veya veritabanı objesi) için dokümantasyon, doğrulama vb. işlerin tamamını yapar.

Eğer dönüş tipi annotation’ını eklerseniz, araçlar ve editörler (doğru şekilde) fonksiyonunuzun, declare ettiğiniz tipten (ör. Pydantic model) farklı bir tip (ör. dict) döndürdüğünü söyleyip hata verir.

Bu gibi durumlarda, dönüş tipi yerine *path operation decorator* parametresi olan `response_model`’i kullanabilirsiniz.

`response_model` parametresini herhangi bir *path operation* içinde kullanabilirsiniz:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* vb.

{* ../../docs_src/response_model/tutorial001_py310.py hl[17,22,24:27] *}

/// note | Not

`response_model`’in "decorator" metodunun (`get`, `post` vb.) bir parametresi olduğuna dikkat edin. Body ve diğer parametreler gibi, sizin *path operation function*’ınızın parametresi değildir.

///

`response_model`, Pydantic model field’ı için declare edeceğiniz aynı tipi alır; yani bir Pydantic model olabilir ama örneğin `List[Item]` gibi Pydantic model’lerden oluşan bir `list` de olabilir.

FastAPI bu `response_model`’i; dokümantasyon, doğrulama vb. her şey için ve ayrıca çıktı verisini **tip tanımına göre dönüştürmek ve filtrelemek** için kullanır.

/// tip | İpucu

Editörünüzde, mypy vb. ile sıkı type kontrolü yapıyorsanız, fonksiyon dönüş tipini `Any` olarak declare edebilirsiniz.

Böylece editöre bilerek her şeyi döndürebileceğinizi söylemiş olursunuz. Ancak FastAPI, `response_model` ile dokümantasyon, doğrulama, filtreleme vb. işlemleri yine de yapar.

///

### `response_model` Önceliği { #response-model-priority }

Hem dönüş tipi hem de `response_model` declare ederseniz, FastAPI’de `response_model` önceliklidir ve o kullanılır.

Böylece, response model’den farklı bir tip döndürdüğünüz durumlarda bile editör ve mypy gibi araçlar için fonksiyonlarınıza doğru type annotation’lar ekleyebilir, aynı zamanda FastAPI’nin `response_model` üzerinden veri doğrulama, dokümantasyon vb. yapmasını sağlayabilirsiniz.

Ayrıca `response_model=None` kullanarak, ilgili *path operation* için response model oluşturulmasını devre dışı bırakabilirsiniz. Bu, Pydantic field’ı olarak geçerli olmayan şeyler için type annotation eklediğinizde gerekebilir; aşağıdaki bölümlerden birinde bunun örneğini göreceksiniz.

## Aynı input verisini geri döndürmek { #return-the-same-input-data }

Burada `UserIn` adında bir model declare ediyoruz; bu model plaintext bir password içerecek:

{* ../../docs_src/response_model/tutorial002_py310.py hl[7,9] *}

/// info | Bilgi

`EmailStr` kullanmak için önce [`email-validator`](https://github.com/JoshData/python-email-validator) paketini kurun.

Bir [virtual environment](../virtual-environments.md) oluşturduğunuzdan, onu aktive ettiğinizden emin olun ve ardından örneğin şöyle kurun:

```console
$ pip install email-validator
```

veya şöyle:

```console
$ pip install "pydantic[email]"
```

///

Bu model ile hem input’u declare ediyoruz hem de output’u aynı model ile declare ediyoruz:

{* ../../docs_src/response_model/tutorial002_py310.py hl[16] *}

Artık bir browser password ile user oluşturduğunda, API response içinde aynı password’ü geri döndürecek.

Bu örnekte sorun olmayabilir; çünkü password’ü gönderen kullanıcı zaten aynı kişi.

Ancak aynı modeli başka bir *path operation* için kullanırsak, kullanıcının password’lerini her client’a gönderiyor olabiliriz.

/// danger

Tüm riskleri bildiğinizden ve ne yaptığınızdan emin olmadığınız sürece, bir kullanıcının plain password’ünü asla saklamayın ve bu şekilde response içinde göndermeyin.

///

## Bir output modeli ekleyin { #add-an-output-model }

Bunun yerine, plaintext password içeren bir input modeli ve password’ü içermeyen bir output modeli oluşturabiliriz:

{* ../../docs_src/response_model/tutorial003_py310.py hl[9,11,16] *}

Burada *path operation function* password içeren aynı input user’ı döndürüyor olsa bile:

{* ../../docs_src/response_model/tutorial003_py310.py hl[24] *}

...`response_model` olarak, password’ü içermeyen `UserOut` modelimizi declare ettik:

{* ../../docs_src/response_model/tutorial003_py310.py hl[22] *}

Dolayısıyla **FastAPI**, output model’de declare edilmemiş tüm verileri (Pydantic kullanarak) filtrelemekle ilgilenir.

### `response_model` mi Return Type mı? { #response-model-or-return-type }

Bu durumda iki model farklı olduğu için fonksiyon dönüş tipini `UserOut` olarak annotate etseydik, editör ve araçlar farklı class’lar olduğu için geçersiz bir tip döndürdüğümüzü söyleyip hata verecekti.

Bu yüzden bu örnekte `response_model` parametresinde declare etmek zorundayız.

...ama bunu nasıl aşabileceğinizi görmek için aşağıyı okumaya devam edin.

## Return Type ve Veri Filtreleme { #return-type-and-data-filtering }

Önceki örnekten devam edelim. Fonksiyonu **tek bir tip ile annotate etmek** istiyoruz; ama fonksiyondan gerçekte **daha fazla veri** içeren bir şey döndürebilmek istiyoruz.

FastAPI’nin response model’i kullanarak veriyi **filtrelemeye** devam etmesini istiyoruz. Yani fonksiyon daha fazla veri döndürse bile response, sadece response model’de declare edilmiş field’ları içersin.

Önceki örnekte class’lar farklı olduğu için `response_model` parametresini kullanmak zorundaydık. Ancak bu, editör ve araçların fonksiyon dönüş tipi kontrolünden gelen desteğini alamadığımız anlamına da geliyor.

Ama bu tarz durumların çoğunda modelin amacı, bu örnekteki gibi bazı verileri **filtrelemek/kaldırmak** olur.

Bu gibi durumlarda class’lar ve inheritance kullanarak, fonksiyon **type annotations** sayesinde editör ve araçlarda daha iyi destek alabilir, aynı zamanda FastAPI’nin **veri filtrelemesini** de koruyabiliriz.

{* ../../docs_src/response_model/tutorial003_01_py310.py hl[7:10,13:14,18] *}

Bununla birlikte, code type’lar açısından doğru olduğu için editörler ve mypy araç desteği verir; ayrıca FastAPI’den veri filtrelemeyi de alırız.

Bu nasıl çalışıyor? Bir bakalım. 🤓

### Type Annotations ve Araç Desteği { #type-annotations-and-tooling }

Önce editörler, mypy ve diğer araçlar bunu nasıl görür, ona bakalım.

`BaseUser` temel field’lara sahiptir. Ardından `UserIn`, `BaseUser`’dan miras alır ve `password` field’ını ekler; yani iki modelin field’larının tamamını içerir.

Fonksiyonun dönüş tipini `BaseUser` olarak annotate ediyoruz ama gerçekte bir `UserIn` instance’ı döndürüyoruz.

Editör, mypy ve diğer araçlar buna itiraz etmez; çünkü typing açısından `UserIn`, `BaseUser`’ın subclass’ıdır. Bu da, bir `BaseUser` bekleniyorken `UserIn`’in *geçerli* bir tip olduğu anlamına gelir.

### FastAPI Veri Filtreleme { #fastapi-data-filtering }

FastAPI açısından ise dönüş tipini görür ve döndürdüğünüz şeyin **yalnızca** tipte declare edilen field’ları içerdiğinden emin olur.

FastAPI, Pydantic ile içeride birkaç işlem yapar; böylece class inheritance kurallarının dönen veri filtrelemede aynen kullanılmasına izin vermez. Aksi halde beklediğinizden çok daha fazla veriyi response’ta döndürebilirdiniz.

Bu sayede iki dünyanın da en iyisini alırsınız: **araç desteği** veren type annotations ve **veri filtreleme**.

## Dokümanlarda görün { #see-it-in-the-docs }

Otomatik dokümanları gördüğünüzde, input model ve output model’in her birinin kendi JSON Schema’sına sahip olduğunu kontrol edebilirsiniz:

<img src="/img/tutorial/response-model/image01.png">

Ve her iki model de etkileşimli API dokümantasyonunda kullanılır:

<img src="/img/tutorial/response-model/image02.png">

## Diğer Return Type Annotation’ları { #other-return-type-annotations }

Bazı durumlarda Pydantic field olarak geçerli olmayan bir şey döndürebilir ve bunu fonksiyonda annotate edebilirsiniz; amaç sadece araçların (editör, mypy vb.) sağladığı desteği almaktır.

### Doğrudan Response Döndürmek { #return-a-response-directly }

En yaygın durum, [ileri seviye dokümanlarda daha sonra anlatıldığı gibi doğrudan bir Response döndürmektir](../advanced/response-directly.md).

{* ../../docs_src/response_model/tutorial003_02_py310.py hl[8,10:11] *}

Bu basit durum FastAPI tarafından otomatik olarak ele alınır; çünkü dönüş tipi annotation’ı `Response` class’ıdır (veya onun bir subclass’ı).

Araçlar da memnun olur; çünkü hem `RedirectResponse` hem `JSONResponse`, `Response`’un subclass’ıdır. Yani type annotation doğrudur.

### Bir Response Subclass’ını Annotate Etmek { #annotate-a-response-subclass }

Type annotation içinde `Response`’un bir subclass’ını da kullanabilirsiniz:

{* ../../docs_src/response_model/tutorial003_03_py310.py hl[8:9] *}

Bu da çalışır; çünkü `RedirectResponse`, `Response`’un subclass’ıdır ve FastAPI bu basit durumu otomatik olarak yönetir.

### Geçersiz Return Type Annotation’ları { #invalid-return-type-annotations }

Ancak geçerli bir Pydantic tipi olmayan başka rastgele bir obje (ör. bir veritabanı objesi) döndürür ve fonksiyonu da öyle annotate ederseniz, FastAPI bu type annotation’dan bir Pydantic response model oluşturmaya çalışır ve başarısız olur.

Aynı şey, farklı tipler arasında bir <dfn title="Birden fazla tip arasındaki bir birleşim, 'bu tiplerden herhangi biri' anlamına gelir.">birleşim</dfn> kullandığınızda ve bu tiplerden biri veya birkaçı geçerli bir Pydantic tipi değilse de olur; örneğin şu kullanım patlar 💥:

{* ../../docs_src/response_model/tutorial003_04_py310.py hl[8] *}

...bu, type annotation Pydantic tipi olmadığı ve tek bir `Response` class’ı (veya subclass’ı) olmadığı için başarısız olur; bu, bir `Response` ile bir `dict` arasında union’dır (ikiden herhangi biri).

### Response Model’i Devre Dışı Bırakmak { #disable-response-model }

Yukarıdaki örnekten devam edersek; FastAPI’nin varsayılan olarak yaptığı veri doğrulama, dokümantasyon, filtreleme vb. işlemleri istemiyor olabilirsiniz.

Ancak yine de editörler ve type checker’lar (ör. mypy) gibi araçların desteğini almak için fonksiyonda dönüş tipi annotation’ını korumak isteyebilirsiniz.

Bu durumda `response_model=None` ayarlayarak response model üretimini devre dışı bırakabilirsiniz:

{* ../../docs_src/response_model/tutorial003_05_py310.py hl[7] *}

Bu, FastAPI’nin response model üretimini atlamasını sağlar; böylece FastAPI uygulamanızı etkilemeden ihtiyacınız olan herhangi bir return type annotation’ını kullanabilirsiniz. 🤓

## Response Model encoding parametreleri { #response-model-encoding-parameters }

Response model’inizde şu şekilde default değerler olabilir:

{* ../../docs_src/response_model/tutorial004_py310.py hl[9,11:12] *}

* `description: Union[str, None] = None` (veya Python 3.10’da `str | None = None`) için default `None`’dır.
* `tax: float = 10.5` için default `10.5`’tir.
* `tags: List[str] = []` için default, boş bir list’tir: `[]`.

Ancak gerçekte kaydedilmedilerse, bunları sonuçtan çıkarmak isteyebilirsiniz.

Örneğin NoSQL veritabanında çok sayıda optional attribute içeren modelleriniz varsa, default değerlerle dolu çok uzun JSON response’ları göndermek istemeyebilirsiniz.

### `response_model_exclude_unset` parametresini kullanın { #use-the-response-model-exclude-unset-parameter }

*Path operation decorator* parametresi olarak `response_model_exclude_unset=True` ayarlayabilirsiniz:

{* ../../docs_src/response_model/tutorial004_py310.py hl[22] *}

böylece response’a default değerler dahil edilmez; yalnızca gerçekten set edilmiş değerler gelir.

Dolayısıyla ID’si `foo` olan item için bu *path operation*’a request atarsanız, response (default değerler olmadan) şöyle olur:

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

/// info | Bilgi

Ayrıca şunları da kullanabilirsiniz:

* `response_model_exclude_defaults=True`
* `response_model_exclude_none=True`

Bunlar, `exclude_defaults` ve `exclude_none` için [Pydantic dokümanlarında](https://docs.pydantic.dev/1.10/usage/exporting_models/#modeldict) anlatıldığı gibidir.

///

#### Default’u olan field’lar için değer içeren data { #data-with-values-for-fields-with-defaults }

Ama data’nız modelde default değeri olan field’lar için değer içeriyorsa, örneğin ID’si `bar` olan item gibi:

```Python hl_lines="3  5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```

bunlar response’a dahil edilir.

#### Default değerlerle aynı değerlere sahip data { #data-with-the-same-values-as-the-defaults }

Eğer data, default değerlerle aynı değerlere sahipse, örneğin ID’si `baz` olan item gibi:

```Python hl_lines="3  5-6"
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```

FastAPI yeterince akıllıdır (aslında Pydantic yeterince akıllıdır) ve `description`, `tax`, `tags` default ile aynı olsa bile bunların explicit olarak set edildiğini (default’tan alınmadığını) anlar.

Bu yüzden JSON response içinde yer alırlar.

/// tip | İpucu

Default değerlerin yalnızca `None` olmak zorunda olmadığını unutmayın.

Bir list (`[]`), `10.5` gibi bir `float` vb. olabilirler.

///

### `response_model_include` ve `response_model_exclude` { #response-model-include-and-response-model-exclude }

Ayrıca *path operation decorator* parametreleri `response_model_include` ve `response_model_exclude`’u da kullanabilirsiniz.

Bunlar; dahil edilecek attribute isimlerini (geri kalanını atlayarak) ya da hariç tutulacak attribute isimlerini (geri kalanını dahil ederek) belirten `str` değerlerinden oluşan bir `set` alır.

Tek bir Pydantic model’iniz varsa ve output’tan bazı verileri hızlıca çıkarmak istiyorsanız, bu yöntem pratik bir kısayol olabilir.

/// tip | İpucu

Ancak yine de, bu parametreler yerine yukarıdaki yaklaşımı (birden fazla class kullanmayı) tercih etmeniz önerilir.

Çünkü `response_model_include` veya `response_model_exclude` ile bazı attribute’ları atlıyor olsanız bile, uygulamanızın OpenAPI’sinde (ve dokümanlarda) üretilen JSON Schema hâlâ tam modelin JSON Schema’sı olacaktır.

Bu durum, benzer şekilde çalışan `response_model_by_alias` için de geçerlidir.

///

{* ../../docs_src/response_model/tutorial005_py310.py hl[29,35] *}

/// tip | İpucu

`{"name", "description"}` sözdizimi, bu iki değere sahip bir `set` oluşturur.

Bu, `set(["name", "description"])` ile eşdeğerdir.

///

#### `set` yerine `list` kullanmak { #using-lists-instead-of-sets }

Yanlışlıkla `set` yerine `list` veya `tuple` kullanırsanız, FastAPI bunu yine `set`’e çevirir ve doğru şekilde çalışır:

{* ../../docs_src/response_model/tutorial006_py310.py hl[29,35] *}

## Özet { #recap }

Response model’leri tanımlamak ve özellikle private data’nın filtrelendiğinden emin olmak için *path operation decorator* parametresi `response_model`’i kullanın.

Yalnızca explicit olarak set edilmiş değerleri döndürmek için `response_model_exclude_unset` kullanın.
