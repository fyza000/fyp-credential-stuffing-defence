from os import remove
from fastapi import FastAPI, Request
from pydantic import BaseModel
from collections import defaultdict, deque
from datetime import datetime, timedelta

from db import init_db, log_event, latest_events

app = FastAPI(title = "Credential stuffing MVP")

#Request model

class LoginRequest(BaseModel):
   username: str
   password: str

#MVP in-memory tracking (signal A)

IP_WINDOW_SECONDS = 60
IP_RATE_THRESHOLD = 8 # attempts per 60 seconds from same IP
ip_attempts = defaultdict(deque) #{ip: deque ([datetime, datetime, ...])}

def prune_old_attempts(ip: str, now: datetime) -> None:
    """Remove timestamps older than our time window."""
    cutoff = now - timedelta(seconds = IP_WINDOW_SECONDS)

    q = ip_attempts[ip]
    while q and q[0] < cutoff:
        q.popleft()

def calculate_risk(ip: str, user_agent: str) -> tuple [int, list[str]]:
    """
    Returns (score, reasons)
    Implements: 
    - Signal A: IP login rate
    - Signal B: User-Agent sanity
    """
    now = datetime.utcnow()

    # Signal A: IP Login rate (velocity)---
    prune_old_attempts(ip, now)
    ip_attempts[ip].append(now)
    attempts_in_window = len(ip_attempts[ip])

    score = 0
    reasons = []
    
    if attempts_in_window > IP_RATE_THRESHOLD:
        score += 10
        reasons.append(f"High IP velocity: {attempts_in_window} attempts/{IP_WINDOW_SECONDS}s")

    # Signal B: User-Agent sanity

    ua = (user_agent or "").strip()

    if not ua:
        score += 5
        reasons.append("Missing User-Agent header")
    else:
        ua_lower = ua.lower()
        if "curl" in ua_lower or "python" in ua_lower or "httpie" in ua_lower:
            score += 3
            reasons.append("Likely scripted User-Agent")

    return score, reasons

def score_to_decision(score: int) -> str:

    """MVP decision mapping."""

    if score < 5:
        return "ALLOW"
    elif score < 15:
        return "CHALLENGE"
    else:
        return "BLOCK"

#Endpoints
@app.on_event("startup")
def on_startup() -> None:
    init_db()

@app.get("/")
def root():
    return{"status": "FastAPI is running"}

@app.post("/login")
async def login(data: LoginRequest, request: Request):
    ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "")

    score, reasons = calculate_risk(ip=ip, user_agent = user_agent)
    decision = score_to_decision(score)

    #SQLite logging (MVP evidence)
    log_event(
        username=data.username,
        ip=ip,
        user_agent = user_agent,
        risk_score = score,
        decision = decision,
        reasons = reasons,
    )

    return {
        "username": data.username,
        "ip_address": ip,
        "user_agent": user_agent if user_agent else "unknown",
        "risk_score": score,
        "decision": decision,
        "reasons": reasons,
    }

@app.get("/events")
def events(limit: int = 20):
    return {"events": latest_events(limit=limit)}