# Sub Applications - Mounts { #sub-applications-mounts }

अगर आपको दो स्वतंत्र FastAPI applications चाहिए, जिनका अपना स्वतंत्र OpenAPI और अपनी docs UIs हों, तो आप एक मुख्य app रख सकते हैं और एक (या अधिक) sub-application(s) को "mount" कर सकते हैं।

## **FastAPI** application को Mount करना { #mounting-a-fastapi-application }

"Mounting" का मतलब है किसी विशिष्ट path में पूरी तरह "स्वतंत्र" application जोड़ना, जो फिर उस path के अंतर्गत सब कुछ handle करने का ध्यान रखता है, उस sub-application में घोषित _path operations_ के साथ।

### Top-level application { #top-level-application }

सबसे पहले, मुख्य, top-level **FastAPI** application और उसके *path operations* बनाएँ:

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[3, 6:8] *}

### Sub-application { #sub-application }

फिर, अपनी sub-application और उसके *path operations* बनाएँ।

यह sub-application बस एक और standard FastAPI application है, लेकिन यही वह है जिसे "mounted" किया जाएगा:

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[11, 14:16] *}

### Sub-application को mount करें { #mount-the-sub-application }

अपने top-level application, `app`, में sub-application, `subapi`, को mount करें।

इस मामले में, इसे path `/subapi` पर mount किया जाएगा:

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[11, 19] *}

### Automatic API docs देखें { #check-the-automatic-api-docs }

अब, `fastapi` command चलाएँ:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

और docs को [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) पर खोलें।

आप मुख्य app के लिए automatic API docs देखेंगे, जिसमें केवल उसके अपने _path operations_ शामिल होंगे:

<img src="/img/tutorial/sub-applications/image01.png">

और फिर, sub-application के लिए docs को [http://127.0.0.1:8000/subapi/docs](http://127.0.0.1:8000/subapi/docs) पर खोलें।

आप sub-application के लिए automatic API docs देखेंगे, जिसमें केवल उसके अपने _path operations_ शामिल होंगे, सभी सही sub-path prefix `/subapi` के अंतर्गत:

<img src="/img/tutorial/sub-applications/image02.png">

अगर आप दोनों user interfaces में से किसी के साथ interact करने की कोशिश करते हैं, तो वे सही तरह काम करेंगे, क्योंकि browser हर specific app या sub-app से बात कर पाएगा।

### तकनीकी विवरण: `root_path` { #technical-details-root-path }

जब आप ऊपर बताए गए तरीके से कोई sub-application mount करते हैं, तो FastAPI sub-application के लिए mount path communicate करने का ध्यान रखेगा, ASGI specification के एक mechanism का उपयोग करके जिसे `root_path` कहा जाता है।

इस तरह, sub-application को पता होगा कि docs UI के लिए उस path prefix का उपयोग करना है।

और sub-application की अपनी mounted sub-applications भी हो सकती हैं और सब कुछ सही तरह काम करेगा, क्योंकि FastAPI इन सभी `root_path`s को अपने आप handle करता है।

आप `root_path` के बारे में और इसे स्पष्ट रूप से कैसे उपयोग करें, यह [Behind a Proxy](behind-a-proxy.md) वाले section में और सीखेंगे।
