# Server-Sent Events (SSE) { #server-sent-events-sse }

İstemciye veri akışını **Server-Sent Events** (SSE) ile sağlayabilirsiniz.

Bu, [JSON Lines Akışı](stream-json-lines.md) ile benzerdir ancak tarayıcılar tarafından yerel olarak desteklenen [`EventSource` API'si](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) ile `text/event-stream` formatını kullanır.

/// info | Bilgi

FastAPI 0.135.0'da eklendi.

///

## Server-Sent Events Nedir? { #what-are-server-sent-events }

SSE, HTTP üzerinden sunucudan istemciye veri akışı için bir standarttır.

Her olay, aralarında boş satırlar bulunan ve `data`, `event`, `id` ve `retry` gibi "alanlar" içeren küçük bir metin bloğudur.

Şuna benzer:

```
data: {"name": "Portal Gun", "price": 999.99}

data: {"name": "Plumbus", "price": 32.99}

```

SSE; yapay zekâ sohbet akışı, canlı bildirimler, log ve gözlemlenebilirlik (observability) gibi senaryolarda ve sunucunun istemciye güncellemeleri ittiği diğer durumlarda yaygın olarak kullanılır.

/// tip | İpucu

İkili (binary) veri akışı yapmak istiyorsanız, gelişmiş kılavuza bakın: [Veri Akışı](../advanced/stream-data.md).

///

## FastAPI ile SSE Akışı { #stream-sse-with-fastapi }

FastAPI ile SSE akışı yapmak için, *path operation function* içinde `yield` kullanın ve `response_class=EventSourceResponse` olarak ayarlayın.

`EventSourceResponse`'u `fastapi.sse` içinden içe aktarın:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[4,22] *}

Yield edilen her öğe JSON olarak kodlanır ve bir SSE olayının `data:` alanında gönderilir.

Dönüş tipini `AsyncIterable[Item]` olarak bildirirseniz, FastAPI bunu Pydantic ile veriyi **doğrulamak**, **belgelemek** ve **serileştirmek** için kullanır.

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[10:12,23] *}

/// tip | İpucu

Pydantic serileştirmeyi **Rust** tarafında yapacağından, dönüş tipi bildirmediğiniz duruma göre çok daha yüksek **performans** elde edersiniz.

///

### Async Olmayan Path Operation Fonksiyonları { #non-async-path-operation-functions }

Normal `def` fonksiyonlarını (yani `async` olmadan) da kullanabilir ve aynı şekilde `yield` kullanabilirsiniz.

FastAPI, event loop'u bloke etmeyecek şekilde doğru biçimde çalışmasını sağlar.

Bu örnekte fonksiyon async olmadığı için doğru dönüş tipi `Iterable[Item]` olur:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[28:31] hl[29] *}

### Dönüş Tipi Olmadan { #no-return-type }

Dönüş tipini belirtmeyebilirsiniz. FastAPI, veriyi dönüştürmek ve göndermek için [`jsonable_encoder`](./encoder.md) kullanır.

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[34:37] hl[35] *}

## `ServerSentEvent` { #serversentevent }

`event`, `id`, `retry` veya `comment` gibi SSE alanlarını ayarlamanız gerekirse, düz veri yerine `ServerSentEvent` nesneleri yield edebilirsiniz.

`ServerSentEvent`'i `fastapi.sse` içinden içe aktarın:

{* ../../docs_src/server_sent_events/tutorial002_py310.py hl[4,26] *}

`data` alanı her zaman JSON olarak kodlanır. Pydantic modelleri dâhil, JSON olarak serileştirilebilen herhangi bir değeri geçebilirsiniz.

## Ham Veri { #raw-data }

Veriyi JSON kodlaması olmadan göndermeniz gerekiyorsa, `data` yerine `raw_data` kullanın.

Bu, önceden biçimlendirilmiş metin, log satırları veya `[DONE]` gibi özel <dfn title="Özel bir koşulu veya durumu belirtmek için kullanılan değer">"işaretçi"</dfn> değerleri göndermek için kullanışlıdır.

{* ../../docs_src/server_sent_events/tutorial003_py310.py hl[17] *}

/// note | Not

`data` ve `raw_data` birbirini dışlar. Her `ServerSentEvent` için bunlardan yalnızca birini ayarlayabilirsiniz.

///

## `Last-Event-ID` ile Devam Etme { #resuming-with-last-event-id }

Bir tarayıcı bağlantı koptuktan sonra yeniden bağlandığında, son aldığı `id`'yi `Last-Event-ID` header'ında gönderir.

Bunu bir header parametresi olarak okuyup, istemcinin kaldığı yerden akışı sürdürmek için kullanabilirsiniz:

{* ../../docs_src/server_sent_events/tutorial004_py310.py hl[25,27,31] *}

## POST ile SSE { #sse-with-post }

SSE, sadece `GET` değil, **tüm HTTP metodlarıyla** çalışır.

Bu, SSE'yi `POST` üzerinden akıtan [MCP](https://modelcontextprotocol.io) gibi protokoller için kullanışlıdır:

{* ../../docs_src/server_sent_events/tutorial005_py310.py hl[14] *}

## Teknik Detaylar { #technical-details }

FastAPI, bazı SSE en iyi uygulamalarını kutudan çıktığı gibi uygular.

- [HTML spesifikasyonu: Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html#authoring-notes) önerisine uygun olarak, bazı proxy'lerin bağlantıyı kapatmasını önlemek için, 15 saniye boyunca hiç mesaj gelmezse **"keep alive" `ping` yorumu** gönderir.
- Akışın **cache'lenmesini önlemek** için `Cache-Control: no-cache` header'ını ayarlar.
- Nginx gibi bazı proxy'lerde **buffering'i önlemek** için özel `X-Accel-Buffering: no` header'ını ayarlar.

Bunun için ekstra bir şey yapmanız gerekmez, doğrudan çalışır. 🤓
