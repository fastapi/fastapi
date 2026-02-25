# Body - Güncellemeler { #body-updates }

## `PUT` ile değiştirerek güncelleme { #update-replacing-with-put }

Bir öğeyi güncellemek için <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT" class="external-link" target="_blank">HTTP `PUT`</a> operasyonunu kullanabilirsiniz.

Girdi verisini JSON olarak saklanabilecek bir formata (ör. bir NoSQL veritabanı ile) dönüştürmek için `jsonable_encoder` kullanabilirsiniz. Örneğin, `datetime` değerlerini `str`'ye çevirmek gibi.

{* ../../docs_src/body_updates/tutorial001_py310.py hl[28:33] *}

`PUT`, mevcut verinin yerine geçmesi gereken veriyi almak için kullanılır.

### Değiştirerek güncelleme uyarısı { #warning-about-replacing }

Bu, `bar` öğesini `PUT` ile, body içinde şu verilerle güncellemek isterseniz:

```Python
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

zaten kayıtlı olan `"tax": 20.2` alanını içermediği için, input model `"tax": 10.5` varsayılan değerini kullanacaktır.

Ve veri, bu "yeni" `tax` değeri olan `10.5` ile kaydedilecektir.

## `PATCH` ile kısmi güncellemeler { #partial-updates-with-patch }

Veriyi *kısmen* güncellemek için <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH" class="external-link" target="_blank">HTTP `PATCH`</a> operasyonunu da kullanabilirsiniz.

Bu, yalnızca güncellemek istediğiniz veriyi gönderip, geri kalanını olduğu gibi bırakabileceğiniz anlamına gelir.

/// note | Not

`PATCH`, `PUT`'a göre daha az yaygın kullanılır ve daha az bilinir.

Hatta birçok ekip, kısmi güncellemeler için bile yalnızca `PUT` kullanır.

Bunları nasıl isterseniz öyle kullanmakta **özgürsünüz**; **FastAPI** herhangi bir kısıtlama dayatmaz.

Ancak bu kılavuz, aşağı yukarı, bunların nasıl kullanılması amaçlandığını gösterir.

///

### Pydantic'in `exclude_unset` parametresini kullanma { #using-pydantics-exclude-unset-parameter }

Kısmi güncellemeler almak istiyorsanız, Pydantic modelinin `.model_dump()` metodundaki `exclude_unset` parametresini kullanmak çok faydalıdır.

Örneğin: `item.model_dump(exclude_unset=True)`.

Bu, `item` modeli oluşturulurken set edilmiş verileri içeren; varsayılan değerleri hariç tutan bir `dict` üretir.

Sonrasında bunu, yalnızca set edilmiş (request'te gönderilmiş) veriyi içeren; varsayılan değerleri atlayan bir `dict` üretmek için kullanabilirsiniz:

{* ../../docs_src/body_updates/tutorial002_py310.py hl[32] *}

### Pydantic'in `update` parametresini kullanma { #using-pydantics-update-parameter }

Artık `.model_copy()` ile mevcut modelin bir kopyasını oluşturup, güncellenecek verileri içeren bir `dict` ile `update` parametresini geçebilirsiniz.

Örneğin: `stored_item_model.model_copy(update=update_data)`:

{* ../../docs_src/body_updates/tutorial002_py310.py hl[33] *}

### Kısmi güncellemeler özeti { #partial-updates-recap }

Özetle, kısmi güncelleme uygulamak için şunları yaparsınız:

* (İsteğe bağlı olarak) `PUT` yerine `PATCH` kullanın.
* Kayıtlı veriyi alın.
* Bu veriyi bir Pydantic modeline koyun.
* Input modelinden, varsayılan değerler olmadan bir `dict` üretin (`exclude_unset` kullanarak).
    * Bu şekilde, modelinizdeki varsayılan değerlerle daha önce saklanmış değerlerin üzerine yazmak yerine, yalnızca kullanıcının gerçekten set ettiği değerleri güncellersiniz.
* Kayıtlı modelin bir kopyasını oluşturun ve alınan kısmi güncellemeleri kullanarak attribute'larını güncelleyin (`update` parametresini kullanarak).
* Kopyalanan modeli DB'nizde saklanabilecek bir şeye dönüştürün (ör. `jsonable_encoder` kullanarak).
    * Bu, modelin `.model_dump()` metodunu yeniden kullanmaya benzer; ancak değerlerin JSON'a dönüştürülebilecek veri tiplerine çevrilmesini garanti eder (ör. `datetime` -> `str`).
* Veriyi DB'nize kaydedin.
* Güncellenmiş modeli döndürün.

{* ../../docs_src/body_updates/tutorial002_py310.py hl[28:35] *}

/// tip | İpucu

Aynı tekniği HTTP `PUT` operasyonu ile de kullanabilirsiniz.

Ancak buradaki örnek `PATCH` kullanıyor, çünkü bu kullanım senaryoları için tasarlanmıştır.

///

/// note | Not

Input modelin yine de doğrulandığına dikkat edin.

Dolayısıyla, tüm attribute'ların atlanabildiği kısmi güncellemeler almak istiyorsanız, tüm attribute'ları optional olarak işaretlenmiş (varsayılan değerlerle veya `None` ile) bir modele ihtiyacınız vardır.

**Güncelleme** için tüm değerleri optional olan modeller ile **oluşturma** için zorunlu değerlere sahip modelleri ayırmak için, [Extra Models](extra-models.md){.internal-link target=_blank} bölümünde anlatılan fikirleri kullanabilirsiniz.

///
