# IoC containers

/// note

It's assumed that you already have a good understanding of [dependency injection](../tutorial/dependencies/index.md){.internal-link target=_blank} before reading this page.

///

## **D**ependency **I**njection and **D**ependency **I**nversion

When dealing with `Depends`, you may have noticed that the mechanism behind it is essentially just a *function call* identified by its **explicitly referenced name** (with associated *finalization* and *caching* if specified).

Of course, it's possible to use any *callable*, not necessarily a function, but the principle remains the same — the "dependent" code is **hardwired** to a specific object provided as a *dependency*. You can think of it as electronic keys 🎫 and doors🚪: to open the right door, you need to find the key that fits exactly (and only) for it.

Let's see how this approach can get confusing with the increasing complexity of our application. Imagine we have two HTTP clients: one communicating with a distant city 🏢 and the other with a nearby village 🏠. The city server determines the IP "under the hood", while the village one requires it to be explicitly passed (and returns it with the main part of the response, even though we didn't ask for it 🤪).

{* ../../docs_src/ioc_containers/tutorial001_an.py hl[6,37,39,51,63] *}

/// tip

Some functions of the auxiliary code used here and later can be explored on these pages:

* [Settings and environment variables](../advanced/settings.md){.internal-link target=_blank} for `lru_cache`.
* [Bigger applications — multiple files](../tutorial/bigger-applications.md){.internal-link target=_blank} for `APIRouter`.
* [Custom response - HTML, Stream, File, others](../advanced/custom-response.md){.internal-link target=_blank} for `PlainTextResponse`.

///

Currently, the *business logic* details leak into the *framework layer*: our *path operation functions* depend on the **concrete implementation**, not the **abstraction** — violating the **<a href="https://en.wikipedia.org/wiki/Dependency_inversion_principle" class="external-link" target="_blank">Dependency inversion principle</a>**.

It causes us to modify each of them in order to switch between clients and complicates the understanding of the code: we unwittingly give attention to the client type, even though it doesn't matter at the *transport level*.

The easiest and most obvious way to power the FastAPI's built-in **DI** with **dependency inversion** is to create a *global variable*/*factory function* that stores/returns the **current dependency to inject**.

{* ../../docs_src/ioc_containers/tutorial002_an.py ln[37:41] hl[37,39,41,53,65] *}

Now, the **dependency binding** is done in handwritten **inversion of control** solution, and our *path operation functions* simply depends on an **interface** — not caring how it’s implemented.

Back to our analogy. Now we have just one key 🎫 that we can assign (at the reception desk 😏) to the door 🚪 we need now.

## Resolving dependency graph

Both our team and third-party API developers are not standing still, and we want to add more functionality:

* since remote servers sometimes drop connection, we need to manage the number of retries.
* providers have enforced personalized access, so we are required to grant the current user.

We clearly need *decomposition*, so let's use **sub-dependencies**.

{* ../../docs_src/ioc_containers/tutorial003_an.py ln[5:84] hl[5,17:19,22,33:35,38,74:75,78:79,82,84] *}

Here's what was needed:

1. A *factory function* for each **dependency with sub-dependencies**.
2. A construction with `Annotated` for each *factory function* to avoid duplicating `Depends` in multiple signatures.
3. A unique name for each construction with `Annotated` so as not to shadow the origin class name.
4. A `lru_cache` decorator for each *singleton* — in such a case, *factory* is needed even for **lower-level dependency**.
5. To have *singleton factories* sync or use a third-party async cache: `lru_cache` does not support async functions.

While manageable at first, this boilerplate grows quickly and spreads across your codebase — making maintenance more difficult.

We can try to reduce it by helping **FastAPI** resolve **dependency relations**.

{* ../../docs_src/ioc_containers/tutorial004_an.py ln[12:68] hl[12,21,24,35,66,68] *}

But it comes at a cost — the *DI layer* is now **coupled** with the *business layer*. This complicates its testing and debugging, as our classes can now have *side effects* due to misconfigured *dependencies* or unexpected behavior of the used **DI** instrument's source code.

## Dishka integration

/// note

You should consider third-party solutions if you are dissatisfied with:

* inventing custom **inversion of control** mechanism for `Depends`.
* the fact, that either your *business logic* contains details of **DI** or you have to duplicate constructor signatures.
* not being able to use `Depends` outside of *path operation functions*.
* limited scalability due to lack of advanced **dependencies isolation** features.

In other cases, it might be better to stay with **FastAPI `Depends`**: it nicely does the work it was designed for.

///

There are <a href="https://github.com/sfermigier/awesome-dependency-injection-in-python" class="external-link" target="_blank">many</a> **<abbr title="also known as DI frameworks">DI libraries</abbr>** in different stages of their lifecycle. As an example, let's consider **Dishka** because:

* it has strong community support and many <a href="https://dishka.readthedocs.io/en/stable/integrations/index.html" class="external-link" target="_blank">integrations</a>, including with **FastAPI**.
* it builds on lessons <a href="https://dishka.readthedocs.io/en/stable/alternatives.html" class="external-link" target="_blank">learned</a> from earlier DI instruments.
* it complies with **DIP** via **<a href="https://dishka.readthedocs.io/en/stable/provider/index.html" class="external-link" target="_blank">providers</a>**.
* it has an extensive, flexible API ready for an almost boundless scalability even with a *monolith* thanks to **<abbr title="The DI library itself is also sometimes called an IoC container"><a href="https://dishka.readthedocs.io/en/stable/container/index.html" class="external-link" target="_blank">IoC containers</a></abbr>**.
* it's *async-* and *types-oriented* — just like **FastAPI**.

Here's how we can rewrite our application.

{* ../../docs_src/ioc_containers/tutorial005_py310.py hl[9:16,67:75,81,96,108,118,130:131] *}

From now on, **dependency binding** is centralized and done declaratively through `GeoProvider` by the "**abstraction** (`provides`) — **implementation** (`source`)" pairs. And `recursive=true` automates the resolution of **`__init__`-based dependencies**, analysing Python native *type hints*.

Moreover, you can (and should) continue to use `Depends`: not for **DIP**, but for **DI** in the purpose of **request decomposition**. Even with a brief glance at the second *path operation function*, it becomes obvious which *dependency* refers to *transport layer* (operates the explicit *user input*) and which one refers to *services* (operates the complex objects  with "heavy" logic).

However, the value of **dependency isolation** and other advanced features of Dishka (such as <a href="https://dishka.readthedocs.io/en/stable/advanced/context.html" class="external-link" target="_blank">context data</a>, <a href="https://dishka.readthedocs.io/en/stable/advanced/scopes.html" class="external-link" target="_blank">custom scopes</a> or <a href="https://dishka.readthedocs.io/en/stable/advanced/components.html" class="external-link" target="_blank">components</a>) may not seem obvious at first glance: they are revealed on complex and branched projects. As a starting point to understanding them, you might try to write by yourself an additional "fast" router: a client there is not recreated for each request, but is used as a *singleton*.

/// tip

Such a problem is well solved by allocating a separate **container** per router with a declarative scope setting.

///

## Conclusion

As we have realized, **dependency injection** is a *concept* that has many **implementations**. We have considered three of them:

* **FastAPI** `Depends` with passing the **current implementation** — doesn't comply with **DIP**, best suited for **request decomposition**.
* **FastAPI** `Depends` with *global variable*/*wrapper function* — complies with **DIP**, best suited for small number of **sub-dependencies** and *sub-applications*.
* **Dishka** — complies with DIP, best suited for large **dependency graphs** and flexible scalability.
