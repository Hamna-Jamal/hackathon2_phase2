from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from app.skills.base_skill import BaseSkill
from app.models.task import Task
from app.logging.logger import app_logger


class TaskDeletionSkill(BaseSkill):
    """
    Skill responsible for deleting tasks
    """

    async def execute(self, params: Dict[str, Any]) -> bool:
        """
        Execute the task deletion skill
        """
        await app_logger.log_agent_execution(
            agent_name="TaskDeletionSkill",
            action="execute",
            input_data=params,
            output_data={},
            status="processing"
        )

        try:
            task_id = params.get("task_id")
            if not task_id:
                raise ValueError("Task ID is required to delete a task")
                
            stmt = delete(Task).where(Task.id == task_id)
            result = await self.db.execute(stmt)
            await self.db.commit()
            
            success = result.rowcount > 0
            
            await app_logger.log_agent_execution(
                agent_name="TaskDeletionSkill",
                action="execute",
                input_data=params,
                output_data={"success": success},
                status="success"
            )
            return success
        except Exception as e:
            await app_logger.log_agent_execution(
                agent_name="TaskDeletionSkill",
                action="execute",
                input_data=params,
                output_data={},
                status="failed",
                error_message=str(e)
            )
            raise