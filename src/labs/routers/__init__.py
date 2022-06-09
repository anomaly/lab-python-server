"""All routers all amalgamated at the top level

  Each submodule.router is renamed to router_submodule
  this way the top level app can import these and mount
  them at the app level.

"""

from .auth import router as router_auth
from .ext import router as router_ext