from fastapi import FastAPI, Request, HTTPException
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

# Signal C : Device consistency tracking
known_devices = defaultdict(set) #{username: {user_agent_fingerprint}}

# Signal D : Geolocation consistency tracking
known_countries = defaultdict(set)  # {username: {country}}

def prune_old_attempts(ip: str, now: datetime) -> None:
    """Remove timestamps older than our time window."""
    cutoff = now - timedelta(seconds = IP_WINDOW_SECONDS)

    q = ip_attempts[ip]
    while q and q[0] < cutoff:
        q.popleft()


# ------------------------------------
# Simple IP → Country mapping (MVP)
# ------------------------------------

def get_country_from_ip(ip: str) -> str:
    """
    Simulated geolocation resolver.
    Real systems would use a GeoIP database.
    """

    if ip.startswith("127."):
        return "LOCAL"
    elif ip.startswith("192."):
        return "UK"
    elif ip.startswith("10."):
        return "US"
    else:
        return "UNKNOWN"

 # Main risk engine combining multiple behavioural signals
 # Returns cumulative score and reasons for transparency

def calculate_risk(ip: str, user_agent: str, username: str) -> tuple [int, list[str]]:
    """
    Returns (score, reasons)
    Implements: 
    - Signal A: IP login rate
    - Signal B: User-Agent sanity
    - Signal C: Device consistency (new device detection)
    - Signal D: Geolocation anomaly
    """
    now = datetime.utcnow()

    score = 0
    reasons = []

    # Signal A: IP Login rate (velocity)
    # Detect rapid repeated attempts from same IP address
    prune_old_attempts(ip, now)
    ip_attempts[ip].append(now)
    attempts_in_window = len(ip_attempts[ip])

    if attempts_in_window > IP_RATE_THRESHOLD:
        score += 10
        reasons.append(f"High IP velocity: {attempts_in_window} attempts/{IP_WINDOW_SECONDS}s")

    # Signal B: User-Agent sanity
    # Detect missing or suspicious automated client headers
    ua = (user_agent or "").strip()

    if not ua:
        score += 5
        reasons.append("Missing User-Agent header")
        ua_lower = ""
    else:
        ua_lower = ua.lower()
        if "curl" in ua_lower or "python" in ua_lower or "httpie" in ua_lower:
            score += 3
            reasons.append("Likely scripted User-Agent")

    
    # Signal C: Device Consistency
    # Flag first-seen devices for a username as higher risk

    if username and ua_lower :
        if ua_lower not in known_devices[username]:
            score += 5
            reasons.append("New device/User-Agent detected for this user")
            known_devices[username].add(ua_lower)

    
    # Signal D: Geolocation anomaly

    country = get_country_from_ip(ip)

    if username:
        if country not in known_countries[username]:
            score += 7
            reasons.append(f"New country detected: {country}")
            known_countries[username].add(country)

    return score, reasons

# Convert risk score into adaptive authentication response

def score_to_decision(score: int) -> str:

    """MVP decision mapping with MFA tier."""

    if score < 5:
        return "ALLOW"
    elif score < 10:
        return "CHALLENGE"
    elif score < 20:
        return "MFA_REQUIRED"
    else:
        return "BLOCK"


# Endpoints
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

    score, reasons = calculate_risk(ip=ip, user_agent = user_agent,username = data.username)
    decision = score_to_decision(score)

   # store event data audit trail and later evaluation
   # SQLite logging (MVP evidence)
    log_event(
        username=data.username,
        ip=ip,
        user_agent = user_agent,
        risk_score = score,
        decision = decision,
        reasons = reasons,
    )

# Adaptive Mitigation Enforcement

    if decision == "BLOCK":
        raise HTTPException(
            status_code=403,
            detail={
                "message": "Blocked suspicious login attempt",
                "username": data.username,
                "ip_address": ip,
                "user_agent": user_agent if user_agent else "unknown",
                "risk_score": score,
                "reasons": reasons,
                "decision": decision 
            }
        )  
  
    if decision == "CHALLENGE":
        return {
        "message": "Challenge required (CAPTCHA placeholder)",
        "username": data.username,
        "ip_address": ip,
        "user_agent": user_agent if user_agent else "unknown",
        "risk_score": score,
        "reasons": reasons,
        "decision": decision
    }
    
    if decision == "MFA_REQUIRED":
        return {
        "message": "Multi-Factor Authentication required (OTP placeholder)",
        "username": data.username,
        "ip_address": ip,
        "user_agent": user_agent if user_agent else "unknown",
        "risk_score": score,
        "reasons": reasons,
        "decision": decision
    }

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
    