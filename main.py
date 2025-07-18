import os
import subprocess
from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from datetime import datetime

# Load environment variables
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise ValueError("MISTRAL_API_KEY is not set in .env")

# Initialize Mistral client
client = MistralClient(api_key=api_key)

# Simulated alert
alert = "High memory usage detected on service A"

# Context to pass to Mistral
context = """
Logs:
- 2025-07-15 08:01: memory spike 95% usage
Metrics:
- RAM usage: 95%
- CPU usage: 60%
Recent Deployment:
- v3.4.2 deployed 20 mins ago
"""

# Construct chat messages
messages = [
    ChatMessage(role="system", content="You are an incident recovery agent. Based on the input, decide the best recovery step."),
    ChatMessage(role="user", content=f"Alert: {alert}\nContext:\n{context}\nWhat action should I take?")
]

# Get AI decision
response = client.chat(model="mistral-small", messages=messages)
decision = response.choices[0].message.content.strip()

# Print decision
print("\n🔧 Recommended Action from AI:")
print(decision)

# Simulate execution (e.g., restart service)
print("\n⚙️  Executing recovery step...")
try:
    # Simulated command (in real use: systemctl restart service-name or kubectl rollout restart ...)
    command = "echo Restarting service A..."
    result = subprocess.check_output(command, shell=True, text=True)
    execution_result = f"✅ Execution simulated successfully:\n{result}"
except subprocess.CalledProcessError as e:
    execution_result = f"❌ Execution failed:\n{e.output}"

print(execution_result)

# Log everything to a file
# Log everything to a file
log_path = "incident_log.txt"
with open(log_path, "a", encoding="utf-8") as log_file:
    log_file.write("\n--- Incident Log ---\n")
    log_file.write(f"Time: {datetime.now()}\n")
    log_file.write(f"Alert: {alert}\n")
    log_file.write(f"AI Decision:\n{decision}\n")
    log_file.write(f"Execution Result:\n{execution_result}\n")


print(f"\n📝 Log written to {log_path}")
