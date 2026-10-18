# Security { #security }

security, authentication और authorization को handle करने के कई तरीके हैं।

और यह सामान्यतः एक जटिल और "कठिन" विषय होता है।

कई frameworks और systems में केवल security और authentication को handle करने में ही बहुत अधिक effort और code लग जाता है (कई मामलों में यह लिखे गए पूरे code का 50% या उससे अधिक हो सकता है)।

**FastAPI** आपको **Security** से आसानी से, तेज़ी से, standard तरीके से निपटने में मदद करने के लिए कई tools प्रदान करता है, बिना सभी security specifications को पढ़ने और सीखने की ज़रूरत के।

लेकिन पहले, आइए कुछ छोटे concepts देखते हैं।

## जल्दी में हैं? { #in-a-hurry }

अगर आपको इन terms की परवाह नहीं है और आपको बस username और password पर आधारित authentication के साथ security *अभी* जोड़नी है, तो अगले chapters पर जाएँ।

## OAuth2 { #oauth2 }

OAuth2 एक specification है जो authentication और authorization को handle करने के कई तरीके define करती है।

यह काफ़ी विस्तृत specification है और कई जटिल use cases को cover करती है।

इसमें "third party" का उपयोग करके authenticate करने के तरीके शामिल हैं।

यही चीज़ अंदर से उन सभी systems में इस्तेमाल होती है जिनमें "login with Facebook, Google, X (Twitter), GitHub" होता है।

### OAuth 1 { #oauth-1 }

OAuth 1 भी था, जो OAuth2 से बहुत अलग और अधिक जटिल था, क्योंकि इसमें communication को encrypt करने के तरीके पर direct specifications शामिल थीं।

आजकल यह बहुत लोकप्रिय या इस्तेमाल में नहीं है।

OAuth2 यह specify नहीं करता कि communication को कैसे encrypt करना है, यह अपेक्षा करता है कि आपकी application HTTPS के साथ serve की जा रही हो।

/// tip | सुझाव

**deployment** वाले section में आप देखेंगे कि Traefik और Let's Encrypt का उपयोग करके HTTPS को मुफ्त में कैसे setup किया जाता है।

///

## OpenID Connect { #openid-connect }

OpenID Connect एक और specification है, जो **OAuth2** पर आधारित है।

यह OAuth2 को बस extend करता है और कुछ ऐसी चीज़ें specify करता है जो OAuth2 में तुलनात्मक रूप से ambiguous हैं, ताकि इसे अधिक interoperable बनाया जा सके।

उदाहरण के लिए, Google login OpenID Connect का उपयोग करता है (जो अंदर से OAuth2 का उपयोग करता है)।

लेकिन Facebook login OpenID Connect को support नहीं करता। उसका अपना OAuth2 flavor है।

### OpenID ("OpenID Connect" नहीं) { #openid-not-openid-connect }

एक "OpenID" specification भी थी। उसने वही समस्या हल करने की कोशिश की जो **OpenID Connect** करता है, लेकिन वह OAuth2 पर आधारित नहीं थी।

इसलिए, वह एक पूरा अतिरिक्त system था।

आजकल यह बहुत लोकप्रिय या इस्तेमाल में नहीं है।

## OpenAPI { #openapi }

OpenAPI (पहले Swagger के नाम से जाना जाता था) APIs बनाने के लिए open specification है (अब Linux Foundation का हिस्सा)।

**FastAPI** **OpenAPI** पर आधारित है।

इसी वजह से कई automatic interactive documentation interfaces, code generation, आदि होना संभव होता है।

OpenAPI कई security "schemes" define करने का तरीका देता है।

इनका उपयोग करके, आप इन सभी standard-based tools का लाभ उठा सकते हैं, जिनमें ये interactive documentation systems भी शामिल हैं।

OpenAPI निम्नलिखित security schemes define करता है:

* `apiKey`: एक application-specific key जो यहाँ से आ सकती है:
    * एक query parameter.
    * एक header.
    * एक cookie.
* `http`: standard HTTP authentication systems, जिनमें शामिल हैं:
    * `bearer`: एक header `Authorization` जिसमें `Bearer ` plus एक token का value होता है। यह OAuth2 से inherited है।
    * HTTP Basic authentication.
    * HTTP Digest, आदि।
* `oauth2`: security handle करने के सभी OAuth2 तरीके (जिन्हें "flows" कहा जाता है)।
    * इनमें से कई flows OAuth 2.0 authentication provider बनाने के लिए उपयुक्त हैं (जैसे Google, Facebook, X (Twitter), GitHub, आदि):
        * `implicit`
        * `clientCredentials`
        * `authorizationCode`
    * लेकिन एक specific "flow" है जिसे उसी application में सीधे authentication handle करने के लिए पूरी तरह इस्तेमाल किया जा सकता है:
        * `password`: कुछ अगले chapters इसके examples cover करेंगे।
* `openIdConnect`: इसमें OAuth2 authentication data को automatically discover करने का तरीका होता है।
    * यह automatic discovery वही है जो OpenID Connect specification में define की गई है।

/// tip | सुझाव

Google, Facebook, X (Twitter), GitHub, आदि जैसे अन्य authentication/authorization providers को integrate करना भी संभव और तुलनात्मक रूप से आसान है।

सबसे जटिल समस्या उन जैसे authentication/authorization provider बनाना है, लेकिन **FastAPI** आपको इसे आसानी से करने के लिए tools देता है, और आपके लिए heavy lifting करता है।

///

## **FastAPI** utilities { #fastapi-utilities }

FastAPI इन security schemes में से प्रत्येक के लिए `fastapi.security` module में कई tools प्रदान करता है, जो इन security mechanisms का उपयोग आसान बनाते हैं।

अगले chapters में आप देखेंगे कि **FastAPI** द्वारा प्रदान किए गए उन tools का उपयोग करके अपनी API में security कैसे जोड़ें।

और आप यह भी देखेंगे कि यह interactive documentation system में automatically कैसे integrate हो जाता है।
