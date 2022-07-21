from typing import Optional

from .utils import IdentityMixin, DateTimeMixin

class UserRequest(IdentityMixin, DateTimeMixin):
    """ User profile 
    """
    email: Optional[str]
    mobile_number: Optional[str]
    verified: bool
    first_name: Optional[str]
    last_name: Optional[str]

    class Config:
        """ Enable compatibility with SQLAlchemy

        ORM mode will allow pydantic to translate SQLAlchemy results
        into serializable models.

        For a full set of options, see:
        https://pydantic-docs.helpmanual.io/usage/model_config/
        """
        orm_mode = True

    