# OpenTelemetry { #opentelemetry }

जब आपकी API चल रही हो, तो आप जानना चाह सकते हैं कि उसे कितना traffic मिल रहा है, कौन-से requests धीमे हैं, और errors कब होते हैं।

**Telemetry** आपके application के व्यवहार के बारे में data है, जो इन सवालों के जवाब देने में मदद करता है। सामान्य प्रकारों में शामिल हैं:

- **Metrics**: ऐसे measurements जिन्हें आप समय के साथ summarize कर सकते हैं, जैसे response times और संभाले जा रहे requests की संख्या।
- **Traces**: अलग-अलग requests और उन्हें handle करने के लिए किए गए operations के records। हर timed operation को **span** कहा जाता है।
- **Logs**: events के timestamped records, जैसे किसी application का शुरू होना या किसी operation का fail होना।

[**OpenTelemetry**](https://opentelemetry.io/) standards और tools का एक set है, जो telemetry collect करने और उसे monitoring service को भेजने के लिए है, जहाँ आप dashboards में उसे explore कर सकते हैं।

**FastAPI HTTP request traces, metrics, और logs के लिए default रूप से OpenTelemetry support प्रदान करता है**। WebSocket connections भी traces और logs प्रदान करते हैं। उस data को देखने के लिए, उसे receive करने हेतु monitoring service configure करें।

## FastAPI install करें { #install-fastapi }

FastAPI को `standard` extras के साथ install करें, जिनमें telemetry भेजने के लिए packages शामिल होते हैं:

<div class="termy">

```console
$ uv add "fastapi[standard]"
---> 100%
```

</div>

## App बनाएँ { #create-the-app }

`main.py` file बनाएँ:

{* ../../docs_src/opentelemetry/tutorial001_py310.py *}

ध्यान दें कि यह सब default रूप से काम करता है, telemetry को काम करने के लिए आपको कोई custom code लिखने की ज़रूरत नहीं है।

## FastAPI Cloud { #fastapi-cloud }

जब आप `fastapi[standard]` के साथ [FastAPI Cloud](https://fastapicloud.com) पर deploy करते हैं, तो metrics अपने आप काम करते हैं। आपको और कुछ configure करने की ज़रूरत नहीं होती।

Pro plans पर, आप [Metrics dashboard](https://fastapicloud.com/docs/monitoring-and-performance/metrics/) में request counts, error rates, और response times देख सकते हैं।

<img src="/img/tutorial/opentelemetry/image01.png" alt="उदाहरण data के साथ FastAPI Cloud Pro metrics dashboard">

## अन्य monitoring services { #other-monitoring-services }

Telemetry को किसी दूसरी monitoring service पर भेजने के लिए, ऐसा endpoint configure करें जो **OTLP** accept करता हो, जो telemetry भेजने के लिए OpenTelemetry protocol है। Service का HTTP/protobuf base endpoint इस्तेमाल करें।

इन environment variables को set करें, example URL को अपने endpoint से बदलते हुए:

```bash
export OTEL_SERVICE_NAME=my-api
export OTEL_EXPORTER_OTLP_ENDPOINT=https://collector.example.com
```

`OTEL_SERVICE_NAME` monitoring service में आपकी app को identify करता है। Endpoint data receive करने के लिए base URL है। उस URL के अंतर्गत traces `/v1/traces` पर, metrics `/v1/metrics` पर, और logs `/v1/logs` पर भेजे जाते हैं।

अगर आपकी service को authentication चाहिए, तो `OTEL_EXPORTER_OTLP_HEADERS` को उसके द्वारा specify किए गए headers पर set करें, उदाहरण के लिए `api-key=YOUR_API_KEY`।

## App चलाएँ { #run-the-app }

उसी terminal में app start करें:

<div class="termy">

```console
$ uv run fastapi run
```

</div>

किसी दूसरे terminal में, एक request भेजें:

```console
$ curl http://127.0.0.1:8000/items/1
{"item_id":1}
```

अपनी monitoring service खोलें और `my-api` खोजें। अगले export के बाद, आप `GET /items/{item_id}` span वाला trace देख सकते हैं, साथ में request counts, response duration, और active requests के metrics भी।

## Telemetry customize करें { #customize-telemetry }

### Providers और exporters configure करें { #configure-providers-and-exporters }

एक **provider** वे objects प्रदान करता है जो traces, metrics, या logs record करते हैं। उसका configuration नियंत्रित करता है कि उस data को कैसे process और export किया जाता है।

Telemetry libraries OpenTelemetry के global providers configure कर सकती हैं। App start होने से पहले library configure करें, और FastAPI उन providers को automatically इस्तेमाल करता है।

जब environment में OTLP endpoint set होता है, तो FastAPI हर enabled provider में उस destination के लिए एक exporter जोड़ता है। Existing exporters अपने destinations पर data भेजना जारी रखते हैं।

हर destination को एक बार configure करें। अगर कोई दूसरी library पहले से environment destination handle कर रही है, तो उसका environment export disable करें या FastAPI का automatic setup बंद करें:

```python
app = FastAPI(telemetry={"auto_configure": False})
```

आप `telemetry` dictionary में सीधे provider भी pass कर सकते हैं। उदाहरण के लिए, यह provider आपके terminal में request spans print करने के लिए OpenTelemetry का console exporter इस्तेमाल करता है:

{* ../../docs_src/opentelemetry/tutorial002_py310.py hl[2:8] *}

**Exporter** spans को उनके destination तक भेजता है। `BatchSpanProcessor` spans को group करता है और उन्हें background में भेजता है। Console exporter को अपनी monitoring library द्वारा दिए गए exporter से बदलें ताकि उसका destination इस्तेमाल हो सके। अधिक configuration options के लिए [OpenTelemetry की Python instrumentation guide](https://opentelemetry.io/docs/languages/python/instrumentation/) देखें।

Metrics या logs provider देने के लिए उसी dictionary में `meter_provider` या `logger_provider` इस्तेमाल करें। Provider बनाने वाला application या library उसका shutdown manage करता है। FastAPI अपने द्वारा जोड़े गए export components manage करता है।

/// warning | चेतावनी

OpenTelemetry default रूप से global providers इस्तेमाल करता है। [Mounted sub-applications](sub-applications.md) के लिए independent telemetry configuration की guarantee नहीं है।

///

### Request operations trace करें { #trace-request-operations }

Default रूप से, request traces में dependencies resolve करने, आपकी path operation function चलाने, response serialize करने, और FastAPI के `BackgroundTasks` में हर task चलाने के लिए spans शामिल होते हैं। ये spans वही provider और exporters इस्तेमाल करते हैं।

Background task spans request के trace का हिस्सा बने रहते हैं। वे HTTP response span खत्म होने के बाद चलते हैं, इसलिए वे measured response time नहीं बढ़ाते।

केवल HTTP request span record करने के लिए, `operation_spans` को `False` पर set करें:

{* ../../docs_src/opentelemetry/tutorial003_py310.py hl[3] *}


### WebSocket connections trace करें { #trace-websocket-connections }

हर WebSocket connection में `WS /ws/{room}` जैसा एक span होता है, जो handler और dependency cleanup को cover करता है। यह वही providers और settings इस्तेमाल करता है, जिसमें dependency resolution और endpoint execution के लिए `operation_spans` शामिल है।

HTTP request metrics केवल HTTP requests को cover करते हैं। Codes `1000` या `1001` वाले normal WebSocket disconnects error logs produce नहीं करते।

### Errors inspect करें { #inspect-errors }

FastAPI unhandled exceptions को OpenTelemetry logs के रूप में record करता है, जो request या connection के trace से linked होते हैं। Error logs तब भी record किए जाते हैं जब trace sampled नहीं होता।

Exception logs में exception का type, message, और stack trace शामिल होता है। Messages और stack traces में sensitive information हो सकती है। उन्हें filter या redact करने के लिए अपने provider के log processors इस्तेमाल करें, या इन logs को disable करने के लिए `logs` को `False` पर set करें।

FastAPI request validation failures को warning logs के रूप में भी record करता है, जिसमें route और error count होता है। इन logs में invalid input शामिल नहीं होता।

## चुनें कि क्या record करना है { #choose-what-to-record }

`telemetry` dictionary ये settings भी accept करती है:

| Setting | उद्देश्य | Default |
| --- | --- | --- |
| `tracing` | HTTP request और WebSocket connection spans record करें | `True` |
| `metrics` | HTTP request metrics record करें | `True` |
| `logs` | Validation failures और unhandled exceptions record करें | `True` |
| `operation_spans` | Request operations के लिए spans जोड़ें | `True` |
| `exclude` | जब ASGI scope receive करने वाली function `True` return करे, तो requests skip करें | `None` |
| `auto_configure` | Environment variables में set endpoints के लिए exporters जोड़ें | `True` |

उदाहरण के लिए, health checks को exclude करते हुए metrics collect करने के लिए:

```python
from fastapi import FastAPI

app = FastAPI(
    telemetry={
        "tracing": False,
        "exclude": lambda scope: scope["path"] == "/health",
    }
)
```

जब आपका application provider setup खुद handle करता है, जैसे उसके lifespan function के अंदर, तब `auto_configure` को `False` पर set करें।
