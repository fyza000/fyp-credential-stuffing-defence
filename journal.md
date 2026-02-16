#Final Year Project - Weekly Journal 
## Phase 1- Reasearch & Development
##Focus:** Research, literature review, and system design

**Progress:**
-completed background research on credential stuffing
-Reviewed academic and industry literature
-Defined system scope and behavioural signals
-Drafted initial architecture and scoring approach

**Challenges:**
-Balancing detection accuracy with privacy contraints
-Designing scoring thresholds that minimise false positives

**Next Steps:**
-Implement FastAPI scoring API skeleton
-Define initial risk scoring weights and thresholds
-Add Redis state-tracking stub

## Phase 2 - Implementation (Core Prototype)
##Focus:** MVP implementation of behavioural risk scoring API

**Progress:**
-Implemented FastAPI backend with '/login' endpoint
-Development inital risk scoring engine:
 -Signal A: IP velocity tracking 
 -Signal B: User-Agent anomaly detection
_Added decision mapping (ALLOW / CHALLENGE / BLOCK)
-Implemented SQLite database logging for login attempt evidence
-Created '/events' endpoint for retrieving security logs

**Challenges:**
-Selecting realistic scoring thresholds
-Keeping detection lightweight without over-blocing legitimate users

**Next Steps:**
-Add Signal C: Device consistency detection
-Enforce mitigation actions (BLOCK = HTTP 403)
-Begin synthetic traffic simulation for evaluation