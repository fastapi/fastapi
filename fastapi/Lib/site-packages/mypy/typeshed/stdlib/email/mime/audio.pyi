from collections.abc import Callable
from email import _ParamsType
from email.mime.nonmultipart import MIMENonMultipart
from email.policy import Policy

__all__ = ["MIMEAudio"]

class MIMEAudio(MIMENonMultipart):
    def __init__(
        self,
        _audiodata: str | bytes | bytearray,
        _subtype: str | None = None,
        _encoder: Callable[[MIMEAudio], object] = ...,
        *,
        policy: Policy | None = None,
        **_params: _ParamsType,
    ) -> None: ...
