from typing import Optional
from datetime import datetime

from .utils import AppBaseModel

class FileUploadResponse(
    AppBaseModel
):
    presigned_upload_url: str
    expires: int


class FileUploadRequest(
    AppBaseModel
):
    file_name: str
    file_size: int
    mime_type: str