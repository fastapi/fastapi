# Yol Parametreleri { #path-parameters }

Python <abbr title="String Biçimleme: Format String">string biçimlemede</abbr> kullanılan sözdizimiyle path "parametreleri"ni veya "değişkenleri"ni tanımlayabilirsiniz:

{* ../../docs_src/path_params/tutorial001_py310.py hl[6:7] *}

Path parametresi `item_id`'nin değeri, fonksiyonunuza `item_id` argümanı olarak aktarılacaktır.

Yani, bu örneği çalıştırıp <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a> adresine giderseniz, şöyle bir response görürsünüz:

```JSON
{"item_id":"foo"}
```

## Tip İçeren Yol Parametreleri { #path-parameters-with-types }

Standart Python tip belirteçlerini kullanarak path parametresinin tipini fonksiyonun içinde tanımlayabilirsiniz:

{* ../../docs_src/path_params/tutorial002_py310.py hl[7] *}

Bu durumda, `item_id` bir `int` olarak tanımlanır.

/// check | Ek bilgi

Bu sayede, fonksiyon içinde hata denetimi, kod tamamlama vb. konularda editör desteğine kavuşursunuz.

///

## Veri <dfn title="diğer adlarıyla: serileştirme, ayrıştırma, marshalling">dönüştürme</dfn> { #data-conversion }

Bu örneği çalıştırıp tarayıcınızda <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a> adresini açarsanız, şöyle bir response görürsünüz:

```JSON
{"item_id":3}
```

/// check | Ek bilgi

Dikkat edin: fonksiyonunuzun aldığı (ve döndürdüğü) değer olan `3`, string `"3"` değil, bir Python `int`'idir.

Yani, bu tip tanımıyla birlikte **FastAPI** size otomatik request "<dfn title="HTTP request'ten gelen string'i Python verisine dönüştürme">ayrıştırma</dfn>" sağlar.

///

## Veri Doğrulama { #data-validation }

Ancak tarayıcınızda <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a> adresine giderseniz, şuna benzer güzel bir HTTP hatası görürsünüz:

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

çünkü path parametresi `item_id`, `int` olmayan `"foo"` değerine sahipti.

Aynı hata, şu örnekte olduğu gibi `int` yerine `float` verirseniz de ortaya çıkar: <a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2</a>

/// check | Ek bilgi

Yani, aynı Python tip tanımıyla birlikte **FastAPI** size veri doğrulama sağlar.

Dikkat edin: hata ayrıca doğrulamanın geçmediği noktayı da açıkça belirtir.

Bu, API'ınızla etkileşime giren kodu geliştirirken ve debug ederken inanılmaz derecede faydalıdır.

///

## Dokümantasyon { #documentation }

Tarayıcınızı <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> adresinde açtığınızda, aşağıdaki gibi otomatik ve interaktif bir API dokümantasyonu görürsünüz:

<img src="/img/tutorial/path-params/image01.png">

/// check | Ek bilgi

Yine, sadece aynı Python tip tanımıyla **FastAPI** size otomatik ve interaktif dokümantasyon (Swagger UI entegrasyonuyla) sağlar.

Dikkat edin: path parametresi integer olarak tanımlanmıştır.

///

## Standartlara Dayalı Avantajlar, Alternatif Dokümantasyon { #standards-based-benefits-alternative-documentation }

Üretilen şema <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md" class="external-link" target="_blank">OpenAPI</a> standardından geldiği için birçok uyumlu araç vardır.

Bu nedenle **FastAPI**'ın kendisi, <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> adresinden erişebileceğiniz alternatif bir API dokümantasyonu (ReDoc kullanarak) sağlar:

<img src="/img/tutorial/path-params/image02.png">

Aynı şekilde, birçok uyumlu araç vardır. Birçok dil için kod üretme araçları da buna dahildir.

## Pydantic { #pydantic }

Tüm veri doğrulamaları, arka planda <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> tarafından gerçekleştirilir; böylece onun tüm avantajlarından faydalanırsınız. Ve emin ellerde olduğunuzu bilirsiniz.

Aynı tip tanımlarını `str`, `float`, `bool` ve daha birçok karmaşık veri tipiyle kullanabilirsiniz.

Bunların birkaçı, eğitimin sonraki bölümlerinde ele alınacaktır.

## Sıralama Önemlidir { #order-matters }

*Path operation*'lar oluştururken sabit bir path'e sahip olduğunuz durumlarla karşılaşabilirsiniz.

Örneğin `/users/me`'nin, geçerli kullanıcı hakkında veri almak için kullanıldığını varsayalım.

Sonra belirli bir kullanıcı hakkında, kullanıcı ID'si ile veri almak için `/users/{user_id}` şeklinde bir path'iniz de olabilir.

*Path operation*'lar sırayla değerlendirildiği için, `/users/me` için olan path'in `/users/{user_id}` olandan önce tanımlandığından emin olmanız gerekir:

{* ../../docs_src/path_params/tutorial003_py310.py hl[6,11] *}

Aksi halde, `/users/{user_id}` için olan path, `"me"` değerini `user_id` parametresi olarak aldığını "düşünerek" `/users/me` için de eşleşir.

Benzer şekilde, bir path operation'ı yeniden tanımlayamazsınız:

{* ../../docs_src/path_params/tutorial003b_py310.py hl[6,11] *}

Path önce eşleştiği için her zaman ilk olan kullanılır.

## Ön Tanımlı Değerler { #predefined-values }

Bir *path operation*'ınız *path parameter* alıyorsa ama olası geçerli *path parameter* değerlerinin önceden tanımlı olmasını istiyorsanız, standart bir Python <abbr title="Enumeration">`Enum`</abbr> kullanabilirsiniz.

### Bir `Enum` Sınıfı Oluşturalım { #create-an-enum-class }

`Enum`'u import edin ve `str` ile `Enum`'dan miras alan bir alt sınıf oluşturun.

`str`'den miras aldığınızda API dokümanları değerlerin `string` tipinde olması gerektiğini anlayabilir ve doğru şekilde render edebilir.

Sonra, kullanılabilir geçerli değerler olacak sabit değerli class attribute'ları oluşturun:

{* ../../docs_src/path_params/tutorial005_py310.py hl[1,6:9] *}

/// tip | İpucu

Merak ediyorsanız: "AlexNet", "ResNet" ve "LeNet", Makine Öğrenmesi <dfn title="Teknik olarak, Derin Öğrenme model mimarileri">modelleri</dfn>nin sadece isimleridir.

///

### Bir *Path Parameter* Tanımlayalım { #declare-a-path-parameter }

Ardından oluşturduğunuz enum sınıfını (`ModelName`) kullanarak tip belirteciyle bir *path parameter* oluşturun:

{* ../../docs_src/path_params/tutorial005_py310.py hl[16] *}

### Dokümana Göz Atalım { #check-the-docs }

*Path parameter* için kullanılabilir değerler ön tanımlı olduğu için, interaktif dokümanlar bunları güzelce gösterebilir:

<img src="/img/tutorial/path-params/image03.png">

### Python *Enumeration*'ları ile Çalışmak { #working-with-python-enumerations }

*Path parameter*'ın değeri bir *enumeration member* olacaktır.

#### *Enumeration Member*'ları Karşılaştıralım { #compare-enumeration-members }

Bunu, oluşturduğunuz enum `ModelName` içindeki *enumeration member* ile karşılaştırabilirsiniz:

{* ../../docs_src/path_params/tutorial005_py310.py hl[17] *}

#### *Enumeration Value*'yu Alalım { #get-the-enumeration-value }

Gerçek değeri (bu durumda bir `str`) `model_name.value` ile veya genel olarak `your_enum_member.value` ile alabilirsiniz:

{* ../../docs_src/path_params/tutorial005_py310.py hl[20] *}

/// tip | İpucu

`"lenet"` değerine `ModelName.lenet.value` ile de erişebilirsiniz.

///

#### *Enumeration Member*'ları Döndürelim { #return-enumeration-members }

*Path operation*'ınızdan, bir JSON body'nin içine gömülü olsalar bile (ör. bir `dict`) *enum member*'ları döndürebilirsiniz.

İstemciye dönmeden önce, karşılık gelen değerlerine (bu durumda string) dönüştürülürler:

{* ../../docs_src/path_params/tutorial005_py310.py hl[18,21,23] *}

İstemcinizde şöyle bir JSON response alırsınız:

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## Path İçeren Path Parametreleri { #path-parameters-containing-paths }

Diyelim ki `/files/{file_path}` path'ine sahip bir *path operation*'ınız var.

Ama `file_path`'in kendisinin `home/johndoe/myfile.txt` gibi bir *path* içermesi gerekiyor.

Böylece, o dosyanın URL'si şu şekilde olur: `/files/home/johndoe/myfile.txt`.

### OpenAPI Desteği { #openapi-support }

OpenAPI, içinde bir *path* barındıracak bir *path parameter* tanımlamak için bir yöntem desteklemez; çünkü bu, test etmesi ve tanımlaması zor senaryolara yol açabilir.

Yine de, Starlette'in dahili araçlarından birini kullanarak bunu **FastAPI**'da yapabilirsiniz.

Ve dokümanlar, parametrenin bir path içermesi gerektiğini söyleyen herhangi bir dokümantasyon eklemese bile çalışmaya devam eder.

### Path Dönüştürücü { #path-convertor }

Starlette'ten doğrudan gelen bir seçenekle, *path* içeren bir *path parameter*'ı şu URL ile tanımlayabilirsiniz:

```
/files/{file_path:path}
```

Bu durumda parametrenin adı `file_path`'tir ve son kısım olan `:path`, parametrenin herhangi bir *path* ile eşleşmesi gerektiğini söyler.

Yani şununla kullanabilirsiniz:

{* ../../docs_src/path_params/tutorial004_py310.py hl[6] *}

/// tip | İpucu

Parametrenin başında `/home/johndoe/myfile.txt` örneğinde olduğu gibi bir eğik çizgi (`/`) ile başlaması gerekebilir.

Bu durumda URL, `files` ile `home` arasında çift eğik çizgi (`//`) olacak şekilde `/files//home/johndoe/myfile.txt` olur.

///

## Özet { #recap }

**FastAPI** ile kısa, sezgisel ve standart Python tip tanımlarını kullanarak şunları elde edersiniz:

* Editör desteği: hata denetimleri, otomatik tamamlama vb.
* Veri "<dfn title="HTTP request'ten gelen string'i Python verisine dönüştürme">ayrıştırma</dfn>"
* Veri doğrulama
* API annotation ve otomatik dokümantasyon

Ve bunları sadece bir kez tanımlamanız yeterlidir.

Bu, (ham performans dışında) **FastAPI**'ın alternatif framework'lere kıyasla muhtemelen en görünür ana avantajıdır.
