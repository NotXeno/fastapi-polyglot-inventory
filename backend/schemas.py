from pydantic import BaseModel
from typing import Optional

# Item Base Structure
class ItemBase(BaseModel):
    short_name : str
    description : Optional[str] = None
    price : int
    amount : int

# Input from User (POST / PUT)
class ItemCreate(ItemBase):
    pass

# Output to Frontend 
class ItemResponse(ItemBase):
    id: str

    class Config:
        from_attributes = True
