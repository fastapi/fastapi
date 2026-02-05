# Body - Alanlar { #body-fields }

`Query`, `Path` ve `Body` ile *path operation function* parametrelerinde ek doğrulama ve metadata tanımlayabildiğiniz gibi, Pydantic modellerinin içinde de Pydantic'in `Field`'ını kullanarak doğrulama ve metadata tanımlayabilirsiniz.

## `Field`'ı import edin { #import-field }

Önce import etmeniz gerekir:

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[4] *}

/// warning | Uyarı

`Field`'ın, diğerlerinin (`Query`, `Path`, `Body` vb.) aksine `fastapi`'den değil doğrudan `pydantic`'den import edildiğine dikkat edin.

///

## Model attribute'larını tanımlayın { #declare-model-attributes }

Ardından `Field`'ı model attribute'larıyla birlikte kullanabilirsiniz:

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[11:14] *}

`Field`, `Query`, `Path` ve `Body` ile aynı şekilde çalışır; aynı parametrelerin tamamına sahiptir, vb.

/// note | Teknik Detaylar

Aslında, `Query`, `Path` ve birazdan göreceğiniz diğerleri, ortak bir `Param` sınıfının alt sınıflarından nesneler oluşturur; `Param` sınıfı da Pydantic'in `FieldInfo` sınıfının bir alt sınıfıdır.

Pydantic'in `Field`'ı da `FieldInfo`'nun bir instance'ını döndürür.

`Body` ayrıca doğrudan `FieldInfo`'nun bir alt sınıfından nesneler döndürür. Daha sonra göreceğiniz başka bazıları da `Body` sınıfının alt sınıflarıdır.

`fastapi`'den `Query`, `Path` ve diğerlerini import ettiğinizde, bunların aslında özel sınıflar döndüren fonksiyonlar olduğunu unutmayın.

///

/// tip | İpucu

Type, varsayılan değer ve `Field` ile tanımlanan her model attribute'unun yapısının, *path operation function* parametresiyle aynı olduğuna dikkat edin; sadece `Path`, `Query` ve `Body` yerine `Field` kullanılmıştır.

///

## Ek bilgi ekleyin { #add-extra-information }

`Field`, `Query`, `Body` vb. içinde ek bilgi tanımlayabilirsiniz. Bu bilgiler oluşturulan JSON Schema'ya dahil edilir.

Örnek (examples) tanımlamayı öğrenirken, dokümanların ilerleyen kısımlarında ek bilgi ekleme konusunu daha ayrıntılı göreceksiniz.

/// warning | Uyarı

`Field`'a geçirilen ekstra key'ler, uygulamanız için üretilen OpenAPI schema'sında da yer alır.
Bu key'ler OpenAPI spesifikasyonunun bir parçası olmak zorunda olmadığından, örneğin [OpenAPI validator](https://validator.swagger.io/) gibi bazı OpenAPI araçları üretilen schema'nızla çalışmayabilir.

///

## Özet { #recap }

Model attribute'ları için ek doğrulamalar ve metadata tanımlamak üzere Pydantic'in `Field`'ını kullanabilirsiniz.

Ayrıca, ek keyword argument'ları kullanarak JSON Schema'ya ekstra metadata da iletebilirsiniz.
