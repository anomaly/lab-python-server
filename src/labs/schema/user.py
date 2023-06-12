from typing import Optional

from .utils import AppBaseModel,\
    IdentityMixin, DateTimeMixin

class UserRequest(
    AppBaseModel
):
    """ User profile 
    """
    email: str
    # password: str
    first_name: str
    last_name: str

    
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

