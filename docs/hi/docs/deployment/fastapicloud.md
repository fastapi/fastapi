# FastAPI Cloud { #fastapi-cloud }

आप अपनी FastAPI app को सिर्फ **एक command** से [FastAPI Cloud](https://fastapicloud.com) पर deploy कर सकते हैं। 🚀

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

CLI अपने-आप आपकी FastAPI application का पता लगा लेगा और उसे cloud पर deploy कर देगा। अगर आप logged in नहीं हैं, तो authentication प्रक्रिया पूरी करने के लिए आपका browser खुलेगा।

बस इतना ही! अब आप उस URL पर अपनी app access कर सकते हैं। ✨

## FastAPI Cloud के बारे में { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** उसी author और team द्वारा बनाया गया है जो **FastAPI** के पीछे हैं।

यह कम से कम प्रयास में API को **build** करने, **deploy** करने, और **access** करने की प्रक्रिया को सरल बनाता है।

यह FastAPI के साथ apps बनाने वाले उसी **developer experience** को उन्हें cloud पर **deploy** करने में भी लाता है। 🎉

यह app deploy करते समय ज़रूरी अधिकांश चीज़ों का भी ध्यान रखेगा, जैसे:

* HTTPS
* Replication, requests के आधार पर autoscaling के साथ
* आदि।

FastAPI Cloud, *FastAPI and friends* open source projects का मुख्य sponsor और funding provider है। ✨

## दूसरे cloud providers पर deploy करें { #deploy-to-other-cloud-providers }

FastAPI open source है और standards पर आधारित है। आप FastAPI apps को अपने चुने हुए किसी भी cloud provider पर deploy कर सकते हैं।

उनके साथ FastAPI apps deploy करने के लिए अपने cloud provider की guides follow करें। 🤓

## अपने खुद के server पर deploy करें { #deploy-your-own-server }

मैं आपको इस **Deployment** guide में आगे सभी details भी सिखाऊँगा, ताकि आप समझ सकें कि क्या हो रहा है, क्या होना चाहिए, या FastAPI apps को अपने-आप, अपने खुद के servers के साथ भी कैसे deploy करना है। 🤓
