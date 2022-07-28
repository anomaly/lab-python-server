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

from passlib.context import CryptContext

# Password hashing and validation helpers

# The following should not be called directly
_pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def verify_password(plain_password, hashed_password) -> bool:
    return _pwd_context.verify(
        plain_password,
        hashed_password
    )

def hash_password(password) -> str:
    return _pwd_context.hash(password)

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
            ForeignKey("user.user.id"),
            nullable=False)

    @declared_attr
    def last_updated_by_user_id(cls):
        return Column(UUID(as_uuid=True),
            ForeignKey("user.user.id"),
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
    async def create(cls, async_db_session, **kwargs):
        new_instance = cls(**kwargs)
        async_db_session.add(new_instance)
        await async_db_session.commit()
        async_db_session.refresh(new_instance) # Ensure we get the id
        return new_instance

    @classmethod
    async def update(cls, async_db_session, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )

        await async_db_session.execute(query)
        await async_db_session.commit()

    @classmethod
    async def get(cls, async_db_session, id):
        query = select(cls).where(cls.id == id)
        results = await async_db_session.execute(query)
        (result,) = results.one()
        return result

    @classmethod
    async def get_all(cls, async_db_session):
        query = select(cls)
        users = await async_db_session.execute(query)
        users = users.scalars().all()
        return users

    @classmethod
    async def delete(cls, async_db_session, id):
        query = sqlalchemy_delete(cls).where(cls.id == id)
        await async_db_session.execute(query)
        try:
            await async_db_session.commit()
        except Exception:
            await async_db_session.rollback()
            raise
        return True


