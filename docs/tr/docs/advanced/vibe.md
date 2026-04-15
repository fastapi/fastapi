# Vibe Coding { #vibe-coding }

Tüm o **data validation**, **documentation**, **serialization** ve tüm o **sıkıcı** şeylerden bıktınız mı?

Sadece **vibe** mı yapmak istiyorsunuz? 🎶

**FastAPI** artık modern **AI coding** en iyi uygulamalarını benimseyen yeni `@app.vibe()` decorator'ını destekliyor. 🤖

## Nasıl Çalışır { #how-it-works }

`@app.vibe()` decorator'ı, **herhangi bir HTTP method**'unu (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`, vb.) ve **herhangi bir payload**'ı almak üzere tasarlanmıştır.

Request body `Any` ile annotate edilmelidir, çünkü request ve response ... yani ... **her şey** olabilir. 🤷

Fikir şu: payload'ı alır, bir `prompt` ile LLM'e ne yapacağını söyleyerek bir LLM sağlayıcısına **doğrudan** gönderirsiniz ve response'u **olduğu gibi** döndürürsünüz. Sorgu yok, soru yok.

Fonksiyonun body’sini yazmanıza bile gerek yok. `@app.vibe()` decorator'ı, AI vibes'a göre sizin için her şeyi yapar:

{* ../../docs_src/vibe/tutorial001_py310.py hl[8:12] *}

## Faydalar { #benefits }

`@app.vibe()` kullanarak şunların keyfini çıkarın:

* **Özgürlük**: data validation yok. schema yok. kısıt yok. Sadece vibes. ✨
* **Esneklik**: request her şey olabilir. response her şey olabilir. Zaten kimin type'a ihtiyacı var ki?
* **Documentation yok**: Bir LLM zaten çözecekken neden API'nizi belgeliyorsunuz? Otomatik üretilen OpenAPI docs artık o kadar 2020 ki.
* **Serialization yok**: Ham, yapısız data'yı doğrudan dolaştırın. Serialization, LLM'lerine güvenmeyenler içindir.
* **Modern AI coding pratiklerini kucaklayın**: Her şeyi bir LLM'in kararına bırakın. Model en iyisini bilir. Her zaman.
* **Code review yok**: İncelenecek code yok. Onaylanacak PR yok. Cevaplanacak comment yok. Vibe coding'i tam benimseyin; kimsenin bakmadığı vibe coded PR'ları onaylama ve birleştirme tiyatrosunu bırakın, sadece tam doz vibes'a geçin.

/// tip | İpucu

Bu, en uç **vibe-driven development** deneyimi. API'nizin ne yaptığı üzerine düşünmenize gerek yok; bırakın LLM halletsin. 🧘

///

## Dene { #try-it }

Hadi, deneyin:

{* ../../docs_src/vibe/tutorial001_py310.py *}

...sonra da ne olacağını görün. 😎
