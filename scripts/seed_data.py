import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.user import User
from app.models.task import Task
from app.models.agent_log import AgentLog
import uuid
from datetime import datetime, timedelta


async def seed_database():
    """
    Seed the database with sample data
    """
    # Create async engine
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Create a sample user
        user_id = uuid.uuid4()
        sample_user = User(
            id=user_id,
            email="sample@example.com"
        )
        session.add(sample_user)
        
        # Create sample tasks
        sample_tasks = [
            Task(
                id=uuid.uuid4(),
                user_id=user_id,
                title="Complete project proposal",
                description="Finish the project proposal document and submit to stakeholders",
                status="todo",
                priority="high",
                due_date=datetime.utcnow() + timedelta(days=3)
            ),
            Task(
                id=uuid.uuid4(),
                user_id=user_id,
                title="Review code changes",
                description="Review the pull request for the new feature implementation",
                status="in_progress",
                priority="medium",
                due_date=datetime.utcnow() + timedelta(days=1)
            ),
            Task(
                id=uuid.uuid4(),
                user_id=user_id,
                title="Team meeting",
                description="Attend weekly team sync meeting",
                status="completed",
                priority="low",
                completed_at=datetime.utcnow() - timedelta(hours=2)
            ),
            Task(
                id=uuid.uuid4(),
                user_id=user_id,
                title="Research new technologies",
                description="Look into new frameworks for the upcoming project",
                status="todo",
                priority="medium",
                due_date=datetime.utcnow() + timedelta(days=7)
            )
        ]
        
        session.add_all(sample_tasks)
        
        # Create sample agent logs
        sample_logs = [
            AgentLog(
                id=uuid.uuid4(),
                agent_name="TaskAgent",
                task_id=sample_tasks[0].id,
                user_id=user_id,
                action="create_task",
                status="success",
                input_data={"title": "Complete project proposal", "priority": "high"},
                output_data={"id": str(sample_tasks[0].id), "status": "created"}
            ),
            AgentLog(
                id=uuid.uuid4(),
                agent_name="NLPAgent",
                task_id=sample_tasks[1].id,
                user_id=user_id,
                action="natural_language_command",
                status="success",
                input_data={"command": "create task 'Review code changes'"},
                output_data={"result": "Task created successfully"}
            )
        ]
        
        session.add_all(sample_logs)
        
        await session.commit()
    
    print("Database seeded with sample data successfully!")


if __name__ == "__main__":
    asyncio.run(seed_database())