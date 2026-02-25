# OpenAPI Callback'leri { #openapi-callbacks }

Başka biri tarafından (muhtemelen API'nizi *kullanacak* olan aynı geliştirici tarafından) oluşturulmuş bir *external API*'ye request tetikleyebilen bir *path operation* ile bir API oluşturabilirsiniz.

API uygulamanızın *external API*'yi çağırdığı sırada gerçekleşen sürece "callback" denir. Çünkü dış geliştiricinin yazdığı yazılım API'nize bir request gönderir ve ardından API'niz *geri çağrı* yaparak (*call back*), bir *external API*'ye request gönderir (muhtemelen aynı geliştiricinin oluşturduğu).

Bu durumda, o external API'nin nasıl görünmesi *gerektiğini* dokümante etmek isteyebilirsiniz. Hangi *path operation*'a sahip olmalı, hangi body'yi beklemeli, hangi response'u döndürmeli, vb.

## Callback'leri olan bir uygulama { #an-app-with-callbacks }

Bunların hepsine bir örnekle bakalım.

Fatura oluşturmayı sağlayan bir uygulama geliştirdiğinizi düşünün.

Bu faturaların `id`, `title` (opsiyonel), `customer` ve `total` alanları olacak.

API'nizin kullanıcısı (external bir geliştirici) API'nizde bir POST request ile fatura oluşturacak.

Sonra API'niz (varsayalım ki):

* Faturayı external geliştiricinin bir müşterisine gönderir.
* Parayı tahsil eder.
* API kullanıcısına (external geliştiriciye) tekrar bir bildirim gönderir.
    * Bu, external geliştiricinin sağladığı bir *external API*'ye (*sizin API'nizden*) bir POST request gönderilerek yapılır (işte bu "callback"tir).

## Normal **FastAPI** uygulaması { #the-normal-fastapi-app }

Önce callback eklemeden önce normal API uygulamasının nasıl görüneceğine bakalım.

Bir `Invoice` body alacak bir *path operation*'ı ve callback için URL'yi taşıyacak `callback_url` adlı bir query parametresi olacak.

Bu kısım oldukça standart; kodun çoğu muhtemelen size zaten tanıdık gelecektir:

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[7:11,34:51] *}

/// tip | İpucu

`callback_url` query parametresi, Pydantic'in <a href="https://docs.pydantic.dev/latest/api/networks/" class="external-link" target="_blank">Url</a> tipini kullanır.

///

Tek yeni şey, *path operation decorator*'ına argüman olarak verilen `callbacks=invoices_callback_router.routes`. Bunun ne olduğuna şimdi bakacağız.

## Callback'i dokümante etmek { #documenting-the-callback }

Callback'in gerçek kodu, büyük ölçüde sizin API uygulamanıza bağlıdır.

Ve bir uygulamadan diğerine oldukça değişebilir.

Sadece bir-iki satır kod bile olabilir, örneğin:

```Python
callback_url = "https://example.com/api/v1/invoices/events/"
httpx.post(callback_url, json={"description": "Invoice paid", "paid": True})
```

Ancak callback'in belki de en önemli kısmı, API'nizin kullanıcısının (external geliştiricinin) *external API*'yi doğru şekilde uyguladığından emin olmaktır; çünkü *sizin API'niz* callback'in request body'sinde belirli veriler gönderecektir, vb.

Dolayısıyla sıradaki adım olarak, *sizin API'nizden* callback almak için o *external API*'nin nasıl görünmesi gerektiğini dokümante eden kodu ekleyeceğiz.

Bu dokümantasyon, API'nizde `/docs` altındaki Swagger UI'da görünecek ve external geliştiricilere *external API*'yi nasıl inşa edeceklerini gösterecek.

Bu örnek callback'in kendisini implemente etmiyor (o zaten tek satır kod olabilir), sadece dokümantasyon kısmını ekliyor.

/// tip | İpucu

Gerçek callback, sadece bir HTTP request'tir.

Callback'i kendiniz implemente ederken <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a> veya <a href="https://requests.readthedocs.io/" class="external-link" target="_blank">Requests</a> gibi bir şey kullanabilirsiniz.

///

## Callback dokümantasyon kodunu yazın { #write-the-callback-documentation-code }

Bu kod uygulamanızda çalıştırılmayacak; sadece o *external API*'nin nasıl görünmesi gerektiğini *dokümante etmek* için gerekiyor.

Ancak **FastAPI** ile bir API için otomatik dokümantasyonu kolayca nasıl üreteceğinizi zaten biliyorsunuz.

O halde aynı bilgiyi kullanarak, *external API*'nin nasıl görünmesi gerektiğini dokümante edeceğiz... external API'nin implemente etmesi gereken *path operation*'ları oluşturarak (API'nizin çağıracağı olanlar).

/// tip | İpucu

Bir callback'i dokümante eden kodu yazarken, kendinizi *external geliştirici* olarak hayal etmek faydalı olabilir. Ve şu anda *sizin API'nizi* değil, *external API*'yi implemente ettiğinizi düşünün.

Bu bakış açısını (external geliştiricinin bakış açısını) geçici olarak benimsemek; parametreleri nereye koyacağınızı, body için Pydantic modelini, response için modelini vb. external API tarafında nasıl tasarlayacağınızı daha net hale getirebilir.

///

### Bir callback `APIRouter` oluşturun { #create-a-callback-apirouter }

Önce bir veya daha fazla callback içerecek yeni bir `APIRouter` oluşturun.

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[1,23] *}

### Callback *path operation*'ını oluşturun { #create-the-callback-path-operation }

Callback *path operation*'ını oluşturmak için, yukarıda oluşturduğunuz aynı `APIRouter`'ı kullanın.

Normal bir FastAPI *path operation*'ı gibi görünmelidir:

* Muhtemelen alması gereken body'nin bir deklarasyonu olmalı, örn. `body: InvoiceEvent`.
* Ayrıca döndürmesi gereken response'un deklarasyonu da olabilir, örn. `response_model=InvoiceEventReceived`.

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[14:16,19:20,26:30] *}

Normal bir *path operation*'dan 2 temel farkı vardır:

* Gerçek bir koda ihtiyaç duymaz; çünkü uygulamanız bu kodu asla çağırmayacak. Bu yalnızca *external API*'yi dokümante etmek için kullanılır. Yani fonksiyon sadece `pass` içerebilir.
* *path*, bir <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression" class="external-link" target="_blank">OpenAPI 3 expression</a> (aşağıda daha fazlası) içerebilir; böylece parametreler ve *sizin API'nize* gönderilen orijinal request'in bazı parçalarıyla değişkenler kullanılabilir.

### Callback path ifadesi { #the-callback-path-expression }

Callback *path*'i, *sizin API'nize* gönderilen orijinal request'in bazı parçalarını içerebilen bir <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression" class="external-link" target="_blank">OpenAPI 3 expression</a> barındırabilir.

Bu örnekte, bu bir `str`:

```Python
"{$callback_url}/invoices/{$request.body.id}"
```

Yani API'nizin kullanıcısı (external geliştirici) *sizin API'nize* şu adrese bir request gönderirse:

```
https://yourapi.com/invoices/?callback_url=https://www.external.org/events
```

ve JSON body şu şekilde olursa:

```JSON
{
    "id": "2expen51ve",
    "customer": "Mr. Richie Rich",
    "total": "9999"
}
```

o zaman *sizin API'niz* faturayı işleyecek ve daha sonra bir noktada `callback_url`'ye (yani *external API*'ye) bir callback request gönderecek:

```
https://www.external.org/events/invoices/2expen51ve
```

ve JSON body yaklaşık şöyle bir şey içerecek:

```JSON
{
    "description": "Payment celebration",
    "paid": true
}
```

ve o *external API*'den şu gibi bir JSON body içeren response bekleyecek:

```JSON
{
    "ok": true
}
```

/// tip | İpucu

Callback URL'sinin, `callback_url` içindeki query parametresi olarak alınan URL'yi (`https://www.external.org/events`) ve ayrıca JSON body'nin içindeki fatura `id`'sini (`2expen51ve`) birlikte kullandığına dikkat edin.

///

### Callback router'ını ekleyin { #add-the-callback-router }

Bu noktada, yukarıda oluşturduğunuz callback router'ında gerekli callback *path operation*'ları (external geliştiricinin *external API*'de implemente etmesi gerekenler) hazır.

Şimdi *sizin API'nizin path operation decorator*'ında `callbacks` parametresini kullanarak, callback router'ının `.routes` attribute'unu (bu aslında route/*path operation*'lardan oluşan bir `list`) geçin:

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[33] *}

/// tip | İpucu

`callback=` içine router'ın kendisini (`invoices_callback_router`) değil, `invoices_callback_router.routes` şeklinde `.routes` attribute'unu verdiğinize dikkat edin.

///

### Dokümanları kontrol edin { #check-the-docs }

Artık uygulamanızı başlatıp <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> adresine gidebilirsiniz.

*Path operation*'ınız için, *external API*'nin nasıl görünmesi gerektiğini gösteren bir "Callbacks" bölümünü içeren dokümanları göreceksiniz:

<img src="/img/tutorial/openapi-callbacks/image01.png">
