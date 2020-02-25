Configure cache by using [aiocache](https://github.com/argaen/aiocache)


### Import the aiocache

```Python hl_lines="1"
{!./src/cache/tutorial001.py!}
```

### Configure cache backend

```Python hl_lines="8 9 10 11 12 13 14 15 16 17 18 19"
{!./src/cache/tutorial001.py!}
```

!!! tip
    aiochache supports other backends such as **Memcached**, it also supports other serializers. Please check its [documentation](https://aiocache.readthedocs.io/en/latest/) to get more information.

### Using cached decorator

```Python hl_lines="26"
{!./src/cache/tutorial001.py!}
```

Set the defined **cache alias** and the **ttl**, if no ttl is provided, cache will never expire.


### Using cache to set values

You can also use cache to set values:

```Python
cache = caches.get('default')
await cache.set("key", "value")
assert await cache.get("key") == "value"
```
