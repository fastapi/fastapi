# Yol Parametreleri ve Sayısal Doğrulamalar

`Query` ifadesi ile sorgu parametreleri için tanımladığınız doğrulamalar ve üstverileri aynı şekilde `Path` ifadesi için de tanımlayabilirsiniz.

## Path İfadesini İçeri Aktaralım

Öncelikle, `fastapi` paketinden `Path` ifadesini ve sonra `Annotated` ifadesini içeri aktaralım:

=== "Python 3.10+"

    ```Python hl_lines="1  3"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="1  3"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="3-4"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001_an.py!}
    ```

=== "Python 3.10+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="1"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001_py310.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="3"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001.py!}
    ```

!!! info "Bilgi"
    FastAPI, 0.95.0 versiyonu ile birlikte `Annotated` ifadesini desteklemeye (ve önermeye) başladı.

    Daha eski bir sürüme sahipseniz `Annotated` ifadesini kullanırken hata alacaksınızdır.

    `Annotated` ifadesini kullanmadan önce [FastAPI versiyon güncellemesini](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank} en az 0.95.1 sürümüne getirdiğinizden emin olunuz.

## Üstveri Tanımlayalım

`Query` ifadesinde geçerli olan tüm parametreleri kullanabilirsiniz.

Örneğin, `item_id` yol parametresi için `title` üstverisi tanımlamak adına şunu yazabilirsiniz:

=== "Python 3.10+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001_an.py!}
    ```

=== "Python 3.10+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="8"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001_py310.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="10"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001.py!}
    ```

!!! note "Not"
    Yol parametreleri, yolun bir parçası olduklarından dolayı her zaman zorunlu haldedirlerdir.

    Bu nedenle, `...` ifadesini kullanarak onları zorunlu olarak damgalayabilirsiniz.

    Yine de, parametreyi `None` ile tanımlamanıza veya parametreye varsayılan bir değer atamanıza rağmen parametre bunlardan etkilenmeyip her koşulda zorunlu kılınacaktır.

## İhtiyaca Göre Parametreleri Sıralayalım

!!! tip "İpucu"
    Bu durum, `Annotated` kullandığınız şartlarda çok da önemli veya gerekli olmayacaktır.

Diyelim ki `q` sorgu parametresini zorunlu bir `str` olarak tanımlamak istiyorsunuz.

Ve o parametre için farklı bir tanımlama da yapmanıza gerek olmadığından dolayı `Query` ifadesine çok da gerek duymuyorsunuz.

Ama yine de, `item_id` yol parametresi için `Path` ifadesini kullanma ihtiyacı duyuyorsunuz ve bazı nedenlerden dolayı `Annotated` ifadesini kullanmak istemiyorsunuz.

Bu durumda, "varsayılan" değeri olmayan bir parametrenin önüne "varsayılan" değere sahip bir parametre koyarsanız Python huysuzlanacaktır.

Buna rağmen, varsayılan değersiz parametreyi (`q` sorgu parametresini) başa alacak şekilde yeniden sıralayabilirsiniz.

**FastAPI** için bu durumun bir önemi yoktur ve parametreleri isimlerine, tiplerine ve varsayılan tanımlamalarına (`Query`, `Path`, vb.) göre sıra fark etmeksizin ayırt edecektir.

Yani, fonksiyonunuzu bu şekilde tanımlayabilirsiniz:

=== "Python 3.8 Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="7"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial002.py!}
    ```

Unutmamanız gerekir ki, bu tür bir problemi `Annotated` ifadesini kullanmayı tercih ederseniz `Query()` veya `Path()` ifadeleri için fonksiyon parametrelerinin varsayılan değerlerini kullanmadığınızdan dolayı yaşamayacaksınızdır.

=== "Python 3.9+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial002_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial002_an.py!}
    ```

## İhtiyaca Göre Parametre Sıralamada Püf Noktalar

!!! tip "İpucu"
    Bu durum, `Annotated` kullandığınız şartlarda çok da önemli veya gerekli olmayacaktır.

İşte, kullanışlı olabilecek fakat sıkça kullanmayacağınız **küçük bir püf nokta**.

Eğer:

* `q` sorgu parametresini `Query` ifadesi veya herhangi bir varsayılan değer olmadan tanımlamak,
* `item_id` yol parametresini `Path` ifadesi ile tanımlamak,
* bu parametrelere farklı sıralamayla sahip olmak,
* ve `Annotated` ifadesini kullanmamak istiyorsanız

...Python'ın bu durum için özel bir sözdizimi vardır.

`*` simgesini, fonksiyonun ilk parametresi olarak geçebilirsiniz.

Python, `*` simgesi ile özel bir şey yapmayıp varsayılan değerleri olmasa bile ardından gelen parametrelerin, anahtar kelime argümanları (anahtar-değer eşleri) diğer bir deyişle <abbr title="Buradan gelir: K-ey W-ord Arg-uments"><code>kwargs</code></abbr> olarak çağırılması gerektiğinin farkında olacaktır.

```Python hl_lines="7"
{!../../../docs_src/path_params_numeric_validations/tutorial003.py!}
```

### `Annotated` ile Daha İyi

Eğer `Annotated` ifadesini kullanıyorsanız fonksiyon parametrelerinin varsayılan değerlerini kullanmayacağınızdan dolayı bu tarz bir probleme ve `*` simgesini kullanmaya ihtiyacınız kalmayacağını aklınızda bulundurabilirsiniz.

=== "Python 3.9+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial003_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial003_an.py!}
    ```

## Sayı Doğrulamaları: -dan Büyük veya Eşit

`Query` ve `Path` ifadeleri (ve ileride göreceğiniz diğerleri) ile sayı kısıtlamaları tanımlayabilirsiniz.

Burada, `ge=1` ifadesi sayesinde `item_id` değeri, `1`'den <abbr title="`g`reater than or `e`qual">"büyük veya eşit"</abbr> olmak zorunda kalacaktır.

=== "Python 3.9+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial004_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial004_an.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="8"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial004.py!}
    ```

## Sayı Doğrulamaları: -dan Büyük ve -dan Küçük veya Eşit

Aynı kural şu ifadeler için de geçerlidir:

* `gt`: <abbr title="`g`reater `t`han">-dan büyük</abbr>
* `le`: <abbr title="`l`ess than or `e`qual">-dan küçük veya eşit</abbr>

=== "Python 3.9+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial005_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial005_an.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="9"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial005.py!}
    ```

## Sayı Doğrulamaları: Float Sayılar, -dan Büyük ve -dan Küçük

Sayı doğrulamaları `float` değerler ile de kullanılabilir.

Sadece <abbr title="greater than or equal"><code>ge</code></abbr> değil <abbr title="greater than"><code>gt</code></abbr> tanımlamasının da yapılabilmesinin önemli olduğu asıl kısım burasıdır. Örneğin, bu tanımlama ile birlikte bir değerin `1`'den küçük olmasına rağmen `0`'dan büyük olmasını zorunlu kılabilirsiniz.

Bu sayede, `0.5` değeri geçerli olurken `0.0` veya `0` değerleri olmayacaktır.

Aynı durum <abbr title="less than"><code>lt (-dan küçük)</code></abbr> için de geçerlidir.

=== "Python 3.9+"

    ```Python hl_lines="13"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial006_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="12"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial006_an.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="11"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial006.py!}
    ```

## Özet

`Query`, `Path` ifadeleri (ve henüz görmediğiniz diğer ifadeler) ile birlikte [Sorgu Parametreleri ve String Doğrulamaları](query-params-str-validations.md){.internal-link target=_blank}'nda da olduğu gibi üstveri ve string doğrulamaları tanımlayabilirsiniz.

Ayrıca, sayısal doğrulamalar için de tanımlama yapabilirsiniz:

* `gt`: <abbr title="`g`reater `t`han"><code>-dan büyük</code></abbr>
* `ge`: <abbr title="`g`reater than or `e`qual"><code>-dan büyük veya eşit</code></abbr>
* `lt`: <abbr title="`l`ess `t`han"><code>-dan küçük</code></abbr>
* `le`: <abbr title="`l`ess than or `e`qual"><code>-dan küçük veya eşit</code></abbr>

!!! info "Bilgi"
    `Query`, `Path` ifadeleri ve ileride göreceğiniz diğer sınıflar `Param` ortak sınıfının alt sınıflarıdır.

    Bunların hepsi, aşina olmuş olduğunuz ek doğrulama ve üstveri tanımlamaları için aynı parametrelerden faydalanır.

!!! note "Teknik Detaylar"
    `Query`, `Path` ifadeleri ve `fastapi` paketinden içeri aktarılan diğer ifadeler aslında birer fonksiyondur.

    Bu fonksiyonlar çağrıldıkları zaman aynı isime sahip sınıfların örneklerini döndürürler.

    Yani, fonksiyon olan `Query` ifadesini içeri aktarıp çağırdığınızda yine `Query` isminde bir sınıfın örneğini geri döndürür.

    Bu fonksiyonlar (direkt olarak sınıf kullanımı yerine), editörünüzün onların tipleri hakkında hata tespit etmemesi adına mevcutta bulunurlar.

    Bu sayede, bahsedilen hataları görmezden gelmek adına özel düzenlemeler yapmadan editörünüzü ve kod araçlarınızı kullanabilirsiniz.
