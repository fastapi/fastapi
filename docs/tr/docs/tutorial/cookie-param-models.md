# Cookie Parametre Modelleri { #cookie-parameter-models }

Birbirleriyle ilişkili bir **cookie** grubunuz varsa, bunları tanımlamak için bir **Pydantic model** oluşturabilirsiniz. 🍪

Bu sayede **model'i yeniden kullanabilir**, **birden fazla yerde** tekrar tekrar kullanabilir ve tüm parametreler için validation ve metadata'yı tek seferde tanımlayabilirsiniz. 😎

/// note | Not

Bu özellik FastAPI'nin `0.115.0` sürümünden itibaren desteklenmektedir. 🤓

///

/// tip | İpucu

Aynı teknik `Query`, `Cookie` ve `Header` için de geçerlidir. 😎

///

## Pydantic Model ile Cookies { #cookies-with-a-pydantic-model }

İhtiyacınız olan **cookie** parametrelerini bir **Pydantic model** içinde tanımlayın ve ardından parametreyi `Cookie` olarak bildirin:

{* ../../docs_src/cookie_param_models/tutorial001_an_py310.py hl[9:12,16] *}

**FastAPI**, request ile gelen **cookies** içinden **her bir field** için veriyi **extract** eder ve size tanımladığınız Pydantic model'i verir.

## Dokümanları Kontrol Edin { #check-the-docs }

Tanımlanan cookie'leri `/docs` altındaki docs UI'da görebilirsiniz:

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// note | Not

Tarayıcıların cookie'leri özel biçimlerde ve arka planda yönetmesi nedeniyle, **JavaScript**'in cookie'lere erişmesine kolayca izin vermediğini aklınızda bulundurun.

`/docs` altındaki **API docs UI**'a giderseniz, *path operation*'larınız için cookie'lerin **dokümantasyonunu** görebilirsiniz.

Ancak verileri **doldurup** "Execute" düğmesine tıklasanız bile, docs UI **JavaScript** ile çalıştığı için cookie'ler gönderilmez; dolayısıyla hiç değer girmemişsiniz gibi bir **error** mesajı görürsünüz.

///

## Fazladan Cookie'leri Yasaklayın { #forbid-extra-cookies }

Bazı özel kullanım senaryolarında (muhtemelen çok yaygın değildir) almak istediğiniz cookie'leri **kısıtlamak** isteyebilirsiniz.

API'niz artık kendi <dfn title="Bu bir şaka, sadece bilginize. Cookie onaylarıyla ilgisi yok, ama API'nin de artık zavallı cookie'leri reddedebilmesi komik. Bir cookie alın. 🍪">cookie onayı</dfn>'nı kontrol etme gücüne sahip. 🤪🍪

Pydantic'in model configuration'ını kullanarak `extra` olan herhangi bir field'ı `forbid` edebilirsiniz:

{* ../../docs_src/cookie_param_models/tutorial002_an_py310.py hl[10] *}

Bir client **fazladan cookie** göndermeye çalışırsa, bir **error** response alır.

Onayınızı almak için bunca çaba harcayan zavallı cookie banner'ları... <dfn title="Bu da başka bir şaka. Dikkate almayın. Cookie'niz için biraz kahve alın. ☕">API'nin bunu reddetmesi için</dfn>. 🍪

Örneğin client, değeri `good-list-please` olan bir `santa_tracker` cookie'si göndermeye çalışırsa, client `santa_tracker` <dfn title="Noel Baba cookie eksikliğini onaylamıyor. 🎅 Tamam, artık cookie şakası yok.">cookie'ye izin verilmiyor</dfn> diyen bir **error** response alır:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["cookie", "santa_tracker"],
            "msg": "Extra inputs are not permitted",
            "input": "good-list-please",
        }
    ]
}
```

## Özet { #summary }

**FastAPI**'de <dfn title="Gitmeden önce son bir cookie alın. 🍪">**cookie**</dfn> tanımlamak için **Pydantic model**'lerini kullanabilirsiniz. 😎
