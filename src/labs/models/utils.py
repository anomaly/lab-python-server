"""A package that provides utilities shared by models

    The reason was housing them in utils is to avoid circular
    depdendencies.

"""

from sqlalchemy import Column, DateTime, ForeignKey, text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update,\
    delete as sqlalchemy_delete

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
            ForeignKey("core.user.id"),
            nullable=False)

    @declared_attr
    def last_updated_by_user_id(cls):
        return Column(UUID(as_uuid=True),
            ForeignKey("core.user.id"),
            nullable=False)


class ModelCRUDMixin:
    """
    A CRUD Mixin designed to abstract CRUD operations for all
    SQLAlchemy defined models.

    Adapted from the work of Ahmed Nafies:
    - https://bit.ly/3coTT7j
    - https://bit.ly/3OmhtPw
    """
    @classmethod
    async def create(cls, **kwargs):
        async_db_session.add(cls(**kwargs))
        await async_db_session.commit()

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )

        await async_db_session.execute(query)
        await async_db_session.commit()

    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.id == id)
        results = await async_db_session.execute(query)
        (result,) = results.one()
        return result

    @classmethod
    async def get_all(cls):
        query = select(cls)
        users = await db.execute(query)
        users = users.scalars().all()
        return users

    @classmethod
    async def delete(cls, id):
        query = sqlalchemy_delete(cls).where(cls.id == id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True