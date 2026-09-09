from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import UploadFile, File
from agents.orchestrator_agent import OrchestratorAgent
from services.file_storage_service import FileStorageService
from services.indexing_service import IndexingService

app = FastAPI()
agent = OrchestratorAgent()

storage_service = FileStorageService()
indexing_service = IndexingService()

class Request(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: Request):
    response = agent.orchestrate(req.message)
    return {"response": response}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Save the uploaded file to the "documents" directory
    content = await file.read()
    file_name = file.filename
    if file_name is None:
        raise HTTPException(status_code=400, detail="Uploaded file must include a filename.")

    storage_service.save_file(file_name, content)
    indexing_service.index_documents(file_name, 1000)
    return {"info": f"File '{file_name}' uploaded and indexed successfully."}
    
