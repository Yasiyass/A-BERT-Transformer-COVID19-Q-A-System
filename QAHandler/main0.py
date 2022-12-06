from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI()

class QOb(BaseModel):
    question: str
    num_answers: int

@app.post("/query")
async def query(qob: QOb):
    return {"answer": "my_dummy"}
#uvicorn main0:app  --port 8080 #http://127.0.0.1:8080/docs