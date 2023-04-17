""" Describes Models to store objects in an S3 compatible bucket.


"""
from uuid import uuid4
from datetime import timedelta
from typing import TYPE_CHECKING, Union

from sqlalchemy import event
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .utils import DateTimeMixin, IdentifierMixin, ModelCRUDMixin, fk_user_uuid

from ..db import Base
from ..utils import minio_client
from ..config import config

class S3FileMetadata(
    Base,
    DateTimeMixin,
    IdentifierMixin,
    ModelCRUDMixin
):
    """ S3 File object storage and usage pattern.

    This model is used to store metadata about files stored in an S3 compatible
    object store, and then let various parts of your application link to 
    the objects for application specific use.

    e.g. user has uploaded identification documents.

    """

    __tablename__ = "s3_file_metadata"

    s3_key: Mapped[str]
    prefix: Mapped[str]

    file_name: Mapped[str]
    file_size: Mapped[int]

    mime_type: Mapped[str]

    deleted: Mapped[bool] = mapped_column(
        default=False
    )

    legal_hold: Mapped[bool] = mapped_column(
        default=False
    )

    user_id: Mapped[fk_user_uuid]

    user = relationship(
        "User",
        primaryjoin="S3FileMetadata.created_by_user_id==User.id",
        uselist=False,
    )

    @property
    def signed_download_url(self) -> Union[str, None]:
        """
        """
        try:
            return minio_client.presigned_get_object(
                config.S3_BUCKET_NAME,
                self.s3_key,
                expires=timedelta(minutes=config.S3_DOWNLOAD_EXPIRY),
                response_headers={
                    "response-content-disposition": 
                    f'attachment; filename="{self.file_name}"'
                },
            )
        except Exception as e:
            return None

    def get_upload_url(self) -> Union[str, None]:
        try:
            url = minio_client.presigned_put_object(
                config.S3_BUCKET_NAME,
                self.s3_key,
                expires=timedelta(minutes=config.S3_UPLOAD_EXPIRY)
            )
            return url
        except Exception:
            return None
        
    def enable_legal_hold(self) -> bool:
        try:
            minio_client.put_object_legal_hold(
                config.S3_BUCKET_NAME,
                self.s3_key,
                True
            )
            return True
        except Exception:
            return False
        
    def disable_legal_hold(self) -> bool:
        try:
            minio_client.put_object_legal_hold(
                config.S3_BUCKET_NAME,
                self.s3_key,
                False
            )
            return True
        except Exception:
            return False
        

@event.listens_for(S3FileMetadata, 'init')
def receive_init(target, args, kwargs):
    """ Assigns a UUID based on the UUID4 standard as the key for the file upload

    When the application assigns a new S3FileMetadata object, it will be 
    given a UUID to use as the key in the bucket, and this record will act
    as the meta table for translating the object in the bucket to a downloadable
    file.
    """
    target.otp_secret = uuid4()

