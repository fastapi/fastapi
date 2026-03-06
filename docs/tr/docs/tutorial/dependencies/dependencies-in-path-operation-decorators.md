# Path Operation Decorator'lerinde Dependency'ler { #dependencies-in-path-operation-decorators }

Bazı durumlarda bir dependency'nin döndürdüğü değere *path operation function* içinde gerçekten ihtiyacınız olmaz.

Ya da dependency zaten bir değer döndürmüyordur.

Ancak yine de çalıştırılmasını/çözülmesini istersiniz.

Bu gibi durumlarda, `Depends` ile bir *path operation function* parametresi tanımlamak yerine, *path operation decorator*'üne `dependencies` adında bir `list` ekleyebilirsiniz.

## *Path Operation Decorator*'üne `dependencies` Ekleyin { #add-dependencies-to-the-path-operation-decorator }

*Path operation decorator*, opsiyonel bir `dependencies` argümanı alır.

Bu, `Depends()` öğelerinden oluşan bir `list` olmalıdır:

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[19] *}

Bu dependency'ler normal dependency'lerle aynı şekilde çalıştırılır/çözülür. Ancak (eğer bir değer döndürüyorlarsa) bu değer *path operation function*'ınıza aktarılmaz.

/// tip | İpucu

Bazı editörler, kullanılmayan function parametrelerini kontrol eder ve bunları hata olarak gösterebilir.

Bu `dependencies` yaklaşımıyla, editör/araç hatalarına takılmadan dependency'lerin çalıştırılmasını sağlayabilirsiniz.

Ayrıca kodunuzda kullanılmayan bir parametreyi gören yeni geliştiricilerin bunun gereksiz olduğunu düşünmesi gibi bir kafa karışıklığını da azaltabilir.

///

/// info | Bilgi

Bu örnekte uydurma özel header'lar olan `X-Key` ve `X-Token` kullanıyoruz.

Ancak gerçek senaryolarda, security uygularken, entegre [Security yardımcı araçlarını (bir sonraki bölüm)](../security/index.md){.internal-link target=_blank} kullanmak size daha fazla fayda sağlar.

///

## Dependency Hataları ve Return Değerleri { #dependencies-errors-and-return-values }

Normalde kullandığınız aynı dependency *function*'larını burada da kullanabilirsiniz.

### Dependency Gereksinimleri { #dependency-requirements }

Request gereksinimleri (header'lar gibi) veya başka alt dependency'ler tanımlayabilirler:

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[8,13] *}

### Exception Fırlatmak { #raise-exceptions }

Bu dependency'ler, normal dependency'lerde olduğu gibi `raise` ile exception fırlatabilir:

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[10,15] *}

### Return Değerleri { #return-values }

Ayrıca değer döndürebilirler ya da döndürmeyebilirler; dönen değer kullanılmayacaktır.

Yani başka bir yerde zaten kullandığınız, değer döndüren normal bir dependency'yi tekrar kullanabilirsiniz; değer kullanılmasa bile dependency çalıştırılacaktır:

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[11,16] *}

## Bir *Path Operation* Grubu İçin Dependency'ler { #dependencies-for-a-group-of-path-operations }

Daha sonra, muhtemelen birden fazla dosya kullanarak daha büyük uygulamaları nasıl yapılandıracağınızı okurken ([Bigger Applications - Multiple Files](../../tutorial/bigger-applications.md){.internal-link target=_blank}), bir *path operation* grubu için tek bir `dependencies` parametresini nasıl tanımlayacağınızı öğreneceksiniz.

## Global Dependency'ler { #global-dependencies }

Sırada, dependency'leri tüm `FastAPI` uygulamasına nasıl ekleyeceğimizi göreceğiz; böylece her *path operation* için geçerli olacaklar.
