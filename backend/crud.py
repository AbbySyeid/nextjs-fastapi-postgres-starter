from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Message, User

async def get_messages(db: AsyncSession):
    result = await db.execute(select(Message).order_by(Message.id))
    return result.scalars().all()

async def create_message(db: AsyncSession, user_id: int, content: str):
    new_message = Message(user_id=user_id, content=content)
    db.add(new_message)
    return new_message

def generate_bot_response(user_message: str) -> str:
    return f"{user_message[::-1]}"
