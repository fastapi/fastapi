# Asynchronous Code with `await` and `async`

When building an API, you might want your two programs to communicate different things simultaneously. **Asynchronous code**, or **concurrency**, allows your program to perform a task in the background while waiting to finish another task at the same time. Modern versions of Python have support for **asynchronous code** using **coroutines** with **`async` and `await`** syntax. 

## Understanding asynchronous code

**Asynchronous code** are instructions for a program to do two things at the same time. To do this, the asynchronous code tells the program that it needs to wait until `something slow` to finish doing its task. Meanwhile, the program can work on another task while it waits for `something slow` and can return to `something slow` to see if it's finished its tasks.

It's called "asynchronous" because the program doesn't have to be synchronized with `something slow`, or wait for it to be complete before it can do something else. This is opposed to "synchronous" or "sequential" code that follow instructions line-by-line, waiting until a task before starting a new one.

Many standard <abbr title="Input and Output">I/O</abbr> operations can take up a program's time to complete. Some examples of slow tasks include:
* The data from the client to be sent through the network
* The contents of a file in the disk to be read by a system
* A remote API operation
* A database query to return the results

---

### Concurrency

Asynchronous code is also sometimes called **concurrency**. To understand concurrency better, take a look at the following example:

Let's say your in a line with your crush to get burgers from a fast food joint called **Concurrent Burgers**. While you're both standing in line, the cashier takes orders from the people in front of you. 

<img src="/img/async/concurrent-burgers/concurrent-burgers-01.png" class="illustration">

Once it's your turn, you place an order for two burgers.

<img src="/img/async/concurrent-burgers/concurrent-burgers-02.png" class="illustration">

The cashier takes your order to the chef and puts it in a queue along with the other orders. This happens even while the chef is preparing other burgers.

<img src="/img/async/concurrent-burgers/concurrent-burgers-03.png" class="illustration">

After you pay, the cashier gives you your order number.

<img src="/img/async/concurrent-burgers/concurrent-burgers-04.png" class="illustration">

You find a table and pass the time while interacting with your crush, learning more about them.

<img src="/img/async/concurrent-burgers/concurrent-burgers-05.png" class="illustration">

From time to time, you glance at the screen that displays your order number to see if your order is ready. Once it's your turn, you both head back to the counter.

<img src="/img/async/concurrent-burgers/concurrent-burgers-06.png" class="illustration">

You and your crush are finally able to chow down on a delicious meal.

<img src="/img/async/concurrent-burgers/concurrent-burgers-07.png" class="illustration">

!!! credit
    Beautiful illustrations by <a href="https://www.instagram.com/ketrinadrawsalot" class="external-link" target="_blank">Ketrina Thompson</a>. 🎨

Let's review that scenario again but now imagine you're a computer program. As you wait in line, you're "idle." But once it's your turn, you get started on the `get_burgers` task: you read the menu, decide your order, pay, and verify that the order and the charge are correct. However, the task can't be complete because the burgers need time to cook. You "pause" your interaction with the cashier and go look for a table.

After finding a table, you switch your attention to another task called `get_to_know_crush`. You ask questions, flirt, and say a joke. Once the cashier announces that the burgers are finished, you don't get up immediately. You know that no one will steal your order because you have the number of your turn and they theirs. Instead, you for your crush to finish telling their story (or finish processing the task `get_to_know_crush`). 

Once you're both ready (or finish the current task), you go back to the cashier and "resume" your interaction. Finally, you get the burgers and thank the cashier, finishing the `get_burgers` task. Finally, it's time to eat the burgers and start a new task `eat_burgers`.

Examples of concurrency in code include:
* Messaging
* Banking
* Social media

---

### Parallelism

**Parallelism** is related to concurrency but with some key differences. To understand parallelism, take a look at the example below:

The first date went well and now you're crush wants to try the burgers from a place called **Parallel Burgers**. You both approach one of several lines as you wait for the people ahead of you. Rather than simply placing the order, the people ahead wait for their burgers to be made on the spot.

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

!!! credit
    Beautiful illustrations by <a href="https://www.instagram.com/ketrinadrawsalot" class="external-link" target="_blank">Ketrina Thompson</a>. 🎨

The main difference between the two scenarios is that you had to wait for the cashier to take, make, and deliver your order. If you were a computer program, you would have been **synchronized** with the cashier, because you had to wait for the exact moment the task was done (otherwise someone else would have taken the burgers). But this also means that you both had to wait at the counter for a long time and didn't have any time to speak to your crush. As a result, it made your second date less interesting. 

!!! info
    While concurrency worked better in this situation, this example only demonstrates how parallelism works. If instead, the cashiers were cleaners tasked to clean a dirty mansion, a **concurrent system** would make it so one person has to wait to clean one room after the other. However, with a **parallel system**, multiple people can clean the rooms at the same time and reduce the time spent.

Examples of parallelism used in code are in **CPU bound** problems. Because the CPU takes most of the time completing the task is used in completing the task (rather than waiting), that's what makes it CPU bound. Common examples of CPU bound operations are things that require complex math processing, such as:
* **Computer vision** - An image is composed of millions of pixels, with each pixel having three values to represent color. Computer vision is a process that requires computing something on those pixels all at the same time.
* **Machine Learning** - Requires lots of matrix and vector multiplications. Imagine a huge spreadsheet with numbers, then multipling them all together at the same time.
* **Deep Learning** - A sub-field of Machine Learning. Rather than only one spreadsheet, imagine many more and multiplying the values in those spreadsheets at the same time.

To see more information about parallelism in production, see the [Deployment](deployment/index.md) section.

---

### Concurrency versus parallelism

Concurrency and parallelism are both useful depending on the situation. See the table below to understand the main advantages of each.

![concurrency_parallelism_difference_chart](https://github.com/physicsmagician/fastapi/assets/59658246/1f7c99e9-ed61-4773-ab0d-7ec5ad9a136b)

When combining asynchronicity and parallelism, you achieve higher performance than most of the tested NodeJS frameworks and on par with Go <a href="https://www.techempower.com/benchmarks/#section=data-r17&hw=ph&test=query&l=zijmkf-1" class="external-link" target="_blank">(all thanks to Starlette)</a>. Because Python is the main language for Data Science, Machine Learning, and Deep Learning, FastAPI already hits the ground running when tackling problems in these fields.

## Using `async` and `await`

Modern versions of Python have an intuitive way to define asynchronous code by making it look just like normal **sequential code** and do the "awaiting" for you at the right moments. 

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

As opposed to using `def`:

```Python hl_lines="2"
# This is not asynchronous
def get_sequential_burgers(number: int):
    # Do some sequential stuff to create the burgers
    return burgers
```

!!! caveat
    `async def` can only be called inside of functions also defined with `async def`. It's like the chicken and the egg: How do you call the first `async` function? The original function is called the **first parameter function**. FastAPI already keeps track of this for you.

With `async def`, Python knows that inside that function it has to be aware of `await` expressions, and that it can "pause" the execution of that function and go do something else before coming back.

When calling an `async def` function, you have to "await" it. So, this won't work:

```Python
# This won't work, because get_burgers was defined with: async def
burgers = get_burgers(2)
```

If you're using a library that tells you that you can call it with `await`, you need to create the **path operation function** that uses it with `async def`:

```Python hl_lines="2-3"
@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

---

### Coroutines

A **Coroutine** is simply the thing returned by an `async def` function. Python knows that it is something like a function that it can start and that it will end at some point, but that it might be paused internally too, whenever there is an `await` inside of it.

---

### Other asynchronous code

While this method of using `async` and `await` is new in Python, it makes working with asynchronous code simplier. Similar syntax is also in modern versions of JavaScript, in Browser, and NodeJS. 

Before that, handling asynchronous code was more complicated. In previous version of Python, you would have to use threads or <a href="https://www.gevent.org/" class="external-link" target="_blank">Gevent</a>. And in previous versions of NodeJS, Browser JavaScript, you would have to use callbacks (which very easily lead to <a href="http://callbackhell.com/" class="external-link" target="_blank">callback hell</a>).

## Technical details of concurrency in FastAPI

FastAPI uses concurrency (rooted in the <a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO Python asynchronous library</a>) for web development and offers the potential to use the benefits of parallelism and multiprocessing for CPU bound workloads like those in Machine Learning systems. If you're curious, you can see more high-level details in this section.

---

### Path operation functions

When you declare a **path operation function** with normal `def` instead of `async def`, it is run in an external threadpool that is then awaited instead of being called directly (as it would block the server).

If you are coming from another async framework that does not work in the way described above and you are used to defining trivial compute-only **path operation functions** with plain `def` for a tiny performance gain (about 100 nanoseconds), please note that in FastAPI the effect would be quite opposite. In these cases, it's better to use `async def` unless your **path operation functions** use code that performs blocking <abbr title="Input/Output: disk reading or writing, network communications.">I/O</abbr>.

Still, in both situations, chances are that FastAPI will [still be faster](index.md#performance){.internal-link target=_blank} than (or at least comparable to) your previous framework.

---

### Dependencies

The same applies for [dependencies](tutorial/dependencies/index.md){.internal-link target=_blank}. If a dependency is a standard `def` function instead of `async def`, it is run in the external threadpool.

---

### Sub-dependencies

You can have multiple dependencies and [sub-dependencies](tutorial/dependencies/sub-dependencies.md){.internal-link target=_blank} requiring each other (as parameters of the function definitions), some of them might be created with `async def` and some with normal `def`. It would still work, and the ones created with normal `def` would be called on an external thread (from the threadpool) instead of being "awaited".

---

### Other utility functions

Any other utility function that you call directly can be created with normal `def` or `async def` and FastAPI won't affect the way you call it. This is in contrast to the functions that FastAPI calls for you: **path operation functions** and dependencies. If your utility function is a normal function with `def`, it will be called directly (as you write it in your code), not in a threadpool, if the function is created with `async def` then you should `await` for that function when you call it in your code.
