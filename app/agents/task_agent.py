from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.base_agent import BaseAgent
from app.skills.task_creation_skill import TaskCreationSkill
from app.skills.task_query_skill import TaskQuerySkill
from app.skills.task_update_skill import TaskUpdateSkill
from app.skills.task_deletion_skill import TaskDeletionSkill
from app.skills.task_completion_skill import TaskCompletionSkill
from app.logging.logger import app_logger


class TaskAgent(BaseAgent):
    """
    Agent responsible for handling task-related operations
    """

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session)
        self.creation_skill = TaskCreationSkill(db_session)
        self.query_skill = TaskQuerySkill(db_session)
        self.update_skill = TaskUpdateSkill(db_session)
        self.deletion_skill = TaskDeletionSkill(db_session)
        self.completion_skill = TaskCompletionSkill(db_session)

    async def execute(self, params: Dict[str, Any]) -> Any:
        """
        Execute the task agent with the given parameters
        """
        action = params.get("action", "unknown")
        await app_logger.log_agent_execution(
            agent_name="TaskAgent",
            action=action,
            input_data=params,
            output_data={},
            status="processing"
        )

        try:
            if action == "create":
                result = await self.creation_skill.execute(params.get("data", {}))
            elif action == "get":
                task_id = params.get("task_id") or params.get("id")
                result = await self.query_skill.execute({"task_id": task_id})
            elif action == "get_all":
                result = await self.query_skill.execute(params)
            elif action == "update":
                result = await self.update_skill.execute(params)
            elif action == "delete":
                result = await self.deletion_skill.execute(params)
            elif action == "complete":
                result = await self.completion_skill.execute(params)
            elif action == "natural_language":
                # Handle natural language commands
                result = await self.handle_natural_language(params.get("command", ""))
            else:
                raise ValueError(f"Unknown action: {action}")

            await app_logger.log_agent_execution(
                agent_name="TaskAgent",
                action=action,
                input_data=params,
                output_data=result,
                status="success"
            )
            return result
        except Exception as e:
            await app_logger.log_agent_execution(
                agent_name="TaskAgent",
                action=action,
                input_data=params,
                output_data={},
                status="failed",
                error_message=str(e)
            )
            raise

    async def handle_natural_language(self, command: str) -> Any:
        """
        Handle natural language commands and convert to appropriate actions
        """
        # This is a simplified implementation
        # In a real application, this would use NLP to parse the command
        command_lower = command.lower()

        if "create" in command_lower or "add" in command_lower:
            # Extract task details from command
            # This is a simplified implementation
            title = command.replace("create", "").replace("add", "").strip()
            if title:
                return await self.creation_skill.execute({"title": title})
            else:
                return {"error": "Could not extract task details from command"}
        elif "list" in command_lower or "show" in command_lower:
            return await self.query_skill.execute({})
        elif "complete" in command_lower or "done" in command_lower:
            # Simplified - assumes the user wants to complete the first task
            # In a real implementation, this would parse the command better
            return {"message": "Complete task command received", "command": command}
        else:
            return {"error": f"Could not understand command: {command}"}