from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_

from app.skills.base_skill import BaseSkill
from app.models.task import Task
from app.logging.logger import app_logger


class TaskQuerySkill(BaseSkill):
    """
    Skill responsible for querying tasks
    """

    async def execute(self, params: Dict[str, Any]) -> Any:
        """
        Execute the task query skill - can handle both single task and list queries
        """
        await app_logger.log_agent_execution(
            agent_name="TaskQuerySkill",
            action="execute",
            input_data=params,
            output_data={},
            status="processing"
        )

        try:
            task_id = params.get("task_id")
            if task_id:
                # Query for a specific task
                query = select(Task).where(Task.id == task_id)
                result = await self.db.execute(query)
                task = result.scalar_one_or_none()

                result = task.to_dict() if task else None
            else:
                # Query for multiple tasks
                skip = params.get("skip", 0)
                limit = params.get("limit", 100)
                status_filter = params.get("status_filter")
                priority = params.get("priority")

                query = select(Task)

                # Apply filters if provided
                conditions = []
                if status_filter:
                    conditions.append(Task.status == status_filter)
                if priority:
                    conditions.append(Task.priority == priority)

                if conditions:
                    query = query.where(and_(*conditions))

                # Apply pagination
                query = query.offset(skip).limit(limit)

                result = await self.db.execute(query)
                tasks = result.scalars().all()

                result = [task.to_dict() for task in tasks]

            await app_logger.log_agent_execution(
                agent_name="TaskQuerySkill",
                action="execute",
                input_data=params,
                output_data=result,
                status="success"
            )
            return result
        except Exception as e:
            await app_logger.log_agent_execution(
                agent_name="TaskQuerySkill",
                action="execute",
                input_data=params,
                output_data={},
                status="failed",
                error_message=str(e)
            )
            raise