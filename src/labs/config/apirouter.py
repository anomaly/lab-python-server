""" FastAPI router configuration

These are the recommended settings for the FastAPI router. They are
what work with the infrastructure requirements of Anomaly projects.

Some of these are application related so they should ideally be
updated to represent the application.
"""

from pydantic import BaseSettings

class APIRouterSettings(BaseSettings):

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
