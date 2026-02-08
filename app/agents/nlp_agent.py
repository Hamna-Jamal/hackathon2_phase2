from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
import re

from app.agents.base_agent import BaseAgent
from app.skills.task_creation_skill import TaskCreationSkill
from app.skills.task_query_skill import TaskQuerySkill
from app.skills.task_update_skill import TaskUpdateSkill
from app.skills.task_deletion_skill import TaskDeletionSkill
from app.skills.task_completion_skill import TaskCompletionSkill
from app.logging.logger import app_logger


class NLPAgent(BaseAgent):
    """
    Natural Language Processing Agent that interprets human language commands
    """

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session)
        self.creation_skill = TaskCreationSkill(db_session)
        self.query_skill = TaskQuerySkill(db_session)
        self.update_skill = TaskUpdateSkill(db_session)
        self.deletion_skill = TaskDeletionSkill(db_session)
        self.completion_skill = TaskCompletionSkill(db_session)

        # Define patterns for different types of commands
        self.patterns = {
            'create': [
                r'create task "(.+)"',
                r'add task "(.+)"',
                r'make task "(.+)"',
                r'new task "(.+)"'
            ],
            'list': [
                r'list tasks',
                r'show tasks',
                r'view tasks',
                r'all tasks'
            ],
            'complete': [
                r'complete task (\d+)',
                r'finish task (\d+)',
                r'mark task (\d+) as complete',
                r'done with task (\d+)'
            ]
        }

    async def execute(self, params: Dict[str, Any]) -> Any:
        """
        Execute the NLP agent with the given parameters
        """
        command = params.get("command", "")
        if not command:
            return {"error": "No command provided"}

        await app_logger.log_agent_execution(
            agent_name="NLPAgent",
            action="parse_command",
            input_data=params,
            output_data={},
            status="processing"
        )

        try:
            # Parse the command to determine the action
            parsed_command = self.parse_command(command)

            if parsed_command["action"] == "create":
                result = await self.handle_create(parsed_command)
            elif parsed_command["action"] == "list":
                result = await self.handle_list(parsed_command)
            elif parsed_command["action"] == "complete":
                result = await self.handle_complete(parsed_command)
            else:
                result = {"error": f"Could not understand command: {command}"}

            await app_logger.log_agent_execution(
                agent_name="NLPAgent",
                action=parsed_command["action"],
                input_data=params,
                output_data=result,
                status="success"
            )
            return result
        except Exception as e:
            await app_logger.log_agent_execution(
                agent_name="NLPAgent",
                action="error",
                input_data=params,
                output_data={},
                status="failed",
                error_message=str(e)
            )
            raise

    def parse_command(self, command: str) -> Dict[str, Any]:
        """
        Parse a natural language command and return structured data
        """
        command_lower = command.lower().strip()

        # Check for create patterns
        for pattern in self.patterns['create']:
            match = re.search(pattern, command_lower)
            if match:
                return {
                    "action": "create",
                    "title": match.group(1)
                }

        # Check for list patterns
        for pattern in self.patterns['list']:
            if re.search(pattern, command_lower):
                return {
                    "action": "list"
                }

        # Check for complete patterns
        for pattern in self.patterns['complete']:
            match = re.search(pattern, command_lower)
            if match:
                return {
                    "action": "complete",
                    "task_id": match.group(1)
                }

        # If no pattern matches, return unknown
        return {
            "action": "unknown",
            "original_command": command
        }

    async def handle_create(self, parsed_command: Dict[str, Any]) -> Any:
        """
        Handle a create task command
        """
        title = parsed_command.get("title", "")
        if not title:
            return {"error": "Could not extract task title from command"}

        # Create the task using the skill
        result = await self.creation_skill.execute({
            "title": title,
            "description": "",
            "priority": "medium"
        })

        return {
            "action": "create",
            "result": result,
            "message": f"Created task: {title}"
        }

    async def handle_list(self, parsed_command: Dict[str, Any]) -> Any:
        """
        Handle a list tasks command
        """
        # Get all tasks using the query skill
        result = await self.query_skill.execute({})

        return {
            "action": "list",
            "result": result,
            "message": f"Found {len(result)} tasks" if isinstance(result, list) else "Retrieved tasks"
        }

    async def handle_complete(self, parsed_command: Dict[str, Any]) -> Any:
        """
        Handle a complete task command
        """
        task_id = parsed_command.get("task_id")
        if not task_id:
            return {"error": "Could not extract task ID from command"}

        # Complete the task using the completion skill
        result = await self.completion_skill.execute({"task_id": task_id})

        if result:
            return {
                "action": "complete",
                "result": result,
                "message": f"Completed task {task_id}"
            }
        else:
            return {
                "action": "complete",
                "error": f"Could not find task with ID {task_id}"
            }