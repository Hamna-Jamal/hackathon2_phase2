from pydantic import BaseModel
from typing import Any, Dict, Optional


class AgentRunRequest(BaseModel):
    agent_name: str
    params: Dict[str, Any]


class AgentRunResponse(BaseModel):
    result: Any
    success: bool
    message: Optional[str] = None