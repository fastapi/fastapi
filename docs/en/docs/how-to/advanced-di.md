# Advanced DI

/// note

It's assumed that you already have a good understanding of [dependency injection](../tutorial/dependencies/index.md){.internal-link target=_blank} before reading this page.

///

## FastAPI DI limitations

When dealing with `Depends`, you may have noticed that the mechanism behind it is essentially just a *function call* identified by its **explicitly referenced name** (with associated *finalization* and *caching* if specified).

Of course, it's possible to use any *callable object*, not necessarily a function, but the principle remains the same — the "dependent" code is **hardwired** to a specific implementation of the dependency. You can think of it as electronic keys 🎫 and doors🚪: to open the right door, you need to find the key that fits exactly (and only) for it.

Let's see how this approach can get confusing with the increasing complexity of our application. Imagine we have two HTTP clients: one communicating with a distant city 🏢 and the other with a nearby village 🏠. The city server determines the IP "under the hood", while the village one requires it to be explicitly passed (and returns it with the main part of the response, even though we didn't ask for it 🤪).

{* ../../docs_src/advanced_di/tutorial001_an.py hl[5,9,50,51,54,57,58,61,64,65,68,79] *}

/// note

Some functions of the auxiliary code used here can be explored on these pages:

* [Settings and environment variables](../advanced/settings.md){.internal-link target=_blank} for `lru_cache`.
* [Bigger applications — multiple files](../tutorial/bigger-applications.md){.internal-link target=_blank} for `APIRouter`.
* [Custom response - HTML, Stream, File, others](../advanced/custom-response.md){.internal-link target=_blank} for `PlainTextResponse`.

///

So, we need:

1. A factory function for each dependency.
2. A construction with `Annotated` for each dependency to avoid duplicating `Depends` if one dependency will be used in multiple *path operations*.
3. A unique name for each construction with `Annotated` so as not to shadow the origin class name.
4. A `lru_cache` decorator for each *singleton*.

While manageable at first, this list grows quickly and spreads across your codebase — making maintenance more difficult.

And the most important, *path operations* depend on the **concrete implementation**, not the **abstraction** — violating the **<a href="https://en.wikipedia.org/wiki/Dependency_inversion_principle" class="external-link" target="_blank">Dependency inversion principle</a>**.

We can at least try to reduce the amount of code.

{* ../../docs_src/advanced_di/tutorial002_an.py hl[19,20,23,28] *}

But this comes at a cost — the DI logic is now **intertwined** with the *business layer*, causing harder decoupling and less flexible testing. And we don't solve original problems.

## Dishka integration

/// tip

You only need third-party solutions if you want to fully comply with **dependency inversion**. If you only need **dependency injection**, it might be better to stay with FastAPI `Depends`: it nicely does the job it was designed for.

///

There are <a href="https://github.com/sfermigier/awesome-dependency-injection-in-python" class="external-link" target="_blank">many</a> **<abbr title="also known as DI frameworks">DI libraries</abbr>** in different stages of their lifecycle. As an example, let's consider **Dishka** because:

* it has strong community support and many integrations, including with FastAPI.
* it builds on lessons learned from earlier DI instruments.
* it complies with **DIP** through **providers** and **<abbr title="The DI library itself is also sometimes called an IoC container">IoC containers</abbr>**.
* it's *async-* and *types-oriented* — just like FastAPI.
* it provides an extensive, flexible API ready for complex use cases.

/// info

If you're familiar with other frameworks (and not only web), there's good news for you: Dishka has <a href="https://dishka.readthedocs.io/en/stable/integrations/index.html" class="external-link" target="_blank">integrations</a> with a large part of them. 😎

///

Here's how we can rewrite our application.

{* ../../docs_src/advanced_di/tutorial003_py310.py hl[8,9,10,11,12,13,14,15,16,57,58,59,60,61,62,65,73,89,90,91,92] *}

Now, the implementation binding is done in configuration, and our *path operation* simply depends on an **interface** — not caring how it’s implemented.

Back to our analogy. Now we have just one key 🎫 that we can assign (at the reception desk 😏) to the door 🚪 we need now.

## Learn more

Dishka also supports techniques you already know from `Depends` such as:

* dependencies with yield.
* automatic analysis of `__init__`.

and introduces new ones:

* context data.
* custom scopes.
* components.

Details — in the excellent <a href="https://dishka.readthedocs.io/en/stable/index.html" class="external-link" target="_blank">documentation</a>.
