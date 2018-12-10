from fastapi import APIRouter

router = APIRouter()


@router.get("/dog")
def get_b_dog():
    return "B Woof"


@router.get("/cat")
def get_b_cat():
    return "B Meow"
