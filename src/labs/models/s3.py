""" Describes Models to store objects in an S3 compatible bucket.


"""
from datetime import timedelta
from typing import TYPE_CHECKING, Union

from sqlalchemy import Boolean, Column, ForeignKey, String, Integer
from sqlalchemy.sql import expression
from sqlalchemy.orm import relationship

from .utils import DateTimeMixin, IdentifierMixin, ModelCRUDMixin
from ..utils import minio_client
from ..config import config

class S3FileMetadata(DateTimeMixin, IdentifierMixin, ModelCRUDMixin):
    """
    
    """

    __tablename__ = "s3_file_metadata"

    s3_key = Column(String,
        nullable=False)
    prefix = Column(String,
        default="",
        nullable=False)

    file_name = Column(String,
        nullable=False)
    file_size = Column(Integer,
        nullable=False)
    mime_type = Column(String,
        nullable=False)

    deleted = Column(Boolean,
        server_default=expression.false(),
        nullable=False)

    user = relationship(
        "User",
        primaryjoin="S3FileMetadata.created_by_user_id==User.id",
        uselist=False,
    )

    @property
    def signed_download_url(self) -> Union[str, None]:
        try:
            return minio_client.presigned_get_object(
                config.S3_BUCKET_NAME,
                self.s3_key,
                expires=timedelta(hours=1),
                response_headers={
                    "response-content-disposition": f'attachment; filename="{self.file_name}"'
                },
            )
        except Exception as e:
            return None

