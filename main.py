from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from spatial_analysis import perform_spatial_analysis # Link to logic file

app = FastAPI()

# Secure CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://sensor-lab-pro.vercel.app", 
        "http://localhost:3000" # For local testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This Model fixes the 422 error by telling FastAPI exactly what to expect
class AnalysisRequest(BaseModel):
    value: int 

@app.get("/")
def read_root():
    return {"status": "Backend is running successfully"}

@app.post("/spatial-analysis")
async def spatial_analysis_endpoint(request: AnalysisRequest):
    try:
        # Pass the frontend's 'value' to the logic function
        result = perform_spatial_analysis(request.value)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))