# Eşzamanlılık ve async / await

*path operasyon fonksiyonu* için `async def`sözyazımı,  asenkron kod, eşzamanlılık ve paralellik hakkında bazı bilgiler.

## Aceleniz mi var?

<abbr title="too long; didn't read"><strong>TL;DR:</strong></abbr>

Eğer onları `await` ile çağırmanızı söyleyen üçüncü taraf bir kütüphane kullanıyorsanız, örneğin:

```Python
results = await some_library()
```

O zaman *path operasyon fonksiyonunu*  `async def` ile tanımlayın:

```Python hl_lines="2"
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

!!! not
    `await` yalnızca `async def` ile tanımlanan fonksiyonların içinde kullanılabilir.

---

Eğer üçüncü parti kütüphaneler ile beraber birşeyler ile etkileşimde bulunuyorsak(veri tabanı,  API, dosya işlemleri, vb.) ve  `await` kulanımı desteklenmiyorsa, (birçok veri tabanı kütüphanesi için geçerlidir), o zaman *path operasyon fonksiyonunu* normal bir şekilde, yalnızca `def` kullanarak da tanımlayabiliriz, örneğin:

```Python hl_lines="2"
@app.get('/')
def results():
    results = some_library()
    return results
```

---

Eğer uygulamanız (bir şekilde) başka bir şeyle iletişim kurması gerekmiyor ama  yanıt vermesini beklemeniz gerekiyorsa `async def` kullanabilirsiniz.

---

Sadece bilmiyorsanız, normal `def` kullanın.

---

**Not**: *path operasyon fonksiyonlarında* istediğiniz şekilde `def` yada `async def` kullanabilirsiniz. Sizin için en iyi olan seçeneği kullanabilirsiniz. FastAPI onlarla doğru olanı yapacaktır.

Yukarıdaki durumlardan herhangi birinde FastAPI yine de asenkron olarak çalışacak ve son derece hızlı olacaktır.

Ancak yukarıdaki adımları takip ederek bazı performans optimizasyonları yapabiliriz

## Teknik Detaylar

Python modern versiyonlarında **`async` ve `await`** sözdizimi ile **"coroutines"**  kullanan **"asenkron kod"** desteğine sahiptir.

Bu ifadeyi aşağıdaki bölümlerde daha da ayrıntılı açıklayalım:

* **Asenkron kod**
* **`async` ve `await`**
* **Coroutines**

## Asenkron kod

Asenkron kod programlama dilinin 💬 bilgisayara / programa 🤖 kodun bir noktasında, *başka bir kodun* bir yerde bitmesini 🤖 beklemesi gerektiğini söylemenin bir yoludur. Bu *başka koda* "slow-file" denir 📝.

Böylece, bu süreçte bilgisayar "slow-file" 📝 tamamlanırken gidip başka işler yapabilir.

Sonra bilgisayar / program 🤖 her fırsatı olduğunda o noktada yaptığı tüm işleri 🤖 bitirene kadar geri dönücek. Ve 🤖 yapması gerekeni yaparak, beklediği görevlerden herhangi birinin bitip bitmediğini görecek.

Ardından, 🤖 bitirmek için ilk görevi alır ("slow-file" 📝) ve onunla ne yapması gerekiyorsa onu devam ettirir.

Bu "başka bir şey için bekle" normalde, aşağıdakileri beklemek gibi (işlemcinin ve RAM belleğinin hızına kıyasla) nispeten "yavaş" olan <abbr title="Input ve Output (Giriş ve Çıkış)">I/O</abbr> işlemlerine atıfta bulunur:  

* istemci tarafından ağ üzerinden veri göndermek
* ağ üzerinden istemciye gönderilen veriler
* sistem tarafından okunacak ve programınıza verilecek bir dosya içeriği
* programınızın diske yazılmak üzere sisteme verdiği dosya içerikleri
* uzak bir API işlemi
* bir veritabanı bitirme işlemi
* sonuçları döndürmek için bir veritabanı sorgusu
* vb.

Yürütme süresi çoğunlukla  <abbr title="Input ve Output (Giriş ve Çıkış)">I/O</abbr> işlemleri beklenerek tüketildiğinden bunlara "I/O bağlantılı" işlemler denir.

Buna "asenkron" denir, çünkü bilgisayar/program yavaş görevle "senkronize" olmak zorunda değildir, görevin tam olarak biteceği anı bekler, hiçbir şey yapmadan, görev sonucunu alabilmek ve çalışmaya devam edebilmek için .

Bunun yerine, "asenkron" bir sistem olarak, bir kez bittiğinde,  bilgisayarın / programın yapması gerekeni bitirmesi için biraz (birkaç mikrosaniye) sırada bekleyebilir ve ardından sonuçları almak için geri gelebilir ve onlarla çalışmaya devam edebilir.

"Senkron" ("asenkron"un aksine) için genellikle "sıralı" terimini de kullanırlar, çünkü bilgisayar/program, bu adımlar beklemeyi içerse bile, farklı bir göreve geçmeden önce tüm adımları sırayla izler.


### Eşzamanlılık (Concurrency) ve Burgerler


Yukarıda açıklanan bu **asenkron** kod fikrine bazen **"eşzamanlılık"** da denir. **"Paralellikten"** farklıdır.

**Eşzamanlılık** ve **paralellik**, "aynı anda az ya da çok olan farklı işler" ile ilgilidir.

Ancak *eşzamanlılık* ve *paralellik* arasındaki ayrıntılar oldukça farklıdır.


Farkı görmek için burgerlerle ilgili aşağıdaki hikayeyi hayal edin:

### Eşzamanlı Burgerler

<!-- Cinsiyetten bağımsız olan aşçı emojisi "🧑‍🍳" tarayıcılarda yeterince iyi görüntülenmiyor. Bu yüzden erken "👨‍🍳" ve kadın "👩‍🍳" aşçıları karışık bir şekilde kullanıcağım. -->

Aşkınla beraber 😍 dışarı hamburger yemeye çıktınız 🍔, kasiyer 💁 öndeki insanlardan sipariş alırken siz sıraya girdiniz.

Sıra sizde ve sen aşkın 😍 ve kendin için 2 çılgın hamburger 🍔 söylüyorsun.

Ödemeyi yaptın 💸.

Kasiyer 💁 mutfakdaki aşçıya 👨‍🍳 hamburgerleri 🍔 hazırlaması gerektiğini söyler ve aşçı bunu bilir (o an önceki müşterilerin siparişlerini hazırlıyor olsa bile).

Kasiyer 💁 size bir sıra numarası verir.

Beklerken askınla 😍 bir masaya oturur ve uzun bir süre konuşursunuz(Burgerleriniz çok çılgın olduğundan ve hazırlanması biraz zaman alıyor ✨🍔✨).

Hamburgeri beklerkenki zamanı 🍔, aşkının ne kadar zeki ve tatlı olduğuna hayran kalarak harcayabilirsin ✨😍✨.

Aşkınla 😍 konuşurken arada sıranın size gelip gelmediğini kontrol ediyorsun.

Nihayet sıra size geldi. Tezgaha gidip hamburgerleri 🍔kapıp masaya geri dönüyorsun.

Aşkınla hamburgerlerinizi yiyor 🍔 ve iyi vakit geçiriyorsunuz ✨.

---

Bu hikayedeki bilgisayar / program 🤖 olduğunuzu hayal edin.

Sırada beklerken boştasın 😴, sıranı beklerken herhangi bir "üretim" yapmıyorsun. Ama bu sıra hızlı çünkü kasiyer sadece siparişleri alıyor (onları hazırlamıyor), burada bir sıknıtı yok.

Sonra sıra size geldiğinde gerçekten "üretken" işler yapabilirsiniz 🤓, menüyü oku, ne istediğine larar ver, aşkının seçimini al 😍, öde 💸, doğru kartı çıkart, ödemeyi kontrol et, faturayı kontrol et, siparişin doğru olup olmadığını kontrol et, vb.

Ama hamburgerler 🍔 hazır olmamasına rağmen Kasiyer 💁 ile işiniz "duraklıyor" ⏸, çünkü hamburgerlerin hazır olmasını bekliyoruz 🕙.

Ama tezgahtan uzaklaşıp sıranız gelene kadarmasanıza dönebilir 🔀 ve dikkatinizi aşkınıza 😍 verebilirsiniz vr bunun üzerine "çalışabilirsiniz" ⏯ 🤓. Artık "üretken" birşey yapıyorsunuz 🤓, sevgilinle 😍 flört eder gibi.

Kasiyer 💁  "Hamburgerler hazır !" 🍔 dediğinde ve görüntülenen numara sizin numaranız olduğunda hemen koşup hamburgerlerinizi almaya çalışmıyorsunuz. Biliyorsunuzki kimse sizin hamburgerlerinizi 🍔 çalmayacak çünkü sıra sizin.

Yani Aşkınızın😍 hikayeyi bitirmesini bekliyorsunuz (çalışmayı bitir ⏯ / görev işleniyor.. 🤓), nazikçe gülümseyin ve hamburger yemeye gittiğinizi söyleyin ⏸.

Ardından tezgaha 🔀, şimdi biten ilk göreve ⏯ gidin, Hamburgerleri 🍔 alın, teşekkür edin ve masaya götürün. sayacın bu adımı tamamlanır ⏹. Bu da yeni bir görev olan  "hamburgerleri ye" 🔀 ⏯ görevini başlatırken "hamburgerleri al" ⏹ görevini bitirir.

### Parallel Hamburgerler

Şimdi bunların "Eşzamanlı Hamburger" değil, "Paralel Hamburger" olduğunu düşünelim.

Hamburger 🍔 almak için 😍 aşkınla Paralel fast food'a gidiyorsun.

You stand in line while several (let's say 8) cashiers that at the same time are cooks 👩‍🍳👨‍🍳👩‍🍳👨‍🍳👩‍🍳👨‍🍳👩‍🍳👨‍🍳 take the orders from the people in front of you.

Everyone before you is waiting 🕙 for their burgers 🍔 to be ready before leaving the counter because each of the 8 cashiers goes and prepares the burger right away before getting the next order.

Then it's finally your turn, you place your order of 2 very fancy burgers 🍔 for your crush 😍 and you.

You pay 💸.

The cashier goes to the kitchen 👨‍🍳.

You wait, standing in front of the counter 🕙, so that no one else takes your burgers 🍔 before you do, as there are no numbers for turns.

As you and your crush 😍 are busy not letting anyone get in front of you and take your burgers whenever they arrive 🕙, you cannot pay attention to your crush 😞.

This is "synchronous" work, you are "synchronized" with the cashier/cook 👨‍🍳. You have to wait 🕙 and be there at the exact moment that the cashier/cook 👨‍🍳 finishes the burgers 🍔 and gives them to you, or otherwise, someone else might take them.

Then your cashier/cook 👨‍🍳 finally comes back with your burgers 🍔, after a long time waiting 🕙 there in front of the counter.

You take your burgers 🍔 and go to the table with your crush 😍.

You just eat them, and you are done 🍔 ⏹.

There was not much talk or flirting as most of the time was spent waiting 🕙 in front of the counter 😞.

---

In this scenario of the parallel burgers, you are a computer / program 🤖 with two processors (you and your crush 😍), both waiting 🕙 and dedicating their attention ⏯ to be "waiting on the counter" 🕙 for a long time.

The fast food store has 8 processors (cashiers/cooks) 👩‍🍳👨‍🍳👩‍🍳👨‍🍳👩‍🍳👨‍🍳👩‍🍳👨‍🍳. While the concurrent burgers store might have had only 2 (one cashier and one cook) 💁 👨‍🍳.

But still, the final experience is not the best 😞.

---

This would be the parallel equivalent story for burgers 🍔.

For a more "real life" example of this, imagine a bank.

Up to recently, most of the banks had multiple cashiers 👨‍💼👨‍💼👨‍💼👨‍💼 and a big line 🕙🕙🕙🕙🕙🕙🕙🕙.

All of the cashiers doing all the work with one client after the other 👨‍💼⏯.

And you have to wait 🕙 in the line for a long time or you lose your turn.

You probably wouldn't want to take your crush 😍 with you to do errands at the bank 🏦.

### Burger Conclusion

In this scenario of "fast food burgers with your crush", as there is a lot of waiting 🕙, it makes a lot more sense to have a concurrent system ⏸🔀⏯.

This is the case for most of the web applications.

Many, many users, but your server is waiting 🕙 for their not-so-good connection to send their requests.

And then waiting 🕙 again for the responses to come back.

This "waiting" 🕙 is measured in microseconds, but still, summing it all, it's a lot of waiting in the end.

That's why it makes a lot of sense to use asynchronous ⏸🔀⏯ code for web APIs.

Most of the existing popular Python frameworks (including Flask and Django) were created before the new asynchronous features in Python existed. So, the ways they can be deployed support parallel execution and an older form of asynchronous execution that is not as powerful as the new capabilities.

Even though the main specification for asynchronous web Python (ASGI) was developed at Django, to add support for WebSockets.

That kind of asynchronicity is what made NodeJS popular (even though NodeJS is not parallel) and that's the strength of Go as a programming language.

And that's the same level of performance you get with **FastAPI**.

And as you can have parallelism and asynchronicity at the same time, you get higher performance than most of the tested NodeJS frameworks and on par with Go, which is a compiled language closer to C <a href="https://www.techempower.com/benchmarks/#section=data-r17&hw=ph&test=query&l=zijmkf-1" class="external-link" target="_blank">(all thanks to Starlette)</a>.

### Is concurrency better than parallelism?

Nope! That's not the moral of the story.

Concurrency is different than parallelism. And it is better on **specific** scenarios that involve a lot of waiting. Because of that, it generally is a lot better than parallelism for web application development. But not for everything.

So, to balance that out, imagine the following short story:

> You have to clean a big, dirty house.

*Yep, that's the whole story*.

---

There's no waiting 🕙 anywhere, just a lot of work to be done, on multiple places of the house.

You could have turns as in the burgers example, first the living room, then the kitchen, but as you are not waiting 🕙 for anything, just cleaning and cleaning, the turns wouldn't affect anything.

It would take the same amount of time to finish with or without turns (concurrency) and you would have done the same amount of work.

But in this case, if you could bring the 8 ex-cashier/cooks/now-cleaners 👩‍🍳👨‍🍳👩‍🍳👨‍🍳👩‍🍳👨‍🍳👩‍🍳👨‍🍳, and each one of them (plus you) could take a zone of the house to clean it, you could do all the work in **parallel**, with the extra help, and finish much sooner.

In this scenario, each one of the cleaners (including you) would be a processor, doing their part of the job.

And as most of the execution time is taken by actual work (instead of waiting), and the work in a computer is done by a <abbr title="Central Processing Unit">CPU</abbr>, they call these problems "CPU bound".

---

Common examples of CPU bound operations are things that require complex math processing.

For example:

* **Audio** or **image processing**.
* **Computer vision**: an image is composed of millions of pixels, each pixel has 3 values / colors, processing that normally requires computing something on those pixels, all at the same time.
* **Machine Learning**: it normally requires lots of "matrix" and "vector" multiplications. Think of a huge spreadsheet with numbers and multiplying all of them together at the same time.
* **Deep Learning**: this is a sub-field of Machine Learning, so, the same applies. It's just that there is not a single spreadsheet of numbers to multiply, but a huge set of them, and in many cases, you use a special processor to build and / or use those models.

### Concurrency + Parallelism: Web + Machine Learning

With **FastAPI** you can take the advantage of concurrency that is very common for web development (the same main attractive of NodeJS).

But you can also exploit the benefits of parallelism and multiprocessing (having multiple processes running in parallel) for **CPU bound** workloads like those in Machine Learning systems.

That, plus the simple fact that Python is the main language for **Data Science**, Machine Learning and especially Deep Learning, make FastAPI a very good match for Data Science / Machine Learning web APIs and applications (among many others).

To see how to achieve this parallelism in production see the section about [Deployment](deployment/index.md){.internal-link target=_blank}.

## `async` and `await`

Modern versions of Python have a very intuitive way to define asynchronous code. This makes it look just like normal "sequential" code and do the "awaiting" for you at the right moments.

When there is an operation that will require waiting before giving the results and has support for these new Python features, you can code it like:

```Python
burgers = await get_burgers(2)
```

The key here is the `await`. It tells Python that it has to wait ⏸ for `get_burgers(2)` to finish doing its thing 🕙 before storing the results in `burgers`. With that, Python will know that it can go and do something else 🔀 ⏯ in the meanwhile (like receiving another request).

For `await` to work, it has to be inside a function that supports this asynchronicity. To do that, you just declare it with `async def`:

```Python hl_lines="1"
async def get_burgers(number: int):
    # Do some asynchronous stuff to create the burgers
    return burgers
```

...instead of `def`:

```Python hl_lines="2"
# This is not asynchronous
def get_sequential_burgers(number: int):
    # Do some sequential stuff to create the burgers
    return burgers
```

With `async def`, Python knows that, inside that function, it has to be aware of `await` expressions, and that it can "pause" ⏸ the execution of that function and go do something else 🔀 before coming back.

When you want to call an `async def` function, you have to "await" it. So, this won't work:

```Python
# This won't work, because get_burgers was defined with: async def
burgers = get_burgers(2)
```

---

So, if you are using a library that tells you that you can call it with `await`, you need to create the *path operation functions* that uses it with `async def`, like in:

```Python hl_lines="2-3"
@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

### More technical details

You might have noticed that `await` can only be used inside of functions defined with `async def`.

But at the same time, functions defined with `async def` have to be "awaited". So, functions with `async def` can only be called inside of functions defined with `async def` too.

So, about the egg and the chicken, how do you call the first `async` function?

If you are working with **FastAPI** you don't have to worry about that, because that "first" function will be your *path operation function*, and FastAPI will know how to do the right thing.

But if you want to use `async` / `await` without FastAPI, <a href="https://docs.python.org/3/library/asyncio-task.html#coroutine" class="external-link" target="_blank">check the official Python docs</a>.

### Other forms of asynchronous code

This style of using `async` and `await` is relatively new in the language.

But it makes working with asynchronous code a lot easier.

This same syntax (or almost identical) was also included recently in modern versions of JavaScript (in Browser and NodeJS).

But before that, handling asynchronous code was quite more complex and difficult.

In previous versions of Python, you could have used threads or <a href="https://www.gevent.org/" class="external-link" target="_blank">Gevent</a>. But the code is way more complex to understand, debug, and think about.

In previous versions of NodeJS / Browser JavaScript, you would have used "callbacks". Which leads to <a href="http://callbackhell.com/" class="external-link" target="_blank">callback hell</a>.

## Coroutines

**Coroutine** is just the very fancy term for the thing returned by an `async def` function. Python knows that it is something like a function that it can start and that it will end at some point, but that it might be paused ⏸ internally too, whenever there is an `await` inside of it.

But all this functionality of using asynchronous code with `async` and `await` is many times summarized as using "coroutines". It is comparable to the main key feature of Go, the "Goroutines".

## Conclusion

Let's see the same phrase from above:

> Modern versions of Python have support for **"asynchronous code"** using something called **"coroutines"**, with **`async` and `await`** syntax.

That should make more sense now. ✨

All that is what powers FastAPI (through Starlette) and what makes it have such an impressive performance.

## Very Technical Details

!!! warning
    You can probably skip this.

    These are very technical details of how **FastAPI** works underneath.

    If you have quite some technical knowledge (co-routines, threads, blocking, etc) and are curious about how FastAPI handles `async def` vs normal `def`, go ahead.

### Path operation functions

When you declare a *path operation function* with normal `def` instead of `async def`, it is run in an external threadpool that is then awaited, instead of being called directly (as it would block the server).

If you are coming from another async framework that does not work in the way described above and you are used to define trivial compute-only *path operation functions* with plain `def` for a tiny performance gain (about 100 nanoseconds), please note that in **FastAPI** the effect would be quite opposite. In these cases, it's better to use `async def` unless your *path operation functions* use code that performs blocking <abbr title="Input/Output: disk reading or writing, network communications.">I/O</abbr>.

Still, in both situations, chances are that **FastAPI** will [still be faster](/#performance){.internal-link target=_blank} than (or at least comparable to) your previous framework.

### Dependencies

The same applies for dependencies. If a dependency is a standard `def` function instead of `async def`, it is run in the external threadpool.

### Sub-dependencies

You can have multiple dependencies and sub-dependencies requiring each other (as parameters of the function definitions), some of them might be created with `async def` and some with normal `def`. It would still work, and the ones created with normal `def` would be called on an external thread (from the threadpool) instead of being "awaited".

### Other utility functions

Any other utility function that you call directly can be created with normal `def` or `async def` and FastAPI won't affect the way you call it.

This is in contrast to the functions that FastAPI calls for you: *path operation functions* and dependencies.

If your utility function is a normal function with `def`, it will be called directly (as you write it in your code), not in a threadpool, if the function is created with `async def` then you should `await` for that function when you call it in your code.

---

Again, these are very technical details that would probably be useful if you came searching for them.

Otherwise, you should be good with the guidelines from the section above: <a href="#in-a-hurry">In a hurry?</a>.
