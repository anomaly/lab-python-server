"""API backend

  The package provides the main application programmer interface (API) that
  the clients (web or otherwise) will use to interact with the application.

  The end points will depend on database models defined by the core package, 
  most requests will be synchronous and will return a JSON response. Others
  will schedule tasks that are dealt with by the background workers (see worker).

  API endpoints are built and served using the FastAPI micro-framework.

"""
from .. import __title__, __version__
from fastapi import FastAPI, Request

from .routers import router_ext

"""A FastAPI application that serves handlers
"""
app = FastAPI(
    title=__title__,
    version=__version__,
    description="Sample API",
    docs_url="/docs",
    terms_of_service="https://github.com/anomaly/labs",
    contact={
      "name": "Anomaly Software",
      "url": "https://github.com/anomaly/labs",
      "email": "oss@anomaly.ltd"
    },
    license_info={
      "name": "Apache 2.0",
      "url": "https://www.apache.org/licenses/LICENSE-2.0"
    },
    openapi_tags=[
      {
        "name": "auth",
        "description": "Authentication related endpoints"
      }
    ]
    )

app.include_router(router_ext, prefix="/ext", tags=[])

@app.get("/")
async def root(request: Request):
  """Placeholder for the root endpoint
  """
  return {
    "message": "Welcome to the {} API".format(__name__),
    "root_path": request.scope.get("root_path")
  }

# Hook up any events worth responding to
# https://fastapi.tiangolo.com/advanced/events/