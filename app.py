from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# Define the common parameter structure for both APIs
class AgentRequest:
    def __init__(self, name: str, description: str, language: str):
        self.name = name
        self.description = description
        self.language = language


def call_vapi(data: AgentRequest):
    url = "https://api.vapi.ai/assistants/create" 
    headers = {
        "Authorization": "Bearer YOUR_VAPI_API_KEY"
    }
    payload = {
        "name": data.name,
        "description": data.description,
        "language": data.language
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def call_retell(data: AgentRequest):
    url = "https://api.retellai.com/agents" 
    headers = {
        "Authorization": "Bearer YOUR_RETELL_API_KEY"
    }
    payload = {
        "agent_name": data.name,
        "agent_description": data.description,
        "language": data.language
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

@app.post("/create_agent")
async def create_agent(data: AgentRequest, api_choice: str):
    """
    Unified API endpoint to create agent via either VAPI or Retell AI.
    :param data: Agent creation details (name, description, language)
    :param api_choice: API choice ("vapi" or "retell")
    :return: Response from the selected API
    """
    if api_choice == "vapi":
        return call_vapi(data)
    elif api_choice == "retell":
        return call_retell(data)
    else:
        raise HTTPException(status_code=400, detail="Invalid API choice. Choose 'vapi' or 'retell'.")

# Run with Uvicorn (for development use)
# uvicorn app:app --reload
