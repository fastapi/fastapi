# Path Operation Yapılandırması { #path-operation-configuration }

Onu yapılandırmak için *path operation decorator*’ınıza geçebileceğiniz çeşitli parametreler vardır.

/// warning | Uyarı

Bu parametrelerin *path operation function*’ınıza değil, doğrudan *path operation decorator*’ına verildiğine dikkat edin.

///

## Response Status Code { #response-status-code }

*Path operation*’ınızın response’unda kullanılacak (HTTP) `status_code`’u tanımlayabilirsiniz.

`404` gibi `int` kodu doğrudan verebilirsiniz.

Ancak her sayısal kodun ne işe yaradığını hatırlamıyorsanız, `status` içindeki kısayol sabitlerini kullanabilirsiniz:

{* ../../docs_src/path_operation_configuration/tutorial001_py310.py hl[1,15] *}

Bu status code response’da kullanılacak ve OpenAPI şemasına eklenecektir.

/// note | Teknik Detaylar

`from starlette import status` da kullanabilirsiniz.

**FastAPI**, geliştirici olarak işinizi kolaylaştırmak için `starlette.status`’u `fastapi.status` olarak da sunar. Ancak kaynağı doğrudan Starlette’tir.

///

## Tags { #tags }

*Path operation*’ınıza tag ekleyebilirsiniz; `tags` parametresine `str` öğelerinden oluşan bir `list` verin (genellikle tek bir `str`):

{* ../../docs_src/path_operation_configuration/tutorial002_py310.py hl[15,20,25] *}

Bunlar OpenAPI şemasına eklenecek ve otomatik dokümantasyon arayüzleri tarafından kullanılacaktır:

<img src="/img/tutorial/path-operation-configuration/image01.png">

### Enum ile Tags { #tags-with-enums }

Büyük bir uygulamanız varsa, zamanla **birden fazla tag** birikebilir ve ilişkili *path operation*’lar için her zaman **aynı tag**’i kullandığınızdan emin olmak isteyebilirsiniz.

Bu durumlarda tag’leri bir `Enum` içinde tutmak mantıklı olabilir.

**FastAPI** bunu düz string’lerde olduğu gibi aynı şekilde destekler:

{* ../../docs_src/path_operation_configuration/tutorial002b_py310.py hl[1,8:10,13,18] *}

## Özet ve açıklama { #summary-and-description }

Bir `summary` ve `description` ekleyebilirsiniz:

{* ../../docs_src/path_operation_configuration/tutorial003_py310.py hl[17:18] *}

## Docstring’den Açıklama { #description-from-docstring }

Açıklamalar genelde uzun olur ve birden fazla satıra yayılır; bu yüzden *path operation* açıklamasını, fonksiyonun içinde <dfn title="dokümantasyon için kullanılan, fonksiyon içinde ilk ifade olarak yer alan (herhangi bir değişkene atanmayan) çok satırlı string">docstring</dfn> olarak tanımlayabilirsiniz; **FastAPI** de onu buradan okur.

Docstring içinde <a href="https://en.wikipedia.org/wiki/Markdown" class="external-link" target="_blank">Markdown</a> yazabilirsiniz; doğru şekilde yorumlanır ve gösterilir (docstring girintisi dikkate alınarak).

{* ../../docs_src/path_operation_configuration/tutorial004_py310.py hl[17:25] *}

Interactive docs’ta şöyle kullanılacaktır:

<img src="/img/tutorial/path-operation-configuration/image02.png">

## Response description { #response-description }

`response_description` parametresi ile response açıklamasını belirtebilirsiniz:

{* ../../docs_src/path_operation_configuration/tutorial005_py310.py hl[18] *}

/// info | Bilgi

`response_description` özellikle response’u ifade eder; `description` ise genel olarak *path operation*’ı ifade eder.

///

/// check | Ek bilgi

OpenAPI, her *path operation* için bir response description zorunlu kılar.

Bu yüzden siz sağlamazsanız, **FastAPI** otomatik olarak "Successful response" üretir.

///

<img src="/img/tutorial/path-operation-configuration/image03.png">

## Bir *path operation*’ı Deprecate Etmek { #deprecate-a-path-operation }

Bir *path operation*’ı kaldırmadan, <dfn title="eskimiş, kullanılması önerilmez">deprecated</dfn> olarak işaretlemeniz gerekiyorsa `deprecated` parametresini verin:

{* ../../docs_src/path_operation_configuration/tutorial006_py310.py hl[16] *}

Interactive docs’ta deprecated olduğu net şekilde işaretlenecektir:

<img src="/img/tutorial/path-operation-configuration/image04.png">

Deprecated olan ve olmayan *path operation*’ların nasıl göründüğüne bakın:

<img src="/img/tutorial/path-operation-configuration/image05.png">

## Özet { #recap }

*Path operation*’larınızı, *path operation decorator*’larına parametre geçirerek kolayca yapılandırabilir ve metadata ekleyebilirsiniz.
