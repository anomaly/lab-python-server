"""Routers for the API

Aggregates all the sub-routers for the API. This is ultimately used
by the top level FastAPI application.

"""

from .ext import router as router_ext