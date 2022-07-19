"""Tasks for the app

    Define each set of tasks in a logical package e.g email
    you should use subpackage to keep things more managable.

    Import the tasks packages that you wish Celery to pick up
    on here and the deamon will register them.

    This repository provides examples of periodic and triggered tasks

"""

from .email import *
from .periodic import *
from .otp import *

