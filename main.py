from fastapi import FastAPI
from pydantic import BaseModel
from app import graph
from fastapi.responses import PlainTextResponse
import time

start = time.time()
app = FastAPI()

class QuestionRequest(BaseModel):
    question:str

@app.post("/analyse")
async def analyse(request:QuestionRequest):
    answer = await graph.ainvoke({
        "question":request.question
    })
    print(f"Total App Time: {time.time()-start:.2f}s")

    return PlainTextResponse(
        content=answer["final_answer"]
    )