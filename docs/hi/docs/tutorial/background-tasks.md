# Background Tasks { #background-tasks }

आप background tasks define कर सकते हैं जिन्हें response लौटाने के *बाद* चलाया जाए।

यह उन operations के लिए उपयोगी है जिन्हें request के बाद होना होता है, लेकिन client को response पाने से पहले operation के पूरा होने का इंतज़ार करने की वास्तव में ज़रूरत नहीं होती।

इसमें, उदाहरण के लिए, ये शामिल हैं:

* कोई action करने के बाद भेजे गए email notifications:
    * क्योंकि email server से connect करना और email भेजना आम तौर पर "slow" (कई seconds) होता है, आप response तुरंत लौटा सकते हैं और email notification को background में भेज सकते हैं।
* data process करना:
    * उदाहरण के लिए, मान लीजिए आपको एक file मिलती है जिसे किसी slow process से गुजरना है, आप "Accepted" (HTTP 202) का response लौटा सकते हैं और file को background में process कर सकते हैं।

## `BackgroundTasks` का उपयोग करना { #using-backgroundtasks }

सबसे पहले, `BackgroundTasks` import करें और अपनी *path operation function* में `BackgroundTasks` की type declaration के साथ एक parameter define करें:

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[1,13] *}

**FastAPI** आपके लिए `BackgroundTasks` type का object बनाएगा और उसे उस parameter के रूप में pass करेगा।

## task function बनाएँ { #create-a-task-function }

background task के रूप में चलाने के लिए एक function बनाएँ।

यह बस एक standard function है जो parameters receive कर सकता है।

यह `async def` या normal `def` function हो सकता है, **FastAPI** जानता होगा कि इसे सही तरीके से कैसे handle करना है।

इस case में, task function एक file में लिखेगा (email भेजने का simulation करते हुए)।

और क्योंकि write operation `async` और `await` का उपयोग नहीं करता, हम function को normal `def` के साथ define करते हैं:

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[6:9] *}

## background task जोड़ें { #add-the-background-task }

अपनी *path operation function* के अंदर, अपनी task function को *background tasks* object में method `.add_task()` के साथ pass करें:

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[14] *}

`.add_task()` arguments के रूप में receive करता है:

* background में चलाने के लिए एक task function (`write_notification`)।
* arguments की कोई भी sequence जो order में task function को pass की जानी चाहिए (`email`)।
* कोई भी keyword arguments जो task function को pass किए जाने चाहिए (`message="some notification"`)।

## Dependency Injection { #dependency-injection }

`BackgroundTasks` का उपयोग dependency injection system के साथ भी काम करता है, आप कई levels पर `BackgroundTasks` type का parameter declare कर सकते हैं: किसी *path operation function* में, dependency (dependable) में, sub-dependency में, आदि।

**FastAPI** जानता है कि हर case में क्या करना है और same object को कैसे reuse करना है, ताकि सभी background tasks merge हो जाएँ और बाद में background में run हों:


{* ../../docs_src/background_tasks/tutorial002_an_py310.py hl[13,15,22,25] *}


इस example में, response भेजे जाने के *बाद* messages `log.txt` file में लिखे जाएँगे।

अगर request में कोई query थी, तो उसे एक background task में log में लिखा जाएगा।

और फिर *path operation function* पर generate हुआ एक और background task `email` path parameter का उपयोग करके एक message लिखेगा।

## Technical Details { #technical-details }

class `BackgroundTasks` सीधे [`starlette.background`](https://www.starlette.dev/background/) से आती है।

इसे सीधे FastAPI में import/include किया गया है ताकि आप इसे `fastapi` से import कर सकें और गलती से `starlette.background` से alternative `BackgroundTask` (अंत में `s` के बिना) import करने से बच सकें।

सिर्फ `BackgroundTasks` (और `BackgroundTask` नहीं) का उपयोग करने से, इसे *path operation function* parameter के रूप में use करना संभव होता है और **FastAPI** आपके लिए बाकी चीज़ें handle करता है, ठीक वैसे ही जैसे `Request` object को सीधे use करते समय होता है।

FastAPI में अकेले `BackgroundTask` का उपयोग करना अभी भी संभव है, लेकिन आपको अपने code में object बनाना होगा और उसे शामिल करते हुए Starlette `Response` return करना होगा।

आप [Background Tasks के लिए Starlette के official docs](https://www.starlette.dev/background/) में अधिक details देख सकते हैं।

## सावधानी { #caveat }

अगर आपको heavy background computation perform करनी है और यह ज़रूरी नहीं है कि वह same process द्वारा run हो (उदाहरण के लिए, आपको memory, variables, आदि share करने की ज़रूरत नहीं है), तो आपको [Celery](https://docs.celeryq.dev) जैसे दूसरे बड़े tools का उपयोग करने से लाभ हो सकता है।

उन्हें आम तौर पर अधिक complex configurations, RabbitMQ या Redis जैसे message/job queue manager की ज़रूरत होती है, लेकिन वे आपको multiple processes में, और खासकर multiple servers में, background tasks run करने देते हैं।

लेकिन अगर आपको उसी **FastAPI** app से variables और objects access करने हैं, या आपको छोटे background tasks perform करने हैं (जैसे email notification भेजना), तो आप आसानी से `BackgroundTasks` का उपयोग कर सकते हैं।

## Recap { #recap }

background tasks जोड़ने के लिए *path operation functions* और dependencies में parameters के साथ `BackgroundTasks` import और use करें।
