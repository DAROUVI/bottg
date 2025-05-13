# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

DATABASE_URL = os.getenv("postgresql://${{PGUSER}}:${{POSTGRES_PASSWORD}}@${{RAILWAY_PRIVATE_DOMAIN}}:5432/${{PGDATABASE}}").replace("postgresql://", "postgresql+psycopg2://")

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