from langchain.agents import Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from tools import restart_container, list_containers
import os

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# LangChain wrapper for Mistral
class MistralLangChainWrapper(ChatOpenAI):
    def _call(self, messages, stop=None):
        client = MistralClient(api_key=MISTRAL_API_KEY)
        response = client.chat(model="mistral-small", messages=[
            {"role": m.type, "content": m.content} for m in messages
        ])
        return response.choices[0].message.content

tools = [
    Tool(name="Restart Docker Container", func=restart_container, description="Restarts a docker container by name"),
    Tool(name="List Containers", func=list_containers, description="Lists running docker containers"),
]

def run_alert_agent(alert_description: str) -> str:
    llm = MistralLangChainWrapper()
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    
    prompt = f"""
    Analyze the following alert and suggest multiple recovery steps.
    Then choose the best one and execute it.

    Alert: {alert_description}
    """
    result = agent.run(prompt)
    return result
