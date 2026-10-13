import os
import shutil
from fastapi.responses import FileResponse
from typing import Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.rag_engine import RAGEngine
from app.evaluator import RAGEvaluator

app = FastAPI(title="Production-Ready RAG API", version="1.0.0")

# API Anahtarı ortam değişkeninden okunur
API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6LpkiiVVY-CKAH-qVQi_S_Cwov5NjtqYjI_edIa-HkMIQ")
rag = RAGEngine(api_key=API_KEY)
evaluator = RAGEvaluator(api_key=API_KEY)

class QuestionRequest(BaseModel):
    question: str
    evaluate: Optional[bool] = False

# @app.get("/")
# def health_check():
#     return {"status": "active", "service": "PDF RAG API"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".txt")):
        raise HTTPException(status_code=400, detail="Yalnızca PDF veya TXT dosyaları desteklenmektedir.")
    
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        chunk_count = rag.process_pdf(file_path)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            
    return {"message": "Dosya başarıyla indekslendi", "parca_sayisi": chunk_count}

@app.post("/ask")
def ask_question(request: QuestionRequest):
    result = rag.query(request.question)
    response_data = {
        "question": request.question,
        "answer": result["answer"],
        "retrieved_context": result["context"]
    }
    
    if request.evaluate and hasattr(evaluator, "evaluate"):
        try:
            eval_scores = evaluator.evaluate(
                request.question,
                result["context"],
                result["answer"]
            )
            response_data["evaluation"] = eval_scores
        except Exception:
            response_data["evaluation"] = None
        
    return response_data
@app.get("/")
def home():
    return FileResponse("index.html")