"""A package that provides utilities shared by models

    The reason was housing them in utils is to avoid circular
    depdendencies.

"""

from sqlalchemy import Column, DateTime, text
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
