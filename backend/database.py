from sqlalchemy.ext.asyncio import AsyncSession
from config import async_session

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
