from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
ALLOWED_ORIGINS = ["http://localhost:3000"]

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# CORS Middleware setup
def get_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
