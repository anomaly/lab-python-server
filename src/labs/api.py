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

from .config import config

from .routers import router_root
from .broker import broker

from .schema.ext import RootResponse

"""A FastAPI application that serves handlers
"""
app = FastAPI(
  title=__title__,
  version=__version__,
  description=config.api_router.description,
  docs_url=config.api_router.path_docs,
  root_path=config.api_router.path_root,
  terms_of_service=config.api_router.terms_of_service,
  contact=config.api_router.contact,
  license_info=config.api_router.license_info,
  openapi_tags=config.api_router.open_api_tags
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  while True:
    data = await websocket.receive_text()
    await websocket.send_text(f"Message text was: {data}")


# Additional routers of the application described in the routers package
app.include_router(router_root)


# TaskIQ configurartion so we can share FastAPI dependencies in tasks
@app.on_event("startup")
async def app_startup():
    if not broker.is_worker_process:
        await broker.startup()

# On shutdown, we need to shutdown the broker
@app.on_event("shutdown")
async def app_shutdown():
    if not broker.is_worker_process:
        await broker.shutdown()

# Default handler
@app.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def root(request: Request) -> RootResponse:
  """ Placeholder for the root endpoint
  """
  return RootResponse(
    message="Welcome to the {} API".format(__name__),
    root_path=request.scope.get("root_path")
  )

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
