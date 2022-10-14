"""SQLAlchemy context

  This database configuration is configured using asyncio
  https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html


"""

import asyncio
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, configure_mappers, sessionmaker

from .config import config

# SQLAlchemy engine that connects to Postgres
engine = create_async_engine(config.postgres_async_dsn, echo=True)
configure_mappers()

# Get an async session from the engine
async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

# Used by the ORM layer to describe models
Base = declarative_base()

async def init_models():
    """Initialises the models in the database

    References:
    https://stribny.name/blog/fastapi-asyncalchemy/
    """
    import logging
    logging.info("Initialising models")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# TODO: Revise implementation in async context
# Donot use until we have a better understanding of how to use async context
# @asynccontextmanager
# async def session_context():
#     """Provide a transactional scope around a series of operations.
#     """
#     try:
#         yield async_session
#         await async_session.commit()
#     except:  # noqa: E722
#         await async_session.rollback()
#         raise
#     finally:
#         await async_session.close()
