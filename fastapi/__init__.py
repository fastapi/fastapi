"""FastAPI framework, high performance, easy to learn, fast to code, ready for production"""

__version__ = "0.45.0"

from starlette.background import BackgroundTasks

from .applications import FastAPI
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
from .routing import APIRouter
