# Request'i Doğrudan Kullanmak { #using-the-request-directly }

Şu ana kadar, ihtiyacınız olan request parçalarını tipleriyle birlikte tanımlıyordunuz.

Verileri şuradan alarak:

* path'ten parameter olarak.
* Header'lardan.
* Cookie'lerden.
* vb.

Bunu yaptığınızda **FastAPI**, bu verileri doğrular (validate eder), dönüştürür ve API'niz için dokümantasyonu otomatik olarak üretir.

Ancak bazı durumlarda `Request` nesnesine doğrudan erişmeniz gerekebilir.

## `Request` nesnesi hakkında detaylar { #details-about-the-request-object }

**FastAPI** aslında altta **Starlette** çalıştırır ve üstüne çeşitli araçlardan oluşan bir katman ekler. Bu yüzden gerektiğinde Starlette'in <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">`Request`</a> nesnesini doğrudan kullanabilirsiniz.

Bu ayrıca şu anlama gelir: `Request` nesnesinden veriyi doğrudan alırsanız (örneğin body'yi okursanız) FastAPI bu veriyi doğrulamaz, dönüştürmez veya dokümante etmez (otomatik API arayüzü için OpenAPI ile).

Buna rağmen normal şekilde tanımladığınız diğer herhangi bir parameter (örneğin Pydantic model ile body) yine doğrulanır, dönüştürülür, annotate edilir, vb.

Ama bazı özel durumlarda `Request` nesnesini almak faydalıdır.

## `Request` nesnesini doğrudan kullanın { #use-the-request-object-directly }

*Path operation function* içinde client'ın IP adresini/host'unu almak istediğinizi düşünelim.

Bunun için request'e doğrudan erişmeniz gerekir.

{* ../../docs_src/using_request_directly/tutorial001_py310.py hl[1,7:8] *}

Tipi `Request` olan bir *path operation function* parameter'ı tanımladığınızda **FastAPI**, o parameter'a `Request` nesnesini geçmesi gerektiğini anlar.

/// tip | İpucu

Bu örnekte, request parameter'ının yanında bir path parameter'ı da tanımladığımıza dikkat edin.

Dolayısıyla path parameter'ı çıkarılır, doğrulanır, belirtilen tipe dönüştürülür ve OpenAPI ile annotate edilir.

Aynı şekilde, diğer parameter'ları normal biçimde tanımlamaya devam edip buna ek olarak `Request` de alabilirsiniz.

///

## `Request` dokümantasyonu { #request-documentation }

<a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">Resmi Starlette dokümantasyon sitesinde `Request` nesnesiyle ilgili daha fazla detayı</a> okuyabilirsiniz.

/// note | Teknik Detaylar

`from starlette.requests import Request` de kullanabilirsiniz.

**FastAPI** bunu size (geliştiriciye) kolaylık olsun diye doğrudan sunar. Ancak kendisi doğrudan Starlette'ten gelir.

///
