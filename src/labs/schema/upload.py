from typing import Optional
from datetime import datetime

from .utils import AppBaseModel

class FileUploadResponse(
    AppBaseModel
):
    url: str
    expiry_date: datetime


class FileUploadRequest(
    AppBaseModel
):
    file_name: str
    file_size: int
    mime_type: str