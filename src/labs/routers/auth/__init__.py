""" Authentication related handler

  Common handlers for authentication, which is sub-divided to
  modules, each one of them has a router which will be imported
  and mounted onto the router that the package.

"""
from fastapi import APIRouter
from .verify import router as router_verify
 
"""Mounts all the sub routers for the authentication module"""
router = APIRouter(tags=["auth"])

router.include_router(router_verify)
