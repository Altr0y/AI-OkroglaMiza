#Chat: Ko uporabnik v frontendu klikne "Pošlji", React pošlje zahtevo na http://localhost:8000/api/round-table (ai.py).

import asyncio
import json
import uvicorn

import os
import time
import logging
from collections import defaultdict

from typing import List
from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

app = FastAPI()

AGENTS_REGISTRY = {
    "qwen": "qwen3:4b",
    "ministral": "ministral-3:3b",
    "deepseek": "deepseek-r1:1.5b"
}

class ChatRequest(BaseModel):
    query: str
    selected_agents: List[str]

async def run_model_and_enqueue(agent_key: str, user_input: str, queue: asyncio.Queue):
    model_id = AGENTS_REGISTRY[agent_key]
    
    llm = ChatOllama(
        model=model_id,
        temperature=0.7,
        base_url="http://127.0.0.1:11434" 
    )
    
    messages = [HumanMessage(content=user_input)]
    
    try:
        async for chunk in llm.astream(messages):
            await queue.put({
                "agent_key": agent_key,
                "content": chunk.content,
                "done": False
            })
    except Exception as e:
        await queue.put({
            "agent_key": agent_key,
            "content": f"\nNapaka pri modelu {model_id}: {str(e)}",
            "done": False
        })
    
    await queue.put({"agent_key": agent_key, "done": True})

async def stream_manager(request: ChatRequest):
    queue = asyncio.Queue()
    
    valid_agents = [k for k in request.selected_agents if k in AGENTS_REGISTRY]
    
    if not valid_agents:
        yield f"data: {json.dumps({'error': 'Noben veljaven agent ni bil izbran'})}\n\n"
        return

    tasks = [
        asyncio.create_task(run_model_and_enqueue(agent, request.query, queue))
        for agent in valid_agents
    ]
    
    active_agents = len(tasks)
    
    while active_agents > 0:
        item = await queue.get()
        if item.get("done") is True:
            active_agents -= 1
        else:
            yield f"data: {json.dumps(item)}\n\n"
            
    yield "data: [DONE]\n\n"

@app.post("/api/round-table")
async def chat_endpoint(request: ChatRequest = Body(...)):
    return StreamingResponse(stream_manager(request), media_type="text/event-stream")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

INTERNAL_API_TOKEN = os.getenv("INTERNAL_API_TOKEN", "dev-secret")

RATE_LIMIT = 10
WINDOW = 60
_request_log = defaultdict(list)

MAX_QUERY_LEN = 1000
MAX_AGENTS = 3

@app.middleware("http")
async def security_middleware(request: Request, call_next):
    if request.url.path == "/api/round-table":
        ip = request.client.host
        now = time.time()

        token = request.headers.get("X-Internal-Token")
        if token != INTERNAL_API_TOKEN:
            logging.warning(f"Forbidden request from {ip}")
            raise HTTPException(status_code=403, detail="Forbidden")

        _request_log[ip] = [t for t in _request_log[ip] if now - t < WINDOW]
        if len(_request_log[ip]) >= RATE_LIMIT:
            logging.warning(f"Rate limit exceeded from {ip}")
            raise HTTPException(status_code=429, detail="Too many requests")
        _request_log[ip].append(now)

        body = await request.json()
        query = body.get("query", "")
        agents = body.get("selected_agents", [])

        if len(query) > MAX_QUERY_LEN:
            raise HTTPException(status_code=400, detail="Query too long")

        if len(agents) > MAX_AGENTS:
            raise HTTPException(status_code=400, detail="Too many agents")

        logging.info(f"AI request from {ip} with {len(agents)} agents")

    return await call_next(request)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)