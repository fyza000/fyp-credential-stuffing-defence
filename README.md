# fyp-credential-stuffing-defence
**Final Year Project – BSc (Hons) Computer Security and Forensics**
**Student:** Faiza Noor Noushad

---

## Project Overview

This project implements a lightweight, rule-based credential stuffing defence system that detects and mitigates automated login attacks using behavioural risk scoring.

The system analyses multiple non-sensitive contextual signals — including IP velocity, User-Agent behaviour, device consistency, and geolocation anomalies — to distinguish between legitimate users and automated attacks. Based on the calculated risk score, the system applies adaptive mitigation strategies such as allowing access, issuing challenges, requiring multi-factor authentication, or blocking the request.

The solution is designed to be interpretable, modular, and suitable for environments where complex machine learning-based approaches are not practical.

---

## Key Features

- Multi-signal behavioural risk analysis
- Rule-based risk scoring engine
- Adaptive authentication decisions: ALLOW, CHALLENGE, MFA_REQUIRED, BLOCK
- SQLite-based logging of login events
- Synthetic traffic generator for evaluation
- Retrieval of authentication logs via API

---

## System Architecture

The system consists of three main components:

- **Authentication Service** (`auth.py`) – handles login requests and risk evaluation
- **Database Layer** (`db.py`) – stores login event data
- **Traffic Simulator** (`attack_sim.py`) – generates test scenarios for evaluation

---

## Technology Stack

- FastAPI (Python)
- SQLite (data storage)
- Python in-memory data structures for behavioural tracking
- Requests library (traffic simulation)

---

## How to Run

**1. Clone the repository**
```bash
git clone https://github.com/fyza000/fyp-credential-stuffing-defence.git
cd fyp-credential-stuffing-defence
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the FastAPI server**
```bash
uvicorn auth:app --reload
```

**5. Access the API**

| Endpoint | URL |
|----------|-----|
| Login | http://127.0.0.1:8000/login |
| Events | http://127.0.0.1:8000/events |
| API Docs | http://127.0.0.1:8000/docs |

---

## Evaluation

The system can be tested using the synthetic traffic generator:

```bash
python attack_sim.py
```

This simulates:
- Legitimate user behaviour
- Credential stuffing attack bursts
- Scripted bot traffic

---

## Current Status

- [x] System implemented
- [x] Risk scoring and mitigation logic completed
- [x] Synthetic traffic generator implemented
- [x] Evaluation completed
- [x] Report submitted