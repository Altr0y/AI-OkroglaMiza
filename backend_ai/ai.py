#Chat: Ko uporabnik v frontendu klikne "Pošlji", React pošlje zahtevo na http://localhost:8000/api/round-table (ai.py).

import asyncio
import os
import logging
import uvicorn
from datetime import datetime
from typing import List, Dict, Tuple
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

AGENTS_REGISTRY = {
    "qwen": "qwen3:4b",
    "ministral": "ministral-3:3b",
    "deepseek": "deepseek-r1:1.5b"
}

SUMMARY_MODEL = "deepseek-r1:1.5b"

# Get Ollama host from environment variable, default to localhost for local development
OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")

# Initialize web search tool
search_tool = DuckDuckGoSearchRun()

def get_current_date_time() -> str:
    """Get the current date and time in a readable format."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")

class ChatRequest(BaseModel):
    query: str
    selected_agents: List[str]

class ChatResponse(BaseModel):
    responses: Dict[str, str]
    summary: str

async def run_model_and_collect(agent_key: str, user_input: str, search_results: str = "", search_performed: bool = False) -> Tuple[str, str]:
    """
    Run a model with web search capabilities and collect the complete response.
    Returns (agent_key, response_text) or (agent_key, error_message)
    """
    model_id = AGENTS_REGISTRY[agent_key]
    
    llm = ChatOllama(
        model=model_id,
        temperature=0.7,
        base_url=OLLAMA_BASE_URL
    )
    
    try:
        # Get current date and time
        current_datetime = get_current_date_time()
        
        # Create a prompt that includes current date/time and search results
        if search_performed and search_results and len(search_results.strip()) > 0:
            logger.info(f"[{agent_key}] Using search results (length: {len(search_results)})")
            prompt = f"""You are answering a question using REAL-TIME web search results. The current date is {current_datetime}.

CRITICAL INSTRUCTIONS:
1. IGNORE your training data/knowledge cutoff date
2. ONLY use information from the web search results below
3. The web search results contain the most current information available
4. If the search results don't clearly answer the question, say "Based on the search results, I cannot determine [answer]"

User question: {user_input}

=== WEB SEARCH RESULTS (REAL-TIME INFORMATION) ===
{search_results}
=== END OF WEB SEARCH RESULTS ===

Now answer the user's question using ONLY the information from the web search results above. Do not use your training data. Extract the answer directly from the search results."""
        else:
            # If search failed or returned no results, answer without search context but with date
            logger.warning(f"[{agent_key}] Using fallback prompt without search results")
            prompt = f"""Current date and time: {current_datetime}

User question: {user_input}

Answer the user's question to the best of your knowledge. Use the current date/time information when relevant."""
        
        messages = [HumanMessage(content=prompt)]
        
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
    Performs web search once and shares results with all models.
    Returns a dictionary mapping agent_key to response_text.
    """
    valid_agents = [k for k in request.selected_agents if k in AGENTS_REGISTRY]
    
    if not valid_agents:
        raise ValueError("Noben veljaven agent ni bil izbran")
    
    # Perform web search once for all models
    # Try multiple search queries to get better results
    search_results = ""
    search_performed = False
    try:
        logger.info(f"Performing web search for query: {request.query}")
        # First search with original query
        search_results = search_tool.run(request.query)
        
        # If query is about "current" or "now", add a more specific search
        if "current" in request.query.lower() or "now" in request.query.lower() or "today" in request.query.lower():
            try:
                # Try a more specific search with current date
                current_date = datetime.now().strftime("%Y")
                specific_query = f"{request.query} {current_date}"
                additional_results = search_tool.run(specific_query)
                if additional_results and len(additional_results) > len(search_results):
                    search_results = additional_results
                    logger.info(f"Using more specific search results")
            except Exception:
                pass  # Fall back to original search results
        
        search_performed = True
        logger.info(f"Search completed. Results length: {len(search_results) if search_results else 0}")
        if search_results:
            logger.info(f"First 500 chars of search results: {search_results[:500]}")
    except Exception as search_error:
        logger.error(f"Web search failed: {str(search_error)}")
        search_results = ""
    
    # Create tasks with shared search results
    tasks = [
        asyncio.create_task(run_model_and_collect(agent, request.query, search_results, search_performed))
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