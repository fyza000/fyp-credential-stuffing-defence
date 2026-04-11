# Final Year Project – Development Journal

---

## Phase 1 – Research and Design
**Focus:** Literature review, problem analysis, and system design  

### Progress
- Completed background research on credential stuffing attacks  
- Reviewed academic and industry literature  
- Identified limitations of traditional defence mechanisms  
- Defined system scope and selected behavioural risk signals  
- Designed initial system architecture and rule-based scoring approach  

### Challenges
- Balancing detection accuracy with user privacy constraints  
- Designing scoring thresholds that minimise false positives  

### Outcome
- Established foundation for a multi-signal risk-based authentication system  
- Defined key signals: IP velocity, User-Agent analysis, device consistency, and geolocation  

---

## Phase 2 – Implementation (Core Prototype)
**Focus:** Development of MVP credential stuffing detection system  

### Progress
- Implemented FastAPI backend with `/login` endpoint  
- Developed rule-based risk scoring engine:
  - Signal A: IP velocity tracking  
  - Signal B: User-Agent anomaly detection  
  - Signal C: Device consistency detection  
  - Signal D: Geolocation anomaly detection  
- Implemented adaptive mitigation logic (ALLOW, CHALLENGE, MFA_REQUIRED, BLOCK)  
- Integrated SQLite database for logging login events  
- Created `/events` endpoint for retrieving stored logs  

### Challenges
- Selecting appropriate scoring thresholds  
- Avoiding excessive false positives for legitimate users  
- Maintaining simplicity while ensuring meaningful detection  

### Outcome
- Fully functional prototype capable of detecting and responding to suspicious login behaviour  
- Modular system design allowing further extension  

---

## Phase 3 – Evaluation and Testing
**Focus:** System evaluation using synthetic traffic  

### Progress
- Developed synthetic traffic generator for controlled testing  
- Simulated multiple scenarios:
  - Legitimate user behaviour  
  - High-frequency credential stuffing attacks  
  - Scripted bot activity using custom User-Agent  
- Collected performance metrics:
  - Detection rate  
  - False positive rate  
  - Response latency  

### Challenges
- Ensuring realistic simulation of attack behaviour  
- Interpreting results in the absence of real-world datasets  

### Outcome
- Validated effectiveness of multi-signal risk scoring approach  
- Identified system limitations and areas for improvement  

---

## Overall Reflection
The project progressed from theoretical research to a fully implemented and evaluated prototype. The iterative approach allowed continuous refinement of the scoring logic and system design. While the system demonstrates effective detection capabilities, limitations such as in-memory state management and simplified geolocation highlight opportunities for future enhancement.