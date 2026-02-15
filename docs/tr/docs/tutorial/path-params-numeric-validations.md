# Path Parametreleri ve Sayısal Doğrulamalar { #path-parameters-and-numeric-validations }

`Query` ile query parametreleri için daha fazla doğrulama ve metadata tanımlayabildiğiniz gibi, `Path` ile de path parametreleri için aynı tür doğrulama ve metadata tanımlayabilirsiniz.

## `Path`'i İçe Aktarın { #import-path }

Önce `fastapi` içinden `Path`'i ve `Annotated`'ı içe aktarın:

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[1,3] *}

/// info | Bilgi

FastAPI, 0.95.0 sürümünde `Annotated` desteğini ekledi (ve bunu önermeye başladı).

Daha eski bir sürüm kullanıyorsanız, `Annotated` kullanmaya çalıştığınızda hata alırsınız.

`Annotated` kullanmadan önce mutlaka FastAPI sürümünü en az 0.95.1 olacak şekilde [FastAPI sürümünü yükseltin](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank}.

///

## Metadata Tanımlayın { #declare-metadata }

`Query` için geçerli olan parametrelerin aynısını tanımlayabilirsiniz.

Örneğin, `item_id` path parametresi için bir `title` metadata değeri tanımlamak isterseniz şunu yazabilirsiniz:

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[10] *}

/// note | Not

Bir path parametresi her zaman zorunludur, çünkü path'in bir parçası olmak zorundadır. `None` ile tanımlasanız veya bir varsayılan değer verseniz bile bu hiçbir şeyi değiştirmez; yine her zaman zorunlu olur.

///

## Parametreleri İhtiyacınıza Göre Sıralayın { #order-the-parameters-as-you-need }

/// tip | İpucu

`Annotated` kullanıyorsanız, bu muhtemelen o kadar önemli ya da gerekli değildir.

///

Diyelim ki query parametresi `q`'yu zorunlu bir `str` olarak tanımlamak istiyorsunuz.

Ayrıca bu parametre için başka bir şey tanımlamanız gerekmiyor; dolayısıyla `Query` kullanmanıza da aslında gerek yok.

Ancak `item_id` path parametresi için yine de `Path` kullanmanız gerekiyor. Ve bir sebepten `Annotated` kullanmak istemiyorsunuz.

Python, "default" değeri olan bir parametreyi, "default" değeri olmayan bir parametreden önce yazarsanız şikayet eder.

Ama bunların sırasını değiştirebilir ve default değeri olmayan parametreyi (query parametresi `q`) en başa koyabilirsiniz.

Bu **FastAPI** için önemli değildir. FastAPI parametreleri isimlerine, tiplerine ve default tanımlarına (`Query`, `Path`, vb.) göre tespit eder; sırayla ilgilenmez.

Dolayısıyla fonksiyonunuzu şöyle tanımlayabilirsiniz:

{* ../../docs_src/path_params_numeric_validations/tutorial002_py310.py hl[7] *}

Ancak şunu unutmayın: `Annotated` kullanırsanız bu problem olmaz; çünkü `Query()` veya `Path()` için fonksiyon parametresi default değerlerini kullanmıyorsunuz.

{* ../../docs_src/path_params_numeric_validations/tutorial002_an_py310.py *}

## Parametreleri İhtiyacınıza Göre Sıralayın: Küçük Hileler { #order-the-parameters-as-you-need-tricks }

/// tip | İpucu

`Annotated` kullanıyorsanız, bu muhtemelen o kadar önemli ya da gerekli değildir.

///

İşte bazen işe yarayan **küçük bir hile**; ama çok sık ihtiyacınız olmayacak.

Şunları yapmak istiyorsanız:

* `q` query parametresini `Query` kullanmadan ve herhangi bir default değer vermeden tanımlamak
* `item_id` path parametresini `Path` kullanarak tanımlamak
* bunları farklı bir sırada yazmak
* `Annotated` kullanmamak

...Python bunun için küçük, özel bir sözdizimi sunar.

Fonksiyonun ilk parametresi olarak `*` geçin.

Python bu `*` ile bir şey yapmaz; ama bundan sonraki tüm parametrelerin keyword argument (anahtar-değer çiftleri) olarak çağrılması gerektiğini bilir; buna <abbr title="Kökeni: K-ey W-ord Arg-uments"><code>kwargs</code></abbr> da denir. Default değerleri olmasa bile.

{* ../../docs_src/path_params_numeric_validations/tutorial003_py310.py hl[7] *}

### `Annotated` ile Daha İyi { #better-with-annotated }

Şunu da unutmayın: `Annotated` kullanırsanız, fonksiyon parametresi default değerlerini kullanmadığınız için bu sorun ortaya çıkmaz ve muhtemelen `*` kullanmanız da gerekmez.

{* ../../docs_src/path_params_numeric_validations/tutorial003_an_py310.py hl[10] *}

## Sayı Doğrulamaları: Büyük Eşit { #number-validations-greater-than-or-equal }

`Query` ve `Path` (ve ileride göreceğiniz diğerleri) ile sayı kısıtları tanımlayabilirsiniz.

Burada `ge=1` ile, `item_id` değerinin `1`'den "`g`reater than or `e`qual" olacak şekilde bir tam sayı olması gerekir.

{* ../../docs_src/path_params_numeric_validations/tutorial004_an_py310.py hl[10] *}

## Sayı Doğrulamaları: Büyük ve Küçük Eşit { #number-validations-greater-than-and-less-than-or-equal }

Aynısı şunlar için de geçerlidir:

* `gt`: `g`reater `t`han
* `le`: `l`ess than or `e`qual

{* ../../docs_src/path_params_numeric_validations/tutorial005_an_py310.py hl[10] *}

## Sayı Doğrulamaları: `float` Değerler, Büyük ve Küçük { #number-validations-floats-greater-than-and-less-than }

Sayı doğrulamaları `float` değerler için de çalışır.

Burada <abbr title="greater than - büyüktür"><code>gt</code></abbr> tanımlayabilmek (sadece <abbr title="greater than or equal - büyük veya eşittir"><code>ge</code></abbr> değil) önemli hale gelir. Çünkü örneğin bir değerin `0`'dan büyük olmasını isteyebilirsiniz; `1`'den küçük olsa bile.

Bu durumda `0.5` geçerli bir değer olur. Ancak `0.0` veya `0` geçerli olmaz.

Aynısı <abbr title="less than - küçüktür"><code>lt</code></abbr> için de geçerlidir.

{* ../../docs_src/path_params_numeric_validations/tutorial006_an_py310.py hl[13] *}

## Özet { #recap }

`Query`, `Path` (ve henüz görmedikleriniz) ile metadata ve string doğrulamalarını, [Query Parametreleri ve String Doğrulamalar](query-params-str-validations.md){.internal-link target=_blank} bölümündekiyle aynı şekilde tanımlayabilirsiniz.

Ayrıca sayısal doğrulamalar da tanımlayabilirsiniz:

* `gt`: `g`reater `t`han
* `ge`: `g`reater than or `e`qual
* `lt`: `l`ess `t`han
* `le`: `l`ess than or `e`qual

/// info | Bilgi

`Query`, `Path` ve ileride göreceğiniz diğer class'lar ortak bir `Param` class'ının alt class'larıdır.

Hepsi, gördüğünüz ek doğrulama ve metadata parametrelerini paylaşır.

///

/// note | Teknik Detaylar

`Query`, `Path` ve diğerlerini `fastapi` içinden import ettiğinizde, bunlar aslında birer fonksiyondur.

Çağrıldıklarında, aynı isme sahip class'ların instance'larını döndürürler.

Yani `Query`'yi import edersiniz; bu bir fonksiyondur. Onu çağırdığınızda, yine `Query` adlı bir class'ın instance'ını döndürür.

Bu fonksiyonlar (class'ları doğrudan kullanmak yerine) editörünüzün type'larıyla ilgili hata işaretlememesi için vardır.

Bu sayede, bu hataları yok saymak üzere özel ayarlar eklemeden normal editörünüzü ve coding araçlarınızı kullanabilirsiniz.

///
