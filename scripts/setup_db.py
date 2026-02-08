import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.models.user import User
from app.models.task import Task
from app.models.agent_log import AgentLog
from app.database.base import Base


async def setup_database():
    """
    Set up the database tables
    """
    # Create async engine
    engine = create_async_engine(settings.DATABASE_URL)
    
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    print("Database setup completed successfully!")


if __name__ == "__main__":
    asyncio.run(setup_database())