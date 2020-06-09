"""FastAPI framework, high performance, easy to learn, fast to code, ready for production"""

__version__ = "0.55.1"

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
from .staticfiles import StaticFiles
from .templating import Jinja2Templates
from .testclient import TestClient
from .websockets import WebSocket

__all__ = [
    "status",
    "FastAPI",
    "BackgroundTasks",
    "UploadFile",
    "HTTPException",
    "Body",
    "Cookie",
    "Depends",
    "File",
    "Form",
    "Header",
    "Path",
    "Query",
    "Security",
    "Request",
    "Response",
    "APIRouter",
    "StaticFiles",
    "Jinja2Templates",
    "TestClient",
    "WebSocket",
]
