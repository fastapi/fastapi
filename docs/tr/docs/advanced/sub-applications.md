# Alt Uygulamalar - Mount İşlemi { #sub-applications-mounts }

Kendi bağımsız OpenAPI şemaları ve kendi dokümantasyon arayüzleri olan iki bağımsız FastAPI uygulamasına ihtiyacınız varsa, bir ana uygulama oluşturup bir (veya daha fazla) alt uygulamayı "mount" edebilirsiniz.

## Bir **FastAPI** uygulamasını mount etmek { #mounting-a-fastapi-application }

"Mount" etmek, belirli bir path altında tamamen "bağımsız" bir uygulamayı eklemek anlamına gelir. Ardından o path’in altındaki her şeyi, alt uygulamada tanımlanan _path operation_’lar ile o alt uygulama yönetir.

### Üst seviye uygulama { #top-level-application }

Önce ana, üst seviye **FastAPI** uygulamasını ve onun *path operation*’larını oluşturun:

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[3, 6:8] *}

### Alt uygulama { #sub-application }

Sonra alt uygulamanızı ve onun *path operation*’larını oluşturun.

Bu alt uygulama da standart bir FastAPI uygulamasıdır; ancak "mount" edilecek olan budur:

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[11, 14:16] *}

### Alt uygulamayı mount edin { #mount-the-sub-application }

Üst seviye uygulamanızda (`app`), alt uygulama `subapi`’yi mount edin.

Bu örnekte `/subapi` path’ine mount edilecektir:

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[11, 19] *}

### Otomatik API dokümanlarını kontrol edin { #check-the-automatic-api-docs }

Şimdi dosyanızla birlikte `fastapi` komutunu çalıştırın:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Ardından <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> adresinden dokümanları açın.

Ana uygulama için otomatik API dokümanlarını göreceksiniz; yalnızca onun kendi _path operation_’larını içerir:

<img src="/img/tutorial/sub-applications/image01.png">

Sonra alt uygulamanın dokümanlarını <a href="http://127.0.0.1:8000/subapi/docs" class="external-link" target="_blank">http://127.0.0.1:8000/subapi/docs</a> adresinden açın.

Alt uygulama için otomatik API dokümanlarını göreceksiniz; yalnızca onun kendi _path operation_’larını içerir ve hepsi doğru alt-path öneki `/subapi` altında yer alır:

<img src="/img/tutorial/sub-applications/image02.png">

İki arayüzden herhangi biriyle etkileşime girmeyi denerseniz doğru şekilde çalıştıklarını görürsünüz; çünkü tarayıcı her bir uygulama ya da alt uygulama ile ayrı ayrı iletişim kurabilir.

### Teknik Detaylar: `root_path` { #technical-details-root-path }

Yukarıda anlatıldığı gibi bir alt uygulamayı mount ettiğinizde FastAPI, ASGI spesifikasyonundaki `root_path` adlı bir mekanizmayı kullanarak alt uygulamaya mount path’ini iletmeyi otomatik olarak yönetir.

Bu sayede alt uygulama, dokümantasyon arayüzü için o path önekini kullanması gerektiğini bilir.

Ayrıca alt uygulamanın kendi mount edilmiş alt uygulamaları da olabilir; FastAPI tüm bu `root_path`’leri otomatik olarak yönettiği için her şey doğru şekilde çalışır.

`root_path` hakkında daha fazlasını ve bunu açıkça nasıl kullanacağınızı [Proxy Arkasında](behind-a-proxy.md){.internal-link target=_blank} bölümünde öğreneceksiniz.
