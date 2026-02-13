# Dataclass Kullanımı { #using-dataclasses }

FastAPI, **Pydantic** üzerine inşa edilmiştir ve request/response tanımlamak için Pydantic model'lerini nasıl kullanacağınızı gösteriyordum.

Ancak FastAPI, <a href="https://docs.python.org/3/library/dataclasses.html" class="external-link" target="_blank">`dataclasses`</a> kullanmayı da aynı şekilde destekler:

{* ../../docs_src/dataclasses_/tutorial001_py310.py hl[1,6:11,18:19] *}

Bu destek hâlâ **Pydantic** sayesinde vardır; çünkü Pydantic, <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/#use-of-stdlib-dataclasses-with-basemodel" class="external-link" target="_blank">`dataclasses` için dahili destek</a> sunar.

Yani yukarıdaki kod Pydantic'i doğrudan kullanmasa bile, FastAPI bu standart dataclass'ları Pydantic'in kendi dataclass biçimine dönüştürmek için Pydantic'i kullanmaktadır.

Ve elbette aynı özellikleri destekler:

* veri doğrulama (data validation)
* veri serileştirme (data serialization)
* veri dokümantasyonu (data documentation), vb.

Bu, Pydantic model'lerinde olduğu gibi çalışır. Aslında arka planda da aynı şekilde, Pydantic kullanılarak yapılır.

/// info | Bilgi

Dataclass'ların, Pydantic model'lerinin yapabildiği her şeyi yapamadığını unutmayın.

Bu yüzden yine de Pydantic model'lerini kullanmanız gerekebilir.

Ancak elinizde zaten bir sürü dataclass varsa, bunları FastAPI ile bir web API'yi beslemek için kullanmak güzel bir numaradır. 🤓

///

## `response_model` İçinde Dataclass'lar { #dataclasses-in-response-model }

`response_model` parametresinde `dataclasses` da kullanabilirsiniz:

{* ../../docs_src/dataclasses_/tutorial002_py310.py hl[1,6:12,18] *}

Dataclass otomatik olarak bir Pydantic dataclass'ına dönüştürülür.

Bu sayede şeması API docs kullanıcı arayüzünde görünür:

<img src="/img/tutorial/dataclasses/image01.png">

## İç İçe Veri Yapılarında Dataclass'lar { #dataclasses-in-nested-data-structures }

İç içe veri yapıları oluşturmak için `dataclasses` ile diğer type annotation'ları da birleştirebilirsiniz.

Bazı durumlarda yine de Pydantic'in `dataclasses` sürümünü kullanmanız gerekebilir. Örneğin, otomatik oluşturulan API dokümantasyonunda hata alıyorsanız.

Bu durumda standart `dataclasses` yerine, drop-in replacement olan `pydantic.dataclasses` kullanabilirsiniz:

{* ../../docs_src/dataclasses_/tutorial003_py310.py hl[1,4,7:10,13:16,22:24,27] *}

1. `field` hâlâ standart `dataclasses` içinden import edilir.

2. `pydantic.dataclasses`, `dataclasses` için bir drop-in replacement'tır.

3. `Author` dataclass'ı, `Item` dataclass'larından oluşan bir liste içerir.

4. `Author` dataclass'ı, `response_model` parametresi olarak kullanılır.

5. Request body olarak dataclass'larla birlikte diğer standart type annotation'ları da kullanabilirsiniz.

    Bu örnekte, `Item` dataclass'larından oluşan bir listedir.

6. Burada `items` içeren bir dictionary döndürüyoruz; `items` bir dataclass listesi.

    FastAPI, veriyi JSON'a <dfn title="veriyi aktarılabilir bir formata dönüştürme">serileştirme</dfn>yi yine başarır.

7. Burada `response_model`, `Author` dataclass'larından oluşan bir listenin type annotation'ını kullanıyor.

    Yine `dataclasses` ile standart type annotation'ları birleştirebilirsiniz.

8. Bu *path operation function*, `async def` yerine normal `def` kullanıyor.

    Her zaman olduğu gibi, FastAPI'de ihtiyaca göre `def` ve `async def`’i birlikte kullanabilirsiniz.

    Hangisini ne zaman kullanmanız gerektiğine dair hızlı bir hatırlatma isterseniz, [`async` ve `await`](../async.md#in-a-hurry){.internal-link target=_blank} dokümanındaki _"In a hurry?"_ bölümüne bakın.

9. Bu *path operation function* dataclass döndürmüyor (isterse döndürebilir), onun yerine dahili verilerle bir dictionary listesi döndürüyor.

    FastAPI, response'u dönüştürmek için (dataclass'ları içeren) `response_model` parametresini kullanacaktır.

Karmaşık veri yapıları oluşturmak için `dataclasses` ile diğer type annotation'ları pek çok farklı kombinasyonda birleştirebilirsiniz.

Daha spesifik ayrıntılar için yukarıdaki kod içi annotation ipuçlarına bakın.

## Daha Fazla Öğrenin { #learn-more }

`dataclasses`'ı diğer Pydantic model'leriyle de birleştirebilir, onlardan kalıtım alabilir, kendi model'lerinize dahil edebilirsiniz, vb.

Daha fazlası için <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/" class="external-link" target="_blank">Pydantic'in dataclasses dokümantasyonuna</a> bakın.

## Sürüm { #version }

Bu özellik FastAPI `0.67.0` sürümünden beri mevcuttur. 🔖
