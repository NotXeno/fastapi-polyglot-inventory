# fastapi-polyglot-inventory
A Microservices and Polyglot Persistence for Inventory System with the combination of Python and FastAPI

Before run the program, you need to : 
1. Open the docker desktop
2. Terminal opened to the root of the project :D

## How to run?

### Step 1 : Start the database
1. Run :
   ```bash
   docker-compose up -d
   ```
3. Check the Docker Desktop if it's run already

### Step 2 : Boot up the backend
1. Navigate the terminal to the backend folder
2. Activate the virtual environments
   **Windows:** `.\venv\Scripts\activate`
3. Install the requirements library
   ```bash
   pip install -r requirements.txt
   ```
4. Start the server
   ```bash
   fastapi dev main.py
   ```

### Step 3 : Open the frontend
1. Ummm, open it manually by double click the index.html (inside frontend folder) :D

### Step 4 (Optional) : Checking MongoDB Logs
```bash
docker exec -it inventory-mongodb mongosh
use inventory_logs
db.api_logs.find()
```

Tips : 
- db.api_logs.find().sort({timestamp: -1}).limit(5) used to check last 5 logs
- db.api_logs.find() used to check all of the logs
