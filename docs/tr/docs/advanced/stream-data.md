# Veri Akışı { #stream-data }

Veriyi JSON olarak yapılandırabiliyorsanız, [JSON Lines Akışı](../tutorial/stream-json-lines.md) kullanın.

Ancak saf ikili (binary) veri ya da string akıtmak istiyorsanız, bunu şöyle yapabilirsiniz.

/// info | Bilgi

FastAPI 0.134.0 ile eklendi.

///

## Kullanım Senaryoları { #use-cases }

Doğrudan bir AI LLM (Büyük Dil Modeli) servisinin çıktısından saf string'leri akıtmak istediğinizde kullanabilirsiniz.

Ayrıca **büyük ikili (binary) dosyaları** akıtmak için de kullanabilirsiniz; veriyi okurken her parçayı (chunk) sırayla gönderirsiniz, tamamını belleğe almak zorunda kalmazsınız.

Bu şekilde **video** veya **ses** de akıtabilirsiniz; hatta işledikçe üretilip gönderilebilir.

## `yield` ile bir `StreamingResponse` { #a-streamingresponse-with-yield }

*Path operation function* içinde `response_class=StreamingResponse` belirtirseniz, her veri parçasını sırayla göndermek için `yield` kullanabilirsiniz.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[1:23] hl[20,23] *}

FastAPI her veri parçasını olduğu gibi `StreamingResponse`'a verir; JSON'a ya da benzeri bir formata dönüştürmeye çalışmaz.

### Async Olmayan Path Operation Function'lar { #non-async-path-operation-functions }

Normal `def` fonksiyonlarını (yani `async` olmadan) da kullanabilir ve aynı şekilde `yield` yazabilirsiniz.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[26:29] hl[27] *}

### Tip Annotasyonu Yok { #no-annotation }

İkili (binary) veri akıtıyorsanız dönüş tipi annotasyonu belirtmeniz şart değildir.

FastAPI veriyi Pydantic ile JSON'a çevirmeye veya herhangi bir şekilde serileştirmeye çalışmayacağı için, bu durumda tip annotasyonu sadece editörünüz ve araçlarınız içindir; FastAPI tarafından kullanılmaz.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[32:35] hl[33] *}

Bu aynı zamanda `StreamingResponse` ile veriyi tam olarak ihtiyaç duyduğunuz biçimde üretme ve encode etme konusunda hem bir özgürlük hem de bir sorumluluk verdiği anlamına gelir; tip annotasyonlarından bağımsızdır. 🤓

### Bytes Akışı { #stream-bytes }

Başlıca kullanım senaryolarından biri string yerine `bytes` akıtmaktır; elbette bunu yapabilirsiniz.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[44:47] hl[47] *}

## Özel bir `PNGStreamingResponse` { #a-custom-pngstreamingresponse }

Yukarıdaki örneklerde veri baytları akıtıldı, ancak response'ta bir `Content-Type` header'ı yoktu; bu nedenle istemci hangi tür veriyi aldığını bilmiyordu.

Akıttığınız veri türüne uygun `Content-Type` header'ını ayarlayan, `StreamingResponse`'tan türetilmiş özel bir alt sınıf (subclass) oluşturabilirsiniz.

Örneğin, `media_type` özniteliğini kullanarak `Content-Type` header'ını `image/png` olarak ayarlayan bir `PNGStreamingResponse` oluşturabilirsiniz:

{* ../../docs_src/stream_data/tutorial002_py310.py ln[6,19:20] hl[20] *}

Ardından bu yeni sınıfı *path operation function* içinde `response_class=PNGStreamingResponse` olarak kullanabilirsiniz:

{* ../../docs_src/stream_data/tutorial002_py310.py ln[23:27] hl[23] *}

### Bir Dosyayı Simüle Etme { #simulate-a-file }

Bu örnekte, yalnızca bellekte yaşayan ama aynı arayüzü kullanmamıza izin veren, dosya benzeri bir nesne olan `io.BytesIO` ile bir dosyayı simüle ediyoruz.

Örneğin, bir dosyada yapabileceğimiz gibi, içeriğini tüketmek için üzerinde iterate edebiliriz.

{* ../../docs_src/stream_data/tutorial002_py310.py ln[1:27] hl[3,12:13,25] *}

/// note | Teknik Detaylar

Diğer iki değişken olan `image_base64` ve `binary_image`, Base64 ile encode edilmiş bir görüntüdür; daha sonra bayt'lara çevrilip `io.BytesIO`'ya aktarılır.

Sadece bu örnek aynı dosyada yaşayabilsin, kopyalayıp olduğu gibi çalıştırabilesiniz diye. 🥚

///

`with` bloğu kullanarak, jeneratör fonksiyonu (içinde `yield` olan fonksiyon) tamamlandığında dosya benzeri nesnenin kapandığından emin oluruz. Yani response gönderimi bittikten sonra.

Bu özel örnekte o kadar da önemli değil, çünkü sahte ve bellekte (yani `io.BytesIO` ile). Ancak gerçek bir dosyada, onunla işiniz bittiğinde dosyanın kapandığından emin olmak önemlidir.

### Dosyalar ve Async { #files-and-async }

Çoğu durumda dosya benzeri nesneler, varsayılan olarak async ve await ile uyumlu değildir.

Örneğin, `await file.read()` ya da `async for chunk in file` gibi şeyler yoktur.

Ve birçok durumda, diskte ya da ağda okundukları için, okumak engelleyici (event loop'u bloke edebilen) bir işlem olabilir.

/// info | Bilgi

Yukarıdaki örnek aslında bir istisna; çünkü `io.BytesIO` nesnesi zaten bellekte, dolayısıyla onu okumak hiçbir şeyi bloke etmez.

Ancak çoğu durumda bir dosyayı veya dosya benzeri bir nesneyi okumak bloke edicidir.

///

Event loop'u bloke etmemek için, *path operation function*'ı `async def` yerine normal `def` ile tanımlayabilirsiniz; böylece FastAPI ana döngüyü bloke etmemek için bunu bir thread pool worker (iş parçacığı havuzu çalışanı) üzerinde çalıştırır.

{* ../../docs_src/stream_data/tutorial002_py310.py ln[30:34] hl[31] *}

/// tip | İpucu

Async bir fonksiyonun içinden bloklayıcı kod çağırmanız ya da bloklayıcı bir fonksiyonun içinden async bir fonksiyon çağırmanız gerekirse, FastAPI'nin kardeş kütüphanesi olan [Asyncer](https://asyncer.tiangolo.com)'ı kullanabilirsiniz.

///

### `yield from` { #yield-from }

Bir şeyin (ör. dosya benzeri bir nesne) üzerinde iterate ederken, her öğe için `yield` yapıyorsanız, `for` döngüsünü yazmak yerine `yield from` ile her öğeyi doğrudan yield edebilirsiniz.

Bu FastAPI'ye özgü değildir, tamamen Python'dur, ama bilinmesi güzel bir püf noktasıdır. 😎

{* ../../docs_src/stream_data/tutorial002_py310.py ln[37:40] hl[40] *}
