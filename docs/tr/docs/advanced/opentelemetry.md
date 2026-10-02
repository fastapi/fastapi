# OpenTelemetry { #opentelemetry }

API'niz çalışırken ne kadar trafik aldığını, hangi request'lerin yavaş olduğunu ve hataların ne zaman oluştuğunu bilmek isteyebilirsiniz.

**Telemetri**, uygulamanızın davranışı hakkında bu soruları yanıtlamanıza yardımcı olan verilerdir. Yaygın türleri şunlardır:

- **Metrikler**: Response süreleri ve işlenen request sayısı gibi zaman içinde özetleyebileceğiniz ölçümler.
- **Trace'ler**: Tek tek request'lerin ve bunları işlemek için gerçekleştirilen işlemlerin kayıtları. Süresi ölçülen her işleme **span** denir.
- **Log'lar**: Uygulamanın başlatılması veya bir işlemin başarısız olması gibi olayların zaman damgalı kayıtları.

[**OpenTelemetry**](https://opentelemetry.io/), telemetri verilerini toplamak ve bunları panolarda inceleyebileceğiniz bir izleme hizmetine göndermek için kullanılan standartlar ve araçlar bütünüdür.

**FastAPI, HTTP request trace'leri, metrikleri ve log'ları için varsayılan olarak OpenTelemetry desteği sunar**. WebSocket bağlantıları da trace ve log üretir. Bu verileri görmek için onları alacak bir izleme hizmeti yapılandırın.

## FastAPI'yi Yükleyin { #install-fastapi }

FastAPI'yi, telemetri göndermek için gereken paketleri içeren `standard` ek bağımlılıklarıyla yükleyin:

<div class="termy">

```console
$ uv add "fastapi[standard]"
---> 100%
```

</div>

## Uygulamayı Oluşturun { #create-the-app }

`main.py` adlı bir dosya oluşturun:

{* ../../docs_src/opentelemetry/tutorial001_py310.py *}

Her şeyin varsayılan olarak çalıştığına dikkat edin; telemetrinin çalışması için özel bir kod yazmanız gerekmez.

## FastAPI Cloud { #fastapi-cloud }

Uygulamanızı `fastapi[standard]` ile [FastAPI Cloud](https://fastapicloud.com)'a dağıttığınızda metrikler otomatik olarak çalışır. Başka bir yapılandırma yapmanız gerekmez.

Pro planlarında request sayılarını, hata oranlarını ve response sürelerini [Metrikler panosunda](https://fastapicloud.com/docs/monitoring-and-performance/metrics/) görüntüleyebilirsiniz.

<img src="/img/tutorial/opentelemetry/image01.png" alt="Örnek veriler içeren FastAPI Cloud Pro metrikler panosu">

## Diğer İzleme Hizmetleri { #other-monitoring-services }

Telemetri verilerini başka bir izleme hizmetine göndermek için OpenTelemetry'nin telemetri gönderme protokolü olan **OTLP**'yi kabul eden bir endpoint yapılandırın. Hizmetin HTTP/protobuf temel endpoint'ini kullanın.

Örnek URL'yi kendi endpoint'inizle değiştirerek şu ortam değişkenlerini ayarlayın:

```bash
export OTEL_SERVICE_NAME=my-api
export OTEL_EXPORTER_OTLP_ENDPOINT=https://collector.example.com
```

`OTEL_SERVICE_NAME`, izleme hizmetinde uygulamanızı tanımlar. Endpoint, verilerin alınacağı temel URL'dir. Trace'ler bu URL altındaki `/v1/traces` adresine, metrikler `/v1/metrics` adresine ve log'lar `/v1/logs` adresine gönderilir.

Hizmetiniz kimlik doğrulaması gerektiriyorsa `OTEL_EXPORTER_OTLP_HEADERS` değerini, hizmetin belirttiği header'lara göre ayarlayın. Örneğin: `api-key=YOUR_API_KEY`.

## Uygulamayı Çalıştırın { #run-the-app }

Uygulamayı aynı terminalde başlatın:

<div class="termy">

```console
$ uv run fastapi run
```

</div>

Başka bir terminalden bir request gönderin:

```console
$ curl http://127.0.0.1:8000/items/1
{"item_id":1}
```

İzleme hizmetinizi açıp `my-api` uygulamasını bulun. Bir sonraki veri aktarımından sonra `GET /items/{item_id}` span'i içeren bir trace ile birlikte request sayısı, response süresi ve etkin request metriklerini görebilirsiniz.

## Telemetriyi Özelleştirin { #customize-telemetry }

### Provider ve Exporter'ları Yapılandırın { #configure-providers-and-exporters }

**Provider** (sağlayıcı), trace, metrik veya log kaydeden nesneleri sağlar. Yapılandırması, bu verilerin nasıl işleneceğini ve dışa aktarılacağını belirler.

Telemetri kütüphaneleri, OpenTelemetry'nin global provider'larını yapılandırabilir. Kütüphaneyi uygulama başlamadan önce yapılandırın; FastAPI bu provider'ları otomatik olarak kullanır.

Ortam değişkenlerinde bir OTLP endpoint'i ayarlandığında FastAPI, etkin olan her provider'a bu hedef için bir exporter ekler. Mevcut exporter'lar kendi hedeflerine veri göndermeye devam eder.

Her hedefi yalnızca bir kez yapılandırın. Ortam değişkenlerinde belirtilen hedefe gönderimi zaten başka bir kütüphane yönetiyorsa o kütüphanenin bu hedefe veri aktarımını devre dışı bırakın veya FastAPI'nin otomatik yapılandırmasını kapatın:

```python
app = FastAPI(telemetry={"auto_configure": False})
```

Ayrıca `telemetry` sözlüğünde doğrudan bir provider da iletebilirsiniz. Örneğin aşağıdaki provider, request span'lerini terminalinize yazdırmak için OpenTelemetry'nin konsol exporter'ını kullanır:

{* ../../docs_src/opentelemetry/tutorial002_py310.py hl[2:8] *}

**Exporter** (dışa aktarıcı), span'leri hedeflerine gönderir. `BatchSpanProcessor`, span'leri gruplandırıp arka planda gönderir. İzleme kütüphanenizin hedefini kullanmak için konsol exporter'ını, o kütüphanenin sağladığı bir exporter ile değiştirin. Daha fazla yapılandırma seçeneği için [OpenTelemetry'nin Python enstrümantasyon rehberine](https://opentelemetry.io/docs/languages/python/instrumentation/) bakın.

Bir metrik veya log provider'ı sağlamak için aynı sözlükte `meter_provider` ya da `logger_provider` kullanın. Provider'ın kapatılmasını, onu oluşturan uygulama veya kütüphane yönetir. FastAPI ise kendisinin eklediği dışa aktarma bileşenlerini yönetir.

/// warning | Uyarı

OpenTelemetry varsayılan olarak global provider'ları kullanır. [Bağlanan alt uygulamalar](sub-applications.md) için bağımsız telemetri yapılandırması garanti edilmez.

///

### Request İşlemlerini İzleyin { #trace-request-operations }

Varsayılan olarak request trace'leri; bağımlılıkların çözümlenmesi, path işlemi fonksiyonunuzun çalıştırılması, response'un serileştirilmesi ve FastAPI'nin `BackgroundTasks` sınıfındaki her görevin çalıştırılması için span'ler içerir. Bu span'ler aynı provider ve exporter'ları kullanır.

Arka plan görevlerinin span'leri, request'in trace'inin bir parçası olmaya devam eder. HTTP response span'i bittikten sonra çalıştıkları için ölçülen response süresini artırmazlar.

Yalnızca HTTP request span'ini kaydetmek için `operation_spans` değerini `False` olarak ayarlayın:

{* ../../docs_src/opentelemetry/tutorial003_py310.py hl[3] *}


### WebSocket Bağlantılarını İzleyin { #trace-websocket-connections }

Her WebSocket bağlantısının, handler'ı ve bağımlılık temizliğini kapsayan `WS /ws/{room}` gibi bir span'i vardır. Bağımlılık çözümleme ve endpoint'in çalıştırılması için kullanılan `operation_spans` dahil olmak üzere aynı provider'ları ve ayarları kullanır.

HTTP request metrikleri yalnızca HTTP request'lerini kapsar. `1000` veya `1001` kodlarıyla normal şekilde sonlanan WebSocket bağlantıları hata log'u üretmez.

### Hataları İnceleyin { #inspect-errors }

FastAPI, yakalanmamış istisnaları request'in veya bağlantının trace'iyle ilişkilendirilmiş OpenTelemetry log'ları olarak kaydeder. Trace örneklemeye dahil edilmese bile hata log'ları kaydedilir.

İstisna log'ları; istisnanın türünü, mesajını ve stack trace'ini içerir. Mesajlar ve stack trace'ler hassas bilgiler içerebilir. Bunları filtrelemek veya hassas bilgileri maskelemek için provider'ınızın log işlemcilerini kullanın ya da bu log'ları devre dışı bırakmak için `logs` değerini `False` olarak ayarlayın.

FastAPI, request doğrulama hatalarını da route ve hata sayısını içeren uyarı log'ları olarak kaydeder. Bu log'lar geçersiz girdiyi içermez.

## Nelerin Kaydedileceğini Seçin { #choose-what-to-record }

`telemetry` sözlüğü şu ayarları da kabul eder:

| Ayar | Amaç | Varsayılan |
| --- | --- | --- |
| `tracing` | HTTP request ve WebSocket bağlantı span'lerini kaydetmek | `True` |
| `metrics` | HTTP request metriklerini kaydetmek | `True` |
| `logs` | Doğrulama hatalarını ve yakalanmamış istisnaları kaydetmek | `True` |
| `operation_spans` | Request işlemleri için span eklemek | `True` |
| `exclude` | ASGI scope'unu alan bir fonksiyon `True` döndürdüğünde request'leri atlamak | `None` |
| `auto_configure` | Ortam değişkenlerinde ayarlanan endpoint'ler için exporter eklemek | `True` |

Örneğin, sağlık kontrollerini hariç tutarak metrik toplamak için:

```python
from fastapi import FastAPI

app = FastAPI(
    telemetry={
        "tracing": False,
        "exclude": lambda scope: scope["path"] == "/health",
    }
)
```

Uygulamanız provider kurulumunu kendisi yönetiyorsa, örneğin lifespan fonksiyonu içinde yapıyorsa, `auto_configure` değerini `False` olarak ayarlayın.
