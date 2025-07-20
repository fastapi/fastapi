# Yanıt - Durum Kodunu Değiştirme

Muhtemelen daha önce varsayılan bir [Yanıt Durum Kodu](../tutorial/response-status-code.md){.internal-link target=_blank} belirleyebileceğinizi okumuşsunuzdur.

Ancak bazı durumlarda varsayılan durum kodundan farklı bir durum kodu döndürmeniz gerekebilir.

## Kullanım Senaryosu

Diyelim ki, varsayılan olarak her şeyin yolunda olduğunu belirten `200` HTTP durum kodunu döndürmek istiyorsunuz.

Ancak veri mevcut değilse, onu oluşturmak istiyor ve "Oluşturuldu" anlamına gelen `201` HTTP durum kodunu döndürmek istiyorsunuz.

Ancak yine de döndürdüğünüz verileri bir `response_model` ile filtrelemek ve dönüştürmek istiyorsunuz.

Bu durumlar için bir `Response` parametresi kullanabilirsiniz.

## Bir `Response` Parametresi Kullanın

*yol operasyonu fonksiyonunuzda* `Response` türünde bir parametre belirleyebilirsiniz (çerezler ve headers için yapabileceğiniz gibi).

Ardından *geçici* yanıt nesnesinde `status_code` belirtebilirsiniz.

{* ../../docs_src/response_change_status_code/tutorial001.py hl[1,9,12] *}

Sonunda normalde döndürdüğünüz gibi herhangi bir nesneyi döndürebilirsiniz (bir `dict`, bir veritabanı modeli, vb).

Eğer bir `response_model` belirlediyseniz, döndürdüğünüz nesneyi filtrelemek ve dönüştürmek için kullanılacaktır.

**FastAPI** bu *geçici* yanıtı durum kodunu (ayrıca çerezleri ve headers'ı) çıkarmak için kullanacak ve döndürdüğünüz değeri herhangi bir `response_model` tarafından filtreleyerek son yanıta koyacaktır.

Bağımlılıklarda da `Response` parametresini belirtebilir ve durum kodunu belirleyebilirsiniz. Ancak son belirlenen durum kodu kullanılacaktır.
