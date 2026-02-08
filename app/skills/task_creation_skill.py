from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.skills.base_skill import BaseSkill
from app.models.task import Task
from app.schemas.task import TaskCreate
from app.logging.logger import app_logger


class TaskCreationSkill(BaseSkill):
    """
    Skill responsible for creating tasks
    """

    async def execute(self, params: Dict[str, Any]) -> Any:
        """
        Execute the task creation skill
        """
        await app_logger.log_agent_execution(
            agent_name="TaskCreationSkill",
            action="execute",
            input_data=params,
            output_data={},
            status="processing"
        )

        try:
            # Validate required parameters
            if not params.get("title"):
                raise ValueError("Title is required to create a task")

            # Create task object
            task_create = TaskCreate(
                title=params.get("title"),
                description=params.get("description", ""),
                priority=params.get("priority", "medium"),
                due_date=params.get("due_date")
            )

            # For now, using a placeholder user_id
            # In a real implementation, this would come from the authenticated user
            user_id = params.get("user_id", "12345678-1234-5678-1234-567812345678")  # Placeholder
            db_task = Task(
                user_id=user_id,
                title=task_create.title,
                description=task_create.description,
                status=task_create.status,
                priority=task_create.priority,
                due_date=task_create.due_date
            )

            self.db.add(db_task)
            await self.db.commit()
            await self.db.refresh(db_task)

            result = db_task.to_dict()
            
            await app_logger.log_agent_execution(
                agent_name="TaskCreationSkill",
                action="execute",
                input_data=params,
                output_data=result,
                status="success"
            )
            return result
        except Exception as e:
            await app_logger.log_agent_execution(
                agent_name="TaskCreationSkill",
                action="execute",
                input_data=params,
                output_data={},
                status="failed",
                error_message=str(e)
            )
            raise