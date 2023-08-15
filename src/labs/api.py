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

from .settings import settings

from .routers import router_root
from .broker import broker

from .schema.ext import RootResponse


def generate_operation_id(route: APIRoute) -> str:
    """
        With a little help from FastAPI docs
        https://bit.ly/3rXeAvH

        Globally use the path name as the operation id thus
        making things a lot more readable, note that this requires
        you name your functions really well.

        Read  more about this on the FastAPI docs
        https://shorturl.at/vwz03
    """
    return route.name


"""A FastAPI application that serves handlers
"""
app = FastAPI(
    title=__title__,
    version=__version__,
    description=settings.api_router.__doc__,
    docs_url=settings.api_router.path_docs,
    root_path=settings.api_router.path_root,
    terms_of_service=settings.api_router.terms_of_service,
    contact=settings.api_router.contact,
    license_info=settings.api_router.license_info,
    openapi_tags=settings.api_router.open_api_tags,
    generate_unique_id_function=generate_operation_id,
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
