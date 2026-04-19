# FYP Credential Stuffing Defence
**Final Year Project – BSc (Hons) Computer Security and Forensics**  
**Student:** Faiza Noor Noushad

## Project Overview
This project implements a lightweight, rule-based credential stuffing defence system designed to detect and mitigate automated login attacks using behavioural risk scoring.
The system analyses multiple non-sensitive contextual signals, including IP velocity, User-Agent behaviour, device consistency, and geolocation anomalies, to distinguish between legitimate users and suspicious automated activity.
Based on the calculated risk score, the system applies adaptive mitigation actions such as allowing access, issuing a challenge, requiring multi-factor authentication, or blocking the request.
The solution was designed to be interpretable, modular, and suitable for smaller organisations or environments where complex machine learning-based approaches may not be practical.

## Key Features
- Multi-signal behavioural risk analysis
- Rule-based risk scoring engine
- Adaptive authentication decisions:
  - ALLOW
  - CHALLENGE
  - MFA_REQUIRED
  - BLOCK
- SQLite-based logging of authentication events
- Synthetic traffic generator for evaluation
- Retrieval of stored login events via API
- Lightweight and modular prototype design

## System Architecture
The system consists of three main components:
- **Authentication Service** (`auth_service.py`) – Handles login requests, risk scoring, and mitigation decisions
- **Database Layer** (`db.py`) – Stores authentication event logs using SQLite
- **Traffic Simulator** (`attack_simulator.py`) – Generates synthetic login traffic for testing and evaluation

### High-Level Flow
Login Request → Risk Scoring Engine → Mitigation Decision → Event Logging

## Technology Stack
- Python
- FastAPI
- SQLite
- Uvicorn
- Requests library
- In-memory Python data structures for behavioural tracking

## How to Run
### 1. Clone the Repository
```bash
git clone https://github.com/fyza000/fyp-credential-stuffing-defence.git
cd fyp-credential-stuffing-defence
```
### 2.Create and Activate Virtual Environment
```
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```
### 4. Run the Application
Uvicorn auth_service:app --reload

### 5. Access the API
-Swagger UI: http://127.0.0.1:8000/docs
-Login endpoint:  http://127.0.0.1:8000/docs
-Events endpoint:  http://127.0.0.1:8000/docs

### Evaluation
The prototype can be tested using the synthetic traffic generator: attack_simulator.py

THis simulates:
-Legitimate user behaviour
-Credential stuffing attack bursts
-Scripted bot traffic
-Differentiate mitigation responses under varying risk levels
