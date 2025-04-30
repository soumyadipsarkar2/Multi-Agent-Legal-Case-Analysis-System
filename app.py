from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from orchestrator import analyze

app = FastAPI(title="LegalPulse API")

class AnalyzeRequest(BaseModel):
    document: str

class AnalyzeResponse(BaseModel):
    summary: str
    high_risk: list[str]
    eval_score: float

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_case(req: AnalyzeRequest):
    if not req.document:
        raise HTTPException(400, "Document text required")
    result = analyze(req.document)
    return AnalyzeResponse(**result)

# Run with:
# uvicorn app:app --reload --port 8000
