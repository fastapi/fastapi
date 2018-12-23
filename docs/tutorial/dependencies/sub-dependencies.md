You can create dependencies that have sub-dependencies.

They can be as "deep" as you need them to be.

**FastAPI** will take care of solving them.

### First dependency "dependable"

You could create a first dependency ("dependable") like:

```Python hl_lines="6 7"
{!./src/dependencies/tutorial005.py!}
```
It declares an optional query parameter `q` as a `str`, and then it just returns it.

This is quite simple (not very useful), but will help us focus on how the sub-dependencies work.

### Second dependency, "dependable" and "dependant"

Then you can create another dependency function (a "dependable") that at the same time declares a dependency of its own (so it is a "dependant" too):

```Python hl_lines="11"
{!./src/dependencies/tutorial005.py!}
```

Let's focus on the parameters declared:

* Even though this function is a dependency ("dependable") itself, it also declares another dependency (it "depends" on something else).
    * It depends on the `query_extractor`, and assigns the value returned by it to the parameter `q`.
* It also declares an optional `last_query` cookie, as a `str`.
    * Let's imagine that if the user didn't provide any query `q`, we just use the last query used, that we had saved to a cookie before.

### Use the dependency

Then we can use the dependency with:

```Python hl_lines="19"
{!./src/dependencies/tutorial005.py!}
```

!!! info
    Notice that we are only declaring one dependency in the path operation function, the `query_or_cookie_extractor`.

    But **FastAPI** will know that it has to solve `query_extractor` first, to pass the results of that to `query_or_cookie_extractor` while calling it.


## Recap

Apart from all the fancy words used here, the **Dependency Injection** system is quite simple.

Just functions that look the same as the path operation functions.

But still, it is very powerful, and allows you to declare arbitrarily deeply nested dependency "graphs" (trees).

!!! tip
    All this might not seem as useful with these simple examples.
    
    But you will see how useful it is in the chapters about **security**.

    And you will also see the amounts of code it will save you.
