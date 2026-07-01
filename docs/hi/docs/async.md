# Concurrency और async / await { #concurrency-and-async-await }

*path operation functions* के लिए `async def` syntax और asynchronous code, concurrency, और parallelism के बारे में कुछ पृष्ठभूमि का विवरण।

## जल्दी में हैं? { #in-a-hurry }

<abbr title="too long; didn't read - बहुत लंबा; नहीं पढ़ा"><strong>TL;DR:</strong></abbr>

अगर आप third party libraries का उपयोग कर रहे हैं जो आपको उन्हें `await` के साथ call करने को कहती हैं, जैसे:

```Python
results = await some_library()
```

तो, अपनी *path operation functions* को `async def` के साथ declare करें, जैसे:

```Python hl_lines="2"
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

/// note | नोट

आप `await` का उपयोग केवल `async def` के साथ बनाए गए functions के अंदर कर सकते हैं।

///

---

अगर आप ऐसी third party library का उपयोग कर रहे हैं जो किसी चीज़ (database, API, file system, आदि) से communicate करती है और `await` के उपयोग के लिए support नहीं रखती, (वर्तमान में अधिकांश database libraries के लिए यही स्थिति है), तो अपनी *path operation functions* को सामान्य रूप से, सिर्फ़ `def` के साथ declare करें, जैसे:

```Python hl_lines="2"
@app.get('/')
def results():
    results = some_library()
    return results
```

---

अगर आपके application को (किसी तरह) किसी और चीज़ से communicate करने और उसके response का इंतज़ार करने की ज़रूरत नहीं है, तो `async def` का उपयोग करें, भले ही आपको अंदर `await` का उपयोग करने की आवश्यकता न हो।

---

अगर आपको बस पता नहीं है, तो सामान्य `def` का उपयोग करें।

---

**नोट**: आप अपनी *path operation functions* में `def` और `async def` को जितनी ज़रूरत हो उतना mix कर सकते हैं और हर एक को अपने लिए सबसे अच्छे option से define कर सकते हैं। FastAPI उनके साथ सही काम करेगा।

वैसे भी, ऊपर दिए गए किसी भी case में, FastAPI फिर भी asynchronously काम करेगा और बेहद तेज़ रहेगा।

लेकिन ऊपर दिए गए steps follow करने से, वह कुछ performance optimizations कर पाएगा।

## तकनीकी विवरण { #technical-details }

Python के modern versions में **"asynchronous code"** के लिए support है, जिसमें **`async` और `await`** syntax के साथ **"coroutines"** नाम की चीज़ का उपयोग होता है।

आइए नीचे के sections में इस phrase को हिस्सों में देखें:

* **Asynchronous Code**
* **`async` और `await`**
* **Coroutines**

## Asynchronous Code { #asynchronous-code }

Asynchronous code का मतलब बस इतना है कि language 💬 के पास computer / program 🤖 को यह बताने का एक तरीका है कि code में किसी point पर, उसे 🤖 किसी और जगह पर *किसी और चीज़* के पूरा होने का इंतज़ार करना होगा। मान लीजिए कि वह *कोई और चीज़* "slow-file" 📝 कहलाती है।

तो, उस समय के दौरान, computer कोई और काम कर सकता है, जबकि "slow-file" 📝 finish होती है।

फिर computer / program 🤖 हर बार वापस आएगा जब उसके पास मौका होगा क्योंकि वह फिर से इंतज़ार कर रहा है, या जब भी वह 🤖 उस point पर अपने सारे काम finish कर लेगा। और वह 🤖 देखेगा कि जिन tasks का वह इंतज़ार कर रहा था उनमें से कोई पहले ही finish हो चुका है या नहीं, और जो भी करना था वह करेगा।

इसके बाद, वह 🤖 finish होने वाला पहला task लेता है (मान लीजिए, हमारी "slow-file" 📝) और उसके साथ जो भी करना था उसे continue करता है।

वह "किसी और चीज़ का इंतज़ार" आमतौर पर <abbr title="Input and Output - इनपुट और आउटपुट">I/O</abbr> operations को refer करता है जो अपेक्षाकृत "slow" होते हैं (processor और RAM memory की speed की तुलना में), जैसे इंतज़ार करना:

* client से data network के ज़रिए भेजे जाने का
* आपके program द्वारा भेजे गए data को client द्वारा network के ज़रिए receive किए जाने का
* disk पर मौजूद file की contents को system द्वारा read करके आपके program को दिए जाने का
* आपके program द्वारा system को दिए गए contents को disk पर लिखे जाने का
* किसी remote API operation का
* database operation के finish होने का
* database query के results return करने का
* आदि।

क्योंकि execution time ज़्यादातर <abbr title="Input and Output - इनपुट और आउटपुट">I/O</abbr> operations का इंतज़ार करने में खर्च होता है, उन्हें "I/O bound" operations कहा जाता है।

इसे "asynchronous" इसलिए कहा जाता है क्योंकि computer / program को slow task के साथ "synchronized" होने की ज़रूरत नहीं होती, यानी task finish होने के exact moment का इंतज़ार करते हुए कुछ न करना, ताकि task result लेकर काम continue कर सके।

इसके बजाय, "asynchronous" system होने के कारण, task finish होने के बाद थोड़ी देर (कुछ microseconds) line में इंतज़ार कर सकता है ताकि computer / program जो भी करने गया था उसे finish करे, और फिर वापस आकर results ले और उनके साथ काम continue करे।

"synchronous" ("asynchronous" के विपरीत) के लिए आमतौर पर "sequential" term भी use की जाती है, क्योंकि computer / program किसी दूसरे task पर switch करने से पहले सभी steps को sequence में follow करता है, भले ही उन steps में इंतज़ार शामिल हो।

### Concurrency और Burgers { #concurrency-and-burgers }

ऊपर describe किए गए **asynchronous** code के इस idea को कभी-कभी **"concurrency"** भी कहा जाता है। यह **"parallelism"** से अलग है।

**Concurrency** और **parallelism** दोनों "अलग-अलग चीज़ें लगभग एक ही समय पर हो रही हैं" से संबंधित हैं।

लेकिन *concurrency* और *parallelism* के बीच details काफ़ी अलग हैं।

अंतर देखने के लिए, burgers के बारे में यह कहानी imagine करें:

### Concurrent Burgers { #concurrent-burgers }

आप अपने crush के साथ fast food लेने जाते हैं, आप line में खड़े होते हैं जबकि cashier आपके आगे लोगों के orders ले रहा होता है। 😍

<img src="/img/async/concurrent-burgers/concurrent-burgers-01.png" class="illustration">

फिर आपकी बारी आती है, आप अपने crush और अपने लिए 2 बहुत fancy burgers का order देते हैं। 🍔🍔

<img src="/img/async/concurrent-burgers/concurrent-burgers-02.png" class="illustration">

cashier kitchen में cook से कुछ कहता है ताकि उन्हें पता हो कि उन्हें आपके burgers prepare करने हैं (हालाँकि वे अभी previous clients के burgers prepare कर रहे हैं)।

<img src="/img/async/concurrent-burgers/concurrent-burgers-03.png" class="illustration">

आप pay करते हैं। 💸

cashier आपको आपकी बारी का number देता है।

<img src="/img/async/concurrent-burgers/concurrent-burgers-04.png" class="illustration">

जब आप इंतज़ार कर रहे होते हैं, आप अपने crush के साथ एक table चुनते हैं, बैठते हैं और अपने crush से काफ़ी देर तक बात करते हैं (क्योंकि आपके burgers बहुत fancy हैं और उन्हें prepare होने में कुछ समय लगता है)।

जब आप अपने crush के साथ table पर बैठे हैं, burgers का इंतज़ार करते हुए, आप वह समय यह admire करने में बिता सकते हैं कि आपका crush कितना awesome, cute और smart है ✨😍✨।

<img src="/img/async/concurrent-burgers/concurrent-burgers-05.png" class="illustration">

इंतज़ार करते हुए और अपने crush से बात करते हुए, आप समय-समय पर counter पर displayed number check करते हैं कि क्या आपकी बारी आ चुकी है।

फिर किसी point पर, आखिरकार आपकी बारी आ जाती है। आप counter पर जाते हैं, अपने burgers लेते हैं और table पर वापस आते हैं।

<img src="/img/async/concurrent-burgers/concurrent-burgers-06.png" class="illustration">

आप और आपका crush burgers खाते हैं और अच्छा समय बिताते हैं। ✨

<img src="/img/async/concurrent-burgers/concurrent-burgers-07.png" class="illustration">

/// note | नोट

सुंदर illustrations [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot) द्वारा। 🎨

///

---

Imagine करें कि उस कहानी में आप computer / program 🤖 हैं।

जब आप line में होते हैं, आप बस idle 😴 होते हैं, अपनी बारी का इंतज़ार करते हुए, कोई बहुत "productive" काम नहीं कर रहे होते। लेकिन line तेज़ है क्योंकि cashier सिर्फ़ orders ले रहा है (उन्हें prepare नहीं कर रहा), इसलिए यह ठीक है।

फिर, जब आपकी बारी आती है, आप actual "productive" काम करते हैं, menu process करते हैं, decide करते हैं कि क्या चाहिए, अपने crush की choice लेते हैं, pay करते हैं, check करते हैं कि आपने सही bill या card दिया है, check करते हैं कि आपको correctly charge किया गया है, check करते हैं कि order में सही items हैं, आदि।

लेकिन फिर, भले ही आपके पास अभी burgers नहीं हैं, cashier के साथ आपका काम "on pause" ⏸ है, क्योंकि आपको अपने burgers ready होने का इंतज़ार 🕙 करना है।

लेकिन जब आप counter से दूर जाकर अपनी बारी के number के साथ table पर बैठते हैं, तो आप अपना ध्यान 🔀 अपने crush पर switch कर सकते हैं, और उस पर "work" ⏯ 🤓 कर सकते हैं। फिर आप फिर से कुछ बहुत "productive" कर रहे होते हैं, जैसे अपने crush के साथ flirting 😍।

फिर cashier 💁 आपके number को counter के display पर डालकर कहता है "मैंने burgers बना दिए हैं", लेकिन displayed number आपकी बारी के number में बदलते ही आप तुरंत पागलों की तरह jump नहीं करते। आप जानते हैं कि कोई आपके burgers steal नहीं करेगा क्योंकि आपके पास आपकी बारी का number है, और उनके पास उनका।

तो आप अपने crush के story finish करने का इंतज़ार करते हैं (current work ⏯ / task being processed 🤓 finish करने का), हल्के से smile करते हैं और कहते हैं कि आप burgers लेने जा रहे हैं ⏸।

फिर आप counter 🔀 पर जाते हैं, उस initial task पर जो अब finish हो चुका है ⏯, burgers उठाते हैं, thanks कहते हैं और उन्हें table पर ले जाते हैं। इससे counter के साथ interaction का वह step / task finish हो जाता है ⏹। बदले में, यह "burgers खाने" का एक नया task बनाता है 🔀 ⏯, लेकिन "burgers लेने" वाला previous task finish हो चुका है ⏹।

### Parallel Burgers { #parallel-burgers }

अब imagine करें कि ये "Concurrent Burgers" नहीं, बल्कि "Parallel Burgers" हैं।

आप अपने crush के साथ parallel fast food लेने जाते हैं।

आप line में खड़े होते हैं जबकि कई (मान लें 8) cashiers, जो उसी समय cooks भी हैं, आपके आगे लोगों के orders ले रहे होते हैं।

आपसे पहले सभी लोग counter छोड़ने से पहले अपने burgers ready होने का इंतज़ार कर रहे हैं क्योंकि 8 cashiers में से हर एक next order लेने से पहले तुरंत जाकर burger prepare करता है।

<img src="/img/async/parallel-burgers/parallel-burgers-01.png" class="illustration">

फिर आखिरकार आपकी बारी आती है, आप अपने crush और अपने लिए 2 बहुत fancy burgers का order देते हैं।

आप pay करते हैं 💸।

<img src="/img/async/parallel-burgers/parallel-burgers-02.png" class="illustration">

cashier kitchen में जाता है।

आप counter के सामने खड़े होकर इंतज़ार करते हैं 🕙, ताकि आपके लेने से पहले कोई और आपके burgers न ले जाए, क्योंकि turns के लिए कोई numbers नहीं हैं।

<img src="/img/async/parallel-burgers/parallel-burgers-03.png" class="illustration">

क्योंकि आप और आपका crush इस बात में busy हैं कि कोई आपके आगे न आ जाए और आपके burgers आते ही उन्हें न ले जाए, आप अपने crush पर ध्यान नहीं दे सकते। 😞

यह "synchronous" work है, आप cashier/cook 👨‍🍳 के साथ "synchronized" हैं। आपको इंतज़ार 🕙 करना है और उस exact moment पर वहाँ होना है जब cashier/cook 👨‍🍳 burgers finish करके आपको देता है, नहीं तो कोई और उन्हें ले सकता है।

<img src="/img/async/parallel-burgers/parallel-burgers-04.png" class="illustration">

फिर आपका cashier/cook 👨‍🍳 लंबे समय तक counter के सामने इंतज़ार 🕙 करने के बाद आखिरकार आपके burgers के साथ वापस आता है।

<img src="/img/async/parallel-burgers/parallel-burgers-05.png" class="illustration">

आप अपने burgers लेते हैं और अपने crush के साथ table पर जाते हैं।

आप बस उन्हें खाते हैं, और आपका काम हो जाता है। ⏹

<img src="/img/async/parallel-burgers/parallel-burgers-06.png" class="illustration">

ज़्यादा बात या flirting नहीं हुई क्योंकि ज़्यादातर समय counter के सामने इंतज़ार 🕙 करने में चला गया। 😞

/// note | नोट

सुंदर illustrations [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot) द्वारा। 🎨

///

---

parallel burgers के इस scenario में, आप दो processors (आप और आपका crush) वाला computer / program 🤖 हैं, दोनों इंतज़ार 🕙 कर रहे हैं और अपना ध्यान ⏯ लंबे समय तक "counter पर इंतज़ार" 🕙 करने में लगा रहे हैं।

fast food store के पास 8 processors (cashiers/cooks) हैं। जबकि concurrent burgers store के पास शायद सिर्फ़ 2 (एक cashier और एक cook) रहे होंगे।

लेकिन फिर भी, final experience सबसे अच्छा नहीं है। 😞

---

यह burgers के लिए parallel equivalent story होगी। 🍔

इसका एक अधिक "real life" example देखने के लिए, एक bank imagine करें।

हाल तक, अधिकांश banks में multiple cashiers 👨‍💼👨‍💼👨‍💼👨‍💼 और एक बड़ी line 🕙🕙🕙🕙🕙🕙🕙🕙 होती थी।

सभी cashiers एक client के बाद दूसरे client के साथ पूरा काम करते थे 👨‍💼⏯।

और आपको line में लंबे समय तक इंतज़ार 🕙 करना पड़ता है वरना आपकी बारी चली जाती है।

आप शायद अपने crush 😍 को bank 🏦 में errands करने के लिए अपने साथ नहीं ले जाना चाहेंगे।

### Burger Conclusion { #burger-conclusion }

"अपने crush के साथ fast food burgers" के इस scenario में, क्योंकि बहुत इंतज़ार 🕙 है, concurrent system ⏸🔀⏯ रखना कहीं ज़्यादा meaningful है।

अधिकांश web applications के लिए यही case है।

बहुत सारे users, लेकिन आपका server उनके not-so-good connection से requests भेजने का इंतज़ार 🕙 कर रहा है।

और फिर responses वापस आने का फिर से इंतज़ार 🕙 कर रहा है।

यह "waiting" 🕙 microseconds में measure होती है, लेकिन फिर भी, सब मिलाकर अंत में यह बहुत सारा इंतज़ार बन जाता है।

इसीलिए web APIs के लिए asynchronous ⏸🔀⏯ code use करना बहुत meaningful है।

इसी तरह की asynchronicity ने NodeJS को popular बनाया (हालाँकि NodeJS parallel नहीं है) और यही Go की programming language के रूप में ताकत है।

और यही performance level आपको **FastAPI** के साथ मिलता है।

और क्योंकि आपके पास parallelism और asynchronicity एक ही समय में हो सकते हैं, आपको tested NodeJS frameworks में से अधिकांश से higher performance और Go के बराबर performance मिलती है, जो C के करीब एक compiled language है [(सब Starlette की बदौलत)](https://www.techempower.com/benchmarks/#section=data-r17&hw=ph&test=query&l=zijmkf-1)।

### क्या concurrency parallelism से बेहतर है? { #is-concurrency-better-than-parallelism }

नहीं! यह कहानी की सीख नहीं है।

Concurrency, parallelism से अलग है। और यह **specific** scenarios में बेहतर है जिनमें बहुत इंतज़ार शामिल होता है। इसी कारण, यह web application development के लिए आम तौर पर parallelism से काफ़ी बेहतर होती है। लेकिन हर चीज़ के लिए नहीं।

तो, इसे balance करने के लिए, यह छोटी कहानी imagine करें:

> आपको एक बड़ा, गंदा घर साफ़ करना है।

*हाँ, यही पूरी कहानी है*।

---

कहीं भी कोई इंतज़ार 🕙 नहीं है, बस घर के कई places में बहुत सारा काम करना है।

आप burgers example की तरह turns रख सकते हैं, पहले living room, फिर kitchen, लेकिन क्योंकि आप किसी भी चीज़ का इंतज़ार 🕙 नहीं कर रहे, बस सफ़ाई पर सफ़ाई कर रहे हैं, turns किसी चीज़ को affect नहीं करेंगे।

Turns (concurrency) के साथ या बिना finish करने में उतना ही time लगेगा और आपने उतना ही work किया होगा।

लेकिन इस case में, अगर आप उन 8 ex-cashier/cooks/now-cleaners को ला सकें, और उनमें से हर एक (आपके साथ) घर का एक zone clean करने के लिए ले सके, तो आप extra help के साथ सारा काम **parallel** में कर सकते हैं, और बहुत जल्दी finish कर सकते हैं।

इस scenario में, cleaners में से हर एक (आप सहित) एक processor होगा, अपने हिस्से का job कर रहा होगा।

और क्योंकि execution time का अधिकांश हिस्सा actual work में जाता है (इंतज़ार के बजाय), और computer में work एक <abbr title="Central Processing Unit - केंद्रीय प्रसंस्करण इकाई">CPU</abbr> द्वारा किया जाता है, वे इन problems को "CPU bound" कहते हैं।

---

CPU bound operations के common examples ऐसी चीज़ें हैं जिन्हें complex math processing की आवश्यकता होती है।

उदाहरण के लिए:

* **Audio** या **image processing**।
* **Computer vision**: एक image millions of pixels से बनी होती है, हर pixel में 3 values / colors होते हैं, इसे process करने के लिए आम तौर पर उन pixels पर कुछ compute करना पड़ता है, सब एक ही समय में।
* **Machine Learning**: इसमें आम तौर पर बहुत सारे "matrix" और "vector" multiplications की आवश्यकता होती है। numbers वाली एक huge spreadsheet की कल्पना करें और उन सबको एक ही समय में आपस में multiply करें।
* **Deep Learning**: यह Machine Learning का sub-field है, इसलिए वही लागू होता है। बस यह कि multiply करने के लिए numbers की एक single spreadsheet नहीं होती, बल्कि उनका एक huge set होता है, और कई cases में, आप उन models को build और / या use करने के लिए एक special processor use करते हैं।

### Concurrency + Parallelism: Web + Machine Learning { #concurrency-parallelism-web-machine-learning }

**FastAPI** के साथ आप concurrency का advantage ले सकते हैं जो web development में बहुत common है (NodeJS का वही main attraction)।

लेकिन आप Machine Learning systems जैसे **CPU bound** workloads के लिए parallelism और multiprocessing (parallel में चलने वाले multiple processes) के benefits का भी उपयोग कर सकते हैं।

यह, और साथ में यह simple fact कि Python **Data Science**, Machine Learning और खासकर Deep Learning के लिए main language है, FastAPI को Data Science / Machine Learning web APIs और applications (कई अन्य चीज़ों के बीच) के लिए बहुत अच्छा match बनाता है।

Production में यह parallelism कैसे achieve करें, यह देखने के लिए [Deployment](deployment/index.md) वाला section देखें।

## `async` और `await` { #async-and-await }

Python के modern versions में asynchronous code define करने का बहुत intuitive तरीका है। इससे यह बिल्कुल normal "sequential" code जैसा दिखता है और सही moments पर आपके लिए "awaiting" करता है।

जब कोई operation results देने से पहले इंतज़ार की आवश्यकता रखता है और इन नए Python features के लिए support रखता है, तो आप इसे इस तरह code कर सकते हैं:

```Python
burgers = await get_burgers(2)
```

यहाँ key `await` है। यह Python को बताता है कि उसे `burgers` में results store करने से पहले `get_burgers(2)` के अपना काम 🕙 finish करने का इंतज़ार ⏸ करना है। इससे, Python जान जाएगा कि इस बीच वह कुछ और 🔀 ⏯ कर सकता है (जैसे कोई और request receive करना)।

`await` के काम करने के लिए, उसे ऐसे function के अंदर होना चाहिए जो इस asynchronicity को support करता हो। ऐसा करने के लिए, आप बस उसे `async def` के साथ declare करते हैं:

```Python hl_lines="1"
async def get_burgers(number: int):
    # बर्गर बनाने के लिए कुछ asynchronous काम करें
    return burgers
```

...`def` के बजाय:

```Python hl_lines="2"
# यह asynchronous नहीं है
def get_sequential_burgers(number: int):
    # बर्गर बनाने के लिए कुछ sequential काम करें
    return burgers
```

`async def` के साथ, Python जानता है कि उस function के अंदर उसे `await` expressions के बारे में aware रहना है, और वह उस function की execution को "pause" ⏸ कर सकता है और वापस आने से पहले कुछ और 🔀 कर सकता है।

जब आप किसी `async def` function को call करना चाहते हैं, तो आपको उसे "await" करना होगा। इसलिए, यह काम नहीं करेगा:

```Python
# यह काम नहीं करेगा, क्योंकि get_burgers को async def के साथ define किया गया था
burgers = get_burgers(2)
```

---

तो, अगर आप ऐसी library use कर रहे हैं जो कहती है कि आप उसे `await` के साथ call कर सकते हैं, तो आपको उसे use करने वाली *path operation functions* को `async def` के साथ create करना होगा, जैसे:

```Python hl_lines="2-3"
@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

### अधिक तकनीकी विवरण { #more-technical-details }

आपने notice किया होगा कि `await` का उपयोग केवल `async def` के साथ define किए गए functions के अंदर किया जा सकता है।

लेकिन साथ ही, `async def` के साथ define किए गए functions को "awaited" होना पड़ता है। इसलिए, `async def` वाले functions को भी केवल `async def` के साथ define किए गए functions के अंदर call किया जा सकता है।

तो, egg और chicken के बारे में, आप पहले `async` function को कैसे call करते हैं?

अगर आप **FastAPI** के साथ काम कर रहे हैं तो आपको इसकी चिंता करने की ज़रूरत नहीं है, क्योंकि वह "first" function आपकी *path operation function* होगी, और FastAPI जानता होगा कि सही काम कैसे करना है।

लेकिन अगर आप FastAPI के बिना `async` / `await` use करना चाहते हैं, तो आप ऐसा भी कर सकते हैं।

### अपना async code लिखें { #write-your-own-async-code }

Starlette (और **FastAPI**) [AnyIO](https://anyio.readthedocs.io/en/stable/) पर based हैं, जो इसे Python की standard library [asyncio](https://docs.python.org/3/library/asyncio-task.html) और [Trio](https://trio.readthedocs.io/en/stable/) दोनों के साथ compatible बनाता है।

विशेष रूप से, आप अपने advanced concurrency use cases के लिए सीधे [AnyIO](https://anyio.readthedocs.io/en/stable/) use कर सकते हैं जिन्हें आपके अपने code में अधिक advanced patterns की आवश्यकता होती है।

और अगर आप FastAPI use नहीं भी कर रहे थे, तो भी आप [AnyIO](https://anyio.readthedocs.io/en/stable/) के साथ अपने async applications लिख सकते थे ताकि वे highly compatible हों और उसके benefits (जैसे *structured concurrency*) मिलें।

मैंने AnyIO के ऊपर एक और library बनाई, एक thin layer के रूप में, ताकि type annotations को थोड़ा improve किया जा सके और बेहतर **autocompletion**, **inline errors**, आदि मिल सकें। इसमें एक friendly introduction और tutorial भी है जो आपको **समझने** और **अपना async code** लिखने में मदद करता है: [Asyncer](https://asyncer.tiangolo.com/)। यह विशेष रूप से useful होगा अगर आपको **async code को regular** (blocking/synchronous) code के साथ **combine** करना हो।

### asynchronous code के अन्य रूप { #other-forms-of-asynchronous-code }

`async` और `await` use करने की यह style language में relatively new है।

लेकिन यह asynchronous code के साथ काम करना बहुत आसान बना देती है।

यही syntax (या लगभग identical) हाल ही में JavaScript के modern versions (Browser और NodeJS में) में भी शामिल किया गया था।

लेकिन उससे पहले, asynchronous code handle करना काफ़ी अधिक complex और difficult था।

Python के previous versions में, आप threads या [Gevent](https://www.gevent.org/) use कर सकते थे। लेकिन code को understand, debug, और reason about करना कहीं ज़्यादा complex है।

NodeJS / Browser JavaScript के previous versions में, आप "callbacks" use करते। जो "callback hell" की ओर ले जाता है।

## Coroutines { #coroutines }

**Coroutine** बस उस चीज़ के लिए एक बहुत fancy term है जो `async def` function return करता है। Python जानता है कि यह function जैसी कोई चीज़ है, जिसे वह start कर सकता है और जो किसी point पर end होगी, लेकिन जब भी उसके अंदर कोई `await` होगा तो वह internally pause ⏸ भी हो सकती है।

लेकिन `async` और `await` के साथ asynchronous code use करने की यह सारी functionality कई बार "coroutines" use करने के रूप में summarize की जाती है। यह Go की main key feature, "Goroutines", से comparable है।

## निष्कर्ष { #conclusion }

आइए ऊपर वाली वही phrase देखें:

> Python के modern versions में **"asynchronous code"** के लिए support है, जिसमें **`async` और `await`** syntax के साथ **"coroutines"** नाम की चीज़ का उपयोग होता है।

अब यह अधिक meaningful होना चाहिए। ✨

यही सब FastAPI को power देता है (Starlette के through) और इसे इतनी impressive performance देता है।

## बहुत तकनीकी विवरण { #very-technical-details }

/// warning | चेतावनी

आप शायद इसे skip कर सकते हैं।

ये **FastAPI** के अंदरूनी काम करने के बहुत technical details हैं।

अगर आपके पास काफ़ी technical knowledge है (coroutines, threads, blocking, आदि) और आप curious हैं कि FastAPI `async def` vs normal `def` को कैसे handle करता है, तो आगे बढ़ें।

///

### Path operation functions { #path-operation-functions }

जब आप *path operation function* को `async def` के बजाय normal `def` के साथ declare करते हैं, तो उसे directly call करने के बजाय (क्योंकि वह server को block कर देगा), एक external threadpool में run किया जाता है जिसे फिर await किया जाता है।

अगर आप किसी दूसरे async framework से आ रहे हैं जो ऊपर बताए गए तरीके से काम नहीं करता और आप trivial compute-only *path operation functions* को plain `def` के साथ define करने के आदी हैं ताकि थोड़ा performance gain (लगभग 100 nanoseconds) मिले, तो कृपया ध्यान दें कि **FastAPI** में effect काफ़ी उल्टा होगा। इन cases में, `async def` use करना बेहतर है जब तक कि आपकी *path operation functions* ऐसा code use न करें जो blocking <abbr title="Input/Output - इनपुट/आउटपुट: disk reading या writing, network communications.">I/O</abbr> perform करता हो।

फिर भी, दोनों situations में, संभावना है कि **FastAPI** आपके previous framework से [फिर भी तेज़ होगा](index.md#performance) (या कम से कम comparable होगा)।

### Dependencies { #dependencies }

[dependencies](tutorial/dependencies/index.md) के लिए भी यही लागू होता है। अगर कोई dependency `async def` के बजाय standard `def` function है, तो उसे external threadpool में run किया जाता है।

### Sub-dependencies { #sub-dependencies }

आपके पास multiple dependencies और [sub-dependencies](tutorial/dependencies/sub-dependencies.md) हो सकती हैं जो एक-दूसरे की आवश्यकता रखती हैं (function definitions के parameters के रूप में), उनमें से कुछ `async def` के साथ बनाई गई हो सकती हैं और कुछ normal `def` के साथ। यह फिर भी काम करेगा, और normal `def` के साथ बनाई गई ones को "awaited" किए जाने के बजाय external thread (threadpool से) पर call किया जाएगा।

### अन्य utility functions { #other-utility-functions }

कोई भी अन्य utility function जिसे आप directly call करते हैं, normal `def` या `async def` के साथ बनाया जा सकता है और FastAPI इस बात को affect नहीं करेगा कि आप उसे कैसे call करते हैं।

यह उन functions के contrast में है जिन्हें FastAPI आपके लिए call करता है: *path operation functions* और dependencies।

अगर आपका utility function `def` वाला normal function है, तो वह directly call होगा (जैसे आप अपने code में लिखते हैं), threadpool में नहीं; अगर function `async def` के साथ बनाया गया है तो आपको अपने code में उसे call करते समय उस function को `await` करना चाहिए।

---

फिर से, ये बहुत technical details हैं जो शायद useful हों अगर आप इन्हें खोजते हुए आए हों।

अन्यथा, ऊपर के section की guidelines आपके लिए पर्याप्त होनी चाहिए: <a href="#in-a-hurry">जल्दी में हैं?</a>।
