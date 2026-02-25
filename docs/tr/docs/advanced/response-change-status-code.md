# Response - Status Code Değiştirme { #response-change-status-code }

Muhtemelen daha önce varsayılan bir [Response Status Code](../tutorial/response-status-code.md){.internal-link target=_blank} ayarlayabileceğinizi okumuşsunuzdur.

Ancak bazı durumlarda, varsayılandan farklı bir status code döndürmeniz gerekir.

## Kullanım senaryosu { #use-case }

Örneğin, varsayılan olarak "OK" `200` HTTP status code'u döndürmek istediğinizi düşünün.

Ama veri mevcut değilse onu oluşturmak ve "CREATED" `201` HTTP status code'u döndürmek istiyorsunuz.

Aynı zamanda, döndürdüğünüz veriyi bir `response_model` ile filtreleyip dönüştürebilmeyi de sürdürmek istiyorsunuz.

Bu tür durumlarda bir `Response` parametresi kullanabilirsiniz.

## Bir `Response` parametresi kullanın { #use-a-response-parameter }

*Path operation function* içinde `Response` tipinde bir parametre tanımlayabilirsiniz (cookie ve header'lar için yapabildiğiniz gibi).

Ardından bu *geçici (temporal)* `Response` nesnesi üzerinde `status_code` değerini ayarlayabilirsiniz.

{* ../../docs_src/response_change_status_code/tutorial001_py310.py hl[1,9,12] *}

Sonrasında, normalde yaptığınız gibi ihtiyacınız olan herhangi bir nesneyi döndürebilirsiniz (`dict`, bir veritabanı modeli, vb.).

Ve eğer bir `response_model` tanımladıysanız, döndürdüğünüz nesneyi filtrelemek ve dönüştürmek için yine kullanılacaktır.

**FastAPI**, status code'u (ayrıca cookie ve header'ları) bu *geçici (temporal)* response'tan alır ve `response_model` ile filtrelenmiş, sizin döndürdüğünüz değeri içeren nihai response'a yerleştirir.

Ayrıca `Response` parametresini dependency'lerde de tanımlayıp status code'u orada ayarlayabilirsiniz. Ancak unutmayın, en son ayarlanan değer geçerli olur.
