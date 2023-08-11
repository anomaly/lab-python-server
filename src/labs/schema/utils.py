"""Shared utilities for pydantic models

"""
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict
from humps import camelize


class AppBaseModel(BaseModel):
    """ Pydantic base model for applications

    This class is used to define the base model for all schema
    that we use in the Application, it configures pydantic to
    translate between camcelCase and snake_case for the JSON
    amongst other default settings.

    from_attributes will allow pydantic to translate SQLAlchemy results
    into serializable models.

    For a full set of options, see:
    https://pydantic-docs.helpmanual.io/usage/model_config/
    """
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=camelize,
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
