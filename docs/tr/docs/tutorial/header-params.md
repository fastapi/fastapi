# Header Parametreleri { #header-parameters }

`Query`, `Path` ve `Cookie` parametrelerini nasıl tanımlıyorsanız, Header parametrelerini de aynı şekilde tanımlayabilirsiniz.

## `Header`'ı Import Edin { #import-header }

Önce `Header`'ı import edin:

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[3] *}

## `Header` Parametrelerini Tanımlayın { #declare-header-parameters }

Ardından header parametrelerini, `Path`, `Query` ve `Cookie` ile kullandığınız yapının aynısıyla tanımlayın.

Default değeri ve ek validation ya da annotation parametrelerinin tamamını belirleyebilirsiniz:

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[9] *}

/// note | Teknik Detaylar

`Header`, `Path`, `Query` ve `Cookie`'nin "kardeş" sınıfıdır. Ayrıca aynı ortak `Param` sınıfından kalıtım alır.

Ancak şunu unutmayın: `fastapi`'den `Query`, `Path`, `Header` ve diğerlerini import ettiğinizde, bunlar aslında özel sınıfları döndüren fonksiyonlardır.

///

/// info | Bilgi

Header'ları tanımlamak için `Header` kullanmanız gerekir; aksi halde parametreler query parametreleri olarak yorumlanır.

///

## Otomatik Dönüştürme { #automatic-conversion }

`Header`, `Path`, `Query` ve `Cookie`'nin sağladıklarına ek olarak küçük bir ekstra işlevsellik sunar.

Standart header'ların çoğu, "hyphen" karakteri (diğer adıyla "minus symbol" (`-`)) ile ayrılır.

Ancak `user-agent` gibi bir değişken adı Python'da geçersizdir.

Bu yüzden, default olarak `Header`, header'ları almak ve dokümante etmek için parametre adlarındaki underscore (`_`) karakterlerini hyphen (`-`) ile dönüştürür.

Ayrıca HTTP header'ları büyük/küçük harfe duyarlı değildir; dolayısıyla onları standart Python stiliyle (diğer adıyla "snake_case") tanımlayabilirsiniz.

Yani `User_Agent` gibi bir şey yazıp ilk harfleri büyütmeniz gerekmeden, Python kodunda normalde kullandığınız gibi `user_agent` kullanabilirsiniz.

Herhangi bir nedenle underscore'ların hyphen'lara otomatik dönüştürülmesini kapatmanız gerekirse, `Header`'ın `convert_underscores` parametresini `False` yapın:

{* ../../docs_src/header_params/tutorial002_an_py310.py hl[10] *}

/// warning | Uyarı

`convert_underscores`'u `False` yapmadan önce, bazı HTTP proxy'lerinin ve server'ların underscore içeren header'ların kullanımına izin vermediğini unutmayın.

///

## Yinelenen Header'lar { #duplicate-headers }

Yinelenen header'lar almak mümkündür. Yani aynı header'ın birden fazla değeri olabilir.

Bu tür durumları, type tanımında bir list kullanarak belirtebilirsiniz.

Yinelenen header'daki tüm değerleri Python `list` olarak alırsınız.

Örneğin, birden fazla kez gelebilen `X-Token` header'ını tanımlamak için şöyle yazabilirsiniz:

{* ../../docs_src/header_params/tutorial003_an_py310.py hl[9] *}

Eğer bu *path operation* ile iki HTTP header göndererek iletişim kurarsanız:

```
X-Token: foo
X-Token: bar
```

response şöyle olur:

```JSON
{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
```

## Özet { #recap }

Header'ları `Header` ile tanımlayın; `Query`, `Path` ve `Cookie` ile kullanılan ortak kalıbı burada da kullanın.

Değişkenlerinizdeki underscore'lar konusunda endişelenmeyin, **FastAPI** bunları dönüştürmeyi halleder.
