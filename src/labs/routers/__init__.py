"""All routers all amalgamated at the top level

  Each submodule.router is renamed to router_submodule
  this way the top level app can import these and mount
  them at the app level.

"""

from fastapi import APIRouter

from .auth import router as router_auth
from .ext import router as router_ext
from .users import router as router_users

# Mount all routers at the top level
# this is what the FastAPI app will use
router_root = APIRouter()

router_root.include_router(
  router_auth,
)
router_root.include_router(
  router_ext,
  prefix="/ext",
)
router_root.include_router(
  router_users,
  prefix="/users",
)
