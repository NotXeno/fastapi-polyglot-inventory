from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
# File imports
import models, schemas
from database import engine, get_db, mongo_collection

# Automatically create tables based on models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Middleware
app.add_middleware (
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    action_map = {
        ("POST", "/items/"): "ADD_INVENTORY",
        ("GET", "/items/"): "LIST_INVENTORY",
        ("PUT", "/items/"): "EDIT_INVENTORY",
        ("DELETE", "/items/"): "DELETE_INVENTORY",
    }

    action = "UNKNOWN"
    for (method, path), act in action_map.items():
        if request.method == method and request.url.path.startswith(path):
            action = act
            break

    response = await call_next(request)

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": request.method,
        "endpoint": request.url.path,
        "action": action,
    }

    await mongo_collection.insert_one(log_entry)
    return response

# Endpoints (CRUD)

@app.get("/items/", response_model=list[schemas.ItemResponse])
def read_items(db: Session = Depends(get_db)):
    items = db.query(models.ItemModel).all()
    return items

@app.post("/item/", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
        new_item = models.ItemModel(**item.model_dump())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

@app.put("/item/{item_id}", response_model=schemas.ItemResponse)
def update_item(item_id: str, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.ItemModel).filter(models.ItemModel.id == item_id).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db_item.short_name = item.short_name
    db_item.description = item.description
    db_item.price = item.price
    db_item.amount = item.amount

    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/item/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(models.ItemModel).filter(models.ItemModel.id == item_id).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
     
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}