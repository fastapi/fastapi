from decimal import Decimal

from fastapi import Query


def create_item(price: Decimal = Query(..., max_digits=5, decimal_places=2)):
    return {"price": price}
