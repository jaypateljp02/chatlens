from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings

# For now, if we use SQLite, we use standard sync sqlite or async sqlite.
# The user specified SQLite as a fallback. 
# We'll set up SQLAlchemy async engine. If it's sqlite, it should be sqlite+aiosqlite.
# But for phase 1, we won't fully implement the DB logic yet, just the connection setup.

db_url = settings.DATABASE_URL
if db_url.startswith("sqlite:///"):
    # SQLAlchemy requires aiosqlite for async sqlite
    db_url = db_url.replace("sqlite:///", "sqlite+aiosqlite:///")

engine = create_async_engine(db_url, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session
