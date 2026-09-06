from fastapi import FastAPI
from pydantic import BaseModel
from agents.chat_agent import ChatAgent

app = FastAPI()
agent = ChatAgent()

class Request(BaseModel):
    message: str


@app.post("/chat")
async def chat(request: Request):
    response = agent.run(request.message)
    return {"response": response}