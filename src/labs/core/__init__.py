"""Core package for the application.

  This package contains components that are shared across the application, e.g:
    - Database model definitions
    - Pydantic model definitions
    - Database context (async) configured to speak to Postgres
    - Background worker infrastructure

  Both the worker and API should depend on what's defined in core and the changes
  made to this package should fundamentally affect the application e.g add a model.

"""
__version__ = "0.1.0"

