""" FastAPI router configuration

These are the recommended settings for the FastAPI router. They are
what work with the infrastructure requirements of Anomaly projects.

Some of these are application related so they should ideally be
updated to represent the application.
"""

from pydantic import BaseSettings

class APIRouterSettings(BaseSettings):
    """
        This project provides a reference Python API built using FastAPI, the 
        aim of the project is:

        - To maintain a good know source of habits
        - Demonstrate how applications are meant to be put together at Anomaly
        - Democratize design of robust API    
    """

    terms_of_service: str = "https://github.com/anomaly/labs"
    contact: dict = {
        "name": "Anomaly Labs",
        "url": "https://github.com/anomaly/labs",
        "email": "oss@anomaly.ltd",
    }

    license_info: dict = {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0"
    }

    open_api_tags: list = [
        {
            "name": "auth",
            "description": "Authentication related endpoints"
        }
    ]

    path_root: str = "/api"
    path_docs: str = "/docs"

    class Config:
        """ Env vars are prefixed with FASTAPI_ are loaded
        into instances of this class
        """
        env_prefix = "FASTAPI_"
    
