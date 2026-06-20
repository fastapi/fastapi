# Concurrency और async / await { #concurrency-and-async-await }

*path operation functions* के लिए `async def` syntax के बारे में विवरण और asynchronous code, concurrency, और parallelism के बारे में कुछ पृष्ठभूमि।

## जल्दी में हैं? { #in-a-hurry }

<abbr title="too long; didn't read - बहुत लंबा; नहीं पढ़ा"><strong>TL;DR:</strong></abbr>

अगर आप third party libraries का उपयोग कर रहे हैं जो आपको उन्हें `await` के साथ call करने को कहती हैं, जैसे:

```Python
results = await some_library()
```

तो, अपने *path operation functions* को `async def` के साथ declare करें, जैसे:

```Python hl_lines="2"
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

/// note | नोट

आप `await` का उपयोग केवल `async def` के साथ बनाए गए functions के अंदर ही कर सकते हैं।

///

---

अगर आप ऐसी third party library का उपयोग कर रहे हैं जो किसी चीज़ (database, API, file system, आदि) से communicate करती है और `await` का उपयोग करने का support नहीं रखती, (वर्तमान में अधिकांश database libraries के साथ यही स्थिति है), तो अपने *path operation functions* को सामान्य रूप से, केवल `def` के साथ declare करें, जैसे:

```Python hl_lines="2"
@app.get('/')
def results():
    results = some_library()
    return results
```

---

अगर आपके application को (किसी तरह) किसी और चीज़ से communicate करने और उसके response का इंतज़ार करने की ज़रूरत नहीं है, तो `async def` का उपयोग करें, भले ही आपको अंदर `await` का उपयोग करने की ज़रूरत न हो।

---

अगर आपको पता नहीं है, तो सामान्य `def` का उपयोग करें।

---

**नोट**: आप अपनी ज़रूरत के अनुसार अपने *path operation functions* में `def` और `async def` को mix कर सकते हैं और हर एक को अपने लिए सबसे अच्छे option का उपयोग करके define कर सकते हैं। FastAPI उनके साथ सही काम करेगा।

किसी भी स्थिति में, ऊपर दिए गए किसी भी case में, FastAPI फिर भी asynchronously काम करेगा और बेहद तेज़ होगा।

लेकिन ऊपर दिए गए steps को follow करने से, यह कुछ performance optimizations कर पाएगा।

## तकनीकी विवरण { #technical-details }

Python के आधुनिक versions **"asynchronous code"** का support करते हैं, जो **"coroutines"** नाम की चीज़ का उपयोग करता है, **`async` और `await`** syntax के साथ।

आइए नीचे के sections में इस phrase को हिस्सों में देखते हैं:

* **Asynchronous Code**
* **`async` और `await`**
* **Coroutines**

## Asynchronous Code { #asynchronous-code }

Asynchronous code का मतलब बस यह है कि language 💬 के पास computer / program 🤖 को यह बताने का एक तरीका होता है कि code में किसी point पर, उसे 🤖 कहीं और *किसी और चीज़* के finish होने का इंतज़ार करना होगा। मान लें कि उस *किसी और चीज़* को "slow-file" 📝 कहा जाता है।

तो, उस समय के दौरान, computer कोई और काम कर सकता है, जबकि "slow-file" 📝 finish हो रही होती है।

फिर computer / program 🤖 हर बार वापस आएगा जब उसे मौका मिलेगा क्योंकि वह फिर से इंतज़ार कर रहा होगा, या जब भी वह 🤖 उस point पर अपना सारा काम finish कर लेगा। और वह 🤖 देखेगा कि जिन tasks का वह इंतज़ार कर रहा था, उनमें से कोई पहले ही finish हो चुका है या नहीं, फिर वह जो भी करना था करेगा।

इसके बाद, वह 🤖 finish होने वाला पहला task लेता है (मान लें, हमारी "slow-file" 📝) और उसके साथ जो भी करना था उसे जारी रखता है।

वह "किसी और चीज़ का इंतज़ार" आम तौर पर <abbr title="Input and Output - इनपुट और आउटपुट">I/O</abbr> operations को refer करता है जो अपेक्षाकृत "slow" होते हैं (processor और RAM memory की speed की तुलना में), जैसे इंतज़ार करना:

* client से data network के माध्यम से भेजे जाने का
* आपके program द्वारा भेजा गया data client द्वारा network के माध्यम से receive किए जाने का
* disk पर किसी file की contents system द्वारा पढ़े जाने और आपके program को दिए जाने का
* आपके program द्वारा system को दी गई contents disk पर लिखे जाने का
* किसी remote API operation का
* किसी database operation के finish होने का
* किसी database query द्वारा results return किए जाने का
* आदि।

क्योंकि execution time ज़्यादातर <abbr title="Input and Output - इनपुट और आउटपुट">I/O</abbr> operations का इंतज़ार करने में consume होता है, उन्हें "I/O bound" operations कहा जाता है।

इसे "asynchronous" इसलिए कहा जाता है क्योंकि computer / program को slow task के साथ "synchronized" होने की ज़रूरत नहीं होती, task के finish होने के exact moment का इंतज़ार करते हुए, कुछ भी न करते हुए, ताकि वह task result ले सके और काम जारी रख सके।

इसके बजाय, "asynchronous" system होने के कारण, task finish होने के बाद, computer / program के वापस आने तक थोड़ा सा line में wait कर सकता है (कुछ microseconds), ताकि computer / program जो काम करने गया था उसे finish करे, और फिर वापस आकर results ले और उनके साथ काम जारी रखे।

"Synchronous" ("asynchronous" के विपरीत) के लिए वे आमतौर पर "sequential" term भी use करते हैं, क्योंकि computer / program किसी अलग task पर switch करने से पहले sequence में सभी steps follow करता है, भले ही उन steps में इंतज़ार शामिल हो।

### Concurrency और Burgers { #concurrency-and-burgers }

ऊपर describe किए गए **asynchronous** code के इस idea को कभी-कभी **"concurrency"** भी कहा जाता है। यह **"parallelism"** से अलग है।

**Concurrency** और **parallelism** दोनों "अलग-अलग चीज़ें लगभग एक ही समय पर हो रही हैं" से related हैं।

लेकिन *concurrency* और *parallelism* के बीच के details काफी अलग हैं।

अंतर देखने के लिए, burgers के बारे में निम्न story imagine करें:

### Concurrent Burgers { #concurrent-burgers }

आप अपनी crush के साथ fast food लेने जाते हैं, आप line में खड़े होते हैं जबकि cashier आपके आगे के लोगों से orders ले रहा होता है। 😍

<img src="/img/async/concurrent-burgers/concurrent-burgers-01.png" class="illustration">

फिर आपकी बारी आती है, आप अपनी crush और अपने लिए 2 बहुत fancy burgers का order देते हैं। 🍔🍔

<img src="/img/async/concurrent-burgers/concurrent-burgers-02.png" class="illustration">

Cashier kitchen में cook से कुछ कहता है ताकि उन्हें पता हो कि उन्हें आपके burgers prepare करने हैं (भले ही वे currently previous clients के burgers prepare कर रहे हों)।

<img src="/img/async/concurrent-burgers/concurrent-burgers-03.png" class="illustration">

आप pay करते हैं। 💸

Cashier आपको आपकी turn का number देता है।

<img src="/img/async/concurrent-burgers/concurrent-burgers-04.png" class="illustration">

जब आप wait कर रहे होते हैं, आप अपनी crush के साथ एक table चुनते हैं, बैठते हैं और अपनी crush से लंबे समय तक बात करते हैं (क्योंकि आपके burgers बहुत fancy हैं और prepare होने में कुछ समय लेते हैं)।

जब आप अपनी crush के साथ table पर बैठे होते हैं, burgers का इंतज़ार करते हुए, आप उस समय को यह admire करने में spend कर सकते हैं कि आपकी crush कितनी awesome, cute और smart है ✨😍✨।

<img src="/img/async/concurrent-burgers/concurrent-burgers-05.png" class="illustration">

Wait करते हुए और अपनी crush से बात करते हुए, time to time, आप counter पर displayed number check करते हैं कि क्या आपकी turn आ गई है।

फिर किसी point पर, आखिरकार आपकी turn आ जाती है। आप counter पर जाते हैं, अपने burgers लेते हैं और table पर वापस आते हैं।

<img src="/img/async/concurrent-burgers/concurrent-burgers-06.png" class="illustration">

आप और आपकी crush burgers खाते हैं और अच्छा समय बिताते हैं। ✨

<img src="/img/async/concurrent-burgers/concurrent-burgers-07.png" class="illustration">

/// note | नोट

सुंदर illustrations [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot) द्वारा। 🎨

///

---

कल्पना करें कि उस story में आप computer / program 🤖 हैं।

जब आप line में होते हैं, आप बस idle 😴 होते हैं, अपनी turn का इंतज़ार करते हुए, कुछ बहुत "productive" नहीं कर रहे होते। लेकिन line fast है क्योंकि cashier केवल orders ले रहा है (उन्हें prepare नहीं कर रहा), इसलिए यह ठीक है।

फिर, जब आपकी turn आती है, आप actual "productive" work करते हैं, menu process करते हैं, decide करते हैं कि आपको क्या चाहिए, अपनी crush की choice लेते हैं, pay करते हैं, check करते हैं कि आप correct bill या card दे रहे हैं, check करते हैं कि आपसे सही charge किया गया है, check करते हैं कि order में correct items हैं, आदि।

लेकिन फिर, भले ही आपके पास अभी burgers नहीं हैं, cashier के साथ आपका work "on pause" ⏸ है, क्योंकि आपको अपने burgers ready होने का wait 🕙 करना है।

लेकिन जब आप counter से दूर जाते हैं और अपनी turn के number के साथ table पर बैठते हैं, आप अपना attention अपनी crush पर switch 🔀 कर सकते हैं, और उस पर "work" ⏯ 🤓 कर सकते हैं। फिर आप दोबारा कुछ बहुत "productive" कर रहे होते हैं, जैसे अपनी crush 😍 के साथ flirting।

फिर cashier 💁 counter के display पर आपका number डालकर कहता है "मैंने burgers बना लिए हैं", लेकिन displayed number आपकी turn number में बदलते ही आप तुरंत पागलों की तरह jump नहीं करते। आपको पता है कि कोई आपके burgers नहीं चुराएगा क्योंकि आपके पास आपकी turn का number है, और उनके पास उनका।

तो आप अपनी crush के story finish करने का इंतज़ार करते हैं (current work ⏯ / process हो रहा task 🤓 finish होना), gentle smile करते हैं और कहते हैं कि आप burgers लेने जा रहे हैं ⏸।

फिर आप counter 🔀 पर जाते हैं, उस initial task पर जो अब finish हो चुका है ⏯, burgers उठाते हैं, thanks कहते हैं और उन्हें table पर ले जाते हैं। इससे counter के साथ interaction का वह step / task finish हो जाता है ⏹। यह बदले में, "eating burgers" 🔀 ⏯ का एक नया task create करता है, लेकिन "getting burgers" वाला previous task finish हो चुका है ⏹।

### Parallel Burgers { #parallel-burgers }

अब imagine करें कि ये "Concurrent Burgers" नहीं, बल्कि "Parallel Burgers" हैं।

आप अपनी crush के साथ parallel fast food लेने जाते हैं।

आप line में खड़े होते हैं जबकि कई (मान लें 8) cashiers, जो उसी समय cooks भी हैं, आपके आगे के लोगों से orders ले रहे होते हैं।

आपसे पहले हर कोई counter छोड़ने से पहले अपने burgers ready होने का wait कर रहा है क्योंकि 8 cashiers में से हर एक next order लेने से पहले तुरंत जाकर burger prepare करता है।

<img src="/img/async/parallel-burgers/parallel-burgers-01.png" class="illustration">

फिर आखिरकार आपकी turn आती है, आप अपनी crush और अपने लिए 2 बहुत fancy burgers का order देते हैं।

आप pay करते हैं 💸।

<img src="/img/async/parallel-burgers/parallel-burgers-02.png" class="illustration">

Cashier kitchen में जाता है।

आप counter 🕙 के सामने खड़े होकर wait करते हैं, ताकि आपसे पहले कोई और आपके burgers न ले जाए, क्योंकि turns के लिए कोई numbers नहीं हैं।

<img src="/img/async/parallel-burgers/parallel-burgers-03.png" class="illustration">

क्योंकि आप और आपकी crush इस बात में busy हैं कि कोई आपके आगे न आ जाए और आपके burgers आते ही उन्हें न ले जाए, आप अपनी crush पर attention नहीं दे सकते। 😞

यह "synchronous" work है, आप cashier/cook 👨‍🍳 के साथ "synchronized" हैं। आपको wait 🕙 करना है और exact moment पर वहाँ होना है जब cashier/cook 👨‍🍳 burgers finish करता है और आपको देता है, नहीं तो कोई और उन्हें ले सकता है।

<img src="/img/async/parallel-burgers/parallel-burgers-04.png" class="illustration">

फिर आपका cashier/cook 👨‍🍳 लंबे समय तक counter के सामने wait 🕙 कराने के बाद आखिरकार आपके burgers लेकर वापस आता है।

<img src="/img/async/parallel-burgers/parallel-burgers-05.png" class="illustration">

आप अपने burgers लेते हैं और अपनी crush के साथ table पर जाते हैं।

आप बस उन्हें खाते हैं, और आपका काम हो जाता है। ⏹

<img src="/img/async/parallel-burgers/parallel-burgers-06.png" class="illustration">

ज़्यादा बात या flirting नहीं हुई क्योंकि अधिकतर समय counter के सामने wait 🕙 करने में spend हुआ। 😞

/// note | नोट

सुंदर illustrations [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot) द्वारा। 🎨

///

---

Parallel burgers के इस scenario में, आप एक computer / program 🤖 हैं जिसमें दो processors हैं (आप और आपकी crush), दोनों wait 🕙 कर रहे हैं और लंबे समय तक "counter पर waiting" 🕙 में अपना attention ⏯ dedicate कर रहे हैं।

Fast food store में 8 processors (cashiers/cooks) हैं। जबकि concurrent burgers store में शायद केवल 2 (एक cashier और एक cook) रहे होंगे।

लेकिन फिर भी, final experience सबसे अच्छा नहीं है। 😞

---

यह burgers के लिए parallel equivalent story होगी। 🍔

इसके एक और "real life" example के लिए, एक bank imagine करें।

हाल तक, अधिकांश banks में multiple cashiers 👨‍💼👨‍💼👨‍💼👨‍💼 और एक बड़ी line 🕙🕙🕙🕙🕙🕙🕙🕙 होती थी।

सभी cashiers एक client के बाद दूसरे client के साथ सारा काम कर रहे होते थे 👨‍💼⏯।

और आपको line में लंबे समय तक wait 🕙 करना पड़ता है या आप अपनी turn खो देते हैं।

आप शायद अपनी crush 😍 को bank 🏦 में errands करने के लिए अपने साथ नहीं ले जाना चाहेंगे।

### Burger निष्कर्ष { #burger-conclusion }

"अपनी crush के साथ fast food burgers" के इस scenario में, क्योंकि बहुत waiting 🕙 है, concurrent system ⏸🔀⏯ रखना कहीं अधिक sensible है।

अधिकांश web applications के लिए यही case है।

बहुत, बहुत सारे users, लेकिन आपका server उनकी not-so-good connection द्वारा उनकी requests भेजने का wait 🕙 कर रहा है।

और फिर responses वापस आने का फिर से wait 🕙 कर रहा है।

यह "waiting" 🕙 microseconds में measure की जाती है, लेकिन फिर भी, सबको जोड़ने पर, अंत में काफी waiting हो जाती है।

इसीलिए web APIs के लिए asynchronous ⏸🔀⏯ code use करना बहुत sensible है।

इसी तरह की asynchronicity ने NodeJS को popular बनाया (भले ही NodeJS parallel नहीं है) और यही Go की programming language के रूप में strength है।

और यही same level की performance आपको **FastAPI** के साथ मिलती है।

और क्योंकि आपके पास parallelism और asynchronicity एक ही समय पर हो सकते हैं, आपको tested NodeJS frameworks में से अधिकांश से higher performance मिलती है और Go के बराबर, जो C के करीब एक compiled language है [(यह सब Starlette के कारण)](https://www.techempower.com/benchmarks/#section=data-r17&hw=ph&test=query&l=zijmkf-1)।

### क्या concurrency parallelism से बेहतर है? { #is-concurrency-better-than-parallelism }

नहीं! यह story की moral नहीं है।

Concurrency, parallelism से अलग है। और यह उन **specific** scenarios में बेहतर है जिनमें बहुत waiting शामिल होती है। इसी कारण, web application development के लिए यह आम तौर पर parallelism से बहुत बेहतर है। लेकिन हर चीज़ के लिए नहीं।

तो, इसे balance करने के लिए, निम्न short story imagine करें:

> आपको एक बड़ा, गंदा house clean करना है।

*हाँ, यही पूरी story है*।

---

कहीं भी कोई waiting 🕙 नहीं है, बस बहुत सारा काम करना है, house के multiple places में।

आप burgers example की तरह turns रख सकते थे, पहले living room, फिर kitchen, लेकिन क्योंकि आप किसी चीज़ का wait 🕙 नहीं कर रहे, बस cleaning and cleaning कर रहे हैं, turns किसी चीज़ को affect नहीं करेंगे।

Turns (concurrency) के साथ या बिना finish करने में उतना ही time लगेगा और आपने उतना ही काम किया होगा।

लेकिन इस case में, अगर आप 8 ex-cashier/cooks/now-cleaners ला सकें, और उनमें से हर एक (plus आप) house का एक zone clean करने के लिए ले सके, तो आप extra help के साथ सारा काम **parallel** में कर सकते हैं, और बहुत जल्दी finish कर सकते हैं।

इस scenario में, cleaners में से हर एक (आप सहित) एक processor होगा, job का अपना part कर रहा होगा।

और क्योंकि execution time का अधिकतर हिस्सा actual work (waiting के बजाय) में लगता है, और computer में work <abbr title="Central Processing Unit - केंद्रीय प्रसंस्करण इकाई">CPU</abbr> द्वारा किया जाता है, वे इन problems को "CPU bound" कहते हैं।

---

CPU bound operations के common examples ऐसी चीज़ें हैं जिन्हें complex math processing की ज़रूरत होती है।

उदाहरण के लिए:

* **Audio** या **image processing**।
* **Computer vision**: एक image millions of pixels से composed होती है, हर pixel में 3 values / colors होते हैं, उसे process करने के लिए आम तौर पर उन pixels पर कुछ compute करना पड़ता है, सब एक ही समय पर।
* **Machine Learning**: इसमें आम तौर पर बहुत सारे "matrix" और "vector" multiplications की ज़रूरत होती है। Numbers वाली एक huge spreadsheet के बारे में सोचें और उन सभी को एक ही समय पर multiply करना।
* **Deep Learning**: यह Machine Learning का sub-field है, इसलिए, वही लागू होता है। बस इतना है कि multiply करने के लिए numbers की एक single spreadsheet नहीं होती, बल्कि उनका huge set होता है, और कई cases में, आप उन models को build और / या use करने के लिए एक special processor का उपयोग करते हैं।

### Concurrency + Parallelism: Web + Machine Learning { #concurrency-parallelism-web-machine-learning }

**FastAPI** के साथ आप concurrency का advantage ले सकते हैं जो web development के लिए बहुत common है (NodeJS का वही main attraction)।

लेकिन आप Machine Learning systems जैसे **CPU bound** workloads के लिए parallelism और multiprocessing (multiple processes parallel में चलाना) के benefits का भी exploit कर सकते हैं।

वह, साथ ही यह simple fact कि Python **Data Science**, Machine Learning और खासकर Deep Learning की main language है, FastAPI को Data Science / Machine Learning web APIs और applications (कई अन्य के बीच) के लिए बहुत अच्छा match बनाता है।

Production में इस parallelism को कैसे achieve करें, यह देखने के लिए [Deployment](deployment/index.md) के बारे में section देखें।

## `async` और `await` { #async-and-await }

Python के आधुनिक versions में asynchronous code define करने का बहुत intuitive तरीका है। इससे यह सामान्य "sequential" code जैसा दिखता है और सही moments पर आपके लिए "awaiting" करता है।

जब कोई operation results देने से पहले waiting require करेगा और इन नए Python features का support रखता है, तो आप उसे ऐसे code कर सकते हैं:

```Python
burgers = await get_burgers(2)
```

यहाँ key `await` है। यह Python को बताता है कि `burgers` में results store करने से पहले उसे `get_burgers(2)` के अपना काम 🕙 finish करने का wait ⏸ करना है। इससे, Python जान जाएगा कि वह meanwhile कुछ और 🔀 ⏯ कर सकता है (जैसे कोई दूसरी request receive करना)।

`await` के work करने के लिए, इसे ऐसे function के अंदर होना चाहिए जो इस asynchronicity को support करता हो। ऐसा करने के लिए, आप बस इसे `async def` के साथ declare करते हैं:

```Python hl_lines="1"
async def get_burgers(number: int):
    # Burgers बनाने के लिए कुछ asynchronous काम करें
    return burgers
```

...`def` के बजाय:

```Python hl_lines="2"
# यह asynchronous नहीं है
def get_sequential_burgers(number: int):
    # Burgers बनाने के लिए कुछ sequential काम करें
    return burgers
```

`async def` के साथ, Python जानता है कि उस function के अंदर उसे `await` expressions के बारे में aware रहना है, और वह उस function के execution को "pause" ⏸ कर सकता है और वापस आने से पहले कुछ और 🔀 कर सकता है।

जब आप किसी `async def` function को call करना चाहते हैं, तो आपको उसे "await" करना होता है। इसलिए, यह काम नहीं करेगा:

```Python
# यह काम नहीं करेगा, क्योंकि get_burgers को async def के साथ define किया गया था
burgers = get_burgers(2)
```

---

तो, अगर आप कोई library use कर रहे हैं जो आपको बताती है कि आप उसे `await` के साथ call कर सकते हैं, तो आपको उसका उपयोग करने वाले *path operation functions* को `async def` के साथ create करना होगा, जैसे:

```Python hl_lines="2-3"
@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

### अधिक तकनीकी विवरण { #more-technical-details }

आपने notice किया होगा कि `await` केवल `async def` के साथ defined functions के अंदर ही use किया जा सकता है।

लेकिन उसी समय, `async def` के साथ defined functions को "awaited" होना पड़ता है। इसलिए, `async def` वाले functions केवल `async def` के साथ defined functions के अंदर ही call किए जा सकते हैं।

तो, egg और chicken के बारे में, आप first `async` function को कैसे call करते हैं?

अगर आप **FastAPI** के साथ काम कर रहे हैं तो आपको इसकी चिंता करने की ज़रूरत नहीं है, क्योंकि वह "first" function आपका *path operation function* होगा, और FastAPI जानता होगा कि सही काम कैसे करना है।

लेकिन अगर आप FastAPI के बिना `async` / `await` use करना चाहते हैं, तो आप ऐसा भी कर सकते हैं।

### अपना async code लिखें { #write-your-own-async-code }

Starlette (और **FastAPI**) [AnyIO](https://anyio.readthedocs.io/en/stable/) पर based हैं, जो इसे Python की standard library [asyncio](https://docs.python.org/3/library/asyncio-task.html) और [Trio](https://trio.readthedocs.io/en/stable/) दोनों के साथ compatible बनाता है।

विशेष रूप से, आप अपने advanced concurrency use cases के लिए सीधे [AnyIO](https://anyio.readthedocs.io/en/stable/) use कर सकते हैं जिन्हें आपके अपने code में अधिक advanced patterns की ज़रूरत होती है।

और भले ही आप FastAPI use नहीं कर रहे हों, आप high compatibility और इसके benefits (जैसे *structured concurrency*) पाने के लिए [AnyIO](https://anyio.readthedocs.io/en/stable/) के साथ अपने खुद के async applications भी लिख सकते हैं।

मैंने AnyIO के ऊपर एक और library बनाई, ऊपर एक thin layer के रूप में, ताकि type annotations को थोड़ा improve किया जा सके और बेहतर **autocompletion**, **inline errors**, आदि मिल सकें। इसमें एक friendly introduction और tutorial भी है ताकि आपको **समझने** और **अपना async code** लिखने में मदद मिले: [Asyncer](https://asyncer.tiangolo.com/)। यह विशेष रूप से useful होगा अगर आपको **async code को regular** (blocking/synchronous) code के साथ **combine** करना हो।

### Asynchronous code के अन्य forms { #other-forms-of-asynchronous-code }

`async` और `await` use करने की यह style language में relatively new है।

लेकिन यह asynchronous code के साथ काम करना बहुत आसान बनाती है।

यही same syntax (या लगभग identical) हाल ही में JavaScript के modern versions (Browser और NodeJS में) में भी शामिल किया गया था।

लेकिन उससे पहले, asynchronous code handle करना कहीं अधिक complex और difficult था।

Python के previous versions में, आप threads या [Gevent](https://www.gevent.org/) use कर सकते थे। लेकिन code समझने, debug करने और उसके बारे में सोचने के लिए कहीं अधिक complex होता है।

NodeJS / Browser JavaScript के previous versions में, आप "callbacks" use करते। जो "callback hell" तक ले जाता है।

## Coroutines { #coroutines }

**Coroutine** बस उस चीज़ के लिए बहुत fancy term है जो किसी `async def` function द्वारा return की जाती है। Python जानता है कि यह function जैसी कोई चीज़ है, जिसे वह start कर सकता है और जो किसी point पर end होगी, लेकिन यह internally pause ⏸ भी हो सकती है, जब भी इसके अंदर कोई `await` हो।

लेकिन asynchronous code को `async` और `await` के साथ use करने की यह सारी functionality कई बार "coroutines" use करने के रूप में summarize की जाती है। यह Go की main key feature, "Goroutines" से comparable है।

## निष्कर्ष { #conclusion }

आइए ऊपर वाला वही phrase देखें:

> Python के आधुनिक versions **"asynchronous code"** का support करते हैं, जो **"coroutines"** नाम की चीज़ का उपयोग करता है, **`async` और `await`** syntax के साथ।

अब यह अधिक sense बनाना चाहिए। ✨

यह सब FastAPI (Starlette के माध्यम से) को power करता है और इसे इतनी impressive performance देता है।

## बहुत तकनीकी विवरण { #very-technical-details }

/// warning | चेतावनी

आप शायद इसे skip कर सकते हैं।

ये **FastAPI** अंदर से कैसे काम करता है, इसके बहुत technical details हैं।

अगर आपके पास काफी technical knowledge (coroutines, threads, blocking, आदि) है और आप curious हैं कि FastAPI `async def` बनाम normal `def` को कैसे handle करता है, तो आगे बढ़ें।

///

### Path operation functions { #path-operation-functions }

जब आप किसी *path operation function* को `async def` के बजाय normal `def` के साथ declare करते हैं, तो इसे directly call करने के बजाय (क्योंकि यह server को block करेगा), एक external threadpool में run किया जाता है जिसे फिर awaited किया जाता है।

अगर आप किसी दूसरे async framework से आ रहे हैं जो ऊपर described तरीके से काम नहीं करता और आप tiny performance gain (लगभग 100 nanoseconds) के लिए trivial compute-only *path operation functions* को plain `def` के साथ define करने के आदी हैं, तो कृपया ध्यान दें कि **FastAPI** में effect बिल्कुल उल्टा होगा। इन cases में, `async def` use करना बेहतर है, जब तक कि आपके *path operation functions* ऐसा code use न करें जो blocking <abbr title="Input/Output - इनपुट/आउटपुट: disk पढ़ना या लिखना, network संचार.">I/O</abbr> perform करता हो।

फिर भी, दोनों situations में, संभावना है कि **FastAPI** आपके previous framework से [फिर भी तेज़ होगा](index.md#performance) (या कम से कम comparable होगा)।

### Dependencies { #dependencies }

[Dependencies](tutorial/dependencies/index.md) के लिए भी यही लागू होता है। अगर कोई dependency `async def` के बजाय standard `def` function है, तो उसे external threadpool में run किया जाता है।

### Sub-dependencies { #sub-dependencies }

आपके पास multiple dependencies और [sub-dependencies](tutorial/dependencies/sub-dependencies.md) हो सकती हैं जो एक-दूसरे को require करती हैं (function definitions के parameters के रूप में), उनमें से कुछ `async def` के साथ created हो सकती हैं और कुछ normal `def` के साथ। यह फिर भी work करेगा, और normal `def` के साथ created ones को "awaited" होने के बजाय external thread (threadpool से) पर call किया जाएगा।

### अन्य utility functions { #other-utility-functions }

कोई भी अन्य utility function जिसे आप directly call करते हैं, normal `def` या `async def` के साथ created हो सकता है और FastAPI आपके उसे call करने के तरीके को affect नहीं करेगा।

यह उन functions के contrast में है जिन्हें FastAPI आपके लिए call करता है: *path operation functions* और dependencies।

अगर आपका utility function `def` वाला normal function है, तो उसे directly call किया जाएगा (जैसा आप अपने code में लिखते हैं), threadpool में नहीं; अगर function `async def` के साथ created है तो आपको अपने code में उसे call करते समय उस function को `await` करना चाहिए।

---

फिर से, ये बहुत technical details हैं जो शायद useful होंगे अगर आप इन्हें search करते हुए आए हैं।

अन्यथा, आपको ऊपर के section की guidelines के साथ ठीक होना चाहिए: <a href="#in-a-hurry">जल्दी में हैं?</a>।
