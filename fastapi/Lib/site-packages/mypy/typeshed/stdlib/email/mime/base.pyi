import email.message
from email import _ParamsType
from email.policy import Policy

__all__ = ["MIMEBase"]

class MIMEBase(email.message.Message):
    def __init__(
        self,
        _maintype: str,
        _subtype: str,
        *,
        policy: Policy | None = None,
        **_params: _ParamsType,
    ) -> None: ...
