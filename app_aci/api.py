from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd

app = FastAPI()

df = pd.DataFrame()  # DataFrame global initialisé vide

class Item(BaseModel):
    id: int
    name: str
    age: int

@app.get("/")
def read_root():
    return {"message": "Bienvenue à l'API FastAPI"}

@app.get("/items/", response_model=List[Dict[str, Any]])
def read_items():
    if df.empty:
        raise HTTPException(status_code=404, detail="DataFrame is empty")
    return df.to_dict(orient='records')

@app.get("/items/{item_id}", response_model=Dict[str, Any])
def read_item(item_id: int):
    if df.empty:
        raise HTTPException(status_code=404, detail="DataFrame is empty")
    item = df[df['id'] == item_id]
    if item.empty:
        raise HTTPException(status_code=404, detail="Item not found")
    return item.to_dict(orient='records')[0]

@app.post("/upload/")
def upload_data(data: List[Dict[str, Any]]):
    global df
    df = pd.DataFrame(data)
    return {"message": "DataFrame updated successfully"}
