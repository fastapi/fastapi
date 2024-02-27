# Gövde - Alanlar

*Yol operasyon fonksiyonlarındaki* parametreler için `Query`, `Path` ve `Body` ifadeleri ile ek doğrulama ve üstveri tanımlayabileceğiniz gibi Pydantic'in `Field` ifadesini kullanarak Pydantic modelleri içerisinde de doğrulama ve üstveri tanımı yapabilirsiniz.

## `Field` İfadesini İçeri Aktaralım

Öncelikle, ifadeyi içeri aktarmamız gerekir:

=== "Python 3.10+"

    ```Python hl_lines="4"
    {!> ../../../docs_src/body_fields/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="4"
    {!> ../../../docs_src/body_fields/tutorial001_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="4"
    {!> ../../../docs_src/body_fields/tutorial001_an.py!}
    ```

=== "Python 3.10+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="2"
    {!> ../../../docs_src/body_fields/tutorial001_py310.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="4"
    {!> ../../../docs_src/body_fields/tutorial001.py!}
    ```

!!! warning "Uyarı"
    Fark ettiyseniz, `Field` ifadesi diğer ifadelerin (`Query`, `Path`, `Body`, vb) aksine `fastapi` paketinden değil direkt olarak `pydantic` paketinden içeri aktarılmıştır.

## Model Özellikleri Tanımları

Sonrasında, `Field` ifadesini model özellikleri ile kullanabilirsiniz:

=== "Python 3.10+"

    ```Python hl_lines="11-14"
    {!> ../../../docs_src/body_fields/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="11-14"
    {!> ../../../docs_src/body_fields/tutorial001_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="12-15"
    {!> ../../../docs_src/body_fields/tutorial001_an.py!}
    ```

=== "Python 3.10+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="9-12"
    {!> ../../../docs_src/body_fields/tutorial001_py310.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="11-14"
    {!> ../../../docs_src/body_fields/tutorial001.py!}
    ```

`Field` ifadesi `Query`, `Path` ve `Body` ifadeleri gibi çalışır ve aynı parametrelere sahiptir vb.

!!! note "Teknik Detaylar"
    Aslında, `Query`, `Path` ve ileride göreceğiniz diğer ifadeler, Pydantic paketinde bulunan `FieldInfo` sınıfının bir alt sınıfı olan ortak `Param` sınıfının alt sınıflarının örneklerini oluştururlar.

    Pydantic paketindeki `Field` ifadesi de geriye bir `FieldInfo` örneği döndürür.

    `Body` ifadesi de direkt olarak `FieldInfo` alt sınıfının örneklerini geriye döndürür. Bunların haricinde, ileride göreceğiniz `Body` sınıfının alt sınıfları da mevcuttur.

    Unutmayınız ki, `Query`, `Path` ve `fastapi` paketinden içeri aktardığınız diğer ifadeler, geriye özel sınıf döndüren fonksiyonlardır.

!!! tip "İpucu"
    Fark ettiyseniz, her model özelliğinin, *yol operasyon fonksiyonu* parametrelerindeki yapı gibi bir tipi, varsayılan değeri ve `Path`, `Query` ve `Body` ifadelerinin aksine `Field` ifadesi vardır.

## Ek Bilgi Tanımı

`Field`, `Query`, `Body` vb. ifadelere ek bilgi tanımları yapılabilir ve bu tanımlamalar, oluşturulan JSON Şemasına dahil edilir.

Dokümantasyona ek bilgi tanımı yapmak, örnek tanımlamaları öğrenilirken irdilenecektir.

!!! warning "Uyarı"
    `Field` ifadesine geçilen ek anahtarlar da uygulamanızdaki OpenAPI şemasında mevcut olacaktır.
    Bu anahtarlar, OpenAPI spesifikasyonunun bir parçası olmak zorunda olmadıklarından dolayı [OpenAPI doğrulayıcısı](https://validator.swagger.io/) gibi bazı OpenAPI araçları, oluşturulan şemalar ile uyumlu çalışmayabilir.

## Özet

Model özellikleri bazında ek doğrulama ve üstveri tanımları için Pydantic paketindeki `Field` ifadesinden faydalanabilirsiniz.

Ayrıca, ek anahtar kelime argümanlarını kullanarak da JSON Şemasına ek üstveri geçebilirsiniz.
