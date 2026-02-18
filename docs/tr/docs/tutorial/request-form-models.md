# Form Model'leri { #form-models }

FastAPI'de **form field**'larını tanımlamak için **Pydantic model**'lerini kullanabilirsiniz.

/// info | Bilgi

Form'ları kullanmak için önce <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>'ı yükleyin.

Bir [virtual environment](../virtual-environments.md){.internal-link target=_blank} oluşturduğunuzdan, onu etkinleştirdiğinizden ve ardından paketi kurduğunuzdan emin olun. Örneğin:

```console
$ pip install python-multipart
```

///

/// note | Not

Bu özellik FastAPI `0.113.0` sürümünden itibaren desteklenmektedir. 🤓

///

## Form'lar için Pydantic Model'leri { #pydantic-models-for-forms }

Sadece, **form field** olarak almak istediğiniz alanlarla bir **Pydantic model** tanımlayın ve ardından parametreyi `Form` olarak bildirin:

{* ../../docs_src/request_form_models/tutorial001_an_py310.py hl[9:11,15] *}

**FastAPI**, request içindeki **form data**'dan **her bir field** için veriyi **çıkarır** ve size tanımladığınız Pydantic model'ini verir.

## Dokümanları Kontrol Edin { #check-the-docs }

Bunu `/docs` altındaki doküman arayüzünde doğrulayabilirsiniz:

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## Fazladan Form Field'larını Yasaklayın { #forbid-extra-form-fields }

Bazı özel kullanım senaryolarında (muhtemelen çok yaygın değildir), form field'larını yalnızca Pydantic model'inde tanımlananlarla **sınırlamak** isteyebilirsiniz. Ve **fazladan** gelen field'ları **yasaklayabilirsiniz**.

/// note | Not

Bu özellik FastAPI `0.114.0` sürümünden itibaren desteklenmektedir. 🤓

///

Herhangi bir `extra` field'ı `forbid` etmek için Pydantic'in model konfigürasyonunu kullanabilirsiniz:

{* ../../docs_src/request_form_models/tutorial002_an_py310.py hl[12] *}

Bir client fazladan veri göndermeye çalışırsa, bir **error** response alır.

Örneğin, client şu form field'larını göndermeye çalışırsa:

* `username`: `Rick`
* `password`: `Portal Gun`
* `extra`: `Mr. Poopybutthole`

`extra` field'ının izinli olmadığını söyleyen bir error response alır:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["body", "extra"],
            "msg": "Extra inputs are not permitted",
            "input": "Mr. Poopybutthole"
        }
    ]
}
```

## Özet { #summary }

FastAPI'de form field'larını tanımlamak için Pydantic model'lerini kullanabilirsiniz. 😎
