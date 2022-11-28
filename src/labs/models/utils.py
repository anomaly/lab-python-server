"""A package that provides utilities shared by models

    The reason was housing them in utils is to avoid circular
    depdendencies.

"""

from sqlalchemy import Column, DateTime, ForeignKey, text,\
    update as sqlalchemy_update,\
    delete as sqlalchemy_delete
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import UUID

class IdentifierMixin(object):
    """An ID for a given object

    We primarily use Postgres for our project and lean on using the UUID
    field as identifiers, this sits closer to modern software engineering
    techniques.
    """
    id = Column(UUID(as_uuid=True),
        doc="The ID of the object",
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        nullable=False,
    )
class DateTimeMixin(object):
    """Stores creation and update timestamps

    Each object should know when they were created or updated, these fields
    do not intend to keep historical logs of the object.

    Both fields use SQLAlchemy hooks to populate a value on creation
    and when the object is update, you will not be required to set these
    values manually.
    """
    created_at = Column(DateTime(timezone=True),
        doc="The date and time the object was created",
        server_default=text("now()"),
        nullable=False
    )

    updated_at = Column(DateTime(timezone=True),
        doc="The date and time the object was updated",
        server_default=text("now()"),
        onupdate=text("now()"),
        nullable=False,
    )

class CreatedByMixin(object):
    """ Adds references to created_by and updated_by users

    """
    @declared_attr
    def created_by_user_id(cls):
        return Column(UUID(as_uuid=True),
            ForeignKey("user.id"),
            nullable=False)

    @declared_attr
    def last_updated_by_user_id(cls):
        return Column(UUID(as_uuid=True),
            ForeignKey("user.id"),
            nullable=False)

class ModelCRUDMixin:
    """
    A CRUD Mixin designed to abstract CRUD operations for all
    SQLAlchemy defined models.

    Adapted from the work of Ahmed Nafies:
    - https://bit.ly/3coTT7j
    - https://bit.ly/3OmhtPw

    The aim is to assist in CRUD operations for all models, including
    generic filter, sort and pagination (also includes infinite scroll).

    Pay special attention to the `get` methods, this is the method that
    which use a base builder to construct v2.0 style queries for 
    SQLAlchemy.
    """
    @classmethod
    async def create(
        cls,
        async_db_session,
        **kwargs
    ):
        """ Create a new record and save it the database.

        This is a generic call that takes an async session and
        keyvalue pairs to create a new record in the database.
        """
        new_instance = cls(**kwargs)
        async_db_session.add(new_instance)
        await async_db_session.commit()
        await async_db_session.refresh(new_instance) # Ensure we get the id
        return new_instance

    @classmethod
    async def update(
        cls,
        async_db_session,
        id,
        **kwargs
    ):
        """ Update a record and save it the database.

        This is a generic call that takes an async session and
        keyvalue pairs to update a record in the database.
        """
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )

        await async_db_session.execute(query)
        await async_db_session.commit()

    @classmethod
    async def delete(
        cls,
        async_db_session,
        id
    ):
        """ Delete a record from the database by ID
        """
        query = sqlalchemy_delete(cls).where(cls.id == id)
        await async_db_session.execute(query)
        try:
            await async_db_session.commit()
        except Exception:
            await async_db_session.rollback()
            raise
        return True

    # Helper patterns to make loaders easier to work with
    # when using asyncpg

    @classmethod
    def _base_get_query(cls):
        """
        asyncpg does not support joineload, so we have to selectinload
        any relationships we want to load.

        An example would be loading products and prices of a catalogue
        query = select(cls).options(
            selectinload(cls.products).\
            selectinload(Product.prices)\
        ).\
        where(cls.id == id)

        The default query does not load any relationships, this should
        be overridden by each class to load the relationships they need.

        All getters then inturn call this method to get the base query
        and apply any clauses, orders etc.

        This also means that we can maintain the selectinload pattern
        in one spot.

        All sqlalchemy query methods are factories, so you can chain
        call one on top of the other, e.g:

        query = cls._base_get_query()
        query = query.offset(offset).limit(limit)

        Note: this is not an async call as it does nothing async.
        """
        query = select(cls).options()
        return query

    @classmethod
    async def get(
        cls,
        async_db_session,
        id
    ):
        """ Get a single record from the database by ID

        uses _base_get_query to construct a select statement
        and filters by id        
        """
        query = cls._base_get_query().where(cls.id == id)
        try:
            results = await async_db_session.execute(query)
            (result,) = results.one()
            return result
        except Exception:
            return None

    @classmethod
    async def get_all_in_range(
        cls,
        async_db_session,
        offset: int = 0,
        limit: int = 100,
    ):
        """ Get records with limit and offset

        This is a more useful version of getting blocks of records
        that are in a range.
        """
        query = cls._base_get_query()
        query = query.limit(limit).offset(offset)
        users = await async_db_session.execute(query)
        users = users.scalars().all()
        return users


    @classmethod
    async def get_all(
        cls,
        async_db_session
    ):
        """ Get all records for a table

        There should be very few use cases where this applicable,
        for most use cases this would be a very expensive call.

        Please consider the design of your application if you
        require to use this too often.
        """
        query = cls._base_get_query()
        users = await async_db_session.execute(query)
        users = users.scalars().all()
        return users
