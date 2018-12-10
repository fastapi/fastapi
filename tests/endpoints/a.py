from fastapi import APIRouter

router = APIRouter()


@router.get("/dog")
def get_a_dog():
    return "Woof"


@router.get("/cat")
def get_a_cat():
    return "Meow"
