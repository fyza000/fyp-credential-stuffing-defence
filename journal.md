# Development Journal – Credential Stuffing MVP
## November 2025: Research & Planning
### Completed
- Reviewed credential stuffing attack methods and account takeover risks
- Studied academic and industry sources including OWASP, Cloudflare, Verizon, and Akamai reports
- Compared traditional defences such as CAPTCHA, IP blocking, rate limiting, and MFA
- Defined project scope as a lightweight behavioural detection system suitable for smaller organisations
### Key Decisions
- Selected a rule-based scoring model instead of machine learning for transparency and easier implementation
- Chose to use only non-sensitive contextual signals to reduce privacy concerns
### Issues
- Needed to balance strong detection capability with low friction for legitimate users

## Late November – December 2025: Architecture & Design
### Completed
- Designed FastAPI backend architecture for real-time login evaluation
- Planned `/login` endpoint for risk assessment and `/events` endpoint for viewing logs
- Defined mitigation actions: ALLOW, CHALLENGE, MFA_REQUIRED, and BLOCK
- Designed initial scoring thresholds and risk evaluation flow
### Decisions
- Selected four behavioural signals:
  - IP velocity
  - User-Agent anomaly detection
  - Device consistency
  - Geolocation anomaly

### Notes
- Prioritised modular design so the prototype could be extended later

## December 2025 – January 2026: Core Implementation

### Completed
- Built `auth_service.py` as the main authentication API
- Implemented `calculate_risk()` scoring logic
- Added mitigation decision engine based on cumulative risk score
- Added in-memory state tracking for recent IP and device behaviour

### Issues
- Initial thresholds were too aggressive and triggered MFA too often
- Some legitimate first-time users received higher scores due to no previous behavioural history

### Fixes
- Adjusted thresholds after scenario testing to reduce unnecessary friction
- Refined signal weights to better separate normal and suspicious behaviour

### Outcome
- Working prototype capable of evaluating login attempts in real time

## January 2026: Logging & Database
### Completed
- Added SQLite database for authentication event storage
- Implemented `db.py` for table creation and logging functions
- Built `/events` endpoint to retrieve stored login activity

### Decisions
- Selected SQLite over Redis/PostgreSQL for simplicity, lightweight deployment, and sufficient prototype-scale performance

### Outcome
- Persistent event logs available for testing and evaluation

## February 2026: Testing & Evaluation

### Completed
- Built `attack_simulator.py` to generate synthetic traffic
- Simulated multiple scenarios:
  - Legitimate user behaviour
  - Burst credential stuffing attacks
  - Scripted bot traffic using suspicious User-Agent strings

### Metrics Collected
- Detection rate
- False positive rate
- Average response latency
- Mitigation decisions triggered

### Findings
- Legitimate users experienced low friction and no direct blocking
- Suspicious scenarios triggered MFA or BLOCK responses
- Average response times remained low during testing

## March – April 2026: Final Refinement & Report Writing

### Completed
- Reviewed threshold behaviour and tuning decisions
- Generated graphs and tables for the evaluation chapter
- Documented implementation, findings, and limitations
- Prepared appendices with technical evidence and proposal updates
- Completed proofreading, formatting, and reference checks

### Notes
- Focus shifted toward clarity of documentation and alignment with assessment criteria

## Final Reflection

The project progressed from initial research into a fully implemented and evaluated prototype. An iterative development approach allowed continuous refinement of thresholds, scoring logic, and mitigation behaviour. The final system demonstrated that lightweight behavioural risk scoring can help reduce credential stuffing attempts while maintaining acceptable usability for legitimate users.

Limitations identified included in-memory state management, simplified geolocation logic, and cold-start behaviour where first-time users may receive higher friction. Future improvements include persistent behavioural profiles, real geolocation intelligence, and adaptive threshold optimisation.