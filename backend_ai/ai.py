#Chat: Ko uporabnik v frontendu klikne "Pošlji", React pošlje zahtevo na http://localhost:8000/api/round-table (ai.py).

import asyncio
import os
import uvicorn
from typing import List, Dict, Tuple
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

app = FastAPI()

AGENTS_REGISTRY = {
    "qwen": "qwen3:4b",
    "ministral": "ministral-3:3b",
    "deepseek": "deepseek-r1:1.5b"
}

SUMMARY_MODEL = "deepseek-r1:1.5b"

# Get Ollama host from environment variable, default to localhost for local development
OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")

class ChatRequest(BaseModel):
    query: str
    selected_agents: List[str]

class ChatResponse(BaseModel):
    responses: Dict[str, str]
    summary: str

async def run_model_and_collect(agent_key: str, user_input: str) -> Tuple[str, str]:
    """
    Run a model and collect the complete response.
    Returns (agent_key, response_text) or (agent_key, error_message)
    """
    model_id = AGENTS_REGISTRY[agent_key]
    
    llm = ChatOllama(
        model=model_id,
        temperature=0.7,
        base_url=OLLAMA_BASE_URL
    )
    
    messages = [HumanMessage(content=user_input)]
    
    try:
        response_parts = []
        async for chunk in llm.astream(messages):
            if chunk.content:
                response_parts.append(chunk.content)
        
        full_response = "".join(response_parts)
        return (agent_key, full_response)
    except Exception as e:
        error_message = f"Napaka pri modelu {model_id}: {str(e)}"
        return (agent_key, error_message)

async def collect_all_responses(request: ChatRequest) -> Dict[str, str]:
    """
    Collect complete responses from all selected models running in parallel.
    Returns a dictionary mapping agent_key to response_text.
    """
    valid_agents = [k for k in request.selected_agents if k in AGENTS_REGISTRY]
    
    if not valid_agents:
        raise ValueError("Noben veljaven agent ni bil izbran")
    
    tasks = [
        asyncio.create_task(run_model_and_collect(agent, request.query))
        for agent in valid_agents
    ]
    
    results = await asyncio.gather(*tasks)
    
    responses = {}
    for agent_key, response_text in results:
        responses[agent_key] = response_text
    
    return responses

async def generate_summary(responses: Dict[str, str], original_query: str) -> str:
    """
    Generate a summary of all model responses using a separate dedicated model.
    """
    # Format all responses for the summary prompt
    responses_text = "\n\n".join([
        f"Model {agent_key}:\n{response_text}"
        for agent_key, response_text in responses.items()
    ])
    
    summary_prompt = f"""Originalno vprašanje: {original_query}

Odgovori različnih modelov:

{responses_text}

Prosimo, naredi kratek in jedrnat povzetek vseh odgovorov, ki združi ključne točke iz vseh modelov. Uporabi max 200 znakov za odgovor. Uporabi le kontekst iz odgovorov."""
    
    llm = ChatOllama(
        model=SUMMARY_MODEL,
        temperature=0.7,
        base_url=OLLAMA_BASE_URL
    )
    
    messages = [HumanMessage(content=summary_prompt)]
    
    try:
        summary_parts = []
        async for chunk in llm.astream(messages):
            if chunk.content:
                summary_parts.append(chunk.content)
        
        summary = "".join(summary_parts)
        return summary
    except Exception as e:
        return f"Napaka pri generiranju povzetka: {str(e)}"

@app.post("/api/round-table", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest = Body(...)):
    try:
        # Collect all responses from selected models
        responses = await collect_all_responses(request)
        
        # Generate summary of all responses
        summary = await generate_summary(responses, request.query)
        
        return ChatResponse(responses=responses, summary=summary)
    except ValueError as e:
        # Handle validation errors (e.g., no valid agents selected)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)