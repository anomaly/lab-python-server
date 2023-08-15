"""Shared utilities for pydantic models

"""
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


def to_lower_camel(name: str) -> str:
    """
    Converts a snake_case string to lowerCamelCase
    """
    upper = "".join(word.capitalize() for word in name.split("_"))
    return upper[:1].lower() + upper[1:]


class AppBaseModel(BaseModel):
    """ Pydantic base model for applications

    This class is used to define the base model for all schema
    that we use in the Application, it configures pydantic to
    translate between camcelCase and snake_case for the JSON
    amongst other default settings.

    populate_by_name will allow pydantic to translate SQLAlchemy 
    results into serializable models, while being able to translate
    the aliases back to the original names when serializing to JSON.

    For a full set of options, see:
    https://pydantic-docs.helpmanual.io/usage/model_config/
    """
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_lower_camel,
    )


class IdentityMixin(BaseModel):
    """ Identifier 

    This mixin is used to define the identifier field for all
    models that use UUID as identifiers, which is out preference
    for PostgreSQL.
    """
    id: UUID


class DateTimeMixin(BaseModel):
    """ Adds timestamps to relevant models

    Many of out models will have a created and updated timestamp
    this mixin will add those fields to the schemas
    """
    created_at: datetime
    updated_at: datetime
