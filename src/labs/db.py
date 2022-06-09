"""SQLAlchemy context

  This database configuration is configured using asyncio
  https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html


"""

import asyncio
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base

from .config import config


Base = declarative_base()

# SQLAlchemy engine that connects to Postgres
engine = create_async_engine(config.postgres_async_dsn, echo=True)
# Get an async session from the engine
async_session = AsyncSession(engine, expire_on_commit=False)

@asynccontextmanager
async def session_context():
    """Provide a transactional scope around a series of operations.
    """
    session = async_session()
    try:
        yield session
        await session.commit()
    except:  # noqa: E722
        await session.rollback()
        raise
    finally:
        await session.close()
