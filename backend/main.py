from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from typing import List
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Connection Setup to the Docker
DATABASE_URL = "postgresql://notxeno01:notxeno@localhost:5432/inventory_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define Table Model 
class ItemModel(Base):
    __tablename__ = "items"
    id = Column(String, primary_key=True, index=True) # UUID
    short_name = Column(String, nullable=False) # Short name of the product
    description = Column(String) # Description
    price = Column(Integer) # Price
    amount = Column(Integer) # Amount

# Automatically make table att the PostgreSQL
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (CRUD)
    allow_headers=["*"],  
)

# Phase 1 Model Data
class Item(BaseModel):
    id: str | None = None
    short_name : str
    description : str = None
    price : int
    amount : int

# Access Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD Rest API Endpoints

#CREATE : To Create a ne item in the inventory (POST /item)
@app.post("/item", response_model=Item)
def create_item(item: Item, db: Session = Depends(get_db)):
    new_id = str(uuid.uuid4())  # Generate a unique ID for the item

    db_item = ItemModel(
        id=new_id,
        short_name=item.short_name,
        description=item.description,
        price=item.price,
        amount=item.amount
    )
   
    db.add(db_item)
    db.commit()
    db.refresh(db_item)  # Refresh to get the generated ID and other data
    return db_item

#UPDATE : To Update an item detail that exists in the inventory (PUT /item/{id})
@app.put("/item/{item_id}", response_model=Item)
def update_item(item_id: str, updated_item: Item, db: Session = Depends(get_db)):
    # Finding item from database
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Updating the item details
    db_item.short_name = updated_item.short_name
    db_item.description = updated_item.description
    db_item.price = updated_item.price
    db_item.amount = updated_item.amount

    db.commit()
    db.refresh(db_item)  # Refresh to get the updated data
    return db_item

#DELETE : To Delete an item from the inventory (DELETE /item/{id})
@app.delete("/item/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item) # Deleting the items
    db.commit() 
    return {"message": "Item deleted successfully"}

#LIST VIEW : Get all items basic information in the inventory (GET /items)
@app.get("/items", response_model=List[Item])
def get_items(db: Session = Depends(get_db)):
    return db.query(ItemModel).all()
