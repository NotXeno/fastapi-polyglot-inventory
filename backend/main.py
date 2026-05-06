from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI()

# Phase 1 Model Data
class Item(BaseModel):
    id: str | None = None
    short_name : str
    description : str
    price : int
    amount : int

# Temporary Database

inventory_db = []

# CRUD Rest API Endpoints

#CREATE : To Create a ne item in the inventory (POST /item)
@app.post("/item")
def create_item(item: Item):
    item.id = str(uuid.uuid4())  # Generate a unique ID for the item
    inventory_db.append(item)
    return item

#READ : To Get all of the items in the inventory (GET /item/{id})
@app.get("/item/{item_id}")
def read_item(item_id:str):
    for item in inventory_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

#UPDATE : To Update an item detail that exists in the inventory (PUT /item/{id})
@app.put("/item/{item_id}")
def update_item(item_id: str, updated_item: Item):
    for index, item in enumerate(inventory_db):
        if item.id == item_id:
            updated_item.id = item_id # Make sure the ID same
            inventory_db[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

#DELETE : To Delete an item from the inventory (DELETE /item/{id})
@app.delete("/item/{item_id}")
def delete_item(item_id: str):
    for index, item in enumerate(inventory_db):
        if item.id == item.id:
            inventory_db.pop(index)
            return {"message" : "Item deleted successfully"}
        raise HTTPException(status_code=404, detail="Item not found")

#LIST VIEW : Get all items basic information in the inventory (GET /items)
@app.get("/items")
def list_items():
    return inventory_db
