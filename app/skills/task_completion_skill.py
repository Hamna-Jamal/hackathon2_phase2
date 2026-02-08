from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, func

from app.skills.base_skill import BaseSkill
from app.models.task import Task
from app.logging.logger import app_logger


class TaskCompletionSkill(BaseSkill):
    """
    Skill responsible for completing tasks
    """

    async def execute(self, params: Dict[str, Any]) -> Any:
        """
        Execute the task completion skill
        """
        await app_logger.log_agent_execution(
            agent_name="TaskCompletionSkill",
            action="execute",
            input_data=params,
            output_data={},
            status="processing"
        )

        try:
            task_id = params.get("task_id")
            if not task_id:
                raise ValueError("Task ID is required to complete a task")
                
            # Update the task status to completed and set completed_at timestamp
            stmt = update(Task).where(Task.id == task_id).values(
                status="completed",
                completed_at=func.now()
            )
            result = await self.db.execute(stmt)
            await self.db.commit()

            # Return the updated task if successful
            if result.rowcount > 0:
                # Fetch the updated task
                updated_task = await self.db.get(Task, task_id)
                result = updated_task.to_dict() if updated_task else None
            else:
                result = None

            await app_logger.log_agent_execution(
                agent_name="TaskCompletionSkill",
                action="execute",
                input_data=params,
                output_data=result,
                status="success"
            )
            return result
        except Exception as e:
            await app_logger.log_agent_execution(
                agent_name="TaskCompletionSkill",
                action="execute",
                input_data=params,
                output_data={},
                status="failed",
                error_message=str(e)
            )
            raise