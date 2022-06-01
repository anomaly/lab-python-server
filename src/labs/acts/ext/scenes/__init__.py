"""
"""

from fastapi import APIRouter, Request, status

from ....config import config

router = APIRouter(tags=["ext"])

@router.get("/echo")
async def echo(request: Request):
    """Echo back a response to say hello.

    Purpose of this endpoint is to echo back what was received, this merely
    validated that the server is up and running.
    """
    return {"message": "Hello, world!"}
