# OpenTelemetry { #opentelemetry }

API'niz çalışırken ne kadar trafik aldığını, hangi request'lerin yavaş olduğunu ve hataların ne zaman oluştuğunu bilmek isteyebilirsiniz.

**Telemetri**, uygulamanızın davranışı hakkında bu soruları yanıtlamanıza yardımcı olan verilerdir. Yaygın türleri şunlardır:

- **Metrics**: response süreleri ve işlenen request sayısı gibi zaman içinde özetleyebileceğiniz ölçümler.
- **Traces**: tekil request'lerin ve bu request'leri işlemek için yapılan operasyonların kayıtları. Zamanı ölçülen her operasyona **span** denir.
- **Logs**: bir uygulamanın başlatılması veya bir operasyonun başarısız olması gibi olayların zaman damgalı kayıtları.

[**OpenTelemetry**](https://opentelemetry.io/), telemetri toplamak ve bunları dashboard'larda inceleyebileceğiniz bir monitoring servisine göndermek için kullanılan standartlar ve araçlar kümesidir.

**FastAPI, HTTP request trace'leri, metrics ve log'lar için varsayılan olarak OpenTelemetry desteği sağlar**. WebSocket bağlantıları da trace ve log sağlar. Bu verileri görmek için bunları alacak bir monitoring servisi yapılandırın.

## FastAPI'yi Kurun { #install-fastapi }

FastAPI'yi, telemetri göndermek için gereken paketleri içeren `standard` extras ile kurun:

<div class="termy">

```console
$ uv add "fastapi[standard]"
---> 100%
```

</div>

## Uygulamayı Oluşturun { #create-the-app }

`main.py` adında bir dosya oluşturun:

{* ../../docs_src/opentelemetry/tutorial001_py310.py *}

Her şeyin varsayılan olarak çalıştığına dikkat edin; telemetrinin çalışması için özel bir kod yazmanız gerekmez.

## FastAPI Cloud { #fastapi-cloud }

`fastapi[standard]` ile [FastAPI Cloud](https://fastapicloud.com)'a deploy ettiğinizde metrics otomatik olarak çalışır. Başka bir şey yapılandırmanız gerekmez.

Pro planlarda request sayılarını, hata oranlarını ve response sürelerini [Metrics dashboard](https://fastapicloud.com/docs/monitoring-and-performance/metrics/)'unda görüntüleyebilirsiniz.

<img src="/img/tutorial/opentelemetry/image01.png" alt="Örnek verilerle FastAPI Cloud Pro metrics dashboard'u">

## Diğer Monitoring Servisleri { #other-monitoring-services }

Telemetriyi başka bir monitoring servisine göndermek için, telemetri göndermeye yönelik OpenTelemetry protokolü olan **OTLP**'yi kabul eden bir endpoint yapılandırın. Servisin HTTP/protobuf base endpoint'ini kullanın.

Örnek URL'yi kendi endpoint'inizle değiştirerek şu ortam değişkenlerini ayarlayın:

```bash
export OTEL_SERVICE_NAME=my-api
export OTEL_EXPORTER_OTLP_ENDPOINT=https://collector.example.com
```

`OTEL_SERVICE_NAME`, monitoring servisinde uygulamanızı tanımlar. Endpoint, verileri almak için kullanılan base URL'dir. Trace'ler bu URL altında `/v1/traces`'e, metrics `/v1/metrics`'e ve log'lar `/v1/logs`'a gönderilir.

Servisiniz kimlik doğrulama gerektiriyorsa `OTEL_EXPORTER_OTLP_HEADERS` değerini servisin belirttiği header'lara ayarlayın, örneğin `api-key=YOUR_API_KEY`.

## Uygulamayı Çalıştırın { #run-the-app }

Uygulamayı aynı terminalde başlatın:

<div class="termy">

```console
$ uv run fastapi run
```

</div>

Başka bir terminalde bir request gönderin:

```console
$ curl http://127.0.0.1:8000/items/1
{"item_id":1}
```

Monitoring servisinizi açın ve `my-api`'yi bulun. Bir sonraki export'tan sonra, request sayıları, response süresi ve aktif request'ler için metrics ile birlikte `GET /items/{item_id}` span'ine sahip bir trace görebilirsiniz.

## Telemetriyi Özelleştirin { #customize-telemetry }

### Provider ve Exporter'ları Yapılandırın { #configure-providers-and-exporters }

Bir **provider**, trace'leri, metrics'i veya log'ları kaydeden nesneleri sağlar. Yapılandırması, bu verilerin nasıl işlendiğini ve export edildiğini kontrol eder.

Telemetri kütüphaneleri OpenTelemetry'nin global provider'larını yapılandırabilir. Kütüphaneyi uygulama başlamadan önce yapılandırın; FastAPI bu provider'ları otomatik olarak kullanır.

Ortamda bir OTLP endpoint ayarlandığında FastAPI, etkin olan her provider'a bu hedef için bir exporter ekler. Mevcut exporter'lar verileri kendi hedeflerine göndermeye devam eder.

Her hedefi bir kez yapılandırın. Başka bir kütüphane ortam hedefini zaten yönetiyorsa, onun ortam export'unu devre dışı bırakın veya FastAPI'nin otomatik kurulumunu kapatın:

```python
app = FastAPI(telemetry={"auto_configure": False})
```

Ayrıca `telemetry` sözlüğüne doğrudan bir provider da verebilirsiniz. Örneğin bu provider, request span'lerini terminalinizde yazdırmak için OpenTelemetry'nin console exporter'ını kullanır:

{* ../../docs_src/opentelemetry/tutorial002_py310.py hl[2:8] *}

**Exporter**, span'leri hedeflerine gönderir. `BatchSpanProcessor`, span'leri gruplar ve arka planda gönderir. Kendi hedefini kullanmak için console exporter'ı monitoring kütüphanenizin sağladığı exporter ile değiştirin. Daha fazla yapılandırma seçeneği için [OpenTelemetry'nin Python instrumentation rehberine](https://opentelemetry.io/docs/languages/python/instrumentation/) bakın.

Metrics veya log provider'ı sağlamak için aynı sözlükte `meter_provider` ya da `logger_provider` kullanın. Bir provider oluşturan uygulama veya kütüphane, onun kapatılmasını yönetir. FastAPI ise eklediği export bileşenlerini yönetir.

/// warning | Uyarı

OpenTelemetry varsayılan olarak global provider'lar kullanır. [Mount edilmiş alt uygulamalar](sub-applications.md) için bağımsız telemetri yapılandırması garanti edilmez.

///

### Request İşlemlerini Trace Edin { #trace-request-operations }

Varsayılan olarak request trace'leri; bağımlılıkları çözme, path operation fonksiyonunuzu çalıştırma, response'u serialize etme ve FastAPI'nin `BackgroundTasks` içindeki her görevi çalıştırma için span'ler içerir. Bu span'ler aynı provider ve exporter'ları kullanır.

Background task span'leri request'in trace'inin parçası olarak kalır. HTTP response span'i bittikten sonra çalışırlar, bu yüzden ölçülen response süresini artırmazlar.

Yalnızca HTTP request span'ini kaydetmek için `operation_spans` değerini `False` olarak ayarlayın:

{* ../../docs_src/opentelemetry/tutorial003_py310.py hl[3] *}


### WebSocket Bağlantılarını Trace Edin { #trace-websocket-connections }

Her WebSocket bağlantısının, handler'ı ve bağımlılık temizliğini kapsayan `WS /ws/{room}` gibi bir span'i vardır. Bağımlılık çözümleme ve endpoint çalıştırma için `operation_spans` dahil olmak üzere aynı provider'ları ve ayarları kullanır.

HTTP request metrics yalnızca HTTP request'leri kapsar. `1000` veya `1001` kodlarıyla yapılan normal WebSocket bağlantı kesmeleri error log üretmez.

### Hataları İnceleyin { #inspect-errors }

FastAPI, yakalanmamış exception'ları OpenTelemetry log'ları olarak kaydeder ve bunları request'in veya bağlantının trace'ine bağlar. Error log'ları, trace sample edilmediğinde bile kaydedilir.

Exception log'ları exception'ın türünü, mesajını ve stack trace'ini içerir. Mesajlar ve stack trace'ler hassas bilgiler içerebilir. Bunları filtrelemek veya maskelemek için provider'ınızın log processor'larını kullanın ya da bu log'ları devre dışı bırakmak için `logs` değerini `False` olarak ayarlayın.

FastAPI ayrıca request validation hatalarını route ve hata sayısı ile birlikte warning log'ları olarak kaydeder. Bu log'lar geçersiz input'u içermez.

## Nelerin Kaydedileceğini Seçin { #choose-what-to-record }

`telemetry` sözlüğü şu ayarları da kabul eder:

| Ayar | Amaç | Varsayılan |
| --- | --- | --- |
| `tracing` | HTTP request ve WebSocket bağlantısı span'lerini kaydeder | `True` |
| `metrics` | HTTP request metrics kaydeder | `True` |
| `logs` | Validation hatalarını ve yakalanmamış exception'ları kaydeder | `True` |
| `operation_spans` | Request işlemleri için span'ler ekler | `True` |
| `exclude` | ASGI scope'u alan bir fonksiyon `True` döndürdüğünde request'leri atlar | `None` |
| `auto_configure` | Ortam değişkenlerinde ayarlanan endpoint'ler için exporter'lar ekler | `True` |

Örneğin health check'leri hariç tutarken metrics toplamak için:

```python
from fastapi import FastAPI

app = FastAPI(
    telemetry={
        "tracing": False,
        "exclude": lambda scope: scope["path"] == "/health",
    }
)
```

Uygulamanız provider kurulumunu kendisi yönetiyorsa, örneğin lifespan fonksiyonu içinde, `auto_configure` değerini `False` olarak ayarlayın.
