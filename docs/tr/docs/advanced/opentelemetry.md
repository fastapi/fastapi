# OpenTelemetry { #opentelemetry }

API'niz çalışırken ne kadar trafik aldığını, hangi isteklerin yavaş yanıt verdiğini ve hataların ne zaman meydana geldiğini bilmek isteyebilirsiniz.

**Telemetri**, bu soruları yanıtlamanıza yardımcı olan ve uygulamanızın davranışına ilişkin verilerdir. Yaygın türleri şunlardır:

- **Metrikler (Metrics)**: Yanıt süreleri ve işlenen istek sayısı gibi zaman içinde özetleyebileceğiniz ölçümlerdir.
- **İzler (Traces)**: Tekil isteklerin ve bunları işlemek için gerçekleştirilen işlemlerin kayıtlarıdır. Süresi ölçülen her işleme bir **span (aralık)** denir.
- **Günlükler (Logs)**: Bir uygulamanın başlatılması veya bir işlemin başarısız olması gibi olayların zaman damgalı kayıtlarıdır.

[**OpenTelemetry**](https://opentelemetry.io/), telemetri verilerini toplamak ve panolarda inceleyebileceğiniz bir izleme servisine göndermek için kullanılan standartlar ve araçlar bütünüdür.

**FastAPI, varsayılan olarak OpenTelemetry desteği sunar**; bu destek HTTP istek izlerini, metrikleri ve günlükleri kapsar. WebSocket bağlantıları da izler ve günlükler sağlar. Bu verileri görmek için bunları alacak bir izleme servisi yapılandırmanız yeterlidir.

## FastAPI'ı Kurun { #install-fastapi }

Telemetri verilerini göndermek için gerekli paketleri içeren `standard` ek paketleriyle FastAPI'ı kurun:

<div class="termy">

```console
$ uv add "fastapi[standard]"
---> 100%
```

</div>

## Uygulamayı Oluşturun { #create-the-app }

Bir `main.py` dosyası oluşturun:

{* ../../docs_src/opentelemetry/tutorial001_py310.py *}

Her şeyin varsayılan olarak çalıştığına dikkat edin; telemetrinin çalışması için herhangi bir özel kod yazmanıza gerek yoktur.

## FastAPI Cloud { #fastapi-cloud }

`fastapi[standard]` ile [FastAPI Cloud](https://fastapicloud.com)'a dağıtım yaptığınızda, metrikler otomatik olarak çalışır. Başka hiçbir şey yapılandırmanız gerekmez.

Pro planlarda istek sayılarını, hata oranlarını ve yanıt sürelerini [Metrikler panosunda](https://fastapicloud.com/docs/monitoring-and-performance/metrics/) görüntüleyebilirsiniz.

<img src="/img/tutorial/opentelemetry/image01.png" alt="FastAPI Cloud Pro metrik paneli örnek verilerle">

## Diğer İzleme Servisleri { #other-monitoring-services }

Telemetri verilerini başka bir izleme servisine göndermek için, telemetri gönderiminde OpenTelemetry protokolü olan **OTLP**'yi kabul eden bir uç nokta (endpoint) yapılandırın. Servisin HTTP/protobuf temel uç noktasını kullanın.

Örnek URL'yi kendi uç noktanızla değiştirerek şu ortam değişkenlerini ayarlayın:

```bash
export OTEL_SERVICE_NAME=my-api
export OTEL_EXPORTER_OTLP_ENDPOINT=https://collector.example.com
```

`OTEL_SERVICE_NAME`, uygulamanızı izleme servisinde tanımlar. Uç nokta ise veri alımı için temel URL'dir. İzler `/v1/traces`, metrikler `/v1/metrics` ve günlükler bu URL altındaki `/v1/logs` yoluna gönderilir.

Servisiniz kimlik doğrulama gerektiriyorsa, `OTEL_EXPORTER_OTLP_HEADERS` değişkenini servisin belirttiği başlıklara göre ayarlayın; örneğin `api-key=YOUR_API_KEY`.

## Uygulamayı Çalıştırın { #run-the-app }

Uygulamayı aynı terminalde başlatın:

<div class="termy">

```console
$ uv run fastapi run
```

</div>

Başka bir terminalde bir istek gönderin:

```console
$ curl http://127.0.0.1:8000/items/1
{"item_id":1}
```

İzleme servisinizi açın ve `my-api` uygulamasını bulun. Bir sonraki dışa aktarımdan sonra, istek sayıları, yanıt süresi ve etkin isteklere ilişkin metriklerin yanı sıra `GET /items/{item_id}` span'ine sahip bir iz görebilirsiniz.

## Telemetriyi Özelleştirin { #customize-telemetry }

### Sağlayıcıları ve Dışa Aktarıcıları Yapılandırın { #configure-providers-and-exporters }

Bir **sağlayıcı (provider)**, izleri, metrikleri veya günlükleri kaydeden nesneleri sunar. Yapılandırması, bu verilerin nasıl işleneceğini ve dışa aktarılacağını denetler.

Telemetri kütüphaneleri, OpenTelemetry'nin genel sağlayıcılarını yapılandırabilir. Kütüphaneyi uygulama başlamadan önce yapılandırırsanız, FastAPI bu sağlayıcıları otomatik olarak kullanır.

Ortamda bir OTLP uç noktası belirlendiğinde, FastAPI etkinleştirilmiş her sağlayıcıya bu hedef için bir dışa aktarıcı (exporter) ekler. Mevcut dışa aktarıcılar verileri kendi hedeflerine göndermeye devam eder.

Her hedefi bir kez yapılandırın. Başka bir kütüphane ortam hedefini zaten yönetiyorsa, ortam dışa aktarımını devre dışı bırakın veya FastAPI'ın otomatik kurulumunu kapatın:

```python
app = FastAPI(telemetry={"auto_configure": False})
```

Ayrıca bir sağlayıcıyı doğrudan `telemetry` sözlüğünde iletebilirsiniz. Örneğin, bu sağlayıcı istek span'lerini terminalinize yazdırmak için OpenTelemetry'nin konsol dışa aktarıcısını kullanır:

{* ../../docs_src/opentelemetry/tutorial002_py310.py hl[2:8] *}

**Dışa aktarıcı (exporter)**, span'leri hedeflerine gönderir. `BatchSpanProcessor`, span'leri gruplar ve arka planda gönderir. Hedefini kullanmak için konsol dışa aktarıcısını izleme kütüphanenizin sağladığı bir dışa aktarıcıyla değiştirin. Daha fazla yapılandırma seçeneği için [OpenTelemetry'nin Python enstrümantasyon kılavuzuna](https://opentelemetry.io/docs/languages/python/instrumentation/) bakın.

Bir metrik veya günlük sağlayıcısı tanımlamak için aynı sözlükte `meter_provider` veya `logger_provider` kullanın. Sağlayıcıyı oluşturan uygulama veya kütüphane, sağlayıcının kapatılmasını yönetir. FastAPI eklediği dışa aktarım bileşenlerini yönetir.

/// warning

OpenTelemetry varsayılan olarak genel sağlayıcılar kullanır. [Bağlanmış alt uygulamalar](sub-applications.md) için bağımsız telemetri yapılandırması garanti edilmez.

///

### İstek İşlemlerini İzleyin { #trace-request-operations }

Varsayılan olarak istek izleri; bağımlılıkların çözümlenmesi, yol operasyon fonksiyonunuzun çalıştırılması, yanıtın serileştirilmesi ve FastAPI'ın `BackgroundTasks` içindeki her görevin çalıştırılması için span'ler içerir. Bu span'ler aynı sağlayıcıyı ve dışa aktarıcıları kullanır.

Arka plan görevi span'leri, isteğin izinin bir parçası olarak kalır. HTTP yanıt span'i sona erdikten sonra çalışırlar, bu nedenle ölçülen yanıt süresini artırmazlar.

Yalnızca HTTP istek span'ini kaydetmek için `operation_spans` değerini `False` olarak ayarlayın:

{* ../../docs_src/opentelemetry/tutorial003_py310.py hl[3] *}


### WebSocket Bağlantılarını İzleyin { #trace-websocket-connections }

Her WebSocket bağlantısı, işleyiciyi ve bağımlılık temizliğini kapsayan `WS /ws/{room}` gibi bir span'e sahiptir. Bağımlılık çözümlemesi ve uç nokta yürütmesi için `operation_spans` dahil olmak üzere aynı sağlayıcıları ve ayarları kullanır.

HTTP istek metrikleri yalnızca HTTP isteklerini kapsar. `1000` veya `1001` kodlarıyla gerçekleşen normal WebSocket bağlantı kesintileri hata günlüğü oluşturmaz.

### Hataları İnceleyin { #inspect-errors }

FastAPI, işlenmeyen istisnaları (unhandled exceptions) isteğin veya bağlantının izine bağlı OpenTelemetry günlükleri olarak kaydeder. Hata günlükleri, iz örneklenmemiş olsa bile kaydedilir.

İstisna günlükleri, istisnanın türünü, mesajını ve yığın izini (stack trace) içerir. Mesajlar ve yığın izleri hassas bilgiler barındırabilir. Bunları filtrelemek veya gizlemek için sağlayıcınızın günlük işleyicilerini kullanın ya da bu günlükleri devre dışı bırakmak için `logs` ayarını `False` yapın.

FastAPI ayrıca istek doğrulama hatalarını yol ve hata sayısıyla birlikte uyarı günlüğü olarak kaydeder. Bu günlükler geçersiz girdiyi içermez.

## Nelerin Kaydedileceğini Seçin { #choose-what-to-record }

`telemetry` sözlüğü ayrıca şu ayarları kabul eder:

| Ayar | Amaç | Varsayılan |
| --- | --- | --- |
| `tracing` | HTTP isteği ve WebSocket bağlantı span'lerini kaydeder | `True` |
| `metrics` | HTTP istek metriklerini kaydeder | `True` |
| `logs` | Doğrulama hatalarını ve işlenmeyen istisnaları kaydeder | `True` |
| `operation_spans` | İstek işlemleri için span'ler ekler | `True` |
| `exclude` | ASGI kapsamını (scope) alan bir fonksiyon `True` döndürdüğünde istekleri atlar | `None` |
| `auto_configure` | Ortam değişkenlerinde belirlenen uç noktalar için dışa aktarıcılar ekler | `True` |

Örneğin, sistem durumu kontrollerini (health checks) hariç tutarak metrik toplamak için:

```python
from fastapi import FastAPI

app = FastAPI(
    telemetry={
        "tracing": False,
        "exclude": lambda scope: scope["path"] == "/health",
    }
)
```

Uygulamanız sağlayıcı kurulumunu kendi içinde (örneğin lifespan fonksiyonunda) yönettiğinde `auto_configure` değerini `False` olarak ayarlayın.
