"""
Synthetic Traffic Generator for Evaluation
-------------------------------------------
This script generates controlled login traffic against the local
credential stuffing defence system.

- All traffic is directed to localhost (127.0.0.1)
- No real credentials are used
- No external systems are involved

"""

import requests
import time
from collections import Counter
from statistics import mean

BASE_URL = "http://127.0.0.1:8000/login"


def send_login(username, user_agent=None):
    headers = {"Content-Type": "application/json"}
    if user_agent:
        headers["User-Agent"] = user_agent

    start = time.time()

    response = requests.post(
        BASE_URL,
        json={"username": username, "password": "test123"},
        headers=headers
    )

    latency = time.time() - start

    if response.status_code == 403:
        return "BLOCK", 15, latency

    data = response.json()
    return data.get("decision"), data.get("risk_score"), latency


def run_scenario(label, attempts, delay, user_agent=None):
    decisions = []
    scores = []
    latencies = []

    print(f"\nRunning scenario: {label}")

    for i in range(attempts):
        decision, score, latency = send_login(
            username=label,
            user_agent=user_agent
        )

        decisions.append(decision)
        scores.append(score)
        latencies.append(latency)

        print(f"Attempt {i+1}: {decision} | score={score} | latency={latency:.4f}s")

        time.sleep(delay)

    return decisions, scores, latencies


def calculate_metrics(decisions, ground_truth_attack):
    counts = Counter(decisions)

    total = len(decisions)
    blocked = counts.get("BLOCK", 0)
    challenged = counts.get("CHALLENGE", 0)
    allowed = counts.get("ALLOW", 0)

    if ground_truth_attack:
        detection_rate = blocked / total
        false_positive_rate = 0
    else:
        detection_rate = 0
        false_positive_rate = blocked / total

    return {
        "Total Attempts": total,
        "Blocked": blocked,
        "Challenged": challenged,
        "Allowed": allowed,
        "Detection Rate": detection_rate,
        "False Positive Rate": false_positive_rate,
    }


if __name__ == "__main__":

    results = {}

    # Scenario 1: Legitimate user behaviour
    legit = run_scenario(
        label="legitimate_user",
        attempts=8,
        delay=2
    )
    results["Legitimate"] = (legit, False)

    # Scenario 2: Credential stuffing burst
    burst = run_scenario(
        label="attacker",
        attempts=15,
        delay=0.2
    )
    results["Burst Attack"] = (burst, True)

    # Scenario 3: Scripted User-Agent bot
    bot = run_scenario(
        label="bot_user",
        attempts=10,
        delay=0.5,
        user_agent="curl/7.88.1"
    )
    results["Scripted Bot"] = (bot, True)

    print("\n============================")
    print("Evaluation Summary")
    print("============================")

    for name, ((decisions, scores, latencies), is_attack) in results.items():
        metrics = calculate_metrics(decisions, is_attack)

        print(f"\nScenario: {name}")
        for k, v in metrics.items():
            print(f"{k}: {v}")

        print("Average Risk Score:", mean(scores))
        print("Average Response Time:", mean(latencies))