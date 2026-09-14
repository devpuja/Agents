from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
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
    
    file_name = file.filename
    if not file_name:
        raise HTTPException(status_code=400, detail="Uploaded file must include a filename.")
    
    content = await file.read()
    
    file_path = storage_service.save_file(file_name, content)
    indexing_service.index_documents(file_path, 1000)
    return {"info": f"File '{file_name}' uploaded and indexed successfully."}
    
