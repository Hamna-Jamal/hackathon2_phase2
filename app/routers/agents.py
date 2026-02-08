from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.agent import AgentRunRequest, AgentRunResponse
from app.agents.task_agent import TaskAgent
from app.agents.nlp_agent import NLPAgent

router = APIRouter()


@router.post("/agent/run", response_model=AgentRunResponse)
async def run_agent(
    request: AgentRunRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Execute an AI agent with specified parameters
    """
    try:
        # Initialize the appropriate agent based on the request
        if request.agent_name == "task_agent":
            agent = TaskAgent(db)
        elif request.agent_name == "nlp_agent":
            agent = NLPAgent(db)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown agent: {request.agent_name}"
            )
        
        # Execute the agent
        result = await agent.execute(request.params)
        
        return AgentRunResponse(
            result=result,
            success=True
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing agent: {str(e)}"
        )