from flask import Flask, request
import logging
from agent_logic import run_alert_agent

app = Flask(__name__)

logging.basicConfig(filename='logs/agent.log', level=logging.INFO)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    alerts = data.get("alerts", [])

    for alert in alerts:
        alert_info = alert.get("annotations", {}).get("summary", "No summary")
        logging.info(f"Received alert: {alert_info}")
        try:
            result = run_alert_agent(alert_info)
            logging.info(f"Agent response: {result}")
        except Exception as e:
            logging.error(f"Error handling alert: {e}")

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
