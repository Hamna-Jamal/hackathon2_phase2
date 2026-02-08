from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.skills.task_creation_skill import TaskCreationSkill
from app.skills.task_query_skill import TaskQuerySkill
from app.skills.task_update_skill import TaskUpdateSkill
from app.skills.task_deletion_skill import TaskDeletionSkill


class TaskService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.creation_skill = TaskCreationSkill(db_session)
        self.query_skill = TaskQuerySkill(db_session)
        self.update_skill = TaskUpdateSkill(db_session)
        self.deletion_skill = TaskDeletionSkill(db_session)

    async def create_task(self, task_create: TaskCreate) -> TaskResponse:
        """
        Create a new task using the creation skill
        """
        # Convert Pydantic model to dict for the skill
        task_data = task_create.model_dump()
        task_data["user_id"] = str(UUID("12345678-1234-5678-1234-567812345678"))  # Placeholder

        result = await self.creation_skill.execute(task_data)
        return TaskResponse(**result)

    async def get_tasks(
        self,
        skip: int = 0,
        limit: int = 100,
        status_filter: Optional[str] = None,
        priority: Optional[str] = None
    ) -> List[TaskResponse]:
        """
        Retrieve tasks using the query skill
        """
        params = {
            "skip": skip,
            "limit": limit,
            "status_filter": status_filter,
            "priority": priority
        }

        results = await self.query_skill.execute(params)
        return [TaskResponse(**task_dict) for task_dict in results]

    async def get_task_by_id(self, task_id: UUID) -> Optional[TaskResponse]:
        """
        Retrieve a specific task by ID using the query skill
        """
        params = {"task_id": str(task_id)}
        result = await self.query_skill.execute(params)

        if result:
            return TaskResponse(**result)
        return None

    async def update_task(self, task_id: UUID, task_update: TaskUpdate) -> Optional[TaskResponse]:
        """
        Update a specific task by ID using the update skill
        """
        # Prepare update data
        update_data = task_update.model_dump(exclude_unset=True)
        update_data["task_id"] = str(task_id)

        result = await self.update_skill.execute(update_data)

        if result:
            return TaskResponse(**result)
        return None

    async def delete_task(self, task_id: UUID) -> bool:
        """
        Delete a specific task by ID using the deletion skill
        """
        params = {"task_id": str(task_id)}
        return await self.deletion_skill.execute(params)