from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from motor.motor_asyncio import AsyncIOMotorClient

# PostgreSQL Connection Setup
SQLALCHEMY_DATABASE_URL = "postgresql://notxeno01:notxeno@inventory-postgres:5432/inventory_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Function to open & close DB Connection every requests
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# MongoDB Connection Setup
MONGO_DETAILS = "mongodb://inventory-mongodb:27017"
mongo_client = AsyncIOMotorClient(MONGO_DETAILS)
mongo_db = mongo_client.inventory_logs # Database Logs
mongo_collection = mongo_db.get_collection("api_logs") # API Collection Logs
