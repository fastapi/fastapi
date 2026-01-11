# Yol Parametreleri { #path-parameters }

Yol "parametrelerini" veya "değişkenlerini" Python <abbr title="String Biçimleme: Format String">string biçimlemede</abbr> kullanılan sözdizimi ile tanımlayabilirsiniz.

{* ../../docs_src/path_params/tutorial001_py39.py hl[6:7] *}

Yol parametresi olan `item_id`'nin değeri, fonksiyonunuza `item_id` argümanı olarak aktarılacaktır.

Eğer bu örneği çalıştırıp <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a> sayfasına giderseniz, şöyle bir çıktı ile karşılaşırsınız:

```JSON
{"item_id":"foo"}
```

## Tip İçeren Yol Parametreleri { #path-parameters-with-types }

Standart Python tip belirteçlerini kullanarak yol parametresinin tipini fonksiyonun içerisinde tanımlayabilirsiniz.

{* ../../docs_src/path_params/tutorial002_py39.py hl[7] *}

Bu durumda, `item_id` bir `int` olarak tanımlanacaktır.

/// check | Ek bilgi

Bu sayede, fonksiyon içerisinde hata denetimi, kod tamamlama gibi konularda editör desteğine kavuşacaksınız.

///

## Veri <abbr title="ayrıca şu isimlerle de bilinir: serialization, parsing, marshalling">dönüşümü</abbr> { #data-conversion }

Eğer bu örneği çalıştırıp tarayıcınızda <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a> sayfasını açarsanız, şöyle bir yanıt ile karşılaşırsınız:

```JSON
{"item_id":3}
```

/// check | Ek bilgi

Dikkatinizi çekerim ki, fonksiyonunuzun aldığı (ve döndürdüğü) değer olan `3` bir string `"3"` değil aksine bir Python `int`'idir.

Bu tanımlamayla birlikte, **FastAPI** size otomatik istek <abbr title="HTTP request'i ile birlikte gelen string'i Python verisine dönüştürme">"parsing"</abbr> özelliği sağlar.

///

## Veri Doğrulama { #data-validation }

Eğer tarayıcınızda <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a> sayfasını açarsanız, şuna benzer güzel bir HTTP hatası ile karşılaşırsınız:

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
      "input": "foo"
    }
  ]
}
```

Çünkü burada `item_id` yol parametresi `"foo"` değerini almıştı, ki bu bir `int` değildir.

Aynı hata <a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2</a> sayfasında olduğu gibi `int` yerine `float` bir değer verseydik de ortaya çıkardı.

/// check | Ek bilgi

Böylece, aynı Python tip tanımlaması ile birlikte, **FastAPI** veri doğrulama özelliği sağlar.

Dikkatinizi çekerim ki, karşılaştığınız hata, doğrulamanın geçersiz olduğu mutlak noktayı da açık bir şekilde belirtiyor.

Bu özellik, API'ınızla iletişime geçen kodu geliştirirken ve ayıklarken inanılmaz derecede yararlı olacaktır.

///

## Dokümantasyon { #documentation }

Ayrıca, tarayıcınızı <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> adresinde açarsanız, aşağıdaki gibi otomatik ve interaktif bir API dokümantasyonu ile karşılaşırsınız:

<img src="/img/tutorial/path-params/image01.png">

/// check | Ek bilgi

Üstelik, sadece aynı Python tip tanımlaması ile, **FastAPI** size otomatik ve interaktif (Swagger UI ile entegre) bir dokümantasyon sağlar.

Dikkatinizi çekerim ki, yol parametresi integer olarak tanımlanmıştır.

///

## Standartlara Dayalı Avantajlar, Alternatif Dokümantasyon { #standards-based-benefits-alternative-documentation }

Oluşturulan şema <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md" class="external-link" target="_blank">OpenAPI</a> standardına uygun olduğu için birçok uyumlu araç mevcuttur.

Bu sayede, **FastAPI**'ın bizzat kendisi <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> sayfasından erişebileceğiniz alternatif (ReDoc kullanan) bir API dokümantasyonu sağlar:

<img src="/img/tutorial/path-params/image02.png">

Aynı şekilde, farklı diller için kod türetme araçları da dahil olmak üzere çok sayıda uyumlu araç bulunur.

## Pydantic { #pydantic }

Tüm veri doğrulamaları <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> tarafından arka planda gerçekleştirilir, bu sayede tüm avantajlardan faydalanabilirsiniz. Böylece, emin ellerde olduğunuzu hissedebilirsiniz.

Aynı tip tanımlamalarını `str`, `float`, `bool` ve diğer karmaşık veri tipleri ile kullanma imkanınız vardır.

Bunlardan birkaçı, bu eğitimin ileriki bölümlerinde irdelenmiştir.

## Sıralama Önem Arz Eder { #order-matters }

*Yol operasyonları* tasarlarken sabit yol barındıran durumlar ile karşılaşabilirsiniz.

Farz edelim ki `/users/me` yolu geçerli kullanıcı hakkında bilgi almak için kullanılıyor olsun.

Benzer şekilde `/users/{user_id}` gibi tanımlanmış ve belirli bir kullanıcı hakkında veri almak için kullanıcının ID bilgisini kullanan bir yolunuz da mevcut olabilir.

*Yol operasyonları* sıralı bir şekilde gözden geçirildiğinden dolayı `/users/me` yolunun `/users/{user_id}` yolundan önce tanımlanmış olmasından emin olmanız gerekmektedir:

{* ../../docs_src/path_params/tutorial003_py39.py hl[6,11] *}

Aksi halde, `/users/{user_id}` yolu `"me"` değerinin `user_id` parametresi için gönderildiğini "düşünerek" `/users/me` ile de eşleşir.

Benzer şekilde, bir yol operasyonunu yeniden tanımlamanız mümkün değildir:

{* ../../docs_src/path_params/tutorial003b_py39.py hl[6,11] *}

Yol, ilk kısım ile eşleştiğinden dolayı her koşulda ilk yol operasyonu kullanılacaktır.

## Ön Tanımlı Değerler { #predefined-values }

Eğer *yol parametresi* alan bir *yol operasyonunuz* varsa ve alabileceği *yol parametresi* değerlerinin ön tanımlı olmasını istiyorsanız, standart Python <abbr title="Enumeration">`Enum`</abbr> tipini kullanabilirsiniz.

### Bir `Enum` Sınıfı Oluşturalım { #create-an-enum-class }

`Enum` sınıfını projemize dahil edip `str` ile `Enum` sınıflarını miras alan bir alt sınıf yaratalım.

`str` sınıfı miras alındığından dolayı, API dokümanı, değerlerin `string` tipinde olması gerektiğini anlayabilecek ve doğru bir şekilde işlenecektir.

Sonrasında, sınıf içerisinde, mevcut ve geçerli değerler olacak olan sabit değerli özelliklerini oluşturalım:

{* ../../docs_src/path_params/tutorial005_py39.py hl[1,6:9] *}

/// tip | İpucu

Merak ediyorsanız söyleyeyim, "AlexNet", "ResNet" ve "LeNet" isimleri Makine Öğrenmesi <abbr title="Teknik olarak, Derin Öğrenme model mimarileri">modellerini</abbr> temsil eder.

///

### Bir *Yol Parametresi* Tanımlayalım { #declare-a-path-parameter }

Sonrasında, yarattığımız enum sınıfını (`ModelName`) kullanarak tip belirteci aracılığıyla bir *yol parametresi* oluşturalım:

{* ../../docs_src/path_params/tutorial005_py39.py hl[16] *}

### Dokümana Göz Atalım { #check-the-docs }

*Yol parametresi* için mevcut değerler ön tanımlı olduğundan dolayı, interaktif döküman onları güzel bir şekilde gösterebilir:

<img src="/img/tutorial/path-params/image03.png">

### Python *Enumerationları* ile Çalışmak { #working-with-python-enumerations }

*Yol parametresinin* değeri bir *enumeration üyesi* olacaktır.

#### *Enumeration Üyelerini* Karşılaştıralım { #compare-enumeration-members }

Parametreyi, yarattığınız enum olan `ModelName` içerisindeki *enumeration üyesi* ile karşılaştırabilirsiniz:

{* ../../docs_src/path_params/tutorial005_py39.py hl[17] *}

#### *Enumeration Değerini* Edinelim { #get-the-enumeration-value }

`model_name.value` veya genel olarak `your_enum_member.value` tanımlarını kullanarak (bu durumda bir `str` olan) gerçek değere ulaşabilirsiniz:

{* ../../docs_src/path_params/tutorial005_py39.py hl[20] *}

/// tip | İpucu

`"lenet"` değerine `ModelName.lenet.value` tanımı ile de ulaşabilirsiniz.

///

#### *Enumeration Üyelerini* Döndürelim { #return-enumeration-members }

JSON gövdesine (örneğin bir `dict`) gömülü olsalar bile *yol operasyonundaki* *enum üyelerini* döndürebilirsiniz.

Bu üyeler istemciye iletilmeden önce kendilerine karşılık gelen değerlerine (bu durumda string) dönüştürüleceklerdir:

{* ../../docs_src/path_params/tutorial005_py39.py hl[18,21,23] *}

İstemci tarafında şuna benzer bir JSON yanıtı ile karşılaşırsınız:

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## Yol İçeren Yol Parametreleri { #path-parameters-containing-paths }

Farz edelim ki elinizde `/files/{file_path}` isminde bir *yol operasyonu* var.

Fakat `file_path` değerinin `home/johndoe/myfile.txt` gibi bir *yol* barındırmasını istiyorsunuz.

Sonuç olarak, oluşturmak istediğin URL `/files/home/johndoe/myfile.txt` gibi bir şey olacaktır.

### OpenAPI Desteği { #openapi-support }

Test etmesi ve tanımlaması zor senaryolara sebebiyet vereceğinden dolayı OpenAPI, *yol* barındıran *yol parametrelerini* tanımlayacak bir çözüm sunmuyor.

Ancak bunu, Starlette kütüphanesinin dahili araçlarından birini kullanarak **FastAPI**'da gerçekleştirebilirsiniz.

Parametrenin bir yol içermesi gerektiğini belirten herhangi bir doküman eklemememize rağmen dokümanlar yine de çalışacaktır.

### Yol Dönüştürücü { #path-convertor }

Direkt olarak Starlette kütüphanesinden gelen bir opsiyon sayesinde aşağıdaki gibi *yol* içeren bir *yol parametresi* bağlantısı tanımlayabilirsiniz:

```
/files/{file_path:path}
```

Bu durumda, parametrenin adı `file_path` olacaktır ve son kısım olan `:path` kısmı, parametrenin herhangi bir *yol* ile eşleşmesi gerektiğini belirtecektir.

Böylece şunun gibi bir kullanım yapabilirsiniz:

{* ../../docs_src/path_params/tutorial004_py39.py hl[6] *}

/// tip | İpucu

Parametrenin `/home/johndoe/myfile.txt` olacak şekilde, başında eğik çizgi (`/`) ile başlaması gerekebilir.

Bu durumda, URL, `files` ile `home` arasında iki eğik çizgiye (`//`) sahip olup `/files//home/johndoe/myfile.txt` gibi gözükecektir.

///

## Özet { #recap }

**FastAPI** ile kısa, sezgisel ve standart Python tip tanımlamaları kullanarak şunları elde edersiniz:

* Editör desteği: hata denetimi, otomatik tamamlama, vb.
* Veri "<abbr title="HTTP request'i ile birlikte gelen string'i Python verisine dönüştürme">parsing</abbr>"
* Veri doğrulama
* API annotation'ı ve otomatik dokümantasyon

Ve sadece, bunları bir kez tanımlamanız yeterli.

Diğer frameworkler ile karşılaştırıldığında (ham performans dışında), üstte anlatılan durum muhtemelen **FastAPI**'ın göze çarpan başlıca avantajıdır.
