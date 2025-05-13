import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, select

# Правильное получение DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Заменяем протокол для asyncpg
DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Добавляем sslmode при необходимости (для Railway)
if "railway" in DATABASE_URL:
    DATABASE_URL += "?sslmode=require"

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class Link(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True)
    url = Column(String(500), nullable=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def save_link(url: str):
    async with AsyncSessionLocal() as session:
        link = Link(url=url)
        session.add(link)
        await session.commit()

async def get_links(limit: int = 10):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Link).order_by(Link.id.desc()).limit(limit))
        return result.scalars().all()