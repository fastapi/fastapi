import fastapi.routing


def test_endpoint_context_cache_does_not_reuse_context_for_different_callable(
    monkeypatch,
):
    fastapi.routing._endpoint_context_cache.clear()
    monkeypatch.setattr(fastapi.routing, "id", lambda _: 1, raising=False)

    first_context = fastapi.routing._extract_endpoint_context(
        fastapi.routing.serialize_response
    )
    second_context = fastapi.routing._extract_endpoint_context(
        fastapi.routing._extract_endpoint_context
    )

    assert first_context["function"] == "serialize_response"
    assert second_context["function"] == "_extract_endpoint_context"
