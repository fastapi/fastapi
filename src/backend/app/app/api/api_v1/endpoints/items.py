from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api import deps
from app.models import Item, ItemCreate, ItemOut, ItemUpdate, User

router = APIRouter()

SessionDep = Annotated[Session, Depends(deps.get_db)]
CurrentUser = Annotated[User, Depends(deps.get_current_active_user)]


@router.get("/")
def read_items(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> list[ItemOut]:
    """
    Retrieve items.
    """

    if current_user.is_superuser:
        statement = select(Item).offset(skip).limit(limit)
        return session.exec(statement).all()  # type: ignore
    else:
        statement = (
            select(Item)
            .where(Item.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        return session.exec(statement).all()  # type: ignore


@router.get("/{id}")
def read_item(session: SessionDep, current_user: CurrentUser, id: int) -> ItemOut:
    """
    Get item by ID.
    """
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item  # type: ignore


@router.post("/")
def create_item(
    *, session: SessionDep, current_user: CurrentUser, item_in: ItemCreate
) -> ItemOut:
    """
    Create new item.
    """
    item = Item.from_orm(item_in, update={"owner_id": current_user.id})
    session.add(item)
    session.commit()
    session.refresh(item)
    return item  # type: ignore


@router.put("/{id}")
def update_item(
    *, session: SessionDep, current_user: CurrentUser, id: int, item_in: ItemUpdate
) -> ItemOut:
    """
    Update an item.
    """
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    # TODO: check this actually works
    update_dict = item_in.dict(exclude_unset=True)
    item.from_orm(update_dict)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item  # type: ignore


@router.delete("/{id}")
def delete_item(session: SessionDep, current_user: CurrentUser, id: int) -> ItemOut:
    """
    Delete an item.
    """
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(item)
    session.commit()
    return item  # type: ignore
