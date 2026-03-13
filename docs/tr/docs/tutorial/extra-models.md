# Ek Modeller { #extra-models }

Önceki örnekten devam edersek, birbiriyle ilişkili birden fazla modelin olması oldukça yaygındır.

Bu durum özellikle kullanıcı modellerinde sık görülür, çünkü:

* **input modeli** bir `password` içerebilmelidir.
* **output modeli** `password` içermemelidir.
* **database modeli** büyük ihtimalle hash'lenmiş bir `password` tutmalıdır.

/// danger | Tehlike

Kullanıcının düz metin (plaintext) `password`'ünü asla saklamayın. Her zaman sonradan doğrulayabileceğiniz "güvenli bir hash" saklayın.

Eğer bilmiyorsanız, "password hash" nedir konusunu [güvenlik bölümlerinde](security/simple-oauth2.md#password-hashing){.internal-link target=_blank} öğreneceksiniz.

///

## Birden Çok Model { #multiple-models }

`password` alanlarıyla birlikte modellerin genel olarak nasıl görünebileceğine ve nerelerde kullanılacaklarına dair bir fikir:

{* ../../docs_src/extra_models/tutorial001_py310.py hl[7,9,14,20,22,27:28,31:33,38:39] *}

### `**user_in.model_dump()` Hakkında { #about-user-in-model-dump }

#### Pydantic'in `.model_dump()` Metodu { #pydantics-model-dump }

`user_in`, `UserIn` sınıfına ait bir Pydantic modelidir.

Pydantic modellerinde, model verilerini içeren bir `dict` döndüren `.model_dump()` metodu bulunur.

Yani, şöyle bir Pydantic nesnesi `user_in` oluşturursak:

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

ve sonra şunu çağırırsak:

```Python
user_dict = user_in.model_dump()
```

artık `user_dict` değişkeninde modelin verilerini içeren bir `dict` vardır (Pydantic model nesnesi yerine bir `dict` elde etmiş oluruz).

Ve eğer şunu çağırırsak:

```Python
print(user_dict)
```

şöyle bir Python `dict` elde ederiz:

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### Bir `dict`'i Unpack Etmek { #unpacking-a-dict }

`user_dict` gibi bir `dict` alıp bunu bir fonksiyona (ya da sınıfa) `**user_dict` ile gönderirsek, Python bunu "unpack" eder. Yani `user_dict` içindeki key ve value'ları doğrudan key-value argümanları olarak geçirir.

Dolayısıyla, yukarıdaki `user_dict` ile devam edersek, şunu yazmak:

```Python
UserInDB(**user_dict)
```

şuna eşdeğer bir sonuç üretir:

```Python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

Ya da daha net şekilde, `user_dict`'i doğrudan kullanarak, gelecekte içeriği ne olursa olsun:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### Bir Pydantic Modelinden Diğerinin İçeriğiyle Pydantic Model Oluşturmak { #a-pydantic-model-from-the-contents-of-another }

Yukarıdaki örnekte `user_dict`'i `user_in.model_dump()` ile elde ettiğimiz için, şu kod:

```Python
user_dict = user_in.model_dump()
UserInDB(**user_dict)
```

şuna eşdeğerdir:

```Python
UserInDB(**user_in.model_dump())
```

...çünkü `user_in.model_dump()` bir `dict` döndürür ve biz de bunu `UserInDB`'ye `**` önekiyle vererek Python'ın "unpack" etmesini sağlarız.

Böylece, bir Pydantic modelindeki verilerden başka bir Pydantic model üretmiş oluruz.

#### Bir `dict`'i Unpack Etmek ve Ek Keyword'ler { #unpacking-a-dict-and-extra-keywords }

Sonrasında, aşağıdaki gibi ek keyword argümanı `hashed_password=hashed_password` eklemek:

```Python
UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
```

...şuna benzer bir sonuca dönüşür:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
```

/// warning | Uyarı

Ek destek fonksiyonları olan `fake_password_hasher` ve `fake_save_user` sadece verinin olası bir akışını göstermek içindir; elbette gerçek bir güvenlik sağlamazlar.

///

## Tekrarı Azaltma { #reduce-duplication }

Kod tekrarını azaltmak, **FastAPI**'nin temel fikirlerinden biridir.

Kod tekrarı; bug, güvenlik problemi, kodun senkron dışına çıkması (bir yeri güncelleyip diğerlerini güncellememek) gibi sorunların olasılığını artırır.

Bu modellerin hepsi verinin büyük bir kısmını paylaşıyor ve attribute adlarını ve type'larını tekrar ediyor.

Daha iyisini yapabiliriz.

Diğer modellerimiz için temel olacak bir `UserBase` modeli tanımlayabiliriz. Sonra da bu modelden türeyen (subclass) modeller oluşturup onun attribute'larını (type deklarasyonları, doğrulama vb.) miras aldırabiliriz.

Tüm veri dönüştürme, doğrulama, dokümantasyon vb. her zamanki gibi çalışmaya devam eder.

Bu sayede modeller arasındaki farkları (plaintext `password` olan, `hashed_password` olan ve `password` olmayan) sadece o farklılıklar olarak tanımlayabiliriz:

{* ../../docs_src/extra_models/tutorial002_py310.py hl[7,13:14,17:18,21:22] *}

## `Union` veya `anyOf` { #union-or-anyof }

Bir response'u iki ya da daha fazla type'ın `Union`'ı olarak tanımlayabilirsiniz; bu, response'un bunlardan herhangi biri olabileceği anlamına gelir.

OpenAPI'de bu `anyOf` ile tanımlanır.

Bunu yapmak için standart Python type hint'i olan <a href="https://docs.python.org/3/library/typing.html#typing.Union" class="external-link" target="_blank">`typing.Union`</a>'ı kullanın:

/// note | Not

Bir <a href="https://docs.pydantic.dev/latest/concepts/types/#unions" class="external-link" target="_blank">`Union`</a> tanımlarken en spesifik type'ı önce, daha az spesifik olanı sonra ekleyin. Aşağıdaki örnekte daha spesifik olan `PlaneItem`, `Union[PlaneItem, CarItem]` içinde `CarItem`'dan önce gelir.

///

{* ../../docs_src/extra_models/tutorial003_py310.py hl[1,14:15,18:20,33] *}

### Python 3.10'da `Union` { #union-in-python-3-10 }

Bu örnekte `Union[PlaneItem, CarItem]` değerini `response_model` argümanına veriyoruz.

Bunu bir **type annotation** içine koymak yerine bir **argümana değer** olarak geçtiğimiz için, Python 3.10'da bile `Union` kullanmamız gerekiyor.

Eğer bu bir type annotation içinde olsaydı, dikey çizgiyi kullanabilirdik:

```Python
some_variable: PlaneItem | CarItem
```

Ancak bunu `response_model=PlaneItem | CarItem` atamasına koyarsak hata alırız; çünkü Python bunu bir type annotation olarak yorumlamak yerine `PlaneItem` ile `CarItem` arasında **geçersiz bir işlem** yapmaya çalışır.

## Model Listesi { #list-of-models }

Aynı şekilde, nesne listesi döndüren response'ları da tanımlayabilirsiniz.

Bunun için standart Python `list`'i kullanın:

{* ../../docs_src/extra_models/tutorial004_py310.py hl[18] *}

## Rastgele `dict` ile Response { #response-with-arbitrary-dict }

Bir Pydantic modeli kullanmadan, sadece key ve value type'larını belirterek düz, rastgele bir `dict` ile de response tanımlayabilirsiniz.

Bu, geçerli field/attribute adlarını (Pydantic modeli için gerekli olurdu) önceden bilmiyorsanız kullanışlıdır.

Bu durumda `dict` kullanabilirsiniz:

{* ../../docs_src/extra_models/tutorial005_py310.py hl[6] *}

## Özet { #recap }

Her duruma göre birden fazla Pydantic modeli kullanın ve gerekirse özgürce inheritance uygulayın.

Bir entity'nin farklı "state"lere sahip olması gerekiyorsa, o entity için tek bir veri modeli kullanmak zorunda değilsiniz. Örneğin `password` içeren, `password_hash` içeren ve `password` içermeyen state'lere sahip kullanıcı "entity"si gibi.
