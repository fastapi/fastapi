from aiocache import caches, cached
from fastapi import FastAPI


CACHE_TTL=2


caches.set_config({
    'default': {
        'cache': 'aiocache.RedisCache',
        'endpoint': '127.0.0.1',
        'port': 6379,
        'db': 0,
        'password': 'root',
        'serializer': {
            'class': 'aiocache.serializers.PickleSerializer'
        }
    }
})


app = FastAPI()


@app.get("/")
@cached(alias='default', ttl=2)
async def root():
    return {"message": "Hello World"}
