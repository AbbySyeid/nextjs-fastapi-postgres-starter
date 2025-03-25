from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from config import engine, get_cors_middleware
from crud import create_message, get_messages, generate_bot_response
from models import User
from sqlalchemy.future import select
from database import get_session
from seed import seed_user_if_needed, seed_bot_if_needed

seed_bot_if_needed()
seed_user_if_needed()

app = FastAPI()

get_cors_middleware(app)

class MessageCreate(BaseModel):
    user_id: int
    content: str

class MessageRead(BaseModel):
    id: int
    user_id: int
    content: str

@app.post("/messages/", response_model=MessageCreate)
async def send_message(message: MessageCreate):
    async for session in get_session():
        async with session.begin():
            new_message = await create_message(session, message.user_id, message.content)
            bot_response = generate_bot_response(new_message.content)
            await create_message(session, message.user_id - 1, bot_response)
            return {"user_id": message.user_id, "content": message.content}

@app.get("/messages/", response_model=list[MessageRead])
async def get_all_messages():
    message_data = []
    async for session in get_session():
        async with session.begin():
            messages = await get_messages(session)
            for message in messages:
                message_data.append({"id": message.id, "user_id": message.user_id, "content": message.content})
            return message_data

@app.get("/users/me")
async def get_my_user():
    async for session in get_session():
        async with session.begin():
            result = await session.execute(select(User).order_by(User.id.desc()))
            user = result.scalars().first()
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return {"id": user.id, "name": user.name}
