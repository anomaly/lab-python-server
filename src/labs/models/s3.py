""" Describes Models to store objects in an S3 compatible bucket.


"""
from typing import Optional
from uuid import uuid4
from datetime import timedelta
from typing import Union

from sqlalchemy import event
from sqlalchemy.orm import relationship,\
    mapped_column, Mapped

from .utils import DateTimeMixin, IdentifierMixin,\
    ModelCRUDMixin, fk_user_uuid

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

    Usage: 
        s3_file_metadata = await S3FileMetadata.create(
            session,
            file_name=upload_request.file_name,
            file_size=upload_request.file_size,
            mime_type=upload_request.mime_type,
        )

    You are required to pass in the file_name, file_size and mime_type of the upload.
    This is simply a claim that the application is making not the truth, following this
    use the get_upload_url method to get a signed url to upload the file to the object.

    The application should then queue a validation where the file attributes are checked
    against the bucket and if they match the is_valid flag is set to True.

    The template assumes you require to be an authenticated user to upload files, if
    you require to drop this then you will need to make the necessary changes to the
    tables.

    """

    __tablename__ = "s3_file_metadata"

    # This is the unique key for this object store in the associated bucket
    # which is automatically assigned to the metadata, you do not have to
    # worry about it simply deal with the wrapped methods provided by this class
    s3_key: Mapped[str]
    # Prefix where you want the object to be stored e.g images, files
    prefix: Mapped[Optional[str]]

    file_name: Mapped[str]
    file_size: Mapped[int]

    mime_type: Mapped[str]

    # Is set to True if the object is deemed to be logically deleted
    # see other part of the documentation for logical and physical deletion policy
    deleted: Mapped[bool] = mapped_column(
        default=False
    )

    # Is set to True if the object is currently in held in a legal hold
    legal_hold: Mapped[bool] = mapped_column(
        default=False
    )

    # Is set of True once the application is able to validate
    # the presence of the object on the store
    is_valid: Mapped[bool] = mapped_column(
        default=False
    )

    user_id: Mapped[fk_user_uuid]

    user = relationship(
        "User",
        uselist=False,
    )

    @property
    def presigned_download_url(self) -> Union[str, None]:
        """ Provides a presigned download url for the object in the store

        If there is an issue then you will receive None, the application should not proceed
        with the download if this is the case.
        """
        try:
            return minio_client.presigned_get_object(
                config.S3_BUCKET_NAME,
                self.s3_key,
                expires=timedelta(
                    minutes=config.S3_DOWNLOAD_EXPIRY
                ),
                response_headers={
                    'response-content-disposition': 
                    f'attachment; filename="{self.file_name}"'
                },
            )
        except Exception as e:
            return None

    @property
    def presigned_upload_url(self) -> Union[str, None]:
        """ Use this property to get a URL to create or update the object

        Note that if versioning is not turned on for the object store then this will
        replace the contents of the object on the store.

        Once created you should send this to the browser to action the upload, the
        URL is signed for particular amount of time and will expire post that.

        If you receive None then there is an issue with the object store and you
        should not proceed with the upload.
        """
        try:
            url = minio_client.presigned_put_object(
                config.S3_BUCKET_NAME,
                self.s3_key,
                expires=timedelta(
                    minutes=config.S3_UPLOAD_EXPIRY
                )
            )
            return url
        except Exception:
            return None
        
    def enable_legal_hold(self) -> bool:
        """ The Object Lock legal hold operation enables you to place a legal hold 
        on an object version. Like setting a retention period, a legal hold prevents an 
        object version from being overwritten or deleted. 

        This is a method which is used to enable a legal hold on the object, the
        object must exists in the store and must not already have a legal hold.
        """
        try:
            minio_client.enable_object_legal_hold(
                config.S3_BUCKET_NAME,
                self.s3_key,
            )
            self.legal_hold = True
            return True
        except Exception:
            self.legal_hold = False
            return False
        
    def disable_legal_hold(self) -> bool:
        """ Disables the legal hold if one is placed on the object.

        Note that this method will return a boolean to state the success of the
        operation. This is not the legal hold status of the object.        
        """
        try:
            minio_client.disable_object_legal_hold(
                config.S3_BUCKET_NAME,
                self.s3_key,
            )

            self.legal_hold = False

            return True
        except Exception:
            self.legal_hold = True
            return False
        

@event.listens_for(S3FileMetadata, 'init')
def assigned_s3_key(target, args, kwargs):
    """ Assigns a UUID based on the UUID4 standard as the key for the file upload

    When the application assigns a new S3FileMetadata object, it will be 
    given a UUID to use as the key in the bucket, and this record will act
    as the meta table for translating the object in the bucket to a downloadable
    file.
    """
    target.s3_key = uuid4().hex
    target.prefix = uuid4().hex

