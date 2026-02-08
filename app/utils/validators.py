from typing import Optional
from pydantic import BaseModel, validator
from app.models.task import Task


class TaskValidator:
    """
    Utility class for task validation
    """
    
    @staticmethod
    def validate_title(title: str) -> bool:
        """
        Validate task title
        """
        if not title or len(title.strip()) == 0:
            return False
        if len(title) > 255:
            return False
        return True
    
    @staticmethod
    def validate_status(status: str) -> bool:
        """
        Validate task status
        """
        valid_statuses = ["todo", "in_progress", "completed"]
        return status in valid_statuses
    
    @staticmethod
    def validate_priority(priority: str) -> bool:
        """
        Validate task priority
        """
        valid_priorities = ["low", "medium", "high"]
        return priority in valid_priorities


class UserValidator:
    """
    Utility class for user validation
    """
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None