from fastapi import APIRouter

router = APIRouter(tags=["auth"])

from .verify import *