from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Credential stuffing Risk Scoring API")

Class LoginAttempt(BaseModel):
  username: str
  ip: str
  user_agent: Optional[str] = None
  device_id: Optional[str] = None
  geo_country: Optional[str] = None

@app.get("/health")
def health():
  return {"status": "ok"}

@app.post("/score-login")
def score_login(attempt: LoginAttempt):
   """
   Placeholder endpoit for rsik scoring.
   Scoring rules and redis state tracking will be implemented iteratively.

   """
  return {
    "risk_score":0,
    "decision": "allow",
    "reason":["placeholder"]
  }
