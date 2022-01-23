from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


inventory = {}


# simple end-point
@app.get("/")
def home():
    return {"Data": "Home"}


# end-point with path parameter - get item by item id
@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The ID of the item you like to view", gt=0, lt=5)):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID does not exists")
    return inventory[item_id]


# end-point with query parameter - get item by name
@app.get("/get-by-name")
def get_item(*, name: Optional[str] = None, test: int):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data does not exists")


# end-point with query parameter and path parameter - get item by name
@app.get("/get-by-name/{item_id}")
def get_item(*, item_id: int, name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID does not exists")


# end-point with path parameter - create item
@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item ID already exists")
    # inventory[item_id] = {"name": item.name, "price": item.price, "brand": item.brand}
    inventory[item_id] = item
    return inventory[item_id]


# end-point to update item in inventory
@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID does not exists")
    if item.name is not None:
        inventory[item_id].name = item.name
    if item.price is not None:
        inventory[item_id].price = item.price
    if item.brand is not None:
        inventory[item_id].brand = item.brand
    return inventory[item_id]


# end-point to update item in inventory
@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete", gt=0, lt=5)):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID does not exists")
    del inventory[item_id]
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Item deleted!")
