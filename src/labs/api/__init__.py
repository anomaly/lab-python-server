"""API backend

  The package provides the main application programmer interface (API) that
  the clients (web or otherwise) will use to interact with the application.

  The end points will depend on database models defined by the core package, 
  most requests will be synchronous and will return a JSON response. Others
  will schedule tasks that are dealt with by the background workers (see worker).

  API endpoints are built and served using the FastAPI micro-framework.

"""
__name__ = "Labs"
__version__ = "0.0.1"

from fastapi import FastAPI

from .routers import router as router_misc

"""A FastAPI application that serves handlers
"""
app = FastAPI(
    title=__name__,
    root_path="/api",
    docs_url="/docs",
    openapi_tags=["misc"],
    )

app.include_router(router_misc, prefix="/misc")