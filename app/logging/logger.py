import logging
from datetime import datetime
from typing import Any, Dict
from app.models.agent_log import AgentLog
from app.database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from contextlib import asynccontextmanager


class Logger:
    """
    Custom logger for the application with database logging
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    async def log_agent_execution(
        self,
        agent_name: str,
        action: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        status: str = "success",
        error_message: str = None,
        task_id: str = None,
        user_id: str = None
    ):
        """
        Log agent execution to the database
        """
        # Get a database session from the dependency
        async for session in get_db():
            agent_log = AgentLog(
                agent_name=agent_name,
                action=action,
                input_data=input_data,
                output_data=output_data,
                status=status,
                error_message=error_message,
                task_id=task_id,
                user_id=user_id
            )
            session.add(agent_log)
            await session.commit()
            break  # Only get one session from the generator

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def debug(self, message: str):
        self.logger.debug(message)


# Global logger instance
app_logger = Logger()