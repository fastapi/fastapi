# Asynchronous Code with await and async

Asynchronous code (also called concurrency) allows your program to perform a task in the background while running another task at the same time. In Python, `await` and `async` are used to indicate when this process happens. FastAPI uses concurrency (rooted in the <a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO Python asynchronous library</a>) for web development and offers the potential to use the benefits of parallelism and multiprocessing for CPU bound workloads like those in Machine Learning systems.

This document offers an introduction to:
* Asynchronous code
* Concurrencies and parallelisms
* `async` and `await`
* Coroutines

## Asynchronous Code

**Asynchronous code** refers to the process of how a program does two things at the same time. To do this, the asynchronous code tells the program that it needs to wait until `something slow` to finish doing its task. During that time, the program can work on another task while it waits for `something slow` to finish. Over time, the program can return to `something slow` to see if it's finished its tasks.

Many standard <abbr title="Input and Output">I/O</abbr> operations can take up a program's time to complete. Some examples of slow tasks include:
* the data from the client to be sent through the network
* the contents of a file in the disk to be read by a system
* a remote API operation
* a database query to return the results

It's called "asynchronous" because the program doesn't have to be synchronized with `something slow`, or wait for it to be complete before it can do something else. This is opposed to "synchronous" or "sequential" code that follow instructions line-by-line, waiting until a task before starting a new one.

## Concurrency

Asynchronous code is also sometimes called **concurrency**. To understand concurrency better, take a look at the following example:

Let's say your in a line with your crush to get burgers from a fast food joint called **Concurrent Burgers**. While you're both standing in line, the cashier takes orders from the people in front of you. 

<img src="/img/async/concurrent-burgers/concurrent-burgers-01.png" class="illustration">

Once it's your turn, you place an order for two burgers.

<img src="/img/async/concurrent-burgers/concurrent-burgers-02.png" class="illustration">

The cashier takes your order to the chef and puts it in a queue of orders. This happens even while the chef is preparing other burgers.

<img src="/img/async/concurrent-burgers/concurrent-burgers-03.png" class="illustration">

After you pay, the cashier gives you your order number.

<img src="/img/async/concurrent-burgers/concurrent-burgers-04.png" class="illustration">

You both find a table. While waiting, you spend that time interacting with your crush, learning more about them.

<img src="/img/async/concurrent-burgers/concurrent-burgers-05.png" class="illustration">

From time to time, you glance at the screen that displays your order number to see if your order is ready. Once it's your turn, you both head back to the counter.

<img src="/img/async/concurrent-burgers/concurrent-burgers-06.png" class="illustration">

You and your crush are finally able to chow down on a delicious meal.

<img src="/img/async/concurrent-burgers/concurrent-burgers-07.png" class="illustration">

!!! Credit
    Beautiful illustrations by <a href="https://www.instagram.com/ketrinadrawsalot" class="external-link" target="_blank">Ketrina Thompson</a>. 🎨

Let's review that scenario again but now imagine you're a computer program. As you wait in line, you're "idle." But once it's your turn, you get started on the `get_burgers` task: you read the menu, decide your order, pay, and verify that the order and the charge are correct. However, the task can't be complete because the burgers need time to cook. You "pause" your interaction with the cashier and go look for a table.

After finding a table, you switch your attention to another task `get_to_know_crush`. You ask questions, flirt, and make them laugh here and there. Once the cashier announces that the burgers are finished, you don't get up immediately. You know that no one will steal your order because you have the number of your turn and they theirs. Instead, you for your crush to finish telling their story (or finish processing the task `get_to_know_crush`). 

Once you're both ready (or finish the current task), you go back to the cashier and "resume" your interaction. Finally, you get the burgers and thank the cashier, finishing the `get_burgers` task. Finally, it's time to eat the burgers and start a new task `eat_burgers`.

## Parallelism

**Parallelism** is related to concurrency but with some key differences. To understand parallelism, take a look at the example below:

The first date went well and now you're crush wants to to try the burgers from a place called **Parallel Burgers**. You both approach one of several lines as you wait for the people ahead of you. Rather than simply placing the order, the people ahead wait for their burgers to be made on the spot.

<img src="/img/async/parallel-burgers/parallel-burgers-01.png" class="illustration">

Once it's finally your turn, you place your order and pay the bill.

<img src="/img/async/parallel-burgers/parallel-burgers-02.png" class="illustration">

The cashier dashes to the kitchen to prepare the order. Meanwhile, you both wait at your spot so no one else can take your order (since there are no order numbers to call).

<img src="/img/async/parallel-burgers/parallel-burgers-03.png" class="illustration">

While you're busy guarding your spot, you have no energy to pay attention to your crush.

<img src="/img/async/parallel-burgers/parallel-burgers-04.png" class="illustration">

The cashier finally returns with your order in hand.

<img src="/img/async/parallel-burgers/parallel-burgers-05.png" class="illustration">

You cheerfully grab your order and find a table to eat.

<img src="/img/async/parallel-burgers/parallel-burgers-06.png" class="illustration">

!!! info
    Beautiful illustrations by <a href="https://www.instagram.com/ketrinadrawsalot" class="external-link" target="_blank">Ketrina Thompson</a>. 🎨

The main difference in this scenario than the previous one is that you had to wait for the cashier to both take, make, and hand you your order. As a computer program, you would have been "synchronized" with the cashier, because you had to wait for the exact moment the task was done (otherwise someone else could have taken the burgers). But this also means that you both had to wait at the counter for a long time and didn't have any time to speak to your crush. As a result, it made your second date less interesting.

## Advantages of Concurrency vs Parallelism

Neither concurrency or parallelism are better than the other--it depends on the situation.

For most case scenarios it makes more sense to have a concurrent system where there's a lot of waiting to make the most use of that time. For example, web applications might have incoming requests from users waiting to connect to a server. "Waiting" is measured in microseconds, but it adds up quickly. 

Asynchronous code is also best for web APIs. It's this kind of asynchronicity that makes APIs like **NodeJS** or **Go** (a compiled language similar to C) popular. And this is also the same level of performance you can achieve with FastAPI. 

On the other hand, Parallelism is more useful for situations where it would take the same amount of time to finish a task with or without creating turns (as from the concurrency model). For example, if you had to clean a dirty mansion, it makes more sense to have multiple people cleaning at the same time (in parallel) rather than waiting for one person to do the entire job. Because most of the execution time is taken by the actual work (rather than waiting), and the work is done by a CPU, these are called **CBU bound**.

Examples of CBU bound operations are tasks that require complex math processing, such as:
* Computer vision (displaying an image requires processing millions of pixels with three values at the same time).
* Machine Learning (normally requires lot's of matrix and vector multiplications).
* Deep Learning (a subfield of Machine Learning).

To see more information about parallelism in production, see the [Deployment](deployment/index.md){.internal-link target=_blank} section.

When combining asynchronicity and parallelism, you get higher performance than most of the tested NodeJS frameworks and on par with Go <a href="https://www.techempower.com/benchmarks/#section=data-r17&hw=ph&test=query&l=zijmkf-1" class="external-link" target="_blank">(all thanks to Starlette)</a>. Because Python is the main language for Data Science, Machine Learning, and Deep Learning, Fast API already hits the ground running when tackling problems in these fields.

## `async` and `await`

Modern versions of Python have an intuitive way to define asynchronous code by making it look just like normal "sequential" code and do the "awaiting" for you at the right moments. 

When there is a process that requires waiting before giving the results:

```Python
burgers = await get_burgers(2)
```

The key here is the `await`. It tells Python that it has to wait for `get_burgers(2)` to finish doing its thing before storing the results in `burgers`. With that, Python will know that it can go and do something else in the meanwhile (like receiving another request).

However, for `await` to work, it has to be inside a function that supports this asynchronicity. To do that, declare it with `async def`:

```Python hl_lines="1"
async def get_burgers(number: int):
    # Do some asynchronous stuff to create the burgers
    return burgers
```

As opposed to using the usual `def`:

```Python hl_lines="2"
# This is not asynchronous
def get_sequential_burgers(number: int):
    # Do some sequential stuff to create the burgers
    return burgers
```

!!! Caveat
    One caveat with using functions with `async def` is that it can only be called inside of functions also defined with `async def`. It's like the chicken and the egg: How do you call the first `async` function? With FastAPI, it will know how to do the right thing. 

With `async def`, Python knows that inside that function it has to be aware of `await` expressions, and that it can "pause" the execution of that function and go do something else before coming back.

When calling an `async def` function, you have to "await" it. So, this won't work:

```Python
# This won't work, because get_burgers was defined with: async def
burgers = get_burgers(2)
```

If you're using a library that tells you that you can call it with `await`, you need to create the *path operation functions* that uses it with `async def`:

```Python hl_lines="2-3"
@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

### Write your own async code

Starlette (and **FastAPI**) are based on <a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO</a>, which makes it compatible with both Python's standard library <a href="https://docs.python.org/3/library/asyncio-task.html" class="external-link" target="_blank">asyncio</a> and <a href="https://trio.readthedocs.io/en/stable/" class="external-link" target="_blank">Trio</a>.

In particular, you can directly use <a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO</a> for your advanced concurrency use cases that require more advanced patterns in your own code.

And even if you were not using FastAPI, you could also write your own async applications with <a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO</a> to be highly compatible and get its benefits (e.g. *structured concurrency*).

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

    If you have quite some technical knowledge (coroutines, threads, blocking, etc.) and are curious about how FastAPI handles `async def` vs normal `def`, go ahead.

### Path operation functions

When you declare a *path operation function* with normal `def` instead of `async def`, it is run in an external threadpool that is then awaited, instead of being called directly (as it would block the server).

If you are coming from another async framework that does not work in the way described above and you are used to defining trivial compute-only *path operation functions* with plain `def` for a tiny performance gain (about 100 nanoseconds), please note that in **FastAPI** the effect would be quite opposite. In these cases, it's better to use `async def` unless your *path operation functions* use code that performs blocking <abbr title="Input/Output: disk reading or writing, network communications.">I/O</abbr>.

Still, in both situations, chances are that **FastAPI** will [still be faster](index.md#performance){.internal-link target=_blank} than (or at least comparable to) your previous framework.

### Dependencies

The same applies for [dependencies](tutorial/dependencies/index.md){.internal-link target=_blank}. If a dependency is a standard `def` function instead of `async def`, it is run in the external threadpool.

### Sub-dependencies

You can have multiple dependencies and [sub-dependencies](tutorial/dependencies/sub-dependencies.md){.internal-link target=_blank} requiring each other (as parameters of the function definitions), some of them might be created with `async def` and some with normal `def`. It would still work, and the ones created with normal `def` would be called on an external thread (from the threadpool) instead of being "awaited".

### Other utility functions

Any other utility function that you call directly can be created with normal `def` or `async def` and FastAPI won't affect the way you call it.

This is in contrast to the functions that FastAPI calls for you: *path operation functions* and dependencies.

If your utility function is a normal function with `def`, it will be called directly (as you write it in your code), not in a threadpool, if the function is created with `async def` then you should `await` for that function when you call it in your code.

---

Again, these are very technical details that would probably be useful if you came searching for them.

Otherwise, you should be good with the guidelines from the section above: <a href="#in-a-hurry">In a hurry?</a>.

## Summary

If you are using third party libraries that tell you to call them with `await`, like:

```Python
results = await some_library()
```

Then, declare your *path operation functions* with `async def` like:

```Python hl_lines="2"
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

!!! note
    You can only use `await` inside of functions created with `async def`.

---

If you are using a third party library that communicates with something (a database, an API, the file system, etc.) and doesn't have support for using `await`, (this is currently the case for most database libraries), then declare your *path operation functions* as normally, with just `def`, like:

```Python hl_lines="2"
@app.get('/')
def results():
    results = some_library()
    return results
```

---

If your application (somehow) doesn't have to communicate with anything else and wait for it to respond, use `async def`.

---

If you just don't know, use normal `def`.

---

**Note**: You can mix `def` and `async def` in your *path operation functions* as much as you need and define each one using the best option for you. FastAPI will do the right thing with them.

Anyway, in any of the cases above, FastAPI will still work asynchronously and be extremely fast.

But by following the steps above, it will be able to do some performance optimizations.

## Asynchronous Code

Asynchronous code refers to the process of how a program does two things at the same time. To do this, the code tells the program that it needs to wait until _something slow_ finishes doing its tasks _somewhere else_. During that time, the program can work on another task while it waits for _something slow_ to finish. Over time, the program can return to _something slow_ to see if it's finished its tasks.

Many standard <abbr title="Input and Output">I/O</abbr> operations can take up a program's time to complete. Some examples of slow tasks include:
* the data from the client to be sent through the network
* the contents of a file in the disk to be read by the system and given to your program
* a remote API operation
* a database query to return the results

It's called "asynchronous" because the program doesn't have to be synchronized with the slower task nor wait for it to be complete before it can do something else. This is opposed to "synchronous" or "sequential" code that follow instructions line-by-line, waiting until a task is done before starting a new one.
