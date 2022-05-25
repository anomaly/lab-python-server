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


from turtle import title
from fastapi import FastAPI, Request, status

"""A FastAPI application that serves handlers
"""
app = FastAPI(
    title=__name__,
    root_path="/api",
    docs_url="/docs",
    )

@app.get("/echo")
async def echo(request: Request):
    """Echo back a response to say hello.

    Purpose of this endpoint is to echo back what was received, this merely
    validated that the server is up and running.
    """
    return {"hello": "world"}
