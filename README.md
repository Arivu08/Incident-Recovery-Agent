# 🔧 Autonomous Incident Recovery Agent

An intelligent agent that detects system incidents and autonomously recovers from them using Python, LangChain, and Mistral (LLM).

---

## 🚀 What It Does

- Monitors system health (simulated or real alerts)
- Understands incident context using an LLM
- Chooses the correct fix (e.g., restart, cleanup)
- Executes recovery actions (via shell/Ansible)
- Verifies system recovery
- Logs and optionally sends Slack/email updates

---

## 🧠 Tech Stack

- **Python** – Core language
- **LangChain** – Agent logic + tool calling
- **Mistral** – LLM for intelligent decision-making
- **Shell / Ansible** – Executes fixes
- **Slack API** – Notifications (optional)

---

