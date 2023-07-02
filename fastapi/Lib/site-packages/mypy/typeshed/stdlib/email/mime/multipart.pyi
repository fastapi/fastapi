from collections.abc import Sequence
from email import _ParamsType
from email.message import Message
from email.mime.base import MIMEBase
from email.policy import Policy

__all__ = ["MIMEMultipart"]

class MIMEMultipart(MIMEBase):
    def __init__(
        self,
        _subtype: str = "mixed",
        boundary: str | None = None,
        _subparts: Sequence[Message] | None = None,
        *,
        policy: Policy | None = None,
        **_params: _ParamsType,
    ) -> None: ...
