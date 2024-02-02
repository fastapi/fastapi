# Yol Parametreleri

Yol "parametrelerini" veya "değişkenlerini" Python <abbr title="String Biçimleme: Format String">string biçimlemede</abbr> kullanılan sözdizimi ile tanımlayabilirsiniz.

```Python hl_lines="6-7"
{!../../../docs_src/path_params/tutorial001.py!}
```

Yol parametresi olan `item_id`'nin değeri, fonksiyonunuza `item_id` argümanı olarak aktarılacaktır.

Eğer bu örneği çalıştırıp <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a> sayfasına giderseniz, şöyle bir çıktı ile karşılaşırsınız:

```JSON
{"item_id":"foo"}
```

## Tip İçeren Yol Parametreleri

Standart Python tip belirteçlerini kullanarak yol parametresinin tipini fonksiyonda tanımlayabilirsiniz.

```Python hl_lines="7"
{!../../../docs_src/path_params/tutorial002.py!}
```

Bu durumda, `item_id` bir `int` olarak tanımlanacaktır.

!!! check "Ek bilgi"
    Bu sayede fonksiyonun içerisinde hata denetimi, kod tamamlama gibi konularda editör desteğine kavuşacaksınız.

## Veri <abbr title="Dönüşüm: serialization, parsing ve marshalling olarak da biliniyor">Dönüşümü</abbr>

Eğer bu örneği çalıştırıp ve tarayıcınızda <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a> sayfasını açarsanız, şöyle bir yanıt ile karşılaşırsınız:

```JSON
{"item_id":3}
```

!!! check "Ek bilgi"
    Dikkatinizi çekerim ki, fonksiyonunuzun aldığı (ve döndürdüğü) değer olan `3` bir string `"3"` değil aksine bir Python `int`'idir.

    Böylece, bu tanımlamayla birlikte, **FastAPI** size otomatik istek <abbr title="HTTP isteği ile birlikte gelen string'i Python verisine dönüştürme">"ayrıştırma"</abbr> özelliği sağlar.

## Veri Doğrulama

Fakat, eğer tarayıcınızda <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a> adresine giderseniz, şuna benzer güzel bir HTTP hatası ile karşılaşırsınız:

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

!!! check "Ek bilgi"
    Böylece, aynı Python tip tanımlaması ile birlikte, **FastAPI** size veri doğrulaması özelliği sağlar.

    Dikkatinizi çekerim ki, karşılaştığınız hata, doğrulamanın geçersiz olduğu mutlak noktayı da açık bir şekilde belirtiyor.

    Bu özellik, API'ınızla iletişime geçen kodu geliştirirken ve ayıklarken inanılmaz derecede yararlı olacaktır.

## Dokümantasyon

Ayrıca, tarayıcınızı <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> adresinde açarsanız, aşağıdaki gibi otomatik ve interaktif bir API dökümantasyonu ile karşılaşırsınız:

<img src="/img/tutorial/path-params/image01.png">

!!! check "Ek bilgi"
    Üstelik, sadece aynı Python tip tanımlaması ile, **FastAPI** size otomatik ve interaktif (Swagger UI ile entegre) bir dokümantasyon sağlar.

    Dikkatinizi çekerim ki, yol parametresi integer olarak tanımlanmıştır.

## Standartlara Dayalı Avantajlar, Alternatif Dokümantasyon

Ve türetilmiş olan şema <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md" class="external-link" target="_blank">OpenAPI</a> standartına uygun olduğu için birçok uyumlu araç bulunmaktadır.

Bu sayede, **FastAPI**'ın bizzat kendisi <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> linkinden erişebileceğiniz alternatif (Redoc kullanan) bir API dokümantasyonu sağlar:

<img src="/img/tutorial/path-params/image02.png">

Aynı şekilde, farklı diller için kod türetme araçları içeren çok sayıda uyumlu araç bulunur.

## Pydantic

Tüm veri doğrulamaları <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> tarafından arka planda gerçekleştirilir, bu sayede tüm avantajlardan faydalanabilirsiniz. Böylece, emin ellerde olduğunuzu hissedebilirsiniz.

Aynı tip tanımlamalarını `str`, `float`, `bool` ile ve diğer kompleks veri tipleri ile de kullanma imkanınız vardır.

Bunlardan birkaçı, bu eğitimin ileriki bölümlerinde irdelenmiştir.

## Sıralama Önem Arz Eder

*Yol operasyonları* tasarlarken sabit yol barındıran durumlar ile karşılaşabilirsiniz.

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

## Ön Tanımlı Değerler

Eğer *yol parametresi* alan bir *yol operasyonunuz* varsa ve olağan ve geçerli *yol parametresi* değerlerinin ön tanımlı olmasını istiyorsanız, standart Python <abbr title="Enumeration">`Enum`</abbr> kullanabilirsiniz.

### Bir `Enum` Sınıfı Yarat

`Enum` sınıfını içeri aktarıp `str` ile `Enum` sınıflarını miras alan bir alt sınıf yaratalım.

`str` sınıfı miras alındığından dolayı, API dokümanı, değerlerin `string` tipinden olması gerektiğini anlayabilecek ve doğru bir şekilde işlenecektir.

Sonrasında, sınıf içerisinde, mevcut ve geçerli değerler olacak olan sabit değerli öznitelikleri oluşturalım:

```Python hl_lines="1  6-9"
{!../../../docs_src/path_params/tutorial005.py!}
```

!!! info "Bilgi"
    3.4 sürümünden beri <a href="https://docs.python.org/3/library/enum.html" class="external-link" target="_blank">enumerationlar (ya da enumlar) Python'da mevcuttur</a>.

!!! tip "İpucu"
    Merak ediyorsanız söyleyeyim, "AlexNet", "ResNet" ve "LeNet" isimleri Makine Öğrenmesi <abbr title="Teknik olarak, Derin Öğrenme model mimarileri">modellerini</abbr> temsil eder.

### Bir *Yol Parametresi* Tanımla

Sonrasında, yarattığımız (`ModelName`) isimli enum sınıfını kullanarak tip belirteci aracılığıyla bir *yol parametresi* oluşturalım:

```Python hl_lines="16"
{!../../../docs_src/path_params/tutorial005.py!}
```

### Dokümana Göz At

*Yol parametresi* için mevcut değerler ön tanımlı olduğundan dolayı, interaktif döküman onları güzel bir şekilde gösterebilir:

<img src="/img/tutorial/path-params/image03.png">

### Python *Enumerationları* ile Çalışmak

*Yol parametresinin* değeri bir *enumeration üyesi* olacaktır.

#### *Enumeration Üyelerini* Karşılaştır

Parametreyi, yarattığınız enum olan `ModelName` içerisindeki *enumeration üyesi* ile karşılaştırabilirsiniz:

```Python hl_lines="17"
{!../../../docs_src/path_params/tutorial005.py!}
```

#### *Enumeration Değerini* Elde Et

`model_name.value` veya genel olarak `your_enum_member.value` tanımlarını kullanarak (bu durumda bir `str` olan) gerçek değere ulaşabilirsiniz:

```Python hl_lines="20"
{!../../../docs_src/path_params/tutorial005.py!}
```

!!! tip "İpucu"
    `"lenet"` değerine `ModelName.lenet.value` tanımı ile de ulaşabilirsiniz.

#### *Enumeration Üyelerini* Döndür

JSON gövdesine (örneğin bir `dict`) gömülü olsalar bile *yol operasyonundaki* *enum üyelerini* döndürebilirsiniz.

Bu üyeler istemciye iletilmeden önce kendilerine karşılık gelen değerlerine (bu durumda string) dönüştürüleceklerdir:

```Python hl_lines="18  21  23"
{!../../../docs_src/path_params/tutorial005.py!}
```

İstemci tarafında şuna benzer bir JSON yanıtı ile karşılaşırsınız:

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## Yol İçeren Yol Parametreleri

Farz edelim ki elinizde `/files/{file_path}` isminde bir *path operasyonu* var.

Fakat `file_path` değerinin `home/johndoe/myfile.txt` gibi bir *yol* barındırmasını istiyorsunuz.

Sonuç olarak, oluşturmak istediğin URL `/files/home/johndoe/myfile.txt` gibi bir şey olacaktır.

### OpenAPI Desteği

Test etmesi ve tanımlaması zor senaryolara sebebiyet vereceğinden dolayı OpenAPI, *yol* barındıran *yol parametrelerini* tanımlayacak bir çözüm sunmuyor.

Buna rağmen, bu durumu, Starlette kütüphanesinin dahili araçlarından birini kullanan **FastAPI**'da gerçekleştirebilirsiniz.

Parametrenin bir yol içermesi gerektiğini belirten herhangi bir doküman eklemememize rağmen dokümanlar yine de çalışacaktır.

### Yol Dönüştürücü

Direkt olarak Starlette kütüphanesinden gelen bir opsiyonu ve aşağıdaki gibi bir URL'yi kullanarak *yol* içeren bir *yol parametresi* tanımlayabilirsiniz:

```
/files/{file_path:path}
```

Bu durumda, parametrenin adı `file_path` olacaktır ve son kısım olan `:path` kısmı, parametrenin herhangi bir *yol* ile eşleşmesi gerektiğini belirtecektir.

Böylece şunun gibi bir kullanım yapabilirsiniz:

```Python hl_lines="6"
{!../../../docs_src/path_params/tutorial004.py!}
```

!!! tip "İpucu"
    Parametrenin `/home/johndoe/myfile.txt` yolunu, baştaki (`/`) işareti ile birlikte kullanmanız gerektiği durumlar olabilir.

    Bu durumda, URL, `files` ile `home` arasında iki eğik çizgiye (`//`) sahip olup `/files//home/johndoe/myfile.txt` gibi gözükecektir.

## Özet

**FastAPI** ile kısa, sezgisel ve standart Python tip tanımlamaları kullanarak şunları elde edersiniz:

* Editör desteği: hata denetimi, otomatik tamamlama, vb.
* Veri "<abbr title="HTTP isteği ile birlikte gelen string'i Python verisine dönüştürme">ayrıştırma</abbr>"
* Veri doğrulama
* API anotasyonları ve otomatik dokümantasyon

Ve sadece, bunları bir kez tanımlamanız yeterli.

Diğer frameworkler ile karşılaştırıldığında (ham performans dışında), üstte anlatılan durum muhtemelen **FastAPI**'ın göze çarpan başlıca avantajıdır.
