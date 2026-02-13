# WebSockets { #websockets }

**FastAPI** ile <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API" class="external-link" target="_blank">WebSockets</a> kullanabilirsiniz.

## `websockets` Kurulumu { #install-websockets }

Bir [virtual environment](../virtual-environments.md){.internal-link target=_blank} oluşturduğunuzdan, onu aktive ettiğinizden ve `websockets`'i ("WebSocket" protokolünü kullanmayı kolaylaştıran bir Python kütüphanesi) kurduğunuzdan emin olun:

<div class="termy">

```console
$ pip install websockets

---> 100%
```

</div>

## WebSockets client { #websockets-client }

### Production'da { #in-production }

Production sisteminizde muhtemelen React, Vue.js veya Angular gibi modern bir framework ile oluşturulmuş bir frontend vardır.

WebSockets kullanarak backend'inizle iletişim kurmak için de büyük ihtimalle frontend'inizin sağladığı yardımcı araçları kullanırsınız.

Ya da native kod ile doğrudan WebSocket backend'inizle iletişim kuran native bir mobil uygulamanız olabilir.

Veya WebSocket endpoint'i ile iletişim kurmak için başka herhangi bir yönteminizi de kullanıyor olabilirsiniz.

---

Ancak bu örnek için, tamamı uzun bir string içinde olacak şekilde biraz JavaScript içeren çok basit bir HTML dokümanı kullanacağız.

Elbette bu optimal değil ve production için kullanmazsınız.

Production'da yukarıdaki seçeneklerden birini kullanırsınız.

Ama WebSockets'in server tarafına odaklanmak ve çalışan bir örnek görmek için en basit yol bu:

{* ../../docs_src/websockets/tutorial001_py310.py hl[2,6:38,41:43] *}

## Bir `websocket` Oluşturun { #create-a-websocket }

**FastAPI** uygulamanızda bir `websocket` oluşturun:

{* ../../docs_src/websockets/tutorial001_py310.py hl[1,46:47] *}

/// note | Teknik Detaylar

`from starlette.websockets import WebSocket` da kullanabilirsiniz.

**FastAPI**, geliştirici olarak işinizi kolaylaştırmak için aynı `WebSocket`'i doğrudan sağlar. Ancak aslında doğrudan Starlette'ten gelir.

///

## Mesajları `await` Edin ve Mesaj Gönderin { #await-for-messages-and-send-messages }

WebSocket route'unuzda mesajları `await` edebilir ve mesaj gönderebilirsiniz.

{* ../../docs_src/websockets/tutorial001_py310.py hl[48:52] *}

Binary, text ve JSON verisi alıp gönderebilirsiniz.

## Deneyin { #try-it }

Dosyanızın adı `main.py` ise uygulamanızı şu şekilde çalıştırın:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Tarayıcınızda <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a> adresini açın.

Şuna benzer basit bir sayfa göreceksiniz:

<img src="/img/tutorial/websockets/image01.png">

Input kutusuna mesaj yazıp gönderebilirsiniz:

<img src="/img/tutorial/websockets/image02.png">

Ve WebSockets kullanan **FastAPI** uygulamanız yanıt döndürecektir:

<img src="/img/tutorial/websockets/image03.png">

Birçok mesaj gönderebilir (ve alabilirsiniz):

<img src="/img/tutorial/websockets/image04.png">

Ve hepsinde aynı WebSocket bağlantısı kullanılacaktır.

## `Depends` ve Diğerlerini Kullanma { #using-depends-and-others }

WebSocket endpoint'lerinde `fastapi` içinden import edip şunları kullanabilirsiniz:

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

Diğer FastAPI endpoint'leri/*path operations* ile aynı şekilde çalışırlar:

{* ../../docs_src/websockets/tutorial002_an_py310.py hl[68:69,82] *}

/// info | Bilgi

Bu bir WebSocket olduğu için `HTTPException` raise etmek pek anlamlı değildir; bunun yerine `WebSocketException` raise ederiz.

<a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">Spesifikasyonda tanımlanan geçerli kodlar</a> arasından bir kapatma kodu kullanabilirsiniz.

///

### Dependency'lerle WebSockets'i Deneyin { #try-the-websockets-with-dependencies }

Dosyanızın adı `main.py` ise uygulamanızı şu şekilde çalıştırın:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Tarayıcınızda <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a> adresini açın.

Burada şunları ayarlayabilirsiniz:

* path'te kullanılan "Item ID".
* query parametresi olarak kullanılan "Token".

/// tip | İpucu

query'deki `token` değerinin bir dependency tarafından ele alınacağına dikkat edin.

///

Bununla WebSocket'e bağlanabilir, ardından mesaj gönderip alabilirsiniz:

<img src="/img/tutorial/websockets/image05.png">

## Bağlantı Kopmalarını ve Birden Fazla Client'ı Yönetme { #handling-disconnections-and-multiple-clients }

Bir WebSocket bağlantısı kapandığında, `await websocket.receive_text()` bir `WebSocketDisconnect` exception'ı raise eder; ardından bunu bu örnekteki gibi yakalayıp (catch) yönetebilirsiniz.

{* ../../docs_src/websockets/tutorial003_py310.py hl[79:81] *}

Denemek için:

* Uygulamayı birden fazla tarayıcı sekmesiyle açın.
* Bu sekmelerden mesaj yazın.
* Sonra sekmelerden birini kapatın.

Bu, `WebSocketDisconnect` exception'ını raise eder ve diğer tüm client'lar şuna benzer bir mesaj alır:

```
Client #1596980209979 left the chat
```

/// tip | İpucu

Yukarıdaki uygulama, birden fazla WebSocket bağlantısına mesajları nasıl yönetip broadcast edeceğinizi göstermek için minimal ve basit bir örnektir.

Ancak her şey memory'de, tek bir list içinde yönetildiği için yalnızca process çalıştığı sürece ve yalnızca tek bir process ile çalışacaktır.

FastAPI ile kolay entegre olan ama Redis, PostgreSQL vb. tarafından desteklenen daha sağlam bir şeye ihtiyacınız varsa <a href="https://github.com/encode/broadcaster" class="external-link" target="_blank">encode/broadcaster</a>'a göz atın.

///

## Daha Fazla Bilgi { #more-info }

Seçenekler hakkında daha fazlasını öğrenmek için Starlette dokümantasyonunda şunlara bakın:

* <a href="https://www.starlette.dev/websockets/" class="external-link" target="_blank">`WebSocket` class'ı</a>.
* <a href="https://www.starlette.dev/endpoints/#websocketendpoint" class="external-link" target="_blank">Class tabanlı WebSocket yönetimi</a>.
