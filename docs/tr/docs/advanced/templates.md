# Şablonlar { #templates }

**FastAPI** ile istediğiniz herhangi bir template engine'i kullanabilirsiniz.

Yaygın bir tercih, Flask ve diğer araçların da kullandığı Jinja2'dir.

Bunu kolayca yapılandırmak için, doğrudan **FastAPI** uygulamanızda kullanabileceğiniz yardımcı araçlar vardır (Starlette tarafından sağlanır).

## Bağımlılıkları Yükleme { #install-dependencies }

Bir [virtual environment](../virtual-environments.md){.internal-link target=_blank} oluşturduğunuzdan, etkinleştirdiğinizden ve `jinja2`'yi yüklediğinizden emin olun:

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## `Jinja2Templates` Kullanımı { #using-jinja2templates }

* `Jinja2Templates`'ı içe aktarın.
* Daha sonra tekrar kullanabileceğiniz bir `templates` nesnesi oluşturun.
* Template döndürecek *path operation* içinde bir `Request` parametresi tanımlayın.
* Oluşturduğunuz `templates` nesnesini kullanarak bir `TemplateResponse` render edip döndürün; template'in adını, request nesnesini ve Jinja2 template'i içinde kullanılacak anahtar-değer çiftlerini içeren bir "context" sözlüğünü (dict) iletin.

{* ../../docs_src/templates/tutorial001_py310.py hl[4,11,15:18] *}

/// note

FastAPI 0.108.0 ve Starlette 0.29.0 öncesinde, ilk parametre `name` idi.

Ayrıca, daha önceki sürümlerde `request` nesnesi, Jinja2 için context içindeki anahtar-değer çiftlerinin bir parçası olarak geçirilirdi.

///

/// tip

`response_class=HTMLResponse` olarak tanımlarsanız doküman arayüzü (docs UI) response'un HTML olacağını anlayabilir.

///

/// note | Teknik Detaylar

`from starlette.templating import Jinja2Templates` da kullanabilirsiniz.

**FastAPI**, geliştirici için kolaylık olması adına `starlette.templating` içeriğini `fastapi.templating` olarak da sunar. Ancak mevcut response'ların çoğu doğrudan Starlette'ten gelir. `Request` ve `StaticFiles` için de aynı durum geçerlidir.

///

## Template Yazma { #writing-templates }

Ardından örneğin `templates/item.html` konumunda bir template yazabilirsiniz:

```jinja hl_lines="7"
{!../../docs_src/templates/templates/item.html!}
```

### Template Context Değerleri { #template-context-values }

Şu HTML içeriğinde:

{% raw %}

```jinja
Item ID: {{ id }}
```

{% endraw %}

...gösterilecek olan `id`, sizin "context" olarak ilettiğiniz `dict` içinden alınır:

```Python
{"id": id}
```

Örneğin ID değeri `42` ise, şu şekilde render edilir:

```html
Item ID: 42
```

### Template `url_for` Argümanları { #template-url-for-arguments }

Template içinde `url_for()` da kullanabilirsiniz; argüman olarak, *path operation function*'ınızın kullandığı argümanların aynısını alır.

Dolayısıyla şu bölüm:

{% raw %}

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

{% endraw %}

...*path operation function* olan `read_item(id=id)` tarafından handle edilecek URL'nin aynısına bir link üretir.

Örneğin ID değeri `42` ise, şu şekilde render edilir:

```html
<a href="/items/42">
```

## Template'ler ve statik dosyalar { #templates-and-static-files }

Template içinde `url_for()` kullanabilir ve örneğin `name="static"` ile mount ettiğiniz `StaticFiles` ile birlikte kullanabilirsiniz.

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

Bu örnekte, şu şekilde `static/styles.css` konumundaki bir CSS dosyasına link verir:

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

Ve `StaticFiles` kullandığınız için, bu CSS dosyası **FastAPI** uygulamanız tarafından `/static/styles.css` URL'sinde otomatik olarak servis edilir.

## Daha fazla detay { #more-details }

Template'leri nasıl test edeceğiniz dahil daha fazla detay için <a href="https://www.starlette.dev/templates/" class="external-link" target="_blank">Starlette'in template dokümantasyonuna</a> bakın.
