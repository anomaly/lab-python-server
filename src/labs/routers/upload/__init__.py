"""

"""
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Made available by the router utils
from ..utils import get_current_user

from ...db import get_async_session
from ...models import S3FileMetadata, User
from ...schema import FileUploadRequest, FileUploadResponse

router = APIRouter(tags=["file-uploads"])

@router.post("")
async def get_upload_url(
    upload_request: FileUploadRequest,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
) -> FileUploadResponse:
    """
    """

    s3_file_metadata = await S3FileMetadata.create(
        session,
        file_name=upload_request.file_name,
        file_size=upload_request.file_size,
        mime_type=upload_request.mime_type,
        user=current_user,
    )

    response = FileUploadResponse(
        url=s3_file_metadata.get_upload_url(),
        expiry_date=datetime.now()
    )

    return response

