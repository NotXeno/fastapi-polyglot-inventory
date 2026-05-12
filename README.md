# fastapi-polyglot-inventory
A Microservices and Polyglot Persistence for Inventory System with the combination of Python and FastAPI

Before run the program, you need to : 
1. Open the docker desktop
2. Terminal opened to the root of the project :D

## How to run?

### Step 1 : Start the docker
1. Run :
   ```bash
   docker-compose up -d
   ```
2. Check the Docker Desktop if it's run already
3. After the container running, type this into the browser
```bash
localhost  
```

### Step 2 (Optional) : Checking MongoDB Logs
```bash
docker exec -it inventory-mongodb mongosh
use inventory_logs
db.api_logs.find()
```

Tips : 
- db.api_logs.find().sort({timestamp: -1}).limit(5) used to check last 5 logs
- db.api_logs.find() used to check all of the logs
