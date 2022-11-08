from typing import Optional

from .utils import AppBaseModel,\
    IdentityMixin, DateTimeMixin

class UserRequest(
    AppBaseModel
):
    """ User profile 
    """
    email: Optional[str]
    mobile_number: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]

    
class UserResponse(
    AppBaseModel,
    IdentityMixin,
    DateTimeMixin
):
    """ User profile 
    """
    email: str
    mobile_number: Optional[str]
    verified: bool
    first_name: Optional[str]
    last_name: Optional[str]

