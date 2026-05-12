# Python Version
FROM python:3.9-slim

# Working Directory
WORKDIR /app

# Install Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt                                                                                                                     

# Copy Backend code to container
COPY . .

# Open Port 8000
EXPOSE 8000

# Command for FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 