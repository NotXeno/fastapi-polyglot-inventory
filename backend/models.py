from sqlalchemy import Column, String, Integer, Text
from database import Base 
import uuid

class ItemModel(Base):
    __tablename__ = "items"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4())) # UUID
    short_name = Column(String, index=True) # Short name of the product
    description = Column(Text) # Description
    price = Column(Integer) # Price
    amount = Column(Integer) # Amounts