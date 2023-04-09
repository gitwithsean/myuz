from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
from typing import List
from output_models import Model
from fastapi.middleware.cors import CORSMiddleware
import json, os
# Replace 'Model' with the actual name of the generated model

# Load JSON schema from file
with open("./living_and_the_son_of_death/output.json", 'r') as f:
    data_sample = json.load(f)

instance = Model(**data_sample)

app = FastAPI()
data_storage = instance

@app.middleware("http")
async def add_content_security_policy(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["Content-Security-Policy"] = "script-src 'self' 'unsafe-eval'"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/items/", response_model=Model)
async def create_item(item: Model):
    print(item)  # Add this line to log the received data
    data_storage.append(item)
    return item

@app.get("/items/", response_model=List[Model])
async def get_all_items():
    print(data_storage)  # Add this line to log the stored items
    return [data_storage]

@app.get("/items/{item_id}", response_model=Model)
async def get_item(item_id: int):
    print(item_id)  # Add this line to log the received data
    for item in data_storage:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}", response_model=Model)
async def update_item(item_id: int, updated_item: Model):
    print(item_id)  # Add this line to log the received data
    for index, item in enumerate(data_storage):
        if item.id == item_id:
            data_storage[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

