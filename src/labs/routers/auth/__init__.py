from fastapi import APIRouter
from .verify import *

router = APIRouter(tags=["auth"])
