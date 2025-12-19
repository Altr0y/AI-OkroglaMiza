from fastapi import APIRouter
from pydantic import BaseModel
from agents import loaded_agents, AGENT_CONFIGS

router = APIRouter(tags=["AI Agenti"])

class MultiChatRequest(BaseModel):
    agent_ids: list[str]
    prompt: str

@router.get("/list-agents")
async def list_agents():
    """Vrne seznam vseh razpoložljivih agentov."""
    return AGENT_CONFIGS

@router.post("/chat")
async def chat(req: MultiChatRequest):
    """Pošlje vprašanje izbranim agentom in vrne njihove odgovore."""
    responses = {}
    for aid in req.agent_ids:
        if aid in loaded_agents:
            agent = loaded_agents[aid]
            sys_prompt = next((cfg.get("default_system", "") for cfg in AGENT_CONFIGS if cfg["id"] == aid), "")
            responses[aid] = {
                "name": agent.name,
                "text": agent.generate(req.prompt, sys_prompt)
            }
        else:
            responses[aid] = {"error": "Agent ni naložen."}
    return responses