# Yol Parametreleri

Yol "parametrelerini" veya "değişkenlerini" Python string biçimlemede kullanılan aynı söz dizimi ile tanımlayabilirsin.

```Python hl_lines="6-7"
{!../../../docs_src/path_params/tutorial001.py!}
```

Yol parametresi olan `item_id`'nin değeri, fonksiyonuna `item_id` argümanı olarak geçirilecektir.

Demek oluyor ki, eğer bu örneği çalıştırırsan ve <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a> sayfasına gidersen, şöyle bir yanıt ile karşılaşacaksın:

```JSON
{"item_id":"foo"}
```

## Tip içeren yol parametreleri

Standart Python tip anotasyonları kullanarak yol parametresinin tipini fonksiyonda tanımlayabilirsin.

```Python hl_lines="7"
{!../../../docs_src/path_params/tutorial002.py!}
```

Bu durumda, `item_id` bir `int` olarak tanımlanacaktır.

!!! check
    Bu özellik, fonksiyonunun içinde sana hata denetimi, kod tamamlama ve benzeri gibi özelliklerle birlikte editör desteği kazandıracaktır.

## Veri <abbr title="ayrıca şöyle bilinir: serileştirme, ayrıştırma, hizalama">dönüşümü</abbr>

Eğer bu örneği çalıştırırsan ve tarayıcında <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a> linkini açarsan, şöyle bir yanıt ile karşılaşacaksın:

```JSON
{"item_id":3}
```

!!! check
    Dikkatini çekerim ki, fonksiyonunun aldığı (ve döndürdüğü) değer olan `3` bir string `"3"` değil aksine bir Python `int`'idir.

    Böylece, bu tanımlamayla birlikte, **FastAPI** sana otomatik istek <abbr title="HTTP isteği ile birlikte gelen string'i Python verisine dönüştürme">"ayrıştırma"</abbr> özelliği sağlar.

## Veri doğrulama

Fakat, eğer tarayıcında <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a> adresine gidersen, şuna benzer güzel bir HTTP hatası ile karşılaşacaksın:

```JSON
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "item_id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "foo",
      "url": "https://errors.pydantic.dev/2.1/v/int_parsing"
    }
  ]
}
```

çünkü yol parametresi olan `item_id` değişkeni, veri tipi `int` olmayan `"foo"` gibi bir değere sahipti.

Aynı hata `int` yerine `float` bir değer verseydik de ortaya çıkardı, şuradaki gibi: <a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2</a>

!!! check
    Böylece, aynı Python tip tanımlaması ile birlikte, **FastAPI** sana veri doğrulaması özelliği sağlar.

    Dikkatini çekerim ki, karşılaştığın hata, doğrulamanın geçersiz olduğu mutlak noktayı da açık bir şekilde belirtiyor.

    Bu özellik, API'ınla iletişime geçen kodu geliştirirken ve ayıklarken inanılmaz derecede yararlı olacaktır.

## Dokümantasyon

Ayrıca, tarayıcını <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> adresinde açarsan, aşağıdaki gibi otomatik ve interaktif bir API dökümantasyonu ile karşılaşacaksın:

<img src="/img/tutorial/path-params/image01.png">

!!! check
    Üstelik, sadece aynı Python tip tanımlaması ile, **FastAPI** sana otomatik ve interaktif (Swagger UI ile entegre) bir dokümantasyon sağlar.

    Dikkatini çekerim ki, yol parametresi integer olarak tanımlanmıştır.

## Standartlara dayalı avantajlar, alternatif dokümantasyon

Ve türetilmiş olan şema <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md" class="external-link" target="_blank">OpenAPI</a> standartına uygun olduğu için birçok uyumlu araç bulunmaktadır.

Bu sayede, **FastAPI**'ın kendisi <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> linkinden erişebileceğiniz alternatif (Redoc kullanan) bir API dokümantasyonu sağlar:

<img src="/img/tutorial/path-params/image02.png">

Aynı şekilde, farklı diller için kod türetme araçları içeren çok sayıda uyumlu araç bulunur.

## Pydantic

Tüm veri doğrulamaları <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> tarafından arka planda gerçekleştirilir, bu sayede tüm avantajlardan faydalanabilirsin. Böylece, emin ellerde olduğunu hissedebilirsin.

Aynı tip tanımlamalarını `str`, `float`, `bool` ile ve diğer kompleks veri tipleri ile de kullanabilirsin.

Bunlardan birkaçı, bu eğitimin ileriki bölümlerinde irdelenmiştir.

## Sıralama önem arz eder

*Yol operasyonları* tasarlarken sabit yol barındıran durumlar ile karşılaşabilirsin.

Farz edelim ki `/users/me` yolu geçerli kullanıcı hakkında bilgi almak için kullanılıyor olsun.

Benzer şekilde `/users/{user_id}` gibi tanımlanmış ve belirli bir kullanıcı hakkında veri almak için kullanıcı ID numarası kullanılan bir yolunuz da mevcut olabilir.  

*Yol operasyonları* sıralı bir şekilde gözden geçirildiğinden dolayı `/users/me` yolunun `/users/{user_id}` yolundan önce tanımlanmış olmasından emin olmanız gerekmektedir:

```Python hl_lines="6  11"
{!../../../docs_src/path_params/tutorial003.py!}
```

Aksi halde, `/users/{user_id}` yolu `"me"` değerini alan `user_id` adlı bir parametresi olduğunu "düşünerek" `/users/me` isimli yol ile eşleşir.

Benzer şekilde, bir yol operasyonunu yeniden tanımlamanız mümkün değildir:

```Python hl_lines="6  11"
{!../../../docs_src/path_params/tutorial003b.py!}
```

Yol ilk kısım ile eşleştiğinden dolayı her koşulda ilk yol operasyonu kullanılacaktır.

## Ön tanımlı değerler

Eğer *yol parametresi* alan bir *yol operasyonun* varsa ve olağan ve geçerli *yol parametresi* değerlerinin ön tanımlı olmasını istiyorsan, standart Python <abbr title="Enumeration">`Enum`</abbr> kullanabilirsin.

### Bir `Enum` sınıfı yarat

`Enum` sınıfını içeri aktarıp `str` ile `Enum` sınıflarını miras alan bir alt sınıf yaratalım.

`str` sınıfı miras alındığından dolayı, API dokümanı, değerlerin `string` tipinden olması gerektiğini anlayabilecek ve doğru bir şekilde işlenecektir. 

Sonrasında, sınıf içerisinde, mevcut ve geçerli değerler olacak olan sabit değerli öznitelikleri oluşturalım:

```Python hl_lines="1  6-9"
{!../../../docs_src/path_params/tutorial005.py!}
```

!!! info
    3.4 sürümünden beri <a href="https://docs.python.org/3/library/enum.html" class="external-link" target="_blank">enumerationlar (ya da enumlar) Python'da mevcuttur</a>.

!!! tip
    Merak ediyorsanız söyleyeyim, "AlexNet", "ResNet" ve "LeNet" isimleri Makine Öğrenmesi <abbr title="Teknik olarak, Derin Öğrenme model mimarileri">modellerini</abbr> temsil eder.

### Bir *yol parametresi* tanımla

Sonrasında, yarattığımız (`ModelName`) isimli enum sınıfını kullanarak tip anotasyonu aracılığıyla bir *yol parametresi* oluşturalım:

```Python hl_lines="16"
{!../../../docs_src/path_params/tutorial005.py!}
```

### Dokümana göz at

*Yol parametresi* için mevcut değerler ön tanımlı olduğundan dolayı, interaktif döküman onları güzel bir şekilde gösterebilir:

<img src="/img/tutorial/path-params/image03.png">

### Python *enumerationları* ile çalışmak

*Yol parametresinin* değeri bir *enumeration üyesi* olacaktır.

#### *Enumeration üyelerini* karşılaştır

Parametreyi, yarattığın enum olan `ModelName` içerisindeki *enumeration üyesi* ile karşılaştırabilirsin:

```Python hl_lines="17"
{!../../../docs_src/path_params/tutorial005.py!}
```

#### *Enumeration değerini* elde et

`model_name.value` veya genel olarak `your_enum_member.value` tanımlarını kullanarak (bu durumda bir `str` olan) gerçek değere ulaşabilirsin:

```Python hl_lines="20"
{!../../../docs_src/path_params/tutorial005.py!}
```

!!! tip
    `"lenet"` değerine `ModelName.lenet.value` tanımı ile de ulaşabilirsin.

#### *Enumeration üyelerini* döndür

JSON gövdesine (örneğin bir `dict`) gömülü olsalar bile *yol operasyonundaki* *enum üyelerini* döndürebilirsin.

Bu üyeler istemciye iletilmeden önce kendilerine karşılık gelen değerlerine (bu durumda string) dönüştürüleceklerdir:

```Python hl_lines="18  21  23"
{!../../../docs_src/path_params/tutorial005.py!}
```

İstemci tarafında şuna benzer bir JSON yanıtı göreceksin:

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## Yol içeren yol parametreleri

Farz edelim ki elinde `/files/{file_path}` isminde bir *path operasyonu* var.

Fakat `file_path` değerinin `home/johndoe/myfile.txt` gibi bir *yol* barındırmasını istiyorsun.

Sonuç olarak, oluşturmak istediğin URL `/files/home/johndoe/myfile.txt` gibi bir şey olacaktır.

### OpenAPI desteği

Test etmesi ve tanımlaması zor senaryolara sebebiyet vereceğinden dolayı OpenAPI, *yol* barındıran *yol parametrelerini* tanımlayacak bir çözüm sunmuyor.

Buna rağmen, bu durumu, Starlette kütüphanesinin dahili araçlarından birini kullanan **FastAPI**'da gerçekleştirebilirsin.

Parametrenin bir yol içermesi gerektiğini belirten herhangi bir doküman eklemememize rağmen dokümanlar yine de çalışacaktır.

### Yol dönüştürücü

Direkt olarak Starlette kütüphanesinden gelen bir opsiyonu ve aşağıdaki gibi bir URL'yi kullanarak *yol* içeren bir *yol parametresi* tanımlayabilirsin: 

```
/files/{file_path:path}
```

Bu durumda, parametrenin adı `file_path` olacaktır ve son kısım olan `:path` kısmı, parametrenin herhangi bir *yol* ile eşleşmesi gerektiğini belirtecektir.

Böylece şunun gibi bir kullanım yapabilirsin:

```Python hl_lines="6"
{!../../../docs_src/path_params/tutorial004.py!}
```

!!! tip
    Parametrenin `/home/johndoe/myfile.txt` yolunu, baştaki (`/`) işareti ile birlikte kullanman gerektiği durumlar olabilir.

    Bu durumda, URL `files` ile `home` arasında iki eğik çizgiye (`//`) sahip olup `/files//home/johndoe/myfile.txt` gibi gözükecektir.

## Özet

**FastAPI** ile kısa, sezgisel ve standart Python tip tanımlamaları kullanarak şunları elde edersin:

* Editör desteği: hata denetimi, otomatik tamamlama, vb.
* Veri "<abbr title="HTTP isteği ile birlikte gelen string'i Python verisine dönüştürme">ayrıştırma</abbr>"
* Veri doğrulama
* API anotasyonları ve otomatik dokümantasyon

Ve sadece, bunları bir kez tanımlaman yeterli.

Diğer frameworkler ile karşılaştırıldığında (ham performans dışında), üstte anlatılan durum muhtemelen **FastAPI**'ın göze çarpan başlıca avantajıdır.
