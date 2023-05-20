"""SQLAlchemy context

  This database configuration is configured using asyncio
  https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html


"""

from sqlalchemy.ext.asyncio import create_async_engine,\
    AsyncSession
from sqlalchemy.orm import DeclarativeBase,\
    configure_mappers, sessionmaker


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
class Base(DeclarativeBase):
    """
    SQLAlchemy 2.0 style declarative base class
    https://bit.ly/3WE3Srg
    """
    pass


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


def initialise():
    """ Async IO containers to run the init_models function

    This is called from the command line via poetry scripts.

    Note: while import the models package seems useless, it is
    infact crucial that the models are in context before the
    create_all is called, otherwise the context has no models
    defined and none will be created.    
    """
    import asyncio
    from . import models
    asyncio.run(init_models())

