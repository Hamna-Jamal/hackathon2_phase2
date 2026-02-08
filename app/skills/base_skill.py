from abc import ABC, abstractmethod
from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession


class BaseSkill(ABC):
    """
    Abstract base class for all skills
    """
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    @abstractmethod
    async def execute(self, params: Dict[str, Any]) -> Any:
        """
        Execute the skill with the given parameters
        """
        pass