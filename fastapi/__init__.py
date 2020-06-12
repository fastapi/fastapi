"""FastAPI framework, high performance, easy to learn, fast to code, ready for production"""

__version__ = "0.56.1"

from starlette import status

from .applications import FastAPI
from .background import BackgroundTasks
from .datastructures import UploadFile
from .exceptions import HTTPException
from .param_functions import (
    Body,
    Cookie,
    Depends,
    File,
    Form,
    Header,
    Path,
    Query,
    Security,
)
from .requests import Request
from .responses import Response
from .routing import APIRouter
from .websockets import WebSocket
