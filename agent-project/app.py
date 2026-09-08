from fastapi import FastAPI
from pydantic import BaseModel
from agents.orchestrator_agent import OrchestratorAgent


app = FastAPI()
agent = OrchestratorAgent()

class Request(BaseModel):
    message: str


@app.post("/chat")
async def chat(req: Request):
    response = agent.orchestrate2(req.message)
    return {"response": response}
