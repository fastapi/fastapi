from fastapi import APIRouter


def test_router_tags():
    string_tag = "example"
    list_tag = ["example"]
    router1 = APIRouter(tags=string_tag)
    router2 = APIRouter(tags=list_tag)

    assert router1.tags == router2.tags


def test_router_tags_regression():
    string_tag = "example"
    old_tag_from_single_string = ["e", "x", "a", "m", "p", "l", "e"]
    router = APIRouter(tags=string_tag)

    assert router.tags != old_tag_from_single_string
