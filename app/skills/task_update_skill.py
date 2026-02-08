from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from app.skills.base_skill import BaseSkill
from app.models.task import Task
from app.logging.logger import app_logger


class TaskUpdateSkill(BaseSkill):
    """
    Skill responsible for updating tasks
    """

    async def execute(self, params: Dict[str, Any]) -> Any:
        """
        Execute the task update skill
        """
        await app_logger.log_agent_execution(
            agent_name="TaskUpdateSkill",
            action="execute",
            input_data=params,
            output_data={},
            status="processing"
        )

        try:
            task_id = params.get("task_id")
            if not task_id:
                raise ValueError("Task ID is required to update a task")
                
            # Prepare update data
            update_data = {}
            if "title" in params:
                update_data["title"] = params["title"]
            if "description" in params:
                update_data["description"] = params["description"]
            if "status" in params:
                update_data["status"] = params["status"]
            if "priority" in params:
                update_data["priority"] = params["priority"]
            if "due_date" in params:
                update_data["due_date"] = params["due_date"]
            if "completed_at" in params:
                update_data["completed_at"] = params["completed_at"]

            # Perform the update
            stmt = update(Task).where(Task.id == task_id).values(**update_data)
            result = await self.db.execute(stmt)
            await self.db.commit()

            # Return the updated task
            if result.rowcount > 0:
                # Fetch the updated task
                updated_task = await self.db.get(Task, task_id)
                result = updated_task.to_dict() if updated_task else None
            else:
                result = None

            await app_logger.log_agent_execution(
                agent_name="TaskUpdateSkill",
                action="execute",
                input_data=params,
                output_data=result,
                status="success"
            )
            return result
        except Exception as e:
            await app_logger.log_agent_execution(
                agent_name="TaskUpdateSkill",
                action="execute",
                input_data=params,
                output_data={},
                status="failed",
                error_message=str(e)
            )
            raise