# Server-Sent Events (SSE) { #server-sent-events-sse }

आप **Server-Sent Events** (SSE) का उपयोग करके client को data stream कर सकते हैं।

यह [Stream JSON Lines](stream-json-lines.md) जैसा है, लेकिन `text/event-stream` format का उपयोग करता है, जिसे browsers [`EventSource` API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) के साथ natively support करते हैं।

/// note | नोट

FastAPI 0.135.0 में जोड़ा गया।

///

## Server-Sent Events क्या हैं? { #what-are-server-sent-events }

SSE, HTTP के माध्यम से server से client तक data stream करने के लिए एक standard है।

हर event एक छोटा text block होता है जिसमें `data`, `event`, `id`, और `retry` जैसे "fields" होते हैं, जिन्हें खाली lines से अलग किया जाता है।

यह ऐसा दिखता है:

```
data: {"name": "Portal Gun", "price": 999.99}

data: {"name": "Plumbus", "price": 32.99}

```

SSE का उपयोग आमतौर पर AI chat streaming, live notifications, logs और observability, और अन्य मामलों में किया जाता है जहाँ server client को updates push करता है।

/// tip | सुझाव

अगर आप binary data stream करना चाहते हैं, जैसे video या audio, तो advanced guide देखें: [Data Stream करें](../advanced/stream-data.md).

///

## FastAPI के साथ SSE Stream करें { #stream-sse-with-fastapi }

FastAPI के साथ SSE stream करने के लिए, अपनी *path operation function* में `yield` का उपयोग करें और `response_class=EventSourceResponse` set करें।

`EventSourceResponse` को `fastapi.sse` से import करें:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[4,22] *}

हर yielded item को JSON के रूप में encode किया जाता है और SSE event के `data:` field में भेजा जाता है।

अगर आप return type को `AsyncIterable[Item]` के रूप में declare करते हैं, तो FastAPI इसका उपयोग Pydantic के साथ data को **validate**, **document**, और **serialize** करने के लिए करेगा।

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[10:12,23] *}

/// tip | सुझाव

क्योंकि Pydantic इसे **Rust** side में serialize करेगा, आपको return type declare न करने की तुलना में कहीं बेहतर **performance** मिलेगी।

///

### Non-async *path operation functions* { #non-async-path-operation-functions }

आप नियमित `def` functions (बिना `async`) का भी उपयोग कर सकते हैं, और उसी तरह `yield` का उपयोग कर सकते हैं।

FastAPI सुनिश्चित करेगा कि यह सही तरीके से run हो ताकि यह event loop को block न करे।

क्योंकि इस मामले में function async नहीं है, सही return type `Iterable[Item]` होगा:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[28:31] hl[29] *}

### कोई Return Type नहीं { #no-return-type }

आप return type को छोड़ भी सकते हैं। FastAPI data को convert करने और भेजने के लिए [`jsonable_encoder`](./encoder.md) का उपयोग करेगा।

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[34:37] hl[35] *}

## `ServerSentEvent` { #serversentevent }

अगर आपको `event`, `id`, `retry`, या `comment` जैसे SSE fields set करने की ज़रूरत है, तो आप plain data के बजाय `ServerSentEvent` objects yield कर सकते हैं।

`ServerSentEvent` को `fastapi.sse` से import करें:

{* ../../docs_src/server_sent_events/tutorial002_py310.py hl[4,26] *}

`data` field हमेशा JSON के रूप में encode किया जाता है। आप कोई भी value pass कर सकते हैं जिसे JSON के रूप में serialize किया जा सकता हो, जिसमें Pydantic models भी शामिल हैं।

## Raw Data { #raw-data }

अगर आपको JSON encoding के **बिना** data भेजना है, तो `data` के बजाय `raw_data` का उपयोग करें।

यह pre-formatted text, log lines, या `[DONE]` जैसे विशेष <dfn title="किसी विशेष condition या state को इंगित करने के लिए उपयोग किया गया value">"sentinel"</dfn> values भेजने के लिए उपयोगी है।

{* ../../docs_src/server_sent_events/tutorial003_py310.py hl[17] *}

/// note | नोट

`data` और `raw_data` mutually exclusive हैं। आप हर `ServerSentEvent` पर उनमें से केवल एक ही set कर सकते हैं।

///

## `Last-Event-ID` के साथ फिर से शुरू करना { #resuming-with-last-event-id }

जब कोई browser connection drop होने के बाद reconnect करता है, तो वह अंतिम प्राप्त `id` को `Last-Event-ID` header में भेजता है।

आप इसे header parameter के रूप में read कर सकते हैं और stream को वहाँ से resume करने के लिए उपयोग कर सकते हैं जहाँ client ने छोड़ा था:

{* ../../docs_src/server_sent_events/tutorial004_py310.py hl[25,27,31] *}

## POST के साथ SSE { #sse-with-post }

SSE **किसी भी HTTP method** के साथ काम करता है, केवल `GET` के साथ नहीं।

यह [MCP](https://modelcontextprotocol.io) जैसे protocols के लिए उपयोगी है, जो `POST` पर SSE stream करते हैं:

{* ../../docs_src/server_sent_events/tutorial005_py310.py hl[14] *}

## तकनीकी विवरण { #technical-details }

FastAPI कुछ SSE best practices को out of the box implement करता है।

* जब कोई message नहीं आया हो, तो हर 15 सेकंड में **"keep alive" `ping` comment** भेजें, ताकि कुछ proxies connection को close न कर दें, जैसा कि [HTML specification: Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html#authoring-notes) में सुझाया गया है।
* stream की **caching रोकने** के लिए `Cache-Control: no-cache` header set करें।
* Nginx जैसे कुछ proxies में **buffering रोकने** के लिए एक special header `X-Accel-Buffering: no` set करें।

आपको इसके लिए कुछ भी करने की ज़रूरत नहीं है, यह out of the box काम करता है। 🤓
