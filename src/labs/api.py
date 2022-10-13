"""API backend

  The package provides the main application programmer interface (API) that
  the clients (web or otherwise) will use to interact with the application.

  The end points will depend on database models defined by the core package, 
  most requests will be synchronous and will return a JSON response. Others
  will schedule tasks that are dealt with by the background workers (see worker).

  API endpoints are built and served using the FastAPI micro-framework.

"""
from . import __title__, __version__

from fastapi import FastAPI, Request, Depends, status, WebSocket
from fastapi.responses import JSONResponse

from .routers import router_auth, router_ext

api_description = """
This project provides a reference Python API built using FastAPI, the 
aim of the project is:

- To maintain a good know source of habits
- Demonstrate how applications are meant to be put together at Anomaly
- Democratize design of robust API

"""


"""A FastAPI application that serves handlers
"""
app = FastAPI(
    title=__title__,
    version=__version__,
    description=api_description,
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

# Additional routers of the application described in the routers package
app.include_router(router_auth, prefix="/auth")
app.include_router(router_ext, prefix="/ext")


@app.get("/")
async def root(request: Request):
  """Placeholder for the root endpoint
  """
  return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={
      "message": "Welcome to the {} API".format(__name__),
      "root_path": request.scope.get("root_path")
    }
  )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  while True:
    data = await websocket.receive_text()
    await websocket.send_text(f"Message text was: {data}")

# Hook up any events worth responding to
# https://fastapi.tiangolo.com/advanced/events/