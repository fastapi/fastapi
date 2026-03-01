import gc
import weakref

from fastapi.routing import _endpoint_context_cache, _extract_endpoint_context


def _make_endpoint():
    def endpoint():
        return None

    return endpoint


def test_endpoint_context_cache_releases_endpoints():
    endpoint = _make_endpoint()
    _extract_endpoint_context(endpoint)
    assert endpoint in _endpoint_context_cache

    ref = weakref.ref(endpoint)
    size_with_endpoint = len(_endpoint_context_cache)
    del endpoint
    gc.collect()

    assert ref() is None
    assert len(_endpoint_context_cache) <= size_with_endpoint - 1
