"""API backend

  The package provides the main application programmer interface (API) that
  the clients (web or otherwise) will use to interact with the application.

  The end points will depend on database models defined by the core package, 
  most requests will be synchronous and will return a JSON response. Others
  will schedule tasks that are dealt with by the background workers (see worker).

  API endpoints are built and served using the FastAPI micro-framework.

"""
from . import __title__, __version__

from fastapi import FastAPI, Request, status, WebSocket
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from .routers import router_auth, router_ext, router_users

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
  root_path="/api",
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
app.include_router(router_auth)
app.include_router(router_ext, prefix="/ext")
app.include_router(router_users, prefix="/users")


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

# With a little help from FastAPI docs
# https://bit.ly/3rXeAvH
#
# Globally use the path name as the operation id thus
# making things a lot more readable, note that this requires
# you name your functions really well.
def use_route_names_as_operation_ids(app: FastAPI) -> None:
  """
  Simplify operation IDs so that generated API clients have simpler function
  names.

  Should be called only after all routes have been added.
  """
  for route in app.routes:
    if isinstance(route, APIRoute):
      route.operation_id = route.name

use_route_names_as_operation_ids(app)
