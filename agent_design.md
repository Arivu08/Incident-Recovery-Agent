# 🧠 Autonomous Incident Recovery Agent — Design Document

## 🏗️ High-Level Design (HLD)

### 🎯 Objective
To build an autonomous agent that detects incidents (via Prometheus alerts), gathers system context, determines appropriate recovery actions using an LLM (Mistral), executes those actions, and verifies resolution—all with minimal human involvement.

---

### 🔲 Key Components

| Component              | Responsibility                                                                 |
|------------------------|---------------------------------------------------------------------------------|
| **Alert Listener**     | Receives incident alerts from Prometheus Alertmanager                           |
| **Context Loader**     | Gathers logs, metrics, infra state, and historical incident data                 |
| **LLM Decision Engine**| Uses LangChain + Mistral to generate recovery decisions                          |
| **Execution Layer**    | Executes chosen recovery action (e.g., restart service, rollback, scale up)     |
| **Verification Layer** | Validates issue resolution through alerts and health checks                     |
| **Notification Module**| Sends status updates (Slack, email, etc.)                                       |
| **Audit Logger**       | Stores actions taken and results for traceability and auditing                  |

---

## 🧩 Low-Level Design (LLD)

### 1. Alert Listener
- **Tool**: FastAPI or Flask
- **Function**: Webhook endpoint to receive alerts

```python
@app.post("/alert")
def receive_alert(alert: AlertModel):
    process_alert(alert)
```

---

### 2. Context Loader
- **Tasks**:
  - Fetch metrics from Prometheus API
  - Retrieve recent logs from services
  - Query infrastructure state via shell or APIs
  - Optional: Load past incident patterns

---

### 3. Prompt Builder (LangChain)
- Formats gathered context into a structured prompt for Mistral

```python
prompt = f"""
Alert: {alert_name}
Metrics: {metrics_snapshot}
Logs: {recent_logs}
Infra Status: {infra_status}
What should the agent do to recover?
"""
```

---

### 4. LLM Decision Engine
- **LLM**: Mistral (API-based)
- **LangChain integration**:

```python
from langchain_mistralai.chat_models import ChatMistralAI
llm = ChatMistralAI(api_key=API_KEY)
response = llm.invoke([HumanMessage(content=prompt)])
```

---

### 5. Recovery Executor
- Executes shell commands or API calls based on LLM's suggestion:

```python
if "restart" in action:
    os.system("systemctl restart my-service")
elif "rollback" in action:
    subprocess.run(["sh", "rollback.sh"])
```

---

### 6. Verification Layer
- Poll Prometheus to check if alert is cleared
- Run health-check endpoints or test scripts

```python
def is_resolved(alert_id):
    res = requests.get(f"http://prometheus/api/v1/alerts/{alert_id}")
    return res.json()["status"] == "resolved"
```

---

### 7. Notification Module
- Sends alert recovery summary to Slack or email

```python
send_slack_message(f"Incident {incident_id} resolved via: {action}")
```

---

### 8. Logging & Auditing
- Logs each alert, decision, action, and outcome
- Optional: Store in SQLite or ELK

---

## 🔧 Technologies Used

| Function                | Tool            |
|------------------------|-----------------|
| Alerts                 | Prometheus       |
| LLM                    | Mistral          |
| Agent Framework        | LangChain (Python) |
| Backend Service        | FastAPI / Flask  |
| Infra Actions          | Shell, Ansible, or Terraform (optional) |
| Notification           | Slack / Email    |
| Development Environment| Cursor IDE       |