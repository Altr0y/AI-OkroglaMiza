#Chat: Ko uporabnik v frontendu klikne "Pošlji", React pošlje zahtevo na http://localhost:8000/api/round-table (ai.py).

import asyncio
import json
import uvicorn
from typing import List
from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_community.chat_models import ChatOllama
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

async def run_model_and_enqueue(agent_key, user_input, queue):
  
    model_id = AGENTS_REGISTRY[agent_key]
    
    llm = ChatOllama(model=model_id, temperature=0.7)
    
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

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)