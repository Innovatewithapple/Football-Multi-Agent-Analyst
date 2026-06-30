from fastapi import FastAPI
from pydantic import BaseModel
from app import graph

app = FastAPI()

class QuestionRequest(BaseModel):
    question:str

@app.post("/analyse")
async def analyse(request:QuestionRequest):
    answer = await graph.ainvoke({
        "question":request.question
    })
    final_answer = answer['final_answer']
    return final_answer