# Static Files { #static-files }

आप `StaticFiles` का उपयोग करके किसी directory से static files को अपने-आप serve कर सकते हैं।

/// tip | सुझाव

अगर आपको frontend host करना है, तो इसके बजाय `app.frontend()` का उपयोग करें, इसके बारे में [Frontend](frontend.md) में पढ़ें।

`app.frontend()` अंदरूनी तौर पर `StaticFiles` का उपयोग करता है, जिसमें frontends के लिए कई अतिरिक्त फायदे होते हैं, जैसे client-side routing को handle करना।

///

## `StaticFiles` का उपयोग करें { #use-staticfiles }

* `StaticFiles` import करें।
* किसी विशिष्ट path में `StaticFiles()` instance को "Mount" करें।

{* ../../docs_src/static_files/tutorial001_py310.py hl[2,6] *}

/// note | तकनीकी विवरण

आप `from starlette.staticfiles import StaticFiles` भी उपयोग कर सकते हैं।

**FastAPI** आपकी, developer की, सुविधा के लिए वही `starlette.staticfiles` `fastapi.staticfiles` के रूप में प्रदान करता है। लेकिन यह वास्तव में सीधे Starlette से आता है।

///

### "Mounting" क्या है { #what-is-mounting }

"Mounting" का मतलब है किसी विशिष्ट path में एक पूरी "independent" application जोड़ना, जो फिर सभी sub-paths को handle करने का काम करती है।

यह `APIRouter` का उपयोग करने से अलग है, क्योंकि mounted application पूरी तरह independent होती है। आपकी main application की OpenAPI और docs में mounted application से कुछ भी शामिल नहीं होगा, आदि।

आप इसके बारे में [Advanced User Guide](../advanced/index.md) में और पढ़ सकते हैं।

## विवरण { #details }

पहला `"/static"` उस sub-path को संदर्भित करता है जिस पर यह "sub-application" "mount" की जाएगी। इसलिए, `"/static"` से शुरू होने वाला कोई भी path इसके द्वारा handle किया जाएगा।

`directory="static"` उस directory के नाम को संदर्भित करता है जिसमें आपकी static files होती हैं।

`name="static"` इसे एक नाम देता है, जिसे **FastAPI** द्वारा internally उपयोग किया जा सकता है।

ये सभी parameters "`static`" से अलग हो सकते हैं, इन्हें अपनी application की जरूरतों और विशिष्ट विवरणों के अनुसार adjust करें।

## अधिक जानकारी { #more-info }

अधिक विवरण और options के लिए [Static Files के बारे में Starlette की docs](https://www.starlette.dev/staticfiles/) देखें।
