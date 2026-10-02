# OpenTelemetry { #opentelemetry }

जब आपका API चल रहा होता है, तो आप शायद जानना चाहें कि उसे कितना ट्रैफ़िक मिल रहा है, कौन-से requests धीमे हैं और त्रुटियाँ कब होती हैं।

**Telemetry** आपके एप्लिकेशन के व्यवहार से जुड़ा data है, जो इन सवालों के जवाब देने में मदद करता है। इसके सामान्य प्रकार हैं:

- **Metrics**: ऐसे माप जिन्हें आप समय के साथ संक्षेप में देख सकते हैं, जैसे response में लगने वाला समय और संभाले जा रहे requests की संख्या।
- **Traces**: अलग-अलग requests और उन्हें संभालने के लिए किए गए ऑपरेशन के रिकॉर्ड। हर ऑपरेशन जिसका समय मापा जाता है, एक **span** कहलाता है।
- **Logs**: टाइमस्टैम्प के साथ event के रिकॉर्ड, जैसे किसी एप्लिकेशन का शुरू होना या किसी ऑपरेशन का विफल होना।

[**OpenTelemetry**](https://opentelemetry.io/) telemetry एकत्र करने और उसे किसी मॉनिटरिंग सेवा को भेजने के लिए standards और tools का एक समूह है, जहाँ आप उसे डैशबोर्ड में देख और जाँच सकते हैं।

**FastAPI, HTTP request traces, metrics और logs के लिए default रूप से OpenTelemetry support प्रदान करता है**। WebSocket कनेक्शन भी traces और logs प्रदान करते हैं। उस data को देखने के लिए, उसे प्राप्त करने वाली मॉनिटरिंग सेवा कॉन्फ़िगर करें।

## FastAPI install करें { #install-fastapi }

FastAPI को `standard` extras के साथ install करें, जिनमें telemetry भेजने के लिए packages शामिल हैं:

<div class="termy">

```console
$ uv add "fastapi[standard]"
---> 100%
```

</div>

## ऐप बनाएँ { #create-the-app }

एक file `main.py` बनाएँ:

{* ../../docs_src/opentelemetry/tutorial001_py310.py *}

ध्यान दें कि यह सब default रूप से काम करता है। Telemetry के काम करने के लिए आपको कोई कस्टम कोड लिखने की ज़रूरत नहीं है।

## FastAPI Cloud { #fastapi-cloud }

जब आप `fastapi[standard]` के साथ [FastAPI Cloud](https://fastapicloud.com) पर डिप्लॉय करते हैं, तो metrics अपने आप काम करते हैं। आपको कुछ और कॉन्फ़िगर नहीं करना पड़ता।

Pro प्लान पर, आप [Metrics डैशबोर्ड](https://fastapicloud.com/docs/monitoring-and-performance/metrics/) में requests की संख्या, त्रुटि दर और response में लगने वाला समय देख सकते हैं।

<img src="/img/tutorial/opentelemetry/image01.png" alt="उदाहरण data के साथ FastAPI Cloud Pro metrics डैशबोर्ड">

## अन्य मॉनिटरिंग सेवाएँ { #other-monitoring-services }

किसी अन्य मॉनिटरिंग सेवा को telemetry भेजने के लिए, ऐसा endpoint कॉन्फ़िगर करें जो **OTLP** स्वीकार करता हो। यह telemetry भेजने के लिए OpenTelemetry का प्रोटोकॉल है। सेवा के HTTP/protobuf बेस endpoint का उपयोग करें।

उदाहरण URL की जगह अपना endpoint डालकर, ये environment variables सेट करें:

```bash
export OTEL_SERVICE_NAME=my-api
export OTEL_EXPORTER_OTLP_ENDPOINT=https://collector.example.com
```

`OTEL_SERVICE_NAME` मॉनिटरिंग सेवा में आपके ऐप की पहचान करता है। Endpoint, data प्राप्त करने के लिए बेस URL है। उस URL के अंतर्गत traces को `/v1/traces`, metrics को `/v1/metrics` और logs को `/v1/logs` पर भेजा जाता है।

यदि आपकी सेवा को प्रमाणीकरण की ज़रूरत है, तो `OTEL_EXPORTER_OTLP_HEADERS` में उसके बताए गए headers सेट करें, उदाहरण के लिए `api-key=YOUR_API_KEY`।

## ऐप चलाएँ { #run-the-app }

उसी टर्मिनल में ऐप शुरू करें:

<div class="termy">

```console
$ uv run fastapi run
```

</div>

दूसरे टर्मिनल में, एक request भेजें:

```console
$ curl http://127.0.0.1:8000/items/1
{"item_id":1}
```

अपनी मॉनिटरिंग सेवा खोलें और `my-api` खोजें। अगले एक्सपोर्ट के बाद, आप `GET /items/{item_id}` span वाला एक trace देख सकते हैं, साथ ही requests की संख्या, response की अवधि और सक्रिय requests के metrics भी देख सकते हैं।

## Telemetry को अपनी ज़रूरत के अनुसार बदलें { #customize-telemetry }

### Providers और exporters कॉन्फ़िगर करें { #configure-providers-and-exporters }

एक **provider** ऐसे ऑब्जेक्ट प्रदान करता है जो traces, metrics या logs रिकॉर्ड करते हैं। उसका कॉन्फ़िगरेशन नियंत्रित करता है कि उस data को कैसे प्रोसेस और एक्सपोर्ट किया जाता है।

Telemetry लाइब्रेरी OpenTelemetry के ग्लोबल providers को कॉन्फ़िगर कर सकती हैं। ऐप शुरू होने से पहले लाइब्रेरी को कॉन्फ़िगर करें, और FastAPI अपने आप उन providers का उपयोग करता है।

जब environment में कोई OTLP endpoint सेट होता है, तो FastAPI हर सक्षम provider में उस गंतव्य के लिए एक exporter जोड़ता है। मौजूदा exporters अपने गंतव्यों पर data भेजना जारी रखते हैं।

हर गंतव्य को एक बार कॉन्फ़िगर करें। यदि कोई दूसरी लाइब्रेरी पहले से ही environment में दिए गए गंतव्य को संभाल रही है, तो उसका environment export अक्षम करें या FastAPI का स्वचालित setup बंद करें:

```python
app = FastAPI(telemetry={"auto_configure": False})
```

आप `telemetry` डिक्शनरी में सीधे एक provider भी पास कर सकते हैं। उदाहरण के लिए, यह provider आपके टर्मिनल में request spans प्रिंट करने के लिए OpenTelemetry के console exporter का उपयोग करता है:

{* ../../docs_src/opentelemetry/tutorial002_py310.py hl[2:8] *}

**Exporter**, spans को उनके गंतव्य पर भेजता है। `BatchSpanProcessor`, spans को समूहों में बाँटता है और उन्हें बैकग्राउंड में भेजता है। अपनी मॉनिटरिंग लाइब्रेरी के गंतव्य का उपयोग करने के लिए console exporter की जगह उस लाइब्रेरी द्वारा प्रदान किया गया exporter लगाएँ। कॉन्फ़िगरेशन के और विकल्पों के लिए [OpenTelemetry की Python instrumentation गाइड](https://opentelemetry.io/docs/languages/python/instrumentation/) देखें।

Metrics या logs provider प्रदान करने के लिए उसी डिक्शनरी में `meter_provider` या `logger_provider` का उपयोग करें। Provider बनाने वाला एप्लिकेशन या लाइब्रेरी उसके shutdown को संभालता है। FastAPI अपने जोड़े गए एक्सपोर्ट घटकों को संभालता है।

/// warning | चेतावनी

OpenTelemetry default रूप से ग्लोबल providers का उपयोग करता है। [माउंट किए गए उप-एप्लिकेशन](sub-applications.md) के लिए स्वतंत्र telemetry कॉन्फ़िगरेशन की गारंटी नहीं है।

///

### Request ऑपरेशन को ट्रेस करें { #trace-request-operations }

Default रूप से, request traces में dependencies रिज़ॉल्व करने, आपका path operation function चलाने, response को serialize करने और FastAPI के `BackgroundTasks` में हर टास्क को चलाने के spans शामिल होते हैं। ये spans उसी provider और उन्हीं exporters का उपयोग करते हैं।

बैकग्राउंड टास्क के spans, request के trace का हिस्सा बने रहते हैं। वे HTTP response span समाप्त होने के बाद चलते हैं, इसलिए वे मापे गए response समय को नहीं बढ़ाते।

केवल HTTP request span रिकॉर्ड करने के लिए, `operation_spans` को `False` पर सेट करें:

{* ../../docs_src/opentelemetry/tutorial003_py310.py hl[3] *}


### WebSocket कनेक्शन को ट्रेस करें { #trace-websocket-connections }

हर WebSocket कनेक्शन का एक span होता है, जैसे `WS /ws/{room}`, जो हैंडलर और dependency cleanup को कवर करता है। यह उन्हीं providers और सेटिंग्स का उपयोग करता है, जिनमें dependency resolution और endpoint के निष्पादन के लिए `operation_spans` भी शामिल है।

HTTP request metrics में केवल HTTP requests शामिल होते हैं। कोड `1000` या `1001` के साथ होने वाले सामान्य WebSocket डिस्कनेक्ट, error logs नहीं बनाते।

### त्रुटियों की जाँच करें { #inspect-errors }

FastAPI, संभाले न गए exceptions को OpenTelemetry logs के रूप में रिकॉर्ड करता है, जो request या कनेक्शन के trace से जुड़े होते हैं। Error logs तब भी रिकॉर्ड किए जाते हैं जब trace को सैंपल नहीं किया जाता।

Exception logs में exception का प्रकार, संदेश और stack trace शामिल होते हैं। संदेशों और stack traces में संवेदनशील जानकारी हो सकती है। उन्हें फ़िल्टर करने या उनमें से संवेदनशील जानकारी हटाने के लिए अपने provider के log processors का उपयोग करें, या इन logs को अक्षम करने के लिए `logs` को `False` पर सेट करें।

FastAPI, request validation की विफलताओं को भी route और त्रुटियों की संख्या के साथ warning logs के रूप में रिकॉर्ड करता है। इन logs में अमान्य इनपुट शामिल नहीं होता।

## चुनें कि क्या रिकॉर्ड करना है { #choose-what-to-record }

`telemetry` डिक्शनरी इन सेटिंग्स को भी स्वीकार करती है:

| सेटिंग | उद्देश्य | Default |
| --- | --- | --- |
| `tracing` | HTTP request और WebSocket कनेक्शन के spans रिकॉर्ड करना | `True` |
| `metrics` | HTTP request metrics रिकॉर्ड करना | `True` |
| `logs` | Validation की विफलताएँ और संभाले न गए exceptions रिकॉर्ड करना | `True` |
| `operation_spans` | Request ऑपरेशन के लिए spans जोड़ना | `True` |
| `exclude` | जब ASGI scope प्राप्त करने वाला function `True` लौटाए, तो requests छोड़ देना | `None` |
| `auto_configure` | Environment variables में सेट endpoints के लिए exporters जोड़ना | `True` |

उदाहरण के लिए, health checks को छोड़कर metrics एकत्र करने के लिए:

```python
from fastapi import FastAPI

app = FastAPI(
    telemetry={
        "tracing": False,
        "exclude": lambda scope: scope["path"] == "/health",
    }
)
```

जब आपका एप्लिकेशन provider setup खुद संभालता हो, जैसे अपने lifespan function के अंदर, तो `auto_configure` को `False` पर सेट करें।
