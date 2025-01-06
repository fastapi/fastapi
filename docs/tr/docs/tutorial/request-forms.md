# Form Verisi

İstek gövdesinde JSON verisi yerine form alanlarını karşılamanız gerketiğinde `Form` sınıfını kullanabilirsiniz.

/// info | Bilgi

Formları kullanmak için öncelikle <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a> paketini indirmeniz gerekmektedir.

Örneğin `pip install python-multipart`.

///

## `Form` Sınıfını Projenize Dahil Edin

`Form` sınıfını `fastapi`'den projenize dahil edin:

{* ../../docs_src/request_forms/tutorial001_an_py39.py hl[3] *}

## `Form` Parametrelerini Tanımlayın

Form parametrelerini `Body` veya `Query` için yaptığınız gibi oluşturun:

{* ../../docs_src/request_forms/tutorial001_an_py39.py hl[9] *}

Örneğin, OAuth2 spesifikasyonunun kullanılabileceği ("şifre akışı" olarak adlandırılan) yollardan birinde, form alanları olarak <abbr title="Kullanıcı Adı: Username">"username"</abbr> ve <abbr title="Şifre: Password">"password"</abbr> gönderilmesi gerekir.

Bu <abbr title="Spesifikasyon: Specification">spesifikasyon</abbr> form alanlarını adlandırırken isimlerinin birebir `username` ve `password` olmasını ve JSON verisi yerine form verisi olarak gönderilmesini gerektirir.

`Form` sınıfıyla tanımlama yaparken `Body`, `Query`, `Path` ve `Cookie` sınıflarında kullandığınız aynı validasyon, örnekler, isimlendirme (örneğin `username` yerine `user-name` kullanımı) ve daha fazla konfigurasyonu kullanabilirsiniz.

/// info | Bilgi

`Form` doğrudan `Body` sınıfını miras alan bir sınıftır.

///

/// tip | İpucu

Form gövdelerini tanımlamak için `Form` sınıfını kullanmanız gerekir; çünkü bu olmadan parametreler sorgu parametreleri veya gövde (JSON) parametreleri olarak yorumlanır.

///

## "Form Alanları" Hakkında

HTML formlarının (`<form></form>`) verileri sunucuya gönderirken JSON'dan farklı özel bir kodlama kullanır.

**FastAPI** bu verilerin JSON yerine doğru şekilde okunmasını sağlayacaktır.

/// note | Teknik Detaylar

Form verileri normalde `application/x-www-form-urlencoded` medya tipiyle kodlanır.

Ancak form içerisinde dosyalar yer aldığında `multipart/form-data` olarak kodlanır. Bir sonraki bölümde dosyaların işlenmesi hakkında bilgi edineceksiniz.

Form kodlama türleri ve form alanları hakkında daha fazla bilgi edinmek istiyorsanız <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> web docs for <code>POST</code></a> sayfasını ziyaret edebilirsiniz.

///

/// warning | Uyarı

*Yol operasyonları* içerisinde birden fazla `Form` parametresi tanımlayabilirsiniz ancak bunlarla birlikte JSON verisi kabul eden `Body` alanları tanımlayamazsınız çünkü bu durumda istek gövdesi `application/json` yerine `application/x-www-form-urlencoded` ile kodlanmış olur.

Bu **FastAPI**'ın getirdiği bir kısıtlama değildir, HTTP protokolünün bir parçasıdır.

///

## Özet

Form verisi girdi parametreleri tanımlamak için `Form` sınıfını kullanın.
