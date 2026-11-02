# Form Model'leri { #form-models }

FastAPI'de **form field**'larını tanımlamak için **Pydantic model**'lerini kullanabilirsiniz.

/// note | Not

Form'ları kullanmak için önce [`python-multipart`](https://github.com/Kludex/python-multipart)'ı yükleyin.

Projenize ekleyin:

```console
$ uv add python-multipart
```

///

/// note | Not

Bu özellik FastAPI `0.113.0` sürümünden itibaren desteklenmektedir. 🤓

///

## Form'lar için Pydantic Model'leri { #pydantic-models-for-forms }

Sadece, **form field** olarak almak istediğiniz alanlarla bir **Pydantic model** tanımlayın ve ardından parametreyi `Form` olarak bildirin:

{* ../../docs_src/request_form_models/tutorial001_an_py310.py hl[9:11,15] *}

**FastAPI**, request içindeki **form data**'dan **her bir field** için veriyi **çıkarır** ve size tanımladığınız Pydantic model'ini verir.

[HTML onay kutuları](request-forms.md#boolean-form-fields) için varsayılan değeri `False` olan boolean field'lar tanımlayın.

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

## Form Model'lerini Birleştirin { #combine-form-models }

Birden fazla form model'ini ayrı `Form` parametreleriyle birleştirebilirsiniz.

{* ../../docs_src/request_form_models/tutorial003_an_py310.py hl[9:14,19:21] *}

Client, `name`, `tags` ve `token` değerlerini form field'ları olarak gönderir. Her model, form field'larını bağımsız olarak doğrular.

Her model'in `extra` konfigürasyonu, diğer parametrelerde veya bağımlılıklarda tanımlanan field'lar ve dosyalar dahil tüm form field'larına uygulanır. `extra="forbid"` kullanıldığında, o model'in dışındaki tüm field'lar reddedilir. `extra="allow"` kullanıldığında ise bu field'lar model'e ek veri olarak dahil edilir.

Birden fazla tanım aynı form field adını kullanıyorsa, her biri o field'ın değerini doğrular. OpenAPI şemasının ortak field'ları tutarlı bir şekilde tanımlayabilmesi için bu field'larda uyumlu türler ve kısıtlamalar kullanın.

## İsteğe Bağlı Form Model'leri { #optional-form-models }

Grubu isteğe bağlı hale getirmek için form model'ini `| None` ile tanımlayın ve varsayılan değerini `None` olarak belirleyin.

{* ../../docs_src/request_form_models/tutorial005_an_py310.py hl[17] *}

Ne `name` ne de `age` gönderilirse, `profile` değeri `None` olur. İkisinden biri gönderilirse, FastAPI model'i doğrular ve her iki field'ı da zorunlu tutar. Boş bir değer gönderilmesi de field'ın sağlandığı anlamına gelir.

Varsayılan değer belirtmeden `| None` kullanırsanız parametre yine zorunlu olur.

Fazladan field'lar, model'in `extra` konfigürasyonuna göre işlenir. Yok sayılan fazladan field'lar, model'in sağlanmış sayılmasına neden olmaz.

Yalnızca işaretlenmemiş onay kutuları içeren isteğe bağlı bir model, gönderilmemiş kabul edilir. Model'i açıkça sağlamak için `enabled=false` gibi bir değer gönderin.

## Form Model'lerinin İsteğe Bağlı Union'ları { #optional-unions-of-form-models }

Model'lerden oluşan isteğe bağlı bir union da kullanabilirsiniz.

{* ../../docs_src/request_form_models/tutorial006_an_py310.py hl[9:16,21] *}

Hiçbir form field'ı gönderilmezse, `contact` değeri `None` olur. `name` ile birlikte `kind=person` veya `company_name` ile birlikte `kind=company` gönderin. Discriminator (ayırt edici), hangi model'in doğrulanacağını seçer.

## Form Model'lerinin Union'larını Birleştirin { #combine-unions-of-form-models }

Union'ları diğer form model'leriyle, ayrı `Form` parametreleriyle ve `File` parametreleriyle birleştirebilirsiniz. Her union bağımsız olarak doğrulanır.

{* ../../docs_src/request_form_models/tutorial007_an_py310.py hl[31:35] *}

Tüm field'ları aynı form içinde gönderin. Örneğin, `contact_type=person`, `name=Rick`, `notification_type=email`, `email=rick@example.com` ve `token=secret` gönderin.

`notification` değerini `None` olarak bırakmak için bildirim field'larını göndermeyin.

## Form Model'leri ve Dosyalar { #form-models-and-files }

Bir form model'ini [dosya parametreleriyle](request-files.md) de birleştirebilirsiniz.

{* ../../docs_src/request_form_models/tutorial004_an_py310.py hl[14] *}

Burada client, `name` field'ını ve `avatar` dosyasını `multipart/form-data` kullanarak gönderir.

## Özet { #summary }

FastAPI'de form field'larını tanımlamak için Pydantic model'lerini kullanabilirsiniz. 😎
